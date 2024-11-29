# ----- GF-0657: PORGRAMACIÓN EN SIG | PROFESOR: MANUEL VARGAS TAREA 03 | 
# Ana López (B94386) y Matthias Pelz (B95845)

# ----- Carga y configuración de los paquetes -----

import streamlit as st
import pandas as pd
import plotly.express as px

import geopandas as gpd
import folium

# Para integrar Folium en Streamlit
from streamlit_folium import folium_static, st_folium
from branca.colormap import LinearColormap, linear

# ----- Fuentes de datos -----
# URL del archivo de datos. El archivo original está en: 
# https://raw.githubusercontent.com/Ana69666/-gf0657_ProyectoFinal_b94386_b95845/refs/heads/main/datos/datos_def.csv
FOREST = 'datos/datos_def.csv'
# URL del archivo de datos. El archivo original está en: 
# https://raw.githubusercontent.com/Ana69666/-gf0657_ProyectoFinal_b94386_b95845/main/datos/datos_def.gpkg
PAISES = 'datos/datos_def.gpkg'

# ----- Funciones para recuperar los datos -----

# Función para cargar los datos y almacenarlos en caché 
# para mejorar el rendimiento
@st.cache_data
def cargar_datos_changeforest():
    # Leer el archivo CSV y cargarlo en un DataFrame de pandas
    datos = pd.read_csv(FOREST)
    return datos

# Función para cargar los datos geoespaciales de países
@st.cache_data
def cargar_datos_paises():
    paises = gpd.read_file(PAISES)
    return paises

# ----- Cargar datos -----
st.title('Análisis del cambio de cobertura forestal entre el año 2000 y el 2020')

# Mensajes de estado mientras se cargan los datos
estado_carga_changeforest = st.text('Cargando datos de Changeforest...')
paises_forest = cargar_datos_changeforest()
estado_carga_changeforest.text('Datos de Changeforest cargados exitosamente.')

estado_carga_paises = st.text('Cargando datos geoespaciales de países...')
paises = cargar_datos_paises()
estado_carga_paises.text('Datos geoespaciales de países cargados exitosamente.')

# ----- Preprocesamiento de datos -----
# Este preprocesamiento ya se llevó a cabo en el notebook de la tarea03, en donde se limpió el dataframe y el geodataframe
# para normalizar y eliminar los valores nulos y poder realizar el join correspondiente. Se decidió utilizar el join de ambos para evitar
# tener que volver a realizar este procedimiento en la aplicación. También los datos ya se encuentran sin valores nulos en la columna
# trend, es decir los valores que fueran menores al 5% de la cobertura en el año 2000 y 2020.

# ----- Preparación de datos -----

# Columnas relevantes del conjunto de datos
columnas = [
    'ADM0_ISO', 
    'NAME', 
    'CONTINENT', 
    'REGION_WB', 
    'POP_EST',
    'GDP_MD',
    'forests_2000',
    'forests_2020',
    'trend'
]
datos = paises_forest[columnas]

# Nombres de las columnas en español
columnas_espaniol = {
    'ADM0_ISO': 'Código ISO', 
    'NAME': 'País', 
    'CONTINENT': 'Continente', 
    'REGION_WB': 'Región', 
    'POP_EST': 'Población',
    'GDP_MD': 'PIB',
    'forests_2000': 'Cobertura forestal 2000',
    'forests_2020': 'Cobertura forestal 2020',
    'trend': '(%) de Cambio'
}
datos = datos.rename(columns=columnas_espaniol)

st.dataframe(datos)

# ------- Lista de selección en la barra lateral --------

# Lista de selección por región
# Obtener la lista de regiones únicas
lista_regiones = datos['Región'].unique().tolist()
lista_regiones.sort()

# Añadir la opción "Todas" al inicio de la lista
opciones_regiones = ['Todas'] + lista_regiones

# Crear el selectbox para regiones en la barra lateral
region_seleccionada = st.sidebar.selectbox(
    'Selecciona una región',
    opciones_regiones
)

# Filtrar los datos por región
if region_seleccionada != 'Todas':
    datos_region = datos[datos['Región'] == region_seleccionada]
else:
    datos_region = datos.copy()

# Lista de selección por país basada en la región seleccionada
# Obtener la lista de países únicos de la región seleccionada
lista_paises = datos_region['País'].unique().tolist()
lista_paises.sort()

# Añadir la opción "Todos" al inicio de la lista
opciones_paises = ['Todos'] + lista_paises

# Crear el selectbox para países en la barra lateral
pais_seleccionado = st.sidebar.selectbox(
    'Selecciona un país',
    opciones_paises
)

# Filtrar los datos por país
if pais_seleccionado != 'Todos':
    datos_filtrados = datos_region[datos_region['País'] == pais_seleccionado]
else:
    datos_filtrados = datos_region.copy()


# ----- Filtrar columnas específicas para la segunda tabla -----
# Definir las columnas que deseas mostrar
columnas_especificas = [
    'Código ISO', 'País', 'Región', 'Población',
    'PIB', 'Cobertura forestal 2000', 'Cobertura forestal 2020', '(%) de Cambio'
]

