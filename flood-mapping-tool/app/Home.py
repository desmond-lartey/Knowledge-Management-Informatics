"""Home page for Streamlit app."""
import streamlit as st
from src.config_parameters import params
from src.utils import (
    add_about,
    add_logo,
    set_home_page_style,
    toggle_menu_button,
)
import requests
from io import BytesIO
# Import necessary libraries
import datetime as dt
import ee
import folium
import geemap.foliumap as geemap
import streamlit_ext as ste
from folium.plugins import Draw, Geocoder, MiniMap
from src.config_parameters import params
from src.utils import add_about, add_logo, set_tool_page_style, toggle_menu_button
from src.utils_ee import ee_initialize
from src.utils_flood_analysis import derive_flood_extents
from streamlit_folium import st_folium

#st.legacy_caching.clear_cache()

# Page configuration
st.set_page_config(layout="wide", page_title=params["browser_title"])

# If app is deployed hide menu button
toggle_menu_button()


import requests
import base64
from io import BytesIO

def get_base64_of_bin_file(url_or_path):
    """
    This function will handle both URLs and local file paths.
    It opens the file or fetches it from a URL, then converts it to a base64 string.
    """
    try:
        if url_or_path.startswith('http://') or url_or_path.startswith('https://'):
            response = requests.get(url_or_path)
            if response.status_code == 200:
                file_content = BytesIO(response.content)
            else:
                raise Exception(f"Error fetching file from URL: {url_or_path}, Status Code: {response.status_code}")
        else:
            with open(url_or_path, "rb") as f:
                file_content = f.read()

        return base64.b64encode(file_content).decode("utf-8")
    except Exception as e:
        # Handle any exception (can be replaced with more specific error handling)
        print(f"An error occurred: {e}")
        return None  # Or return a default image's base64 string

# Example usage
add_logo("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/flood-mapping-tool/app/img/MAlogo3.png")
add_about()

# Create sidebar
#add_logo("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/flood-mapping-tool/app/img/MAlogo3.png")
#add_about()

# Set page style
set_home_page_style()

# Page title
st.markdown("# Home")

# Initialize Google Earth Engine with a service account

# Using service account credentials
ee_initialize(force_use_service_account=True)

# Using default credentials
ee_initialize(force_use_service_account=False)

# First section
st.markdown("## Introduction")
st.markdown(
    """
    This tool allows to estimate flood extent using Sentinel-1
    synthetic-aperture radar
    <a href='%s'>SAR</a> data.<br><br>
    The methodology is based on a <a href=
    '%s'>recommended practice</a>
    published by the United Nations Platform for Space-based Information for
    Disaster Management and Emergency Response (UN-SPIDER) and it uses several
    satellite imagery datasets to produce the final output. The datasets are
    retrieved from <a href='%s'>Google Earth
    Engine</a> which is a powerful web-platform for cloud-based processing of
    remote sensing data on large scales. More information on the methodology is
    given in the Description.<br><br>
    This analysis provides a comprehensive overview of a flooding event, across
    different areas of interest, from settlements to countries. However, as
    mentioned in the UN-SPIDER website, the methodology is meant for broad
    information provision in a global context, and contains inherent
    uncertainties. Therefore, it is important that the tool is not used as the
    only source of information for rescue response planning.
    """
    % (
        params["url_sentinel_esa"],
        params["url_unspider_tutorial"],
        params["url_gee"],
    ),
    unsafe_allow_html=True,
)

# Second section
st.markdown("## How to use the tool")
st.markdown(
    """
    <ul>
        <li><p>
            In the sidebar, choose <i>Flood extent analysis</i> to start the
            analysis.
        </p>
        <li><p>
            In the left panel, use the drawing tool to select an area of
            interest on the map. You can delete your selection by clicking on
            the bin icon. While the flood mapping is generated regardless of
            the size of the selected region, you will be able to save raster
            and vector flooding extent only if the side of the rectangular
            selection does not exceed 100 km.
        </p>
        <li><p>
            In the right panel click on the title <i>Choose Image Dates</i>
            in order to expand the section. Here you need to select four dates.
            The first two identify a range of dates based on which the
            reference imagery (before the flooding event) is defined. You can
            select even years worth of data (the reference imagery is
            calculated as the median between the range of observations), but
            make sure you take into account wet and dry seasons if only taking
            a few months. The last two refer to a period of time which comes
            after the flooding event. By setting periods, not single dates, you
            allow the selection of enough tiles to cover the area of interest.
            Sentinel-1 imagery is acquired minimum every 12 days for each point
            on the globe (see Figure 2 in the documentation).
        </p>
        <li>
            <p>
                By clicking on <i>Choose parameters</i>, you will be able to
                set two variables:
            </p>
            <ul>
                <li><p>
                    The <i>threshold</i> is the value against which the
                    difference the two satellite images - before and after the
                    flooding event - is tested. Lower thresholds result in a
                    greater area considered "flooded". It is recommended to set
                    the value to 1.25, which was selected through trial and
                    error. You may want to adjust the value in case of high
                    rates of false positive or negative values, especially in
                    case other sources of information are available and it is
                    possible to compare flood extent estimations between
                    sources.
                </p>
                <li><p>
                    The <i>pass direction</i> has to do with the way the
                    satellite travels around the Earth. Depending on your area
                    of interest and time period, you may find more imagery
                    available for either the <i>Ascending</i> or the
                    <i>Descending</i> pass directions (see Figure 2 in the
                    Documentation). It is recommended to leave the parameter
                    unchanged for a first estimation and change its value in
                    case partial or no imagery is produced.
                </p>
            </ul>
        <li><p>
            Once the parameters are set, you can finally click on <i>Compute
            flood extent</i> to run the calculations. A map will appear
            underneath, with a layer containing the flooded area within the
            area of interest.
        </p>
        <li><p>
            If you wish to export the layer to file, you can click on <i>Export
            to file</i> and download the raster and/or vector data.
        </p>
    </ul>
    <p>
        In case you get errors, follow the intructions. If you have doubts,
        feel free to contact the Data Science team.
    </p>
    """,
    unsafe_allow_html=True,
)
