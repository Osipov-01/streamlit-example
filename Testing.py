import pandas as pd
import random as rd #импорт библиотеки случайных чисел
import matplotlib.pyplot as plt #отображение графиков
import streamlit as st
import numpy as np

st.title("Hello")
 
pd.options.display.float_format = '{:,.1f}'.format

#читаем 2 датасета
mkrf_movies = pd.read_csv('E:/МИИТ/Диплом pandas python/mkrf_movies.csv')
mkrf_shows = pd.read_csv('E:/МИИТ/Диплом pandas python/mkrf_shows.csv')

print(mkrf_movies.info())
print(mkrf_shows.info())
st.write(mkrf_movies.head())
print(mkrf_shows.head())

print(mkrf_movies.dtypes)
print(mkrf_shows.dtypes)

# Преобразование столбцов в формат str, 
# т.к. номер прокатного удостоверения никак в дальнейшем не связан с математическими операциями
mkrf_shows['puNumber'] = mkrf_shows['puNumber'].astype('str')
mkrf_movies['puNumber'] = mkrf_movies['puNumber'].astype('str')

# Объединение двух данных в один - mkrf_movies
print('Размер таблицы до объединения:', mkrf_movies.shape)
mkrf_movies = mkrf_movies.merge(mkrf_shows, on='puNumber', how='left')
print('Размер таблицы после объединения:', mkrf_movies.shape)

mkrf_movies.head()
print(mkrf_movies.dtypes)

def show_start_date(row):
    show_start_date = row['show_start_date']
    show_start_date = show_start_date[:-5]
    return show_start_date

mkrf_movies['show_start_date'] = mkrf_movies.apply(show_start_date, axis=1)

mkrf_movies['show_start_date'] = pd.to_datetime(mkrf_movies['show_start_date'], format='%Y-%m-%dT%H:%M:%S')
mkrf_movies['ratings'] = pd.to_numeric(mkrf_movies['ratings'], errors='coerce')

mkrf_movies[['ratings','show_start_date']].dtypes

print(mkrf_movies.isnull().sum())
print(mkrf_movies.shape)

# Удаление строк с пустыми записями в данных столбцах
mkrf_movies.dropna(subset=['film_studio'], inplace=True) #студия-производитель
mkrf_movies.dropna(subset=['production_country'], inplace=True) #страна-производитель
mkrf_movies.dropna(subset=['director'], inplace=True) #режиссёр
mkrf_movies.dropna(subset=['producer'], inplace=True) #продюсер
mkrf_movies = mkrf_movies.reset_index(drop=True)

#Заполнение столбцов с фильмами без гос.поддержки

#объём возвратных средств государственной поддержки
mkrf_movies['refundable_support'] = mkrf_movies['refundable_support'].fillna(-1) 
#объём невозвратных средств государственной поддержки
mkrf_movies['nonrefundable_support'] = mkrf_movies['nonrefundable_support'].fillna(-1) 
#источник государственного финансирования
mkrf_movies['financing_source'] = mkrf_movies['financing_source'].fillna('Частный') 
#mkrf_movies['budget'] = mkrf_movies['budget'].fillna(rd.randint(1000000,100000000)) #общий бюджет фильма

#Заполнение столбцов значениями -1
mkrf_movies['ratings'] = mkrf_movies['ratings'].fillna(-1) #рейтинг фильма на КиноПоиске
mkrf_movies['box_office'] = mkrf_movies['box_office'].fillna(-1) #сборы в рублях

#Заполнение столбца жанра фильма значением - 'другое'
mkrf_movies['genres'] = mkrf_movies['genres'].fillna('другое') #жанр фильма

def fill_budget(row):
    budget = row['budget']
    if budget is None:
        budget = -1
    elif budget != budget:                          #это условие соблюдается при значении nan
        budget = -1
    return budget

mkrf_movies['budget'] = mkrf_movies.apply(fill_budget, axis=1)

print(mkrf_movies.isnull().sum())
print(mkrf_movies.shape)

mkrf_movies['type'] = mkrf_movies['type'].str.strip()
mkrf_movies['film_studio'] = mkrf_movies['film_studio'].str.strip()
mkrf_movies['production_country'] = mkrf_movies['production_country'].str.strip()

