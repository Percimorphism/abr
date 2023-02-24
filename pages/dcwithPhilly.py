import imp
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pgeocode


st.title("DC and Philly Ridership Heatmap Combined")

## DC
dc_DATA_URL=("./datasource/dcbr-zip-codes.xlsx")
@st.cache(persist=True)
def load_data():
    data = pd.read_excel(dc_DATA_URL, sheet_name='complete', engine='openpyxl')
    data['Zip'] = (data['Zip'].astype(str)).str[:5]
    data['Zip'] = data['Zip'].str.zfill(5)
    return data
dc = load_data()
#st.write(dc)
dc_nomi = pgeocode.Nominatim('US')
dc_loc = dc_nomi.query_postal_code((dc['Zip'].astype(str)).to_list())
# st.write(loc)

dc_heatmap_data = {'zip': dc_loc['postal_code'],
                'lat': dc_loc['latitude'], 
                'lon' : dc_loc['longitude']} 
dc_hm = pd.DataFrame(data=dc_heatmap_data) 
dc_hm = dc_hm.dropna(how='any')
st.write(dc_hm.shape)
#st.write(dc_hm)

## Philly
p_DATA_URL=("./datasource/pbr-zip-codes.xlsx")

@st.cache(persist=True)
def load_data():
    data = pd.read_excel(p_DATA_URL, sheet_name='complete', engine='openpyxl')
    data['Zip'] = (data['Zip'].astype(str)).str[:5]
    data['Zip'] = data['Zip'].str.zfill(5)
    return data

philly = load_data()

p_nomi = pgeocode.Nominatim('US')
p_loc = p_nomi.query_postal_code((philly['Zip'].astype(str)).to_list())

p_heatmap_data = {'zip': p_loc['postal_code'],
                'lat': p_loc['latitude'], 
                'lon' : p_loc['longitude']} 
p_hm = pd.DataFrame(data=p_heatmap_data) 
p_hm = p_hm.dropna(how='any')
st.write(p_hm.shape)

#concatenate DC and Philly
hm = pd.concat([dc_hm, p_hm])
st.write(hm.shape)
st.map(hm[['lat', 'lon']])

