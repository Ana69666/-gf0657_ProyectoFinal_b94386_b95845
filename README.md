# Universidad de Costa Rica - GF-0657 Programación en SIG2024 - Profesor Manuel Vargas  
## Estudiante: Ana María López Ulate y Matthias Pelz Seyfarth
### Proyecto Final: Análisis del Cambio de Cobertura Forestal entre el Año 2000 y 2020  

## Descripción del Proyecto  

La aplicación resultante de este proyecto presenta información sobre los cambios en la cobertura forestal a nivel global entre los años 2000 y 2020 mediante tablas, gráficos interactivos y un mapa dinámico.  

El flujo de trabajo se centra en el manejo y visualización de datos utilizando las bibliotecas **Pandas**, **GeoPandas**, **Plotly** y **Folium**. Estas herramientas permiten:  
- Filtrar y sintetizar la información según regiones o países.  
- Visualizar las tendencias de cambio en la cobertura forestal relacionadas con variables demográficas y económicas, como población y PIB.  
- Explorar las tasas de deforestación mediante un mapa interactivo que permite la selección de países y regiones.  

La aplicación final fue desarrollada con **Streamlit**, lo que facilita su publicación en la plataforma **Streamlit Cloud**. 
El usuario final puede interactuar con los datos a través de filtros dinámicos y explorar tendencias específicas en gráficos y mapas.  

## Fuentes de Datos  
### 1. **Datos sobre Cambio de Cobertura Forestal**  
Los datos de cambio en la cobertura forestal fueron tomados de un conjunto de datos disponible en [Kaggle](https://www.kaggle.com/datasets/konradb/deforestation-dataset). 
Este archivo CSV incluye información como:  
- Cobertura forestal en el año 2000.  
- Cobertura forestal en el año 2020.  

### 2. **Datos Geoespaciales de Países**  
Los datos geoespaciales provienen de un archivo GeoPackage descargado desde [Natural Earth](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_sovereignty.zip). 
Este archivo contiene la geometría y metadatos de los países a nivel global e información sobre población estimada y PIB.  

---

## Resultado Final  

En el siguiente enlace puede explorar la aplicación de consulta interactiva publicada en **Streamlit Cloud**:  
[Streamlit Cloud](https://cambio-coberturaforestal-gf0657.streamlit.app/). 
