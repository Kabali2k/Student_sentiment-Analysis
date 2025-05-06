import streamlit as st
import sqlite3
import pandas as pd
import text2emotion as te
import matplotlib.pyplot as plt
import nltk

# Download 'punkt' if not already available
nltk.download('punkt')

# Initialize DB
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            feedback TEXT,
            sentiment TEXT,
            dominant_emotion TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert feedback into DB
def insert_feedback(name, department, feedback, sentiment, dominant_emotion):
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO feedback (name, department, feedback, sentiment, dominant_emotion)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, department, feedback, sentiment, dominant_emotion))
    conn.commit()
    conn.close()

# Get all feedback
def get_feedback():
    conn = sqlite3.connect('feedback.db')
    df = pd.read_sql_query('SELECT * FROM feedback', conn)
    conn.close()
    return df

# Analyze feedback text
def analyze_feedback(feedback_text):
    emotions = te.get_emotion(feedback_text)
    if not emotions:
        raise ValueError("Could not extract emotions.")
    dominant_emotion = max(emotions, key=emotions.get)
    if dominant_emotion in ['Happy', 'Surprise']:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'
    return sentiment, dominant_emotion

# Main app function
def main():
    st.set_page_config(page_title="Feedback Sentiment & Emotion Analysis App")
    init_db()
    menu = ["Feedback Form", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Feedback Form":
        st.title("Student Feedback Form")
        with st.form(key='feedback_form'):
            name = st.text_input("Student Name")
            department = st.text_input("Department")
            feedback = st.text_area("Feedback")
            submit = st.form_submit_button("Submit Feedback")

        if submit:
            if not name or not department or not feedback:
                st.error("Please fill all fields.")
            else:
                try:
                    sentiment, dominant_emotion = analyze_feedback(feedback)
                    insert_feedback(name, department, feedback, sentiment, dominant_emotion)
                    st.success(f"Feedback submitted! Sentiment: {sentiment}, Emotion: {dominant_emotion}")
                except Exception as e:
                    st.error(f"Error analyzing feedback: {e}")

    elif choice == "Dashboard":
        st.title("Feedback Dashboard")
        df = get_feedback()
        if df.empty:
            st.info("No feedback submitted yet.")
        else:
            st.subheader("All Feedback")
            st.dataframe(df[['name', 'department', 'feedback', 'sentiment', 'dominant_emotion']])

            st.subheader("Sentiment Distribution")
            sentiment_counts = df['sentiment'].value_counts()
            fig1, ax1 = plt.subplots()
            sentiment_counts.plot(kind='bar', ax=ax1)
            ax1.set_xlabel("Sentiment")
            ax1.set_ylabel("Count")
            st.pyplot(fig1)

            st.subheader("Emotion Distribution")
            emotion_counts = df['dominant_emotion'].value_counts()
            fig2, ax2 = plt.subplots()
            emotion_counts.plot(kind='bar', ax=ax2, color='orange')
            ax2.set_xlabel("Emotion")
            ax2.set_ylabel("Count")
            st.pyplot(fig2)

if __name__ == '__main__':
    main()
