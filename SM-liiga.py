import pandas as pd
import streamlit as st

#data = pd.read_csv('C:/Users/User/Desktop/SM-liiga/SM-liiga.csv', encoding='cp1251', sep=';')

a,b = st.slider("Select Price Range:", 1, 16, step = 1)

st.subheader('Input xlsx file')
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    order_places = data['М']
    data.set_index('М', inplace=True)
#st.table(data)
#data = data.sort_values(by='Команда')
    data = data.set_index(order_places)
    data = data.sort_values(by='ЗШ', ascending=False)
    data = data.sort_values(by='±Ш', ascending=False)
    data = data.sort_values(by='ВБ', ascending=False)
    data = data.sort_values(by='В', ascending=False)
    data = data.sort_values(by='О', ascending=False)
    data = data.set_index(order_places)
    data['%О'] = data['%О']*100
#data1 = pd.read_excel(C:/Users/User/Desktop/SM-liiga/SM-liiga.xlsx'')
                                                                                             

    st.dataframe(data[a:b])
    print(data.columns)
    #st.table(data.columns)

choose_tur = ['Тур 1', 'Тур 2',
'Тур 3', 'Тур 4', 'Тур 5', 'Тур 6', 'Тур 7', 'Тур 8', 'Тур 9', 'Тур 10', 'Тур 11','Тур 12','Тур 13',
'Тур 14', 'Тур 15']
