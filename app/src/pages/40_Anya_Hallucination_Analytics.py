import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Hallucination & A/B Test Analytics")
st.write("This dashboard helps Anya monitor hallucination rates and A/B test performance.")

#BACKEND
API_BASE = "http://127.0.0.1:4000/anya"

def fetch_data(endpoint):
    """Generic helper to GET data from backend API."""
    try:
        response = requests.get(f"{API_BASE}/{endpoint}")
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)


st.subheader("Hallucination Statistics")

hall_data, error = fetch_data("hallucinations")

if error:
    st.error(f"Failed to load hallucination stats: {error}")
else:
    df = pd.DataFrame(hall_data)

    st.success("Hallucination data loaded successfully!")

    # Bar Chart
    fig = px.bar(df, x="category", y="count", title="Hallucinations by Category")
    st.plotly_chart(fig, use_container_width=True)

    # Pie Chart
    fig2 = px.pie(df, names="category", values="count", title="Hallucination Severity Breakdown")
    st.plotly_chart(fig2, use_container_width=True)


st.subheader("A/B Test Results")

abtest_data, error = fetch_data("abtests")

if error:
    st.error(f"Failed to load A/B test results: {error}")
else:
    df2 = pd.DataFrame(abtest_data)

    st.success("A/B test data loaded successfully!")
    st.dataframe(df2)

    # Visualization
    fig3 = px.bar(
        df2,
        x="version",
        y=["engagement", "conversion"],
        barmode="group",
        title="A/B Test Engagement & Conversion"
    )
    st.plotly_chart(fig3, use_container_width=True)
