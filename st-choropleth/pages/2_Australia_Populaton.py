import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests

st.set_page_config(layout="wide")

st.title("Population of Australian States")
st.info("Hover over the map to see the names of the states and their population")

#read the files differently

url = "https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/geo/australia.geojson"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    oz = json.loads(response.text)
else:
    print(f"Failed to retrieve data: {response.status_code}")

#read file original
#f = open('geo/australia.geojson')
#oz = json.load(f)
#oz["features"][1]


df = pd.read_csv("https://raw.githubusercontent.com/desmond-lartey/Knowledge-Management-Informatics/Fires/st-choropleth/data/Australian Bureau of Statistics.csv")

col1, col2 = st.columns(2)

fig = px.choropleth(df, geojson=oz, 
                    color="Population at 31 March 2023 ('000)",
                    locations="State", 
                    featureidkey="properties.name",
                    color_continuous_scale="Reds",
                    range_color=(0, 10000),
                    fitbounds = 'geojson',
                    template = 'plotly_dark'
                   )
col1.plotly_chart(fig)

fig = px.scatter_geo(df, geojson=oz, 
                    color="Population at 31 March 2023 ('000)",
                    size="Population at 31 March 2023 ('000)",
                    locations="State", 
                    featureidkey="properties.name",
                    color_continuous_scale="Blues",
                    range_color=(0, 10000),
                    fitbounds = 'geojson',
                    template = 'plotly_dark'
                   )
col2.plotly_chart(fig)