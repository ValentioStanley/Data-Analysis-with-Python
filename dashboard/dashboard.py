import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_byseason_df1(df1):
    byseason_df1 = df1.groupby(by="season").weekday.count().reset_index()
    byseason_df1.rename(columns={
        "weekday": "hariKerja"
    }, inplace=True)
    byseason_df1.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}, inplace=True)
    return byseason_df1

def create_byseason_df2(df2):
    byseason_df2 = df2.groupby(by="season").hr.count().reset_index()
    byseason_df2.rename(columns={
        "hr": "jam"
    }, inplace=True)
    byseason_df2.replace({1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}, inplace=True)
    return byseason_df2

df1 = pd.read_csv("submission\dashboard\df_day.csv")
df2 = pd.read_csv("submission\dashboard\df_hour.csv")

create_byseason_df1(df1)
create_byseason_df2(df2)
st.header('Data: Bike Sharing :sparkles:')
 
st.subheader("Season Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        x="season", 
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
        x="season", 
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