# Filtrar los datos según las columnas específicas
datos_filtrados = datos_filtrados[columnas_especificas]

# ----- Tabla de Tendencias en el cambio de cobertura forestal vs. Desarrollo Económico -----

# Mostrar la tabla
st.subheader('Tendencias en el cambio de cobertura forestal vs. Desarrollo Económico')
st.dataframe(datos_filtrados, hide_index=True)


# ----- Gráfico de dispersión -----------------------------------------------

# Crear el gráfico de dispersión con leyenda
fig = px.scatter(
    datos_filtrados,
    x='Población',  # Eje X (Población)
    y='(%) de Cambio',  # Eje Y (Tasa de Deforestación)
    color='Región',  # Colorear por región
    size='PIB',  # Tamaño de los puntos según el PIB
    hover_name='País',  # Información al pasar el mouse
    title="Relación entre Tasa de Deforestación, Población y PIB por Región"
)

# Actualizar los títulos de los ejes
fig.update_layout(
    xaxis_title="Población",  # Título del eje X
    yaxis_title="Tasa de Deforestación",  # Título del eje Y
)

# Invertir el eje Y para mostrar tendencias decrecientes
fig.update_yaxes(autorange='reversed')

# Mostrar la leyenda y otros ajustes de visualización
fig.update_layout(
    legend_title="Región",  # Título de la leyenda
    legend=dict(
        x=1,  # Posicionar la leyenda fuera del gráfico
        y=1,
        traceorder='normal',
        font=dict(size=10),
        title=dict(font=dict(size=12))
    )
)

# Mostrar el gráfico en Streamlit
st.subheader('Gráfico de dispersión: Relación entre Tasa de Deforestación, Población y PIB por Región')
st.plotly_chart(fig)

# ----- Mapa------------------------------------------


# Unir los datos con el GeoDataFrame de países usando 'Código ISO' y 'ADM0_ISO'
paises_merged = paises.merge(
    datos_filtrados,  # Los datos que ya han sido filtrados
    how='left',  # Realizamos una unión de tipo 'left' (para conservar todos los países)
    left_on='ADM0_ISO',  # Columna en el GeoDataFrame de países
    right_on='Código ISO'  # Columna en el DataFrame de datos
)


# Filtrar los datos para eliminar filas con geometría nula
paises_merged = paises_merged[paises_merged.geometry.notnull()]

# Crear el mapa base
if pais_seleccionado != 'Todos':
    # Obtener el Código ISO del país seleccionado
    codigo_iso = pais_seleccionado  # Usar la selección de país del 'selectbox'
    # Filtrar el GeoDataFrame para obtener la geometría del país
    pais_geom = paises_merged[paises_merged['ADM0_ISO'] == codigo_iso]
    if not pais_geom.empty:
        # Obtener el centroide de la geometría del país
        centroid = pais_geom.geometry.centroid.iloc[0]
        coordenadas = [centroid.y, centroid.x]
        zoom_level = 5
    else:
        # Valores por defecto si no se encuentra el país
        coordenadas = [0, 0]
        zoom_level = 2
else:
    coordenadas = [0, 0]
    zoom_level = 1

# Crear el mapa base con Folium
mapa = folium.Map(location=coordenadas, zoom_start=zoom_level)

# Reemplazar los valores NaN en la columna '% de Cambio' con 0 (o otro valor)
paises_merged['(%) de Cambio'] = paises_merged['(%) de Cambio'].fillna(0)

# Crear una paleta de colores para la columna de cambio en la cobertura forestal
paleta_colores = LinearColormap(
    colors=['red', 'yellow', 'green'],  # Colores desde rojo a verde
    vmin=paises_merged['(%) de Cambio'].min(),  # Valor mínimo
    vmax=paises_merged['(%) de Cambio'].max()   # Valor máximo
)

# Añadir los polígonos al mapa con el cambio de cobertura forestal
folium.GeoJson(
    paises_merged,
    name='Cambio en la cobertura forestal por país',
    style_function=lambda feature: {
        'fillColor': paleta_colores(feature['properties']['(%) de Cambio']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7,
    },
    highlight_function=lambda feature: {
        'weight': 3,
        'color': 'black',
        'fillOpacity': 0.9,
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NAME', '(%) de Cambio', 'Cobertura forestal 2000', 'Cobertura forestal 2020'],
        aliases=['País: ', 'Tasa de Deforestación: ', 'Cobertura 2000: ', 'Cobertura 2020: '],
        localize=True
    )
).add_to(mapa)

# Añadir la leyenda de colores (paleta de colores)
paleta_colores.caption = 'Cambio en la cobertura forestal por país (%)'
paleta_colores.add_to(mapa)

# Agregar el control de capas al mapa
folium.LayerControl().add_to(mapa)

# Mostrar el mapa en Streamlit
st.subheader('Cambio en la proporción de la superfificie forestal entre el 2000 y el 2020')

# Forma antigua para mostrar el mapa en Streamlit
folium_static(mapa)
