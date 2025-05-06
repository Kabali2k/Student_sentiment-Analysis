import streamlit as st
import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()

# Ensure table exists
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        feedback TEXT,
        sentiment TEXT,
        emotion TEXT
    )
''')
conn.commit()

# Load data
try:
    df = pd.read_sql_query('SELECT * FROM feedback', conn)
except Exception as e:
    df = pd.DataFrame(columns=['id', 'name', 'department', 'feedback', 'sentiment', 'emotion'])

# Streamlit dashboard
st.title("📊 Student Feedback Dashboard")

if not df.empty:
    st.dataframe(df)
    st.bar_chart(df['sentiment'].value_counts())
    st.bar_chart(df['emotion'].value_counts())
else:
    st.write("No feedback data available yet.")
