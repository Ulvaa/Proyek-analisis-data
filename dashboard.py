import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#data frame
def create_hari_df(df):
    df_hari = day_data_df.groupby('weekday')['cnt'].sum().reset_index()
    day_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    df_hari['weekday'] = df_hari['weekday'].map(day_mapping)
    return df_hari

def create_jam_df(df):
    df_hour = hour_data_df.groupby('hr')['cnt'].sum().reset_index()
    return df_hour

def create_season_df(df):
    season_grouped = day_data_df.groupby('season')['cnt'].mean().reset_index()
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season_grouped['season'] = season_grouped['season'].map(season_mapping)
    return season_grouped

def create_weather_df(df):
    weather_grouped = day_data_df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_mapping = {1: 'Sunny', 2: 'Cloudy ', 3: 'Light Rain/Light Snow', 4: 'Extreme'}
    weather_grouped['weathersit'] = weather_grouped['weathersit'].map(weather_mapping)
    return weather_grouped

def create_workday_df(df):
    workingday_df = day_data_df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
    workingday_labels = {0: 'Libur', 1: 'Working Day'}
    return workingday_df

day_data_df = pd.read_csv("day_data.csv")
hour_data_df = pd.read_csv("hour_data.csv")

#dataframe filter tanggal

dateday_columns = ["dteday"]
day_data_df.sort_values(by="dteday", inplace=True)
day_data_df.reset_index(inplace=True)
 
for column in dateday_columns:
    day_data_df[column] = pd.to_datetime(day_data_df[column])

#filter
min_date = day_data_df["dteday"].min()
max_date = day_data_df["dteday"].max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# main df
main_df = day_data_df[(day_data_df["dteday"] >= str(start_date)) & 
                (day_data_df["dteday"] <= str(end_date))]

# filter main df
df_hari = create_hari_df(main_df)
df_hour = create_hari_df(main_df)
season_grouped = create_season_df(main_df)
weather_grouped = create_weather_df(main_df)
workingday_df = create_workday_df(main_df)

#header
st.header('The Bikers :bike:')

#grafik 1
st.subheader('Pengguna Harian')

data_grafik1 = day_data_df

df_hari = pd.DataFrame(data_grafik1)

col1 = st.columns(1)
 
with col1[0]:
    total_pengguna = df_hari['cnt'].sum()
    st.metric("Total Pengguna", value=total_pengguna)
 
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    df_hari["dteday"],
    df_hari["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# grafik 2
st.subheader("Musim dan Cuaca")
 
col1, col2 = st.columns(2)
 
with col1:
    df_hari = day_data_df.groupby('season')['cnt'].sum().reset_index()

    day_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

    df_hari['season'] = df_hari['season'].map(day_mapping)

    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
    sns.barplot(
        y="cnt", 
        x="season",
        data=df_hari.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Pengguna Berdasarkan Musim", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    df_hari = day_data_df.groupby('weathersit')['cnt'].sum().reset_index()

    day_mapping = {1: 'Sunny', 2: 'Cloudy', 3: 'Light Rain/Snow', 4: 'Extreme'}

    df_hari['weathersit'] = df_hari['weathersit'].map(day_mapping)
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
    sns.barplot(
        y="cnt", 
        x="weathersit",
        data=df_hari.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Jumlah Pengguna Berdasarkan Cuaca", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# grafik 3
st.subheader("Hari Kerja Vs Hari Libur")

data_work= day_data_df
df_hari = pd.DataFrame(data_work)

# Menghitung jumlah pengguna berdasarkan workingday
workingday_df = df_hari.groupby('workingday')['cnt'].sum().reset_index()
 
col1, col2 = st.columns(2)
 
with col1:
    workingday_df = df_hari.groupby('workingday')['casual'].sum().reset_index()

# label untuk pie chart
    labels = ['Hari Libur', 'Hari Kerja']

# Mengambil data jumlah pengguna casual untuk hari kerja dan hari libur
    sizes = workingday_df['casual']

# Membuat figure untuk pie chart
    fig, ax = plt.subplots(figsize=(8, 8))

# pie chart
    ax.pie(
        sizes,                       
        labels=labels,                
        autopct='%1.1f%%',            
        startangle=90,                
        colors=plt.cm.Paired.colors   
    )

    ax.set_title('Proporsi Pengguna Casual: Hari Libur vs Hari Kerja', fontsize=16)

    st.pyplot(fig)
 
with col2:
    workingday_df = df_hari.groupby('workingday')['registered'].sum().reset_index()

# label untuk pie chart
    labels = ['Hari Libur', 'Hari Kerja']

# Mengambil data jumlah pengguna casual untuk hari kerja dan hari libur
    sizes = workingday_df['registered']

# Membuat figure untuk pie chart
    fig, ax = plt.subplots(figsize=(8, 8))

# pie chart
    ax.pie(
        sizes,                       
        labels=labels,                
        autopct='%1.1f%%',            
        startangle=90,                
        colors=plt.cm.Paired.colors   
    )

    ax.set_title('Proporsi Pengguna Terdaftar Hari Libur vs Hari Kerja', fontsize=16)

    st.pyplot(fig)