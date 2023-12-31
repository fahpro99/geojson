import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

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
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7)

# Convert the state_data DataFrame to a list of lists for HeatMap
heat_data = [[row['Latitude'], row['Longitude'], row['Count']] for _, row in state_data.iterrows()]

# Add HeatMap layer with the heatmap data
heatmap = HeatMap(heat_data, gradient={0.1: 'blue', 0.5: 'lime', 0.8: 'red'}, min_opacity=0.5, max_opacity=0.8)
heatmap.add_to(m)

# Add markers for each district with district names and counts
for _, row in state_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 10pt; font-weight: bold; color: black">{row["District"]}<br>{row["Count"]}</div>'
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

# Create a matplotlib colorbar legend with reversed color scale
norm = Normalize(vmin=state_data['Count'].min(), vmax=state_data['Count'].max())
fig, ax = plt.subplots(figsize=(10, 0.5))  # Adjust the figure size to make the legend smaller
cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.Spectral_r), cax=ax, orientation='horizontal')  # Reverse the heatmap color scale
cbar.set_label('Count')

# Streamlit map display
folium_static(m)  # Use folium_static to embed the Folium map in Streamlit
# Display the colorbar legend in Streamlit
st.pyplot(fig)


