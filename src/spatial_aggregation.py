"""
spatial_aggregation.py
======================
Grid construction and primary measurement extraction (paper Stage 3).

Builds a 100 m grid over the study extent and extracts the three primary
measurements per cell:
  - building coverage from the segmentation mask
  - vegetation coverage from NAIP imagery (NDVI, or excess-green proxy)
  - road density from OpenStreetMap (via OSMnx)

The 100 m cell scale balances sensitivity to local morphology against
computational feasibility and aligns with neighbourhood-scale planning.
"""

import numpy as np
import geopandas as gpd
import rasterio
import rasterio.mask
from shapely.geometry import box, Polygon
import osmnx as ox


PIX_RES_FACTOR = 100  # grid cell edge = 100 x raster pixel resolution (~100 m)


def utm_epsg_from_lonlat(lon, lat):
    """Return the EPSG code of the UTM zone containing (lon, lat)."""
    zone = int((lon + 180) / 6) + 1
    return (32600 + zone) if lat >= 0 else (32700 + zone)


def build_grid(seg_raster_path):
    """Construct a regular grid over the segmentation raster extent."""
    with rasterio.open(seg_raster_path) as src:
        bounds = src.bounds
        res = src.res[0]
        crs = src.crs
    step = res * PIX_RES_FACTOR
    xmin, ymin, xmax, ymax = bounds
    cells = [
        box(x, y, x + step, y + step)
        for x in np.arange(xmin, xmax, step)
        for y in np.arange(ymin, ymax, step)
    ]
    return gpd.GeoDataFrame(geometry=cells, crs=crs)


def extract_coverage(grid, seg_raster_path, naip_raster_path, ndvi_threshold=0.2):
    """
    Extract building and vegetation coverage per grid cell.

    Building coverage: proportion of pixels classified as building.
    Vegetation coverage: proportion of pixels with NDVI > threshold
    (excess-green proxy where near-infrared is unavailable).
    """
    stats = []
    with rasterio.open(seg_raster_path) as seg, rasterio.open(naip_raster_path) as full:
        has_nir = full.count >= 4
        for geom in grid.geometry:
            try:
                seg_arr, _ = rasterio.mask.mask(seg, [geom], crop=True)
                bld_cov = np.count_nonzero(seg_arr[0] == 1) / seg_arr[0].size

                full_arr, _ = rasterio.mask.mask(full, [geom], crop=True)
                r = full_arr[0].astype("float32")
                g = full_arr[1].astype("float32")
                b = full_arr[2].astype("float32")
                if has_nir:
                    nir = full_arr[3].astype("float32")
                    ndvi = (nir - r) / (nir + r + 1e-6)
                    veg_cov = float(np.mean(ndvi > ndvi_threshold))
                else:
                    exg = 2 * g - r - b
                    exg_n = (exg - exg.min()) / (exg.max() - exg.min() + 1e-6)
                    veg_cov = float(np.mean(exg_n > 0.3))

                stats.append({"bld_coverage": bld_cov, "veg_coverage": veg_cov})
            except Exception:
                stats.append({"bld_coverage": 0.0, "veg_coverage": 0.0})

    import pandas as pd
    return pd.concat([grid.reset_index(drop=True),
                      pd.DataFrame(stats)], axis=1)


def extract_road_density(grid):
    """
    Compute road density (km/km2) per cell from OpenStreetMap.

    Roads are retrieved for the grid bounding box, projected to the local
    UTM zone, clipped to each cell, and summed. Road data are obtained
    independently of the segmentation model.
    """
    grid_wgs84 = grid.to_crs(epsg=4326)
    minx, miny, maxx, maxy = grid_wgs84.total_bounds
    poly = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])

    G = ox.graph_from_polygon(poly, network_type="drive")
    _, edges = ox.graph_to_gdfs(G)

    centroid = grid_wgs84.unary_union.centroid
    epsg = utm_epsg_from_lonlat(centroid.x, centroid.y)

    grid_m = grid.to_crs(epsg=epsg)
    edges_m = edges.to_crs(epsg=epsg)

    grid = grid.copy()
    grid["road_density_km_per_km2"] = grid_m.geometry.apply(
        lambda cell: edges_m.clip(cell).length.sum() / 1000.0 / (cell.area / 1e6)
    ).values
    return grid
