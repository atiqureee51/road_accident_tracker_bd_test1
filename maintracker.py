# -*- coding: utf-8 -*-
"""

@author: Atiqur rahaman
"""


import pandas as pd
import matplotlib.pyplot as plt
import math

import time
import numpy as np




import streamlit as st
import pandas as pd
import numpy as np

from distutils import errors
from distutils.log import error
import altair as alt
from itertools import cycle

#https://github.com/atiqureee51/road_accident_tracker_bd_test1/blob/main/bangladesh_geojson_adm2_64_districts_zillas.json

st.title('Road accident tracker bd')


#df=pd.read_csv("https://github.com/atiqureee51/road_accident_tracker_bd_test1/tree/main/data/Districts_of_Bangladesh.csv")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.write('Districts_of_Bangladesh',df)
#st.write('Districts_of_Bangladesh',df)


@st.cache()
#DATA_URL = "data/bangladesh_geojson_adm2_64_districts_zillas.json"
import json
#from json import load
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  bd_districts=json.load(uploaded_file)
  st.write(bd_districts)
#bd_districts=json.load(open(DATA_URL,"r"))
# show data on streamlit
#st.write('64_districts_zillas',bd_districts)



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
from plotly.offline import plot, iplot, init_notebook_mode
init_notebook_mode(connected=True)
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

fig = px.choropleth(
    df,
    locations='id',
    geojson=bd_districts,
    color='Population (thousands)',
    title='Bangladesh Population',
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()


df['Population scale'] = np.log10(df['Population (thousands)'])

fig = px.choropleth(
    df,
    locations='id',
    geojson=bd_districts,
    color='Population scale',
    hover_name='Bengali',
    hover_data=['Area (km2)', 'Population scale'],
    title='Bangladesh Population'
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()



