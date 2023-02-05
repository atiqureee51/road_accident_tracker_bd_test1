# -*- coding: utf-8 -*-
"""

@author: Atiqur rahaman
"""
import math
import time
import numpy as np
from distutils import errors
from distutils.log import error
import altair as alt
from itertools import cycle

#https://github.com/atiqureee51/road_accident_tracker_bd_test1/blob/main/bangladesh_geojson_adm2_64_districts_zillas.json

#st.title('Road accident tracker bd')


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from plotly.subplots import make_subplots

import os

#print(os.getcwd())
#https://github.com/ozgunhaznedar/swiss_renewable_energy_app/blob/main/src/main.py
# checking that the current working directory is correct to ensure that the file paths are working
#if os.getcwd()[-3:] == "src":
#    os.chdir('..')
#print(os.getcwd())


#####################################################################################################################
### LOADING FILES

@st.cache

# LOAD DATAFRAME FUNCTION
def load_data(path):
    df = pd.read_csv(path)
    return df

# LOAD GEIJASON FILE
with open("data/bangladesh_geojson_adm2_64_districts_zillas.json") as response:
    bd_districts = json.load(response)

# LOAD csv DATA
df_raw = load_data(path="data/Districts_of_Bangladesh.csv")
df = deepcopy(df_raw)



#df=pd.read_csv("https://github.com/atiqureee51/road_accident_tracker_bd_test1/tree/main/data/Districts_of_Bangladesh.csv")



# Add title and header
st.title("Road accident tracker bd")
st.header("tracker 1 ")

st.write('Districts_of_Bangladesh',df)

df.District = df.District.apply(lambda x: x.replace(" District",""))


district_id_map = {}
for feature in bd_districts["features"]:
    feature["id"] = feature["id"]
    district_id_map[feature["properties"]["ADM2_EN"]] = feature["id"]
    
df['id'] = df.District.apply(lambda x: district_id_map[x])


df = df.rename(columns={
    'Population (thousands)[28]' : 'Population (thousands)',
    'Area (km2)[28]' : 'Area (km2)' })

import numpy as np
from matplotlib import cm
color = cm.inferno_r(np.linspace(.3, .7, 64))

df.set_index('District')["Population (thousands)"].plot.bar(
    xlabel='District',
    rot=90,
    figsize=(20,10),
    fontsize=10,
    color=color
    )


#pio.renderers.default = 'browser'

# Geographic Map
fig = go.Figure(
    px.choropleth(
        df,
        locations='id',
        geojson=bd_districts,
        color='Population (thousands)',
        title='Bangladesh Population',
    )
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)









df['Population scale'] = np.log10(df['Population (thousands)'])


# Geographic Map 2
fig2 = go.Figure(
    px.choropleth(
        df,
        locations='id',
        geojson=bd_districts,
        color='Population scale',
        hover_data=['Area (km2)', 'Population scale'],
        title='Bangladesh Population',
    )
)
fig2.update_geos(fitbounds="locations", visible=False)
fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig2)

# Geographic Map 3
fig3 = go.Figure(
    px.choropleth_mapbox(df,
            locations='id',
            geojson=bd_districts,
            color='Population scale',
            hover_name='Bengali',
            hover_data=['Population (thousands)','Area (km2)'],
            title='Bangladesh Population',
            mapbox_style='carto-positron',
            center= { 'lat' : 23.6850, 'lon' : 90.3563},
            zoom=4.8,
            opacity=0.6)
)
fig3.update_geos(fitbounds="locations", visible=False)
fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig3)

