import streamlit as st
import sqlite3
import pandas as pd
import text2emotion as te
import nltk
from transformers import pipeline

# Download punkt tokenizer
nltk.download('punkt')

# Set up sentiment analysis pipeline
sentiment_pipeline = pipeline('sentiment-analysis')

# Connect to database
conn = sqlite3.connect('feedback.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, name TEXT, department TEXT, feedback TEXT, sentiment TEXT, emotion TEXT)''')
conn.commit()

st.title("🎓 Student Feedback Form")

name = st.text_input("Your Name")
department = st.selectbox("Department", ["CSE", "ECE", "EEE", "MECH", "CIVIL", "Others"])
feedback = st.text_area("Your Feedback")

if st.button("Submit Feedback"):
    if name and department and feedback:
        sentiment = sentiment_pipeline(feedback)[0]['label']
        emotions = te.get_emotion(feedback)
        dominant_emotion = max(emotions, key=emotions.get)
        c.execute("INSERT INTO feedback (name, department, feedback, sentiment, emotion) VALUES (?, ?, ?, ?, ?)",
                  (name, department, feedback, sentiment, dominant_emotion))
        conn.commit()
        st.success("✅ Feedback submitted successfully!")
    else:
        st.warning("⚠️ Please fill in all fields before submitting.")

st.markdown("---")
st.header("📈 Real-time Feedback Summary")

if st.checkbox("Show Feedback Count"):
    count = c.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    st.info(f"Total feedback submissions: {count}")
