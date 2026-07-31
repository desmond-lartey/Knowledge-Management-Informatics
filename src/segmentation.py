"""
segmentation.py
===============
U-Net semantic segmentation for building detection from NAIP aerial imagery.

Covers three operations from the paper's Stage 2 (Semantic Segmentation):
  - training tile generation
  - model training (U-Net + ResNet-34)
  - model evaluation on held-out validation tiles (IoU, F1, precision, recall, accuracy)

The model produces BINARY BUILDING MASKS ONLY. Road networks are obtained
independently from OpenStreetMap (see spatial_aggregation.py).

Reference: Lartey & Law, "GeoAI to Planning Intelligence".
"""

import os
import numpy as np
from tempfile import NamedTemporaryFile

import geoai
import rasterio


# ---------------------------------------------------------------------------
# Training tile generation
# ---------------------------------------------------------------------------
def generate_training_tiles(states, naip_dir, buildings_dir, out_root,
                            tile_size=512, stride=256):
    """
    Generate paired image-label tiles for each state.

    Tiles of `tile_size` pixels are extracted with a sliding window at
    `stride` pixels, increasing sample diversity and reducing boundary
    artifacts. Building footprint vectors are rasterised and aligned with
    the imagery to produce supervised segmentation samples.

    Parameters
    ----------
    states : list of str
        State codes to process (must have both NAIP and building files).
    naip_dir : str
        Directory containing NAIP_{STATE}.tif files.
    buildings_dir : str
        Directory containing buildings_{STATE}.geojson files.
    out_root : str
        Root directory for per-state tile output.
    tile_size : int
        Tile edge length in pixels (default 512).
    stride : int
        Sliding-window stride in pixels (default 256).
    """
    os.makedirs(out_root, exist_ok=True)
    for state in states:
        raster = os.path.join(naip_dir, f"NAIP_{state}.tif")
        vector = os.path.join(buildings_dir, f"buildings_{state}.geojson")
        out_dir = os.path.join(out_root, state)
        os.makedirs(out_dir, exist_ok=True)

        tiles = geoai.export_geotiff_tiles(
            in_raster=raster,
            out_folder=out_dir,
            in_class_data=vector,
            tile_size=tile_size,
            stride=stride,
            buffer_radius=0,
        )
        print(f"{state}: {len(tiles)} tiles")


# ---------------------------------------------------------------------------
# Model training
# ---------------------------------------------------------------------------
def train_model(images_dir, labels_dir, output_dir,
                epochs=5, batch_size=8, learning_rate=0.001, val_split=0.2):
    """
    Train a U-Net with a ResNet-34 backbone for binary building segmentation.

    Uses mini-batch gradient descent. Model checkpoint is saved to
    `output_dir/best_model.pth`.

    The paper trains across a multi-state dataset of 2,175 tiles (80/20 split)
    for 5 epochs.
    """
    os.makedirs(output_dir, exist_ok=True)
    geoai.train_segmentation_model(
        images_dir=images_dir,
        labels_dir=labels_dir,
        output_dir=output_dir,
        architecture="unet",
        encoder_name="resnet34",
        encoder_weights="imagenet",
        num_channels=3,
        num_classes=2,          # background + building
        batch_size=batch_size,
        num_epochs=epochs,
        learning_rate=learning_rate,
        val_split=val_split,
        verbose=True,
    )


# ---------------------------------------------------------------------------
# Model evaluation
# ---------------------------------------------------------------------------
def evaluate_model(model_path, images_dir, labels_dir,
                   val_split=0.2, seed=42):
    """
    Evaluate the trained model on the held-out validation tiles.

    Reproduces the same 20% validation split used during training (fixed seed),
    runs inference on each validation tile, and accumulates pixel-level
    confusion counts for the building class to compute standard metrics.

    Returns
    -------
    dict with keys: IoU, F1, Precision, Recall, Accuracy
        Values reported in the paper: IoU=0.477, F1=0.646, Precision=0.570,
        Recall=0.746, Accuracy=0.805.
    """
    img_files = sorted(f for f in os.listdir(images_dir) if f.endswith(".tif"))
    lbl_files = sorted(f for f in os.listdir(labels_dir) if f.endswith(".tif"))

    np.random.seed(seed)
    n_total = len(img_files)
    n_val = max(1, int(n_total * val_split))
    val_idx = np.random.choice(n_total, size=n_val, replace=False)

    val_imgs = [os.path.join(images_dir, img_files[i]) for i in val_idx]
    val_lbls = [os.path.join(labels_dir, lbl_files[i]) for i in val_idx]

    TP = FP = FN = TN = 0
    for img_path, lbl_path in zip(val_imgs, val_lbls):
        try:
            with NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
                pred_path = tmp.name
            geoai.semantic_segmentation(
                input_path=img_path, output_path=pred_path,
                model_path=model_path, architecture="unet",
                encoder_name="resnet34", num_channels=3, num_classes=2,
                window_size=512, overlap=256, batch_size=1,
            )
            with rasterio.open(pred_path) as s:
                pred = s.read(1).astype(np.int32)
            with rasterio.open(lbl_path) as s:
                lbl = s.read(1).astype(np.int32)
            if pred.shape != lbl.shape:
                from skimage.transform import resize
                pred = (resize(pred, lbl.shape, order=0,
                               preserve_range=True) > 0.5).astype(np.int32)
            pb = (pred == 1).astype(np.int32)
            lb = (lbl == 1).astype(np.int32)
            TP += int(np.sum((pb == 1) & (lb == 1)))
            FP += int(np.sum((pb == 1) & (lb == 0)))
            FN += int(np.sum((pb == 0) & (lb == 1)))
            TN += int(np.sum((pb == 0) & (lb == 0)))
            os.unlink(pred_path)
        except Exception as e:
            print(f"Skipping tile: {e}")

    precision = TP / (TP + FP + 1e-9)
    recall = TP / (TP + FN + 1e-9)
    iou = TP / (TP + FP + FN + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)
    accuracy = (TP + TN) / (TP + FP + FN + TN + 1e-9)

    return {
        "IoU": round(iou, 4), "F1": round(f1, 4),
        "Precision": round(precision, 4), "Recall": round(recall, 4),
        "Accuracy": round(accuracy, 4),
    }


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------
def run_inference(states, naip_dir, model_path, out_dir):
    """
    Apply the trained model to each state's imagery, producing binary
    building masks. Uses a sliding window (512 px, overlap 256 px) with
    averaged overlapping predictions to minimise edge effects.
    """
    os.makedirs(out_dir, exist_ok=True)
    for state in states:
        out_raster = os.path.join(out_dir, f"{state}_buildings_pred.tif")
        if os.path.exists(out_raster):
            print(f"{state}: prediction exists, skipping")
            continue
        geoai.semantic_segmentation(
            input_path=os.path.join(naip_dir, f"NAIP_{state}.tif"),
            output_path=out_raster,
            model_path=model_path,
            architecture="unet", encoder_name="resnet34",
            num_channels=3, num_classes=2,
            window_size=512, overlap=256, batch_size=2,
        )
        print(f"{state}: saved {out_raster}")
