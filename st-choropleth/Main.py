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

images_dir = r"C:\Users\Gebruiker\Desktop\My Lab\Knowledge-Management-Informatics\Knowledge-Management-Informatics\st-choropleth\images"
image_files = ["a.png", "b.png", "c.png"]

# Display current working directory
st.write('Current working directory:', os.getcwd())

# Check and display whether each image file exists
for filename in image_files:
    image_path = os.path.join(images_dir, filename)
    if os.path.isfile(image_path):
        st.image(image_path)
    else:
        st.error(f"Image {filename} not found at {image_path}")
        # If the file isn't found, list the contents of the directory for debugging
        st.write(f"Contents of {images_dir}:")
        st.write(os.listdir(images_dir))
