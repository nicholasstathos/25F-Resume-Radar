import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:4000/anya"


def get_feedback():
    try:
        response = requests.get(f"{API_BASE}/feedback")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to load feedback: {e}")
        return []


def submit_feedback(text):
    try:
        response = requests.post(f"{API_BASE}/feedback", json={"feedback": text})
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Failed to submit feedback: {e}")
        return False


st.title("Feedback Viewer & Submission")
st.write("Review student feedback and submit new entries.")


st.subheader("Existing Feedback")

feedback = get_feedback()

if feedback:
    df = pd.DataFrame(feedback)
    st.table(df)
else:
    st.info("No feedback available yet.")



st.subheader("Submit New Feedback")

new_feedback = st.text_area("Enter feedback:")

if st.button("Submit"):
    if new_feedback.strip():
        if submit_feedback(new_feedback):
            st.success("Feedback submitted successfully!")
            st.rerun()
    else:
        st.warning("Feedback cannot be empty.")
