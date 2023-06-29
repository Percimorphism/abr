import imp
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pgeocode
import pydeck as pdk


st.title("DC Philly 6-30-23 Ridership signup")

DATA_URL=("./datasource/2023-6-30-Zipcodes.xlsx")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_excel(DATA_URL, sheet_name='zip', engine='openpyxl')
    data['Zip'] = (data['Zip'].astype(str)).str[:5]
    data['Zip'] = data['Zip'].str.zfill(5)

    return data

d = load_data()

nomi = pgeocode.Nominatim('US')
loc = nomi.query_postal_code((d['Zip'].astype(str)).to_list())

heatmap_data = {'zip': loc['postal_code'],
                'lat': loc['latitude'], 
                'lon' : loc['longitude']} 
hm = pd.DataFrame(data=heatmap_data) 

hm_23 = hm.dropna(how='any')
hm_23 = (hm_23.reset_index()).drop(columns=['index'])


# st.map(hm_23[['lat', 'lon']])

# st.pydeck_chart(pdk.Deck(
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=39.9207,
#         longitude=-75.1595,
#         zoom=11,
#         pitch=30,
#     ),
#     layers=[
#         pdk.Layer(
#            'HexagonLayer',
#            data=hm_23,
#            get_position='[lon, lat]',
#            radius=300,
#            elevation_scale=4,
#            elevation_range=[0, 2000],
#            pickable=True,
#            extruded=True,
#         ),
#     ],
# ))



### DC PHILLY FROM 2022
## DC
dc_DATA_URL=("./datasource/dcbr-zip-codes.xlsx")
@st.cache_data(persist=True)
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
#st.write(dc_hm.shape)


## Philly
p_DATA_URL=("./datasource/pbr-zip-codes.xlsx")

@st.cache_data(persist=True)
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
#st.write(p_hm.shape)

#concatenate DC and Philly
hm_22 = pd.concat([dc_hm, p_hm])
hm_22 = (hm_22.reset_index()).drop(columns=['index'])

#st.write(hm_22)
#st.write(hm_23)

st.write("heatmap of riders who siged up for 22 but not yet as of 6-30-23")

a = pd.DataFrame(hm_22.value_counts())
b = pd.DataFrame(hm_23.value_counts())
diff_hm = pd.DataFrame(((b-a).dropna()))
diff_hm = diff_hm.loc[diff_hm.iloc[:, 0] < 0]
diff_hm[0] = abs(diff_hm[0])
diff_hm = diff_hm.reset_index()
diff_hm = diff_hm.reindex(diff_hm.index.repeat(diff_hm[0]))
diff_hm = diff_hm[['zip', 'lat', 'lon']]
#st.write(diff_hm)


st.map(diff_hm[['lat', 'lon']])

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
           data=diff_hm,
           get_position='[lon, lat]',
           radius=300,
           elevation_scale=4,
           elevation_range=[0, 2000],
           pickable=True,
           extruded=True,
        ),
    ],
))
