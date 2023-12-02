import streamlit as st
import pandas as pd
import requests

# Load GeoJSON data
state_geo = requests.get(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/output.json"
).json()

# Load data
state_data = pd.read_csv(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/my_country.csv"
)

APP_TITLE='Network Outages Report Map'
APP_SUB_TITLE='Source : Summit Communication'

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    st.write(state_data.shape)
    st.write(state_data.head())
    st.write(state_data.columns)

if __name__ == '__main__':
    main()