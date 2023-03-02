import streamlit as st
import pandas as pd


file = st.file_uploader()
df = pd.read_excel(file)

print(df.head())

st.table(df.head())
