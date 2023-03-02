import imp
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pgeocode
import pydeck as pdk


st.title("Philly 2023 Field Marketing Heatmap")

DATA_URL=("./datasource/Field Marketing Philly Zips.xlsx")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_excel(DATA_URL, engine='openpyxl')
    data['Zip'] = (data['Zip'].astype(str)).str[:5]
    data['Zip'] = data['Zip'].str.zfill(5)
    return data

pfm = load_data()
st.write(pfm['Zip'].value_counts())


nomi = pgeocode.Nominatim('US')
loc = nomi.query_postal_code((pfm['Zip'].astype(str)).to_list())

heatmap_data = {'zip': loc['postal_code'],
                'lat': loc['latitude'], 
                'lon' : loc['longitude']} 
hm = pd.DataFrame(data=heatmap_data) 

hm = hm.dropna(how='any')
#st.write(hm)

st.map(hm[['lat', 'lon']])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=39.9207,
        longitude=-75.1595,
        zoom=11,
        pitch=30,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=hm,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 2000],
           pickable=True,
           extruded=True,
        ),
    ],
))