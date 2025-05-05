import streamlit as st
import pandas as pd
import os
import text2emotion as te
import transformers 
import pipeline

feedback_file = 'feedback.csv'

st.title("📊 Student Feedback Dashboard")

if os.path.exists(feedback_file):
    df = pd.read_csv(feedback_file)

    if df.empty:
        st.warning("No feedback data available yet.")
    else:
        st.subheader("Feedback Data")
        st.dataframe(df)

        st.subheader("Department-wise Analysis")
        st.bar_chart(df['department'].value_counts())

        st.subheader("Sentiment Analysis")
        st.bar_chart(df['sentiment'].value_counts())

        st.subheader("Emotion Analysis")
        st.bar_chart(df['emotion'].value_counts())

        st.subheader("Recent Feedback")
        st.write(df.tail(10))
else:
    st.warning("No feedback data file found. Please collect feedback first.")
