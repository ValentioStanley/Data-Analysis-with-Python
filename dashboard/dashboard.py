import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_byseason_df1(df1):
    df1.musim_hari = df1.musim_hari.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"})
    group_df1 = df1.groupby(by=["musim_hari","hari_kerja"]).agg({"musim_hari":"count"}).rename(columns={'musim_hari': 'jml_musim_hari'}).reset_index()
    byseason_df1 = pd.merge(left=df1, right=group_df1, on=["musim_hari","hari_kerja"], how="right")
    return byseason_df1

def create_byseason_df2(df2):
    df2.musim_jam = df2.musim_jam.replace({3: "Fall", 4: "Winter"})
    group_df2 = df2.groupby(by=["musim_jam","jam"]).agg({"musim_jam":"count"}).rename(columns={'musim_jam': 'jml_musim_jam'}).reset_index()
    loc_df2 = group_df2.loc[(group_df2.musim_jam=="Fall") | (group_df2.musim_jam=="Winter")].reset_index(drop=True)
    byseason_df2= pd.merge(left=df2, right=loc_df2, on=["musim_jam","jam"], how="right")
    return byseason_df2

def create_bydata_df3(df3): 
    df3.musim_jam = df3.musim_jam.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"})
    df3 = df3.rename(columns={"tgl_hari_jam":"tgl_hari_libur","musim_jam":"musim_libur"})
    group_df3 = df3.groupby(by=["musim_libur"]).agg({"hari_libur":"sum"}).rename(columns={'hari_libur': 'jumlah_libur'}).reset_index()
    return group_df3

def create_bydata_df3(df3): 
    df3.musim_jam = df3.musim_jam.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"})
    df3 = df3.rename(columns={"tgl_hari_jam":"tgl_hari_libur","musim_jam":"musim_libur"})
    group_df3 = df3.groupby(by=["musim_libur"]).agg({"hari_libur":"sum"}).rename(columns={'hari_libur': 'jumlah_libur'}).reset_index()
    return group_df3

def create_byseason_dfs(df, season):
    df = df.rename(columns={"tgl_hari_jam":"tgl_hari_libur","musim_jam":"musim_libur"})
    group_season = df.groupby(by=["musim_libur"]).agg({"hari_libur":"sum"}).rename(columns={'hari_libur': 'jumlah_libur'}).reset_index()
    loc_season = group_season.loc[(group_season.musim_libur==season)].reset_index(drop=True)
    return loc_season

main_data = pd.read_csv('dashboard\main_data.csv')

datetime_col = ["tgl_hari_krj","tgl_hari_jam"]
for column in datetime_col:
    main_data[column] = pd.to_datetime(main_data[column]) 
    
min_date = main_data["tgl_hari_krj"].min()
max_date = main_data["tgl_hari_jam"].max()
 
with st.sidebar:
    st.header('Pilih tanggal hari')
    start_date, end_date = st.date_input(
        label='Jangkauan Waktu',min_value=min_date,max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = main_data[(main_data["tgl_hari_krj"] >= str(start_date)) | (main_data["tgl_hari_jam"] <= str(end_date))]

main_df = pd.DataFrame(main_df)

df1 = main_df[['tgl_hari_krj','musim_hari', 'hari_kerja']].dropna(axis=0, ignore_index=True)
df2 = main_df[['tgl_hari_jam','musim_jam', 'jam']].dropna(axis=0, ignore_index=True)
df3 = main_df[['tgl_hari_jam','musim_jam', 'hari_libur']].dropna(axis=0, ignore_index=True)

df1 = create_byseason_df1(df1)
df2 = create_byseason_df2(df2) 
all_df_hour = create_bydata_df3(df3)

seasons = main_df['musim_jam'].replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}).drop_duplicates()

for season in seasons:
    if season == "Springer":
        df_springer = create_byseason_dfs(df3, season)
    elif season == "Summer":
        df_summer = create_byseason_dfs(df3, season)
    elif season == "Fall":
        df_fall = create_byseason_dfs(df3, season)
    elif season == "Winter":
        df_winter = create_byseason_dfs(df3, season)

st.header('Data: Bike Sharing :partly_sunny_rain:')
 
st.subheader("Demografi Musim")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        x="musim_hari", 
        y="hari_kerja", 
        data=df1.sort_values(by="tgl_hari_krj", ascending=True),
        ax=ax
    )
    ax.set_title("Frekuensi varian musim pada weekday", loc="center", fontsize=50)
    ax.set_ylabel("Hari Kerja", fontsize = 35)
    ax.set_xlabel("Varian Musim", fontsize = 35)
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["All", "Winter", "Fall", "Summer", "Springer"])

with tab1:
    st.header("All season")
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="musim_libur", 
        y="jumlah_libur", 
        data=all_df_hour.sort_values(by="jumlah_libur", ascending=True),
        ax=ax
    )
    ax.set_title("Frekuensi hari libur pada berbagai jenis musim", loc="center", fontsize=35)
    ax.set_xlabel("Jenis musim", fontsize = 35)
    ax.set_ylabel("Jumlah hari libur", fontsize = 35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)

def create_eachseason_bar(df_eachseason):
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        x="musim_libur", 
        y="jumlah_libur", 
        data=df_eachseason,
        ax=ax
    )
    ax.set_title("Frekuensi hari libur pada Musim " + df_eachseason.musim_libur.to_string(index=False), loc="center", fontsize=35)
    ax.set_xlabel("Musim", fontsize = 35)
    ax.set_ylabel("Jumlah hari libur", fontsize = 35)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)

with tab2:
    st.header("Winter")
    create_eachseason_bar(df_winter)
    
with tab3:
    st.header("Fall")
    create_eachseason_bar(df_fall)
    
with tab4:
    st.header("Summer")
    create_eachseason_bar(df_summer)
    
with tab5:
    st.header("Springer")
    create_eachseason_bar(df_springer)
