import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
# AI Machine Learning and decision support system
---
            
### Select the pages from the sidebar to see demonstrations of the various aspects of Plotly's map functions.
            
---
""")

# Image paths for the uploaded images
image_paths = ["/mnt/data/a.png", "/mnt/data/b.png", "/mnt/data/c.png"]

# Create columns for the images
cols = st.columns(3)

# Display each image in a separate column
for i, image_path in enumerate(image_paths):
    # Display the image
    cols[i].image(image_path)