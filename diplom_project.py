import streamlit as st
import pandas as pd


file = st.file_uploader('Загрузка файла о кино')
df = pd.read_excel(file)

print(df.head())

st.table(df.head())
st.write(df.isnull().sum())

st.write(df.shape)
