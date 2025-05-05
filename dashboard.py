import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to SQLite
conn = sqlite3.connect('feedback.db', check_same_thread=False)
df = pd.read_sql_query('SELECT * FROM feedback', conn)

st.title("📊 Student Sentiment Dashboard")

if df.empty:
    st.warning("No feedback submitted yet.")
else:
    st.subheader("Overall Sentiment Counts (VADER)")
    vader_counts = df['sentiment_vader'].value_counts()
    st.bar_chart(vader_counts)

    st.subheader("Department-wise Sentiment (VADER)")
    dept_summary = df.groupby('department')['sentiment_vader'].value_counts().unstack().fillna(0)
    st.write(dept_summary)

    # Pie chart per department
    for dept in df['department'].unique():
        dept_df = df[df['department'] == dept]
        fig = px.pie(dept_df, names='sentiment_vader', title=f'{dept} Sentiment Breakdown')
        st.plotly_chart(fig)

    # Automated alerts
    negative_counts = df[df['sentiment_vader'] == 'Negative'].groupby('department').size()
    for dept, count in negative_counts.items():
        if count > 5:
            st.error(f"🚨 High negative feedback in {dept}: {count} reports")
        else:
            st.success(f"{dept} is doing fine: {count} negative reports")

    # Recommendations
    st.subheader("Recommendations")
    for dept, count in negative_counts.items():
        if count > 5:
            st.info(f"🔧 {dept}: Organize a feedback session or address concerns.")
        else:
            st.success(f"🎉 {dept}: Keep up the good work!")
