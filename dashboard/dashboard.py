import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set_theme(style='darkgrid')

# Helper function
def create_daily_rent_df(df):
    return df.resample(rule='D', on='dteday').agg({"cnt": "sum"}).reset_index()

def create_weather_rent_df(df):
    return df.groupby(by='weathersit').agg({'cnt': 'mean'}).reset_index()

def create_season_rent_df(df):
    return df.groupby(by='season').agg({'cnt': 'sum'}).reset_index()

def create_hourly_rent_df(df):
    return df.groupby(by=['hr', 'workingday']).agg({'cnt': 'mean'}).reset_index()

# Load Data
try:
    all_df = pd.read_csv("main_data.csv")
except FileNotFoundError:
    all_df = pd.read_csv("dashboard/main_data.csv")

# Memastikan tipe datetime dan mengekstrak tanggalnya saja untuk kalender
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
min_date = all_df["dteday"].min().date()
max_date = all_df["dteday"].max().date()

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<br>" * 8, unsafe_allow_html=True)   
    # Filter Rentang Waktu (Terkunci di 2011-2012)
    st.header("📅 Filter Rentang Waktu")
    
    try:
        start_date, end_date = st.date_input(
            label='Pilih Tanggal Peminjaman',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Wajib memilih tanggal mulai dan tanggal akhir!")
        st.stop()

# ==========================================
# FILTERING DATA UTAMA
# ==========================================
main_df = all_df[(all_df["dteday"].dt.date >= start_date) & 
                 (all_df["dteday"].dt.date <= end_date)]

daily_rent_df = create_daily_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
hourly_rent_df = create_hourly_rent_df(main_df)

# ==========================================
# MAIN PAGE (KONTEN DASHBOARD)
# ==========================================
st.title('🚲 Bike Sharing Dashboard')

# 1. METRICS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Peminjaman", value=f"{main_df.cnt.sum():,}")
with col2:
    st.metric("Pelanggan Casual", value=f"{main_df.casual.sum():,}")
with col3:
    st.metric("Pelanggan Terdaftar", value=f"{main_df.registered.sum():,}")

st.markdown("---")

# 2. TREN HARIAN
st.subheader('Tren Peminjaman Sepeda Harian')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_rent_df["dteday"], daily_rent_df["cnt"], marker='o', linewidth=2, color="#3498db")
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. CUACA & MUSIM
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Logika penentuan warna: Highlight warna biru untuk nilai maksimum, sisanya abu-abu
    colors_weather = ["#72BCD4" if val == weather_rent_df['cnt'].max() else "#D3D3D3" for val in weather_rent_df['cnt']]
    
    sns.barplot(
        x='weathersit', 
        y='cnt', 
        data=weather_rent_df, 
        hue='weathersit', 
        palette=colors_weather, # Memasukkan list warna khusus
        legend=False, 
        ax=ax
    )
    st.pyplot(fig)

with col_b:
    st.subheader("Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Logika penentuan warna: Highlight warna biru untuk nilai maksimum, sisanya abu-abu
    colors_season = ["#72BCD4" if val == season_rent_df['cnt'].max() else "#D3D3D3" for val in season_rent_df['cnt']]
    
    sns.barplot(
        x='season', 
        y='cnt', 
        data=season_rent_df, 
        hue='season', 
        palette=colors_season, # Memasukkan list warna khusus
        legend=False, 
        ax=ax
    )
    st.pyplot(fig)

# 4. POLA JAM
st.subheader("Pola Jam: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', hue='workingday', data=hourly_rent_df, palette='Set1', marker='o', ax=ax)
st.pyplot(fig)

# 5. PROPORSI PELANGGAN
st.subheader("Proporsi Tipe Pelanggan")
labels = ['Casual', 'Registered']
sizes = [main_df.casual.sum(), main_df.registered.sum()]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
ax.axis('equal') 
st.pyplot(fig)

st.caption('Copyright (c) 2026 - Bike Sharing Analysis Dashboard by Aufa')



