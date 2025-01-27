import streamlit as st
import pandas as pd


# Configuración de la página
st.set_page_config(page_title="Análisis del Titanic", page_icon="🚢")

# Manejo de errores al cargar datos
try:
    titanic = pd.read_csv("titanic.csv")
except FileNotFoundError:
    st.error("Error: No se encuentra el archivo titanic.csv")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

st.title("Análisis de Supervivientes del Titanic")

# Convertir valores numéricos a texto descriptivo
titanic['Survived'] = titanic['Survived'].map({0: 'Fallecidos', 1: 'Supervivientes'})

# Selector de visualización
vista_seleccionada = st.selectbox(
    "Selecciona el tipo de visualización:",
    ["Por Clase", "Por Género", "Por Edad"]
)

if vista_seleccionada == "Por Clase":
    # Crear un gráfico de barras mostrando supervivientes por clase
    supervivientes_por_clase = titanic.groupby('Pclass')['Survived'].value_counts().unstack()
    supervivientes_por_clase.index = ['Primera Clase', 'Segunda Clase', 'Tercera Clase']
    
    # Mostrar el gráfico
    st.bar_chart(supervivientes_por_clase)
    
    # Mostrar estadísticas
    st.subheader("Tasa de supervivencia por clase:")
    tasa_supervivencia = (titanic.groupby('Pclass')['Survived']
                         .apply(lambda x: (x == 'Supervivientes').mean() * 100)
                         .round(2))
    st.write(tasa_supervivencia.to_frame('Tasa de Supervivencia (%)'))

elif vista_seleccionada == "Por Género":
    supervivientes_por_genero = titanic.groupby('Sex')['Survived'].value_counts().unstack()
    supervivientes_por_genero.index = ['Mujeres', 'Hombres']
    st.bar_chart(supervivientes_por_genero)

elif vista_seleccionada == "Por Edad":
    # Crear grupos de edad
    titanic['Grupo_Edad'] = pd.cut(titanic['Age'], 
                                  bins=[0, 12, 18, 35, 50, 100],
                                  labels=['Niños', 'Adolescentes', 'Jóvenes', 'Adultos', 'Mayores'])
    supervivientes_por_edad = titanic.groupby('Grupo_Edad', observed=True)['Survived'].value_counts().unstack()
    st.bar_chart(supervivientes_por_edad)

# Añadir explicación
st.markdown("""
### Distribución de Supervivientes
El gráfico muestra la distribución de pasajeros que sobrevivieron y fallecieron según la categoría seleccionada.

#### Datos adicionales:
- Total de pasajeros: {}
- Total de supervivientes: {}
- Porcentaje de supervivencia: {:.2f}%
""".format(
    len(titanic),
    (titanic['Survived'] == 'Supervivientes').sum(),
    (titanic['Survived'] == 'Supervivientes').mean() * 100
))

# Añadir línea divisoria
st.markdown("---")

# Análisis estadístico detallado
st.header("Análisis Estadístico de Supervivencia")

# Por Clase
clase_supervivencia = (titanic.groupby('Pclass')['Survived']
                      .apply(lambda x: (x == 'Supervivientes').mean() * 100)
                      .round(2)
                      .sort_values(ascending=False))

# Por Género
genero_supervivencia = (titanic.groupby('Sex')['Survived']
                       .apply(lambda x: (x == 'Supervivientes').mean() * 100)
                       .round(2)
                       .sort_values(ascending=False))

# Por Grupo de Edad (excluyendo NaN)
titanic['Grupo_Edad'] = pd.cut(titanic['Age'], 
                              bins=[0, 12, 18, 35, 50, 100],
                              labels=['Niños', 'Adolescentes', 'Jóvenes', 'Adultos', 'Mayores'])
edad_supervivencia = (titanic.dropna(subset=['Grupo_Edad'])
                     .groupby('Grupo_Edad')['Survived']
                     .apply(lambda x: (x == 'Supervivientes').mean() * 100)
                     .round(2)
                     .sort_values(ascending=False))

# Mostrar resultados
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Por Clase")
    st.write("Mayor supervivencia:")
    st.info(f"1ª Clase: {clase_supervivencia.iloc[0]:.1f}%")
    st.write("Menor supervivencia:")
    st.error(f"3ª Clase: {clase_supervivencia.iloc[-1]:.1f}%")

with col2:
    st.subheader("Por Género")
    st.write("Mayor supervivencia:")
    st.info(f"{genero_supervivencia.index[0].title()}: {genero_supervivencia.iloc[0]:.1f}%")
    st.write("Menor supervivencia:")
    st.error(f"{genero_supervivencia.index[-1].title()}: {genero_supervivencia.iloc[-1]:.1f}%")

with col3:
    st.subheader("Por Edad")
    st.write("Mayor supervivencia:")
    st.info(f"{edad_supervivencia.index[0]}: {edad_supervivencia.iloc[0]:.1f}%")
    st.write("Menor supervivencia:")
    st.error(f"{edad_supervivencia.index[-1]}: {edad_supervivencia.iloc[-1]:.1f}%")

# Perfil óptimo de supervivencia
st.subheader("Perfil con Mayor Probabilidad de Supervivencia:")

# Primero encontramos la mejor combinación que tenga datos suficientes
mejores_perfiles = titanic.groupby(['Pclass', 'Sex', 'Grupo_Edad'])['Survived'].agg(
    supervivencia=lambda x: (x == 'Supervivientes').mean() * 100,
    cantidad=len
).reset_index()

# Filtramos para tener solo grupos con al menos 5 personas
mejores_perfiles = mejores_perfiles[mejores_perfiles['cantidad'] >= 5]
mejor_perfil = mejores_perfiles.sort_values('supervivencia', ascending=False).iloc[0]

st.success(f"""
- {mejor_perfil['Sex'].title()}
- {'Primera' if mejor_perfil['Pclass']==1 else 'Segunda' if mejor_perfil['Pclass']==2 else 'Tercera'} Clase
- {mejor_perfil['Grupo_Edad']}
Tasa de supervivencia: {mejor_perfil['supervivencia']:.1f}%
(Basado en {mejor_perfil['cantidad']} pasajeros)
""")

# Perfil con menor supervivencia
st.subheader("Perfil con Menor Probabilidad de Supervivencia:")
peor_perfil = mejores_perfiles.sort_values('supervivencia').iloc[0]

st.error(f"""
- {peor_perfil['Sex'].title()}
- {'Primera' if peor_perfil['Pclass']==1 else 'Segunda' if peor_perfil['Pclass']==2 else 'Tercera'} Clase
- {peor_perfil['Grupo_Edad']}
Tasa de supervivencia: {peor_perfil['supervivencia']:.1f}%
(Basado en {peor_perfil['cantidad']} pasajeros)
""")



