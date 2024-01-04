import base64
import requests
from io import BytesIO
import os
from datetime import date
import streamlit as st
from src.config_parameters import params

# Check if app is deployed
def is_app_on_streamlit():
    """Check whether the app is on streamlit or runs locally."""
    return "HOSTNAME" in os.environ and os.environ["HOSTNAME"] == "streamlit"

# General layout
def toggle_menu_button():
    """If app is on streamlit, hide menu button."""
    if is_app_on_streamlit():
        st.markdown(
            """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

# Home page
def set_home_page_style():
    """Set style home page."""
    st.markdown(
        """
        <style> p { font-size: %s; } </style>
        """ % params["docs_fontsize"],
        unsafe_allow_html=True,
    )

# Documentation page
def set_doc_page_style():
    """Set style documentation page."""
    st.markdown(
        """
        <style> p { font-size: %s; } </style>
        """ % params["docs_fontsize"],
        unsafe_allow_html=True,
    )

# Tool page
def set_tool_page_style():
    """Set style tool page."""
    st.markdown(
        """
        <style>
            .streamlit-expanderHeader {
                font-size: %s;
                color: #000053;
            }
            .stDateInput > label {
                font-size: %s;
            }
            .stSlider > label {
                font-size: %s;
            }
            .stRadio > label {
                font-size: %s;
            }
            .stButton > button {
                font-size: %s;
                font-weight: %s;
                background-color: %s;
            }
        </style>
        """ % (
            params["expander_header_fontsize"],
            params["widget_header_fontsize"],
            params["widget_header_fontsize"],
            params["widget_header_fontsize"],
            params["button_text_fontsize"],
            params["button_text_fontweight"],
            params["button_background_color"],
        ),
        unsafe_allow_html=True,
    )



# Sidebar
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    """
    Get base64 from image file or URL.

    Inputs:
        png_file (str): Image filename or URL.

    Returns:
        str: Encoded ASCII file.
    """
    try:
        if png_file.startswith('http://') or png_file.startswith('https://'):
            # Handle as URL
            response = requests.get(png_file)
            if response.status_code == 200:
                data = BytesIO(response.content).getvalue()
            else:
                raise Exception(f"Error fetching file from URL: {png_file}, Status Code: {response.status_code}")
        else:
            # Handle as local file
            with open(png_file, "rb") as f:
                data = f.read()
        
        return base64.b64encode(data).decode()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None or handle the error as needed

def build_markup_for_logo(png_file):
    """
    Create full string for navigation bar, including logo and title.

    Inputs:
        png_file (str): image filename

    Returns:
        str: full string with logo and title for sidebar
    """
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    padding-top: 50px;
                    padding-bottom: 10px;
                    background-position: %s;
                    background-size: %s %s;
                }
                [data-testid="stSidebarNav"]::before {
                    content: "%s";
                    margin-left: 20px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                    font-size: %s;
                    font-weight: %s;
                    position: relative;
                    text-align: center;
                    top: 85px;
                }
            </style>
            """ % (
        binary_string,
        params["MA_logo_background_position"],
        params["MA_logo_width"],
        "",
        params["sidebar_header"],
        params["sidebar_header_fontsize"],
        params["sidebar_header_fontweight"],
    )

def add_logo(png_file):
    """
    Add logo to sidebar.

    Inputs:
        png_file (str): image filename

    Returns:
        None
    """
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

def add_about():
    """
    Add about and contacts to sidebar.

    Inputs:
        None

    Returns:
        None
    """
    today = date.today().strftime("%B %d, %Y")
    st.sidebar.markdown("## About")
    st.sidebar.markdown(
        f"""
        <div class='about-section' style='
            background-color: {params["about_box_background_color"]};
            margin: 0px;
            padding: 1em;'
        '>
            <p style='
                margin-left:1em;
                margin: 0px;
                font-size: 1rem;
                margin-bottom: 1em;
            '>
                Last update: {today}
            </p>
            <p style='
                margin-left:1em;
                font-size: 1rem;
                margin: 0px
            '>
                <a href='{params["url_project_wiki"]}'>Wiki reference page</a><br>
                <!-- <a href='{params["url_github_repo"]}'>GitHub repository</a><br>
                <a href='{params["url_data_science_wiki"]}'>Data Science Lab</a> -->
            </p>
            <p style='
                margin-left:1em;
                font-size: 1rem;
                margin: 0px
            '>
                This application was originally created by the Map Action humanitarian team. It was later enhanced by Desmond Lartey, who incorporated features such as impact analysis on various land use types and comprehensive flood damage assessments for each land use category.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # Contacts textbox
    st.sidebar.markdown(" ")
    st.sidebar.markdown("## Contacts")
    contacts_text = ""
    for ds, email in params["data_scientists"].items():
        contacts_text += ds + (
            "<span style='float:right; margin-right: 3px;'><a href='mailto:%s'>%s</a></span><br>" % (email, email)
        )

    st.sidebar.markdown(
        """
        <div class='warning' style='
            background-color: %s;
            margin: 0px;
            padding: 1em;'
        '>
            <p style='
                margin-left:1em;
                font-size: 1rem;
                margin: 0px
            '>
                %s
            </p>
        </div>
        """ % (params["about_box_background_color"], contacts_text),
        unsafe_allow_html=True,
    )
