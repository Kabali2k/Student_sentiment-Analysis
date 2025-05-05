import streamlit as st
from transformers import pipeline
import text2emotion as te
import pandas as pd
import os

feedback_file = 'feedback.csv'

# Load sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def save_feedback(data):
    if os.path.exists(feedback_file):
        df = pd.read_csv(feedback_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(feedback_file, index=False)

st.title("🎓 Student Feedback Form")

name = st.text_input("Name")
department = st.selectbox("Department", ["CSE", "ECE", "EEE", "MECH", "CIVIL"])
feedback = st.text_area("Your Feedback")

if st.button("Submit Feedback"):
    if name and department and feedback:
        sentiment_result = sentiment_pipeline(feedback)[0]
        sentiment = sentiment_result['label']
        emotion = max(te.get_emotion(feedback), key=te.get_emotion(feedback).get)
        
        data = {
            'name': name,
            'department': department,
            'feedback': feedback,
            'sentiment': sentiment,
            'emotion': emotion
        }
        save_feedback(data)
        st.success("Thank you for your feedback!")
    else:
        st.warning("Please fill in all fields before submitting.")
