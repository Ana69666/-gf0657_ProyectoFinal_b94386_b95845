# ----- GF-0657: PORGRAMACIÓN EN SIG | PROFESOR: MANUEL VARGAS TAREA 03 | 
# Ana López (B94386) y Matthias Pelz (B95845)

# ----- Carga y configuración de los paquetes -----

import streamlit as st
import pandas as pd
import plotly.express as px

import geopandas as gpd
import folium
import mapclassify
import branca

# Para integrar Folium en Streamlit
from streamlit_folium import st_folium

# Configuración de pandas para mostrar separadores de miles, 2 dígitos decimales y evitar la notación científica.
pd.set_option('display.float_format', '{:,.2f}'.format)

  
