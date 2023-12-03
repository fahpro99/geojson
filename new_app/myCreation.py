import streamlit as st
import pandas as pd
import requests
import folium

# Load GeoJSON data
state_geo = requests.get(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/output.json"
).json()
# Load data new







# Load data
state_data = pd.read_csv(
    "https://raw.githubusercontent.com/fahpro99/geojson/main/my_country.csv"
)

APP_TITLE='Network Outages Report Map'
APP_SUB_TITLE='Source : Summit Communication'
client='Robi'
District='Dhaka'

def display_client_filter(df):
    client_list = list(df['Client'].unique())
    client_list.sort()
    client = st.sidebar.selectbox('Client', client_list, len(client_list)-1)
    st.header(f'{client}')
    return client

def display_state_filter(df, state_name):
    state_list = [''] + list(df['State Name'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)



def display_outage(new_data,client,District,con_type):
    total=len(new_data)
    new_data=new_data[(new_data['Client'] == client) & (new_data['District'] == District)]
    st.metric(con_type,total)
    if District:
        new_data = new_data[new_data['District'] == District]
        total=len(new_data)
        st.metric(con_type,total)


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    new_data=pd.read_excel('Link_WK_35.xlsx')
    site_data=pd.read_excel('Site_WK_35.xlsx')
    st.subheader(f"{District} outages")
    display_outage(new_data,client,District,'Total Link Outages ')
    display_outage(site_data,client,District,'Total Site Outages ')
    map =folium.Map(location=[23.6850, 90.3563], zoom_start=6,geojson=state_geo)

    choropleth = folium.Choropleth(
        geo_data=state_geo,
        data=new_data,
        columns=('District', 'Client'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.add_to(map)

if __name__ == '__main__':
    main()
