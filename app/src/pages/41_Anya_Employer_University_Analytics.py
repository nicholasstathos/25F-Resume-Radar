import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "http://127.0.0.1:4000/anya"


def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None


st.title("Employer & University Analytics")
st.write("Analyze resume quality grouped by employers and universities.")



st.subheader("Employer Resume Scores")

employers = fetch_data("employers")

if employers:
    df_emp = pd.DataFrame(employers)
    fig_emp = px.bar(df_emp, x="employer", y="avg_score",
                     title="Average Resume Score by Employer",
                     labels={"avg_score": "Average Score"})
    st.plotly_chart(fig_emp, use_container_width=True)
else:
    st.warning("No employer analytics available.")



st.subheader("University Resume Scores")

universities = fetch_data("universities")

if universities:
    df_uni = pd.DataFrame(universities)
    fig_uni = px.bar(df_uni, x="university", y="avg_score",
                     title="Average Resume Score by University",
                     labels={"avg_score": "Average Score"})
    st.plotly_chart(fig_uni, use_container_width=True)
else:
    st.warning("No university analytics available.")

