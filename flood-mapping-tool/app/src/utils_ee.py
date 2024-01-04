import ee
import json
import streamlit as st
from google.oauth2 import service_account

def ee_initialize():
    """Initialize Google Earth Engine using service account credentials."""

    # Retrieve the JSON credentials from Streamlit secrets
    json_credentials = st.secrets["json_data"]

    # Parse the JSON credentials
    credentials_dict = json.loads(json_credentials)

    # Create credentials from the parsed JSON
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # Initialize Google Earth Engine with these credentials
    ee.Initialize(credentials)

# Example usage
ee_initialize()
