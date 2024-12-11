import streamlit as st
import joblib
import pandas as pd
import json

st.title('PetClassifier 🐶🐱')
st.subheader('Clasificador de mascotas')

st.image("./images/image.png", use_container_width=True)

# Carga el modelo y las asignaciones para el color de ojos y el largo del pelo
model = joblib.load('./model/pets_cls_model.joblib')
with open('./model/category_mapping.json', 'r') as f:
    category_mapping = json.load(f)
    
# Extraemos los valores categoricos
eye_color_values = category_mapping['eye_color']
fur_length_values = category_mapping['fur_length']

st.write('Rellena los campos para clasificar tu mascota')

# Creamos los campos de entrada
weight = st.number_input('Peso (kg)', min_value=0.1, max_value=100.0, placeholder='Peso en kg', value=None)
height = st.number_input('Altura (cm)', min_value=10.0, max_value=100.0, placeholder='Altura en cm', value=None)

eye_color_options = {
    'Azul': 'Blue',
    'Marrón': 'Brown',
    'Gris': 'Gray',
    'Verde': 'Green'
}

fur_length_options = {
    'Largo': 'Long',
    'Medio': 'Medium',
    'Corto': 'Short'
}

eye_color = st.selectbox('Color de ojos', list(eye_color_options.keys()), index=None, placeholder='Selecciona un color de ojos')
fur_length = st.selectbox('Largo del pelo', list(fur_length_options.keys()), index=None, placeholder='Selecciona un largo de pelo')

if st.button('Clasificar'):
  eye_color_value = eye_color_options[eye_color]
  fur_length_value = fur_length_options[fur_length]

  # Generamos la columnas binarias para eye_color y fur_length
  eye_color_binary = [int(color == eye_color_value) for color in eye_color_values]
  fur_length_binary = [int(length == fur_length_value) for length in fur_length_values]

  # Creamos un dataframe con los valores introducidos
  input_data = [weight, height] + eye_color_binary + fur_length_binary
  columns = ['weight_kg', 'height_cm'] + [f"eye_color_{color}" for color in eye_color_values] + [f"fur_length_{length}" for length in fur_length_values]
  input_df = pd.DataFrame([input_data], columns=columns)

  # Realizamos la predicción
  prediction = model.predict(input_df)[0]
  prediction_proba = model.predict_proba(input_df)[0]

  # Diccionario para mapear las predicciones a emojis y nombres en español
  animal_emojis = {
    'cat': '🐱',
    'dog': '🐶',
    'rabbit': '🐰'
  }

  animal_names_es = {
    'cat': 'gato',
    'dog': 'perro',
    'rabbit': 'conejo'
  }

  # Realizamos la predicción
  prediction = model.predict(input_df)[0]
  prediction_proba = model.predict_proba(input_df)[0]

  # Mostramos el resultado
  st.write('### Resultado')

  # Mostramos el resultado con el emoji y el nombre en español correspondiente
  st.success(f'La mascota es un {animal_names_es.get(prediction, "")}', icon=animal_emojis.get(prediction, ""))