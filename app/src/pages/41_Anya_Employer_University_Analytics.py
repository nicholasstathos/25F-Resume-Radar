import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "http://127.0.0.1:4000/anya"


def fetch_data(endpoint):
    try:
        r = requests.get(f"{API_BASE}/{endpoint}")
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

st.title("Anya – Employer & University Analytics")

# Employers
st.subheader("Top Employers")
employer_data, employer_err = fetch_data("employers")

if employer_err:
    st.error(f"Error loading employer analytics: {employer_err}")
else:
    df_emp = pd.DataFrame(employer_data)
    fig_emp = px.bar(df_emp, x="employer", y="avg_score")
    st.plotly_chart(fig_emp)

# Universities
st.subheader("Top Universities")
uni_data, uni_err = fetch_data("universities")

if uni_err:
    st.error(f"Error loading university analytics: {uni_err}")
else:
    df_uni = pd.DataFrame(uni_data)
    fig_uni = px.bar(df_uni, x="university", y="avg_score")
    st.plotly_chart(fig_uni)
