import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import pandas as pd
import requests
from branca.colormap import LinearColormap

# Load GeoJSON data
state_geo = requests.get(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/output.json"
).json()

# Load data
state_data = pd.read_csv(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/my_country.csv"
)

# Streamlit app title
st.title("Network outages in Bangladesh")

# Create a Folium map centered on Bangladesh
m = folium.Map(location=[23.6850, 90.3563], zoom_start=6, geojson=state_geo)

# Convert the state_data DataFrame to a list of lists for HeatMap
heat_data = [[row['Latitude'], row['Longitude'], row['Count']] for _, row in state_data.iterrows()]

# Define a linear color gradient based on latitude
colors = ['blue', 'lime', 'red']
colormap = LinearColormap(colors=colors, vmin=min(state_data['Latitude']), vmax=max(state_data['Latitude']))

# Add HeatMap layer with the heatmap data and the latitude-based color gradient
heatmap = HeatMap(heat_data, gradient={0.1: colormap(0.1), 0.5: colormap(0.5), 0.8: colormap(0.8)}, min_opacity=0.5, max_opacity=0.8)
heatmap.add_to(m)

# Add markers for each district with district names and counts
for _, row in state_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=folium.DivIcon(
            icon_size=(120, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 8pt; font-weight: bold; color: black">{row["District"]}<br>{row["Count"]}</div>'
        )
    ).add_to(m)

# Add layer control to the map
folium.LayerControl().add_to(m)

# Display legend inside Streamlit
st.markdown("""
    **Heatmap Legend:**
    - Blue: Low
    - Lime: Medium
    - Red: High
""")

# Streamlit map display
folium_static(m)  # Use folium_static to embed the Folium map in Streamlit
