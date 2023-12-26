import streamlit as st

# This should be the first Streamlit command used in your app, and it should only be called once
st.set_page_config(layout="wide")

st.markdown("""
# AI Machine Learning and decision support system
---

### Select the pages from the sidebar to see demonstrations of the various aspects of Plotly's map functions.

---
""")


# Define your columns
col2, col3, col4 = st.columns(3)

# Use the raw GitHub URLs for the images
col2.image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/a.png")
col3.image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/b.png")
col4.image("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/images/c.png")
