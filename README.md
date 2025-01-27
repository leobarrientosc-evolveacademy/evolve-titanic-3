# Análisis de Supervivientes del Titanic con Streamlit

## Descripción
Una aplicación interactiva para explorar y analizar los factores que influyeron en la supervivencia de los pasajeros del Titanic.

## Introducción
El RMS Titanic fue un transatlántico británico que se hundió en su viaje inaugural en 1912, convirtiéndose en uno de los desastres marítimos más famosos de la historia. El conjunto de datos del Titanic se ha convertido en un recurso clásico para el análisis de datos y el aprendizaje automático, permitiendo explorar factores sociales, económicos y demográficos que pudieron influir en la supervivencia de los pasajeros.

### Objetivo del Proyecto
Este proyecto busca responder preguntas clave como:
- ¿Qué factores socioeconómicos influyeron en la supervivencia?
- ¿Existió un sesgo de género o edad en las tasas de supervivencia?
- ¿Cómo influyó la clase del pasajero en sus posibilidades de sobrevivir?

### Alcance del Proyecto
El análisis incluye:
- Análisis exploratorio de datos
- Visualizaciones interactivas
- Estadísticas descriptivas
- Correlaciones entre variables

## Datos Utilizados

### Fuente de Datos
Los datos provienen de la competencia "Titanic: Machine Learning from Disaster" de Kaggle.

### Descripción del Dataset
- Número de registros: 891 pasajeros
- Variables principales:
  - Survived: Supervivencia (0 = No, 1 = Sí)
  - Pclass: Clase del pasajero (1, 2, 3)
  - Name: Nombre del pasajero
  - Sex: Género
  - Age: Edad
  - SibSp: Número de hermanos/cónyuges a bordo
  - Parch: Número de padres/hijos a bordo
  - Ticket: Número de ticket
  - Fare: Tarifa pagada
  - Cabin: Número de cabina
  - Embarked: Puerto de embarque

### Preprocesamiento de Datos
- Manejo de valores faltantes en edad mediante imputación
- Codificación de variables categóricas
- Normalización de variables numéricas
- Creación de nuevas características

## Funcionalidades de la Aplicación

### Visualizaciones
- Distribución de supervivencia por clase
- Pirámide poblacional por edad y género
- Análisis de tarifas por clase
- Tasas de supervivencia por puerto de embarque
- Correlación entre variables numéricas

### Interactividad
- Filtros por clase de pasajero
- Selectores de variables para visualización
- Rangos de edad ajustables
- Opciones de agrupación de datos

### Hallazgos Clave
- Mayor tasa de supervivencia en primera clase
- Las mujeres tuvieron mayor probabilidad de sobrevivir
- Los niños tuvieron prioridad en el rescate
- El puerto de embarque influyó en la supervivencia

## Instalación y Uso

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicación: `streamlit run app.py`

## Tecnologías Utilizadas
- Python
- Pandas
- Streamlit
- Plotly
- Seaborn

