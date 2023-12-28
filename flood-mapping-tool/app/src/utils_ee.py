"""Module for Earth Engine-related functionalities."""
import ee
import streamlit as st
from ee import oauth
from google.oauth2 import service_account
from src.utils import is_app_on_streamlit

@st.experimental_memo
def ee_initialize(force_use_service_account: bool = False):
    """Initialize Google Earth Engine.

    This function checks whether the app is deployed on Streamlit Cloud and
    initializes Google Earth Engine accordingly. If the app runs locally,
    personal Google account credentials are used. If deployed on Streamlit Cloud,
    it uses credentials from the secrets field in the cloud.

    Args:
        force_use_service_account (bool): If True, a dedicated Google service
            account is used, regardless of whether the app is run locally or
            in the cloud. To use a service account locally, a file named
            "secrets.toml" should be added to the ".streamlit" folder in the
            main project folder.
    """
    try:
        if force_use_service_account or is_app_on_streamlit():
            # Retrieve service account keys from Streamlit secrets
            service_account_keys = st.secrets.get("ee_keys")
            if service_account_keys is None:
                raise ValueError("Service account keys not found in Streamlit secrets.")
            credentials = service_account.Credentials.from_service_account_info(
                service_account_keys, scopes=oauth.SCOPES
            )
            ee.Initialize(credentials)
        else:
            # Initialize with default credentials (local development)
            ee.Initialize()
    except Exception as e:
        print(f"Error initializing Google Earth Engine: {e}")
        raise

# Example usage: ee_initialize(force_use_service_account=True)
