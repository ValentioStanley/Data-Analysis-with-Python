import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

main_data = pd.read_csv('dashboard\main_data.csv')
main_df = pd.DataFrame(main_data)
df1 = main_df[['tgl_hari_krj','musim_hari', 'hari_kerja', 'jml_musim_hari']].dropna(axis=0, ignore_index=True)
df2 = main_df[['tgl_hari_jam','musim_jam', 'jam', 'jml_musim_jam']].dropna(axis=0, ignore_index=True)

st.header('Data: Bike Sharing :partly_sunny_rain:')
 
st.subheader("Demografi Musim")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        x="musim_hari", 
        y="hari_kerja", 
        data=df1.sort_values(by="jml_musim_hari", ascending=True),
        ax=ax
    )
    ax.set_title("Frekuensi varian musim pada weekday", loc="center", fontsize=50)
    ax.set_ylabel("Hari Kerja", fontsize = 35)
    ax.set_xlabel("Frekuensi Musim", fontsize = 35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        x="musim_jam", 
        y="jml_musim_jam", 
        data=df2.sort_values(by="jml_musim_jam", ascending=True),
        ax=ax
    )
    ax.set_title("Frekuensi musim dingin", loc="center", fontsize=50)
    ax.set_ylabel("Jumlah musim dingin", fontsize = 35)
    ax.set_xlabel("Musim dingin", fontsize = 35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)

datetime_col = ["tgl_hari_krj","tgl_hari_jam"]
for column in datetime_col:
    main_data[column] = pd.to_datetime(main_data[column])
main_data.info()   
    
min_date = main_data["tgl_hari_jam"].min()
max_date = main_data["tgl_hari_jam"].max()
 
with st.sidebar:
    st.header('Pilih tanggal hari')
    start_date, end_date = st.date_input(
        label='Jangkauan Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = main_data[(main_data["tgl_hari_jam"] >= str(start_date)) & 
                (main_data["tgl_hari_jam"] <= str(end_date))]
