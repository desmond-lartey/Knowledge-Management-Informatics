import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
# AI Machine Learning and decision support system
---
            
### Select the pages from the sidebar to see demonstrations of the various aspects of Plotly's map functions.
            
---
""")

import streamlit as st
import os

# Define the relative path to your images directory
images_dir = "images"

# Image filenames
image_files = ["a.png", "b.png", "c.png"]

# Create columns for the images
cols = st.columns(3)

# Display each image in a separate column
for i, filename in enumerate(image_files):
    # Construct the full path to the image
    image_path = os.path.join(images_dir, filename)

    # Check if the image exists
    if os.path.exists(image_path):
        # Display the image
        cols[i].image(image_path)
    else:
        # Show a message if the image is not found
        cols[i].write(f"Image {filename} not found at {image_path}")
