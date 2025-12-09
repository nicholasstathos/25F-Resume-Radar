import streamlit as st
import requests
import pandas as pd
import plotly.express as px

from modules.nav import SideBarLinks

API_BASE = "http://host.docker.internal:4000/anya"

SideBarLinks()


def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE}/{endpoint}")
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

st.title("Anya – Hallucination Analytics")
st.write("This dashboard helps Anya monitor hallucination patterns across resumes.")

data, error = fetch_data("hallucinations")

if error:
    st.error(f"Failed to load hallucination stats: {error}")
else:
    df = pd.DataFrame(data)

    st.subheader("Hallucination Categories")
    bar_fig = px.bar(df, x="category", y="count")
    st.plotly_chart(bar_fig)

    pie_fig = px.pie(df, names="category", values="count")
    st.plotly_chart(pie_fig)
