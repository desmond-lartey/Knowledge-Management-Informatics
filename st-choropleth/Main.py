import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
# AI Machine Learning and decision support system
---
            
### Select the pages from the sidebar to see demonstrations of the various aspects of Plotly's map functions.
            
---
""")

import os
import streamlit as st

# Base directory for images
base_dir = "images"  # Relative path

# Image file names
image_files = ["a.png", "b.png", "c.png"]

# Columns for displaying images
cols = st.beta_columns(3)

for i, file in enumerate(image_files):
    # Construct full file path
    file_path = os.path.join(base_dir, file)

    # Check if the file exists
    if os.path.exists(file_path):
        # Display the image in the appropriate column
        cols[i].image(file_path)
    else:
        # Handle the error (e.g., display a placeholder or a warning message)
        cols[i].write(f"Image {file} not found.")