def production_country(row):
    production_country = row['production_country']
    production_country = production_country.replace(' -', '-')
    production_country = production_country.replace('- ', '-')
    production_country = production_country.replace('--', '-')
    production_country = production_country.replace('-', ', ')
    production_country = production_country.replace(',,', ', ')
    production_country = production_country.replace(',', ', ')  
    production_country = production_country.replace(',  ', ', ')
    production_country = production_country.replace('К;анада', 'Канада')
    production_country = production_country.replace('Пуэрто,Рико', 'Пуэрто Рико')
    production_country = production_country.replace('Н.Зеландия', 'Новая Зеландия')
    production_country = production_country.replace('Белоруссия', 'Беларусь')
    production_country = production_country.replace('Республика Беларусь', 'Беларусь')
    production_country = production_country.replace('Республика Казахстан', 'Казахстан')
    production_country = production_country.replace('Чешская Республика', 'Чехия')
    production_country = production_country.replace('Ю.Корея', 'Южная Корея')
    production_country = production_country.replace('Сша', 'США')
#     production_country = production_country.lower()
    if production_country == '2019':
        return None
    return production_country

mkrf_movies['production_country'] = mkrf_movies.apply(production_country, axis=1)
mkrf_movies.dropna(subset=['production_country'], inplace=True)
mkrf_movies = mkrf_movies.reset_index(drop=True)

def refundable_support(row):
    refundable_support = row['refundable_support']
    financing_source = row['financing_source']
    if financing_source == 'Министерство культуры, Фонд кино':
#         if refundable_support == 0:
#             refundable_support = rd.randint(1000000,8173440)
        if refundable_support >= 100000000:
            refundable_support /= 10
    elif financing_source == 'Фонд кино':
#         if refundable_support == 0:
#             refundable_support = rd.randint(1000000,15000000)
        if refundable_support >= 100000000:
            refundable_support /= 10
    return refundable_support

# Устранение аномалий
def nonrefundable_support(row):
    nonrefundable_support = row['nonrefundable_support']
    financing_source = row['financing_source']
    if financing_source == 'Министерство культуры, Фонд кино':
        if nonrefundable_support >= 100000000:
            nonrefundable_support /= 10
    elif financing_source == 'Фонд кино':
#         if nonrefundable_support == 0:
#             nonrefundable_support = rd.randint(1000000,25000000)
        if nonrefundable_support >= 100000000:
            nonrefundable_support /= 10
    return nonrefundable_support

# Устранение аномалий
def budget(row):
    budget = row['budget']
    financing_source = row['financing_source']
    if financing_source == 'Министерство культуры':
#         if budget == 0:
#             budget = rd.randint(1000000,38500000)
        if budget >= 100000000:
            budget /= 10
    elif financing_source == 'Министерство культуры, Фонд кино':
#         if budget == 0:
#             budget = rd.randint(1000000,58449024)
        if budget >= 100000000:
            budget /= 10
    elif financing_source == 'Фонд кино':
#         if budget == 0:
#             budget = rd.randint(1000000,62044646)
        if budget >= 100000000:
            budget /= 10
    return budget

# Устранение аномалий
def box_office(row):
    box_office = row['box_office']
    financing_source = row['financing_source']
    if financing_source == 'Министерство культуры':
        if box_office >= 100000000:
            box_office /= 100
    elif financing_source == 'Министерство культуры, Фонд кино':
        if box_office >= 100000000:
            box_office /= 100
    elif financing_source == 'Фонд кино':
        if box_office >= 1000000000:
            box_office /= 100
    elif financing_source == 'Частный':
#         if box_office == 0:
#             box_office = rd.randint(1000,2591609)
        if box_office >= 1000000000:
            box_office /= 1000
        elif box_office >= 100000000:
            box_office /= 100   
    return box_office

mkrf_movies['refundable_support'] = mkrf_movies.apply(refundable_support, axis=1)
mkrf_movies['nonrefundable_support'] = mkrf_movies.apply(nonrefundable_support, axis=1)
mkrf_movies['budget'] = mkrf_movies.apply(budget, axis=1)
mkrf_movies['box_office'] = mkrf_movies.apply(box_office, axis=1)

def edit_budget(row):
    refundable_support = row['refundable_support']
    nonrefundable_support = row['nonrefundable_support']
    budget = row['budget']
    if budget < refundable_support + nonrefundable_support:
        budget = refundable_support + nonrefundable_support
    return budget

mkrf_movies['budget'] = mkrf_movies.apply(edit_budget, axis=1)

mkrf_movies['show_start_date_year'] = mkrf_movies['show_start_date'].dt.year

def add_main(mkrf_movies, columns):
    for column in columns:
        mkrf_movies[f'main_{column}'] = mkrf_movies[column].dropna().apply(lambda x: x.split(',')[0])
    return mkrf_movies

mkrf_movies = add_main(mkrf_movies, ['director', 'genres'])

