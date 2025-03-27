import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_byseason_df1(df1):
    byseason_df1 = df1.groupby(by="season_day").weekday.count().reset_index()
    byseason_df1.rename(columns={
        "weekday": "hariKerja"
    }, inplace=True)
    byseason_df1.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}, inplace=True)
    return byseason_df1

def create_byseason_df2(df2):
    byseason_df2 = df2.groupby(by="season_hour").hr.count().reset_index()
    byseason_df2.rename(columns={
        "hr": "jam"
    }, inplace=True)
    byseason_df2.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}, inplace=True)
    return byseason_df2

main_data = pd.read_csv('dashboard\main_data.csv')
main_df = pd.DataFrame(main_data)
df1 = main_df[['season_day', 'weekday']].dropna(axis=0, ignore_index=True)
df2 = main_df[['season_hour', 'hr']].dropna(axis=0, ignore_index=True)

create_byseason_df1(df1)
create_byseason_df2(df2)
st.header('Data: Bike Sharing :partly_sunny_rain:')
 
st.subheader("Demografi Cuaca")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        x="season_day", 
        y="hariKerja", 
        data=create_byseason_df1(df1).sort_values(by="hariKerja", ascending=False),
        ax=ax
    )
    ax.set_title("Cuaca paling sering muncul pada berbagai kerja", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        x="season_hour", 
        y="jam", 
        data=create_byseason_df2(df2).sort_values(by="jam", ascending=False),
        ax=ax
    )
    ax.set_title("Cuaca paling sering muncul pada berbagai jam", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)