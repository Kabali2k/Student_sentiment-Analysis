import streamlit as st
import sqlite3
import pandas as pd
import text2emotion as te
import nltk

# Ensure punkt tokenizer is available
nltk.download('punkt')

# Create or connect to database
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
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

# Streamlit app
st.title("🎓 Student Feedback Form")

name = st.text_input("Name")
department = st.text_input("Department")
feedback = st.text_area("Feedback")

if st.button("Submit"):
    if name and department and feedback:
        try:
            emotion_scores = te.get_emotion(feedback)
            if sum(emotion_scores.values()) == 0:
                emotion = "neutral"
            else:
                emotion = max(emotion_scores, key=emotion_scores.get)
        except Exception as e:
            emotion = "error"

        sentiment = "positive" if emotion in ["Happy", "Surprise"] else "negative"

        c.execute('INSERT INTO feedback (name, department, feedback, sentiment, emotion) VALUES (?, ?, ?, ?, ?)',
                  (name, department, feedback, sentiment, emotion))
        conn.commit()

        st.success("Thank you for your feedback!")
    else:
        st.warning("Please fill all fields.")
