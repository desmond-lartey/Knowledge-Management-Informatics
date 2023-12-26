import streamlit as st

# This should be the first Streamlit command used in your app, and it should only be called once
st.set_page_config(layout="wide")

st.markdown("""
# AI Machine Learning and decision support system
---

### Select the Knowledge management info from the sidebar to see demonstrations of the various aspects.

---
""")


# Define your columns
#col2, col3, col4 = st.columns(3)
col1  = st.columns([1])

# Adjust the width of the images as needed
image_width = 750  # Example width, you can adjust this

# Display the images with the specified width
#col2.image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/a.png", width=image_width)
#col3.image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/b.png", width=image_width)
#col4.image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/c.png", width=image_width)

col1[0].image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/d.png", width=image_width)



# Sidebar content
st.sidebar.markdown("""
## About This App
This application, originally developed by Alan Jones, has been extensively modified, upgraded, and enhanced by Desmond Lartey to incorporate various advanced functionalities. The app now integrates AI and machine learning to facilitate predictive analysis and support decision-making across different disciplines. It represents a dynamic fusion of technology and expertise, crafted to offer insightful solutions and decision support in a range of fields.
""")

# Sidebar - Copyright information
st.sidebar.markdown("---")
st.sidebar.markdown("© 2023. All Rights Reserved.")