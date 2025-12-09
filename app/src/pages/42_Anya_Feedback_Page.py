import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

API_BASE = "http://host.docker.internal:4000/anya"

SideBarLinks()


st.title("Anya – User Feedback Dashboard")


def get_feedback():
    try:
        r = requests.get(f"{API_BASE}/feedback")
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)


def send_feedback(message, user="Anya"):
    try:
        body = {"message": message, "user": user}
        r = requests.post(f"{API_BASE}/feedback", json=body)
        r.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)

st.subheader("Submit New Feedback")

feedback_text = st.text_area("Write feedback:", height=120)

if st.button("Submit Feedback", type="primary"):
    if not feedback_text.strip():
        st.error("Message cannot be empty.")
    else:
        ok, err = send_feedback(feedback_text)
        if ok:
            st.success("Feedback submitted successfully!")
        else:
            st.error(f"Error submitting feedback: {err}")


st.subheader("All Feedback Messages")

data, err = get_feedback()

if err:
    st.error(f"Could not load feedback: {err}")
else:
    if len(data) == 0:
        st.info("No feedback submitted yet.")
    else:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
