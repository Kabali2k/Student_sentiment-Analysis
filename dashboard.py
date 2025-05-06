import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Connect to database
conn = sqlite3.connect('feedback.db', check_same_thread=False)
df = pd.read_sql_query('SELECT * FROM feedback', conn)

st.title("📊 Student Feedback Dashboard")

st.subheader("Overall Sentiment Distribution")
sentiment_chart = alt.Chart(df).mark_bar().encode(
    x='sentiment:N',
    y='count()',
    color='sentiment:N'
)
st.altair_chart(sentiment_chart, use_container_width=True)

st.subheader("Department-wise Feedback Count")
dept_chart = alt.Chart(df).mark_bar().encode(
    x='department:N',
    y='count()',
    color='department:N'
)
st.altair_chart(dept_chart, use_container_width=True)

st.subheader("Emotion Distribution")
emotion_chart = alt.Chart(df).mark_bar().encode(
    x='emotion:N',
    y='count()',
    color='emotion:N'
)
st.altair_chart(emotion_chart, use_container_width=True)

st.subheader("View Raw Data")
st.dataframe(df)
