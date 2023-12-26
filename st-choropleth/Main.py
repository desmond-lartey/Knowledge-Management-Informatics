import streamlit as st

# This should be the first Streamlit command used in your app, and it should only be called once
st.set_page_config(layout="wide")

st.markdown("""
# AI Machine Learning and decision support system
---

### Select the pages from the sidebar to see demonstrations of the various aspects of Plotly's map functions.

---
""")

col2, col3, col4 = st.columns(3)

# Ensure that the image paths are correct and relative to your Streamlit application's root directory
col2.image("images/a.png")
col3.image("images/b.png")
col4.image("images/c.png")
