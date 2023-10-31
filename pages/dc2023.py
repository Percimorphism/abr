import imp
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pgeocode
import pydeck as pdk


st.title("DC 2023 Ridership Heatmap")

DATA_URL=("./datasource/dcbr23-zipcodes.xlsx")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_excel(DATA_URL, sheet_name='complete', engine='openpyxl')
    data['Zip'] = (data['Zip'].astype(str)).str[:5]
    data['Zip'] = data['Zip'].str.zfill(5)

    return data

dc = load_data()

st.write(dc['Zip'].value_counts())


nomi = pgeocode.Nominatim('US')
loc = nomi.query_postal_code((dc['Zip'].astype(str)).to_list())
# st.write(loc)

heatmap_data = {'zip': loc['postal_code'],
                'lat': loc['latitude'], 
                'lon' : loc['longitude']} 
hm = pd.DataFrame(data=heatmap_data) 
hm = hm.dropna(how='any')
st.write(hm.shape)

st.map(hm[['lat', 'lon']])


st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=38.9072,
        longitude=-77.0369,
        zoom=11,
        pitch=30,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=hm,
           get_position='[lon, lat]',
           radius=300,
           elevation_scale=10,
           elevation_range=[0, 2000],
           pickable=True,
           extruded=True,
        ),
    ],
))