def support_ratio(row):
    budget = row['budget']
    refundable_support = row['refundable_support']
    nonrefundable_support = row['nonrefundable_support']
    if (refundable_support == -1) | (nonrefundable_support == -1):
        support_ratio = -1
    else:
        support_ratio = (refundable_support + nonrefundable_support)/budget
    return support_ratio

mkrf_movies['support_ratio'] = mkrf_movies.apply(support_ratio, axis=1)

st.write('Обработанная таблица')
st.write(mkrf_movies)

print(mkrf_movies.query('box_office != -1').groupby('show_start_date_year')['title'].count())
mkrf_movies.query('box_office != -1').groupby('show_start_date_year')['title'].count().plot(style='-o', grid=True)
plt.show()



print(mkrf_movies.query('box_office != -1').groupby('show_start_date_year')['box_office'].sum())
(mkrf_movies.query('box_office != -1').groupby('show_start_date_year')['box_office']
 .sum().plot(style='-o', grid=True, figsize=(12,8)))
plt.show()


table = mkrf_movies.query('box_office != -1').pivot_table(values='box_office', index='show_start_date_year', aggfunc=[np.mean, np.median])
st.write(table)
table.plot(style='-o', grid=True)
st.line_chart(table)
plt.show()

table = ( mkrf_movies.query('show_start_date_year >= 2015 and box_office != -1')
 .pivot_table(values='box_office', index='show_start_date_year', columns='age_restriction', aggfunc=[np.sum])
)
print(table)
table.plot(style='-o', grid=True, figsize = (12,8))
st.line_chart(table)
plt.show()

mkrf_movies_support = mkrf_movies.query('financing_source != "Частный"')
#Столбец - (абсолютная) оккупаемость фильма
mkrf_movies_support['profit'] = mkrf_movies_support['box_office'] - mkrf_movies_support['budget']
#Столбец - (относительная) оккупаемость фильма
mkrf_movies_support['relational_profit'] = mkrf_movies_support['box_office']/mkrf_movies_support['budget'] - 1
#Столбец - возможный долг перед государством, т.е. баланс
mkrf_movies_support['balance'] = mkrf_movies_support['box_office'] - mkrf_movies_support['refundable_support']
#Столбец - общая гос. поддержка
mkrf_movies_support['sum_support'] = mkrf_movies_support['refundable_support'] + mkrf_movies_support['nonrefundable_support']

#Столбец - доля гос.поддержки фильма
mkrf_movies_support['fraction_support'] = mkrf_movies_support['sum_support']/mkrf_movies_support['budget']

mkrf_movies_support = mkrf_movies_support.sort_values(by='sum_support', ascending=False)
st.write(mkrf_movies_support[['title','balance','profit','relational_profit','sum_support']].head(10).reset_index())

mkrf_movies_support = mkrf_movies_support.sort_values(by='profit', ascending=False)
st.write(mkrf_movies_support[['title','profit']].head(10).reset_index())
mkrf_movies_support = mkrf_movies_support.sort_values(by='relational_profit', ascending=False)
st.write(mkrf_movies_support[['title','relational_profit']].head(10).reset_index())

mkrf_movies_support = mkrf_movies_support.sort_values(by='profit', ascending=False)
(mkrf_movies_support[['title','profit']].head(10).reset_index()
 .plot(title = 'Рейтинг окупаемости фильмов по абсолютным показателям', x='title', y='profit', kind='bar',
       grid=True, figsize=(10,6)))
mkrf_movies_support_new = mkrf_movies_support[['title','profit']].head(10).reset_index()       
st.bar_chart(mkrf_movies_support_new, x='title', y='profit')


plt.show()
mkrf_movies_support = mkrf_movies_support.sort_values(by='relational_profit', ascending=False)
(mkrf_movies_support[['title','relational_profit']].head(10).reset_index()
 .plot(title = 'Рейтинг окупаемости фильмов по относительным показателям', x='title', y='relational_profit', 
       kind='bar', grid=True, figsize=(10,6)))
plt.show()

mkrf_movies_support = mkrf_movies_support.sort_values(by='ratings', ascending=False)
st.write(mkrf_movies_support[['title','balance','profit','relational_profit','ratings']].head(10).reset_index())

(mkrf_movies_support[['title','ratings']].head(10).reset_index()
 .plot(title = 'Рейтинг фильмов', x='title', y='ratings', kind='bar',
       grid=True, figsize=(10,6)))
plt.show()

table = (mkrf_movies_support.pivot_table(values='fraction_support', index='show_start_date_year', aggfunc=[np.mean, np.median]))
st.write(table)
(table
 .plot(style='-o', grid=True, title='среднюю и медианную долю гос.поддержки фильмов за период 2010-2019 гг.', 
      figsize=(12,8)))
plt.show()