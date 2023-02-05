# -*- coding: utf-8 -*-
"""
Created on Fri May  6 12:07:05 2022
@author: Atiqur rahaman
"""


import pvlib
from pvlib import location
from pvlib import irradiance
import pandas as pd
import matplotlib.pyplot as plt
import math

import time
import numpy as np


from pvlib.pvsystem import PVSystem, FixedMount
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

import streamlit as st
import pandas as pd
import numpy as np

from distutils import errors
from distutils.log import error
import altair as alt
from itertools import cycle
