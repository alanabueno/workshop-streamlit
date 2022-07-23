import streamlit as st
import pandas as pd
import numpy as np

st.title('Embarques de Uber em NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Carregando dados...')
data = load_data(10000)
data_load_state.text("Pronto! (using st.cache)")

if st.checkbox('Mostrar Dados Brutos'):
    st.subheader('Dados Brutos')
    st.write(data)

st.subheader('Número de embarques por hora')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hora', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Mapa de todos os embarques as %s:00' % hour_to_filter)
st.map(filtered_data)