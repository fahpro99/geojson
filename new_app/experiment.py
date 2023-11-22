import requests
import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Load GeoJSON data
state_geo = requests.get(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/output.json"
).json()

# Load data
state_data = pd.read_csv(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/my_country.csv"
)
# Create a Folium map centered on Bangladesh
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7)

fig=px.choropleth(state_data,locations="District",geojson=state_geo,color="Count").add_to(m)

for _, row in state_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=folium.DivIcon(
            icon_size=(120, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 8pt; font-weight: bold; color: black">{row["District"]}<br>{row["Count"]}</div>'
        )
    ).add_to(m)
# Streamlit map display
folium_static(m)  # Use folium_static to embed the Folium map in Streamlit
