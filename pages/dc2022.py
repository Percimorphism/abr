import imp
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pgeocode


st.title("DC 2022 Ridership Heatmap")

DATA_URL=("./datasource/dcbr-zip-codes.xlsx")

# @st.cache_data(persist=True)
def load_data():
    data = pd.read_excel(DATA_URL, sheet_name='complete', engine='openpyxl')
    data['Zip'] = (data['Zip'].astype(str)).str[:5]
    data['Zip'] = data['Zip'].str.zfill(5)

    return data

dc = load_data()
# st.write(dc)

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
