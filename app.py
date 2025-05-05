import streamlit as st
import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Setup analyzers
vader_analyzer = SentimentIntensityAnalyzer()
hf_analyzer = pipeline('sentiment-analysis')

# Connect to SQLite
conn = sqlite3.connect('feedback.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feedback
             (name TEXT, department TEXT, feedback TEXT, sentiment_vader TEXT, sentiment_hf TEXT)''')
conn.commit()

def insert_feedback(name, department, feedback, sentiment_vader, sentiment_hf):
    c.execute('INSERT INTO feedback VALUES (?, ?, ?, ?, ?)', (name, department, feedback, sentiment_vader, sentiment_hf))
    conn.commit()

def get_emotion_vader(text):
    score = vader_analyzer.polarity_scores(text)
    if score['compound'] >= 0.05:
        return 'Positive'
    elif score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def get_emotion_hf(text):
    result = hf_analyzer(text)[0]
    return result['label']

# Streamlit app
st.title("🎓 Student Feedback Form")
st.image("college_logo.png", width=100)

name = st.text_input("Name")
department = st.selectbox("Department", ["BCA", "BCOM", "BBA", "BBA AVIATION",])
feedback = st.text_area("Your feedback")

if st.button("Submit"):
    if name and feedback:
        sentiment_vader = get_emotion_vader(feedback)
        sentiment_hf = get_emotion_hf(feedback)
        insert_feedback(name, department, feedback, sentiment_vader, sentiment_hf)
        st.success("Thank you! Your feedback has been submitted.")
    else:
        st.error("Please fill in all fields.")
