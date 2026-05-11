import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3

st.set_page_config(page_title="Автопарк Напомняния", layout="wide")

# База данни
conn = sqlite3.connect('autopark.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY, 
    reg_number TEXT UNIQUE, 
    brand TEXT, 
    model TEXT, 
    year INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY, 
    vehicle_id INTEGER, 
    doc_type TEXT, 
    end_date TEXT, 
    company TEXT, 
    notes TEXT
)''')
conn.commit()

st.title("🚗 Автопарк - Напомняния")

# Просто меню
page = st.sidebar.selectbox("Избери страница", 
    ["📊 Dashboard", "➕ Добавяне", "📋 Списък", "⚠️ Напомняния"])

if page == "📊 Dashboard":
    st.header("Dashboard")
    docs = pd.read_sql("SELECT * FROM documents", conn)
    if not docs.empty:
        st.dataframe(docs)

elif page == "➕ Добавяне":
    st.header("Добавяне на автомобил")
    with st.form("vehicle"):
        reg = st.text_input("Регистрационен номер")
        brand = st.text_input("Марка")
        model = st.text_input("Модел")
        if st.form_submit_button("Запази автомобил"):
            c.execute("INSERT INTO vehicles (reg_number, brand, model) VALUES (?,?,?)", (reg, brand, model))
            conn.commit()
            st.success("Автомобилът е добавен!")

elif page == "📋 Списък":
    st.header("Автомобили")
    st.dataframe(pd.read_sql("SELECT * FROM vehicles", conn))

elif page == "⚠️ Напомняния":
    st.header("Напомняния")
    st.info("Тук ще се показват предстоящите изтичания")

st.caption("Автопарк приложение - версия 1")
