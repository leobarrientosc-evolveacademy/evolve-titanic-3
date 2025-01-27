import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Análisis del Titanic",
    page_icon="🚢",
    layout="wide"
)

# Título y descripción
st.title("🚢 Análisis de Supervivientes del Titanic")
st.markdown("""
Esta aplicación analiza los factores que influyeron en la supervivencia de los pasajeros del Titanic.
Explora diferentes visualizaciones y descubre patrones interesantes en los datos.
""")

# Cargar datos
@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

# Cargar los datos
try:
    df = cargar_datos()
    st.success("Datos cargados exitosamente!")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Sidebar con filtros
st.sidebar.header("Filtros")
clase_seleccionada = st.sidebar.multiselect(
    "Seleccionar Clase",
    options=sorted(df['Pclass'].unique()),
    default=sorted(df['Pclass'].unique())
)

genero_seleccionado = st.sidebar.multiselect(
    "Seleccionar Género",
    options=sorted(df['Sex'].unique()),
    default=sorted(df['Sex'].unique())
)

# Filtrar datos
df_filtrado = df[
    (df['Pclass'].isin(clase_seleccionada)) &
    (df['Sex'].isin(genero_seleccionado))
]

# Métricas principales
col1, col2, col3 = st.columns(3)
with col1:
    tasa_supervivencia = (df_filtrado['Survived'].mean() * 100).round(2)
    st.metric("Tasa de Supervivencia", f"{tasa_supervivencia}%")
with col2:
    edad_promedio = df_filtrado['Age'].mean().round(2)
    st.metric("Edad Promedio", f"{edad_promedio} años")
with col3:
    tarifa_promedio = df_filtrado['Fare'].mean().round(2)
    st.metric("Tarifa Promedio", f"£{tarifa_promedio}")

# Visualizaciones
st.header("Visualizaciones")

# 1. Supervivencia por Clase y Género
tab1, tab2, tab3 = st.tabs(["Supervivencia por Clase", "Distribución de Edad", "Tarifas"])

with tab1:
    fig_supervivencia = px.bar(
        df_filtrado.groupby(['Pclass', 'Sex'])['Survived'].mean().reset_index(),
        x='Pclass',
        y='Survived',
        color='Sex',
        title='Tasa de Supervivencia por Clase y Género',
        labels={'Survived': 'Tasa de Supervivencia', 'Pclass': 'Clase', 'Sex': 'Género'},
        barmode='group'
    )
    st.plotly_chart(fig_supervivencia, use_container_width=True)

with tab2:
    fig_edad = px.histogram(
        df_filtrado,
        x='Age',
        color='Survived',
        nbins=30,
        title='Distribución de Edad por Supervivencia',
        labels={'Age': 'Edad', 'Survived': 'Sobrevivió'}
    )
    st.plotly_chart(fig_edad, use_container_width=True)

with tab3:
    fig_tarifas = px.box(
        df_filtrado,
        x='Pclass',
        y='Fare',
        color='Survived',
        title='Distribución de Tarifas por Clase y Supervivencia',
        labels={'Fare': 'Tarifa', 'Pclass': 'Clase', 'Survived': 'Sobrevivió'}
    )
    st.plotly_chart(fig_tarifas, use_container_width=True)

# Análisis adicional
st.header("Análisis Detallado")
col1, col2 = st.columns(2)

with col1:
    # Supervivencia por Puerto de Embarque
    fig_embarque = px.pie(
        df_filtrado.groupby('Embarked')['Survived'].mean().reset_index(),
        values='Survived',
        names='Embarked',
        title='Tasa de Supervivencia por Puerto de Embarque'
    )
    st.plotly_chart(fig_embarque, use_container_width=True)

with col2:
    # Supervivencia por Tamaño de Familia
    df_filtrado['FamilySize'] = df_filtrado['SibSp'] + df_filtrado['Parch'] + 1
    fig_familia = px.bar(
        df_filtrado.groupby('FamilySize')['Survived'].mean().reset_index(),
        x='FamilySize',
        y='Survived',
        title='Tasa de Supervivencia por Tamaño de Familia',
        labels={'FamilySize': 'Tamaño de Familia', 'Survived': 'Tasa de Supervivencia'}
    )
    st.plotly_chart(fig_familia, use_container_width=True)

# Datos crudos
if st.checkbox("Mostrar datos crudos"):
    st.subheader("Datos crudos")
    st.dataframe(df_filtrado) 