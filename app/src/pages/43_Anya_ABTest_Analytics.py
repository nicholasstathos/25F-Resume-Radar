import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

API_BASE = "http://127.0.0.1:4000/anya"



def fetch_abtests():
    try:
        r = requests.get(f"{API_BASE}/abtests")
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)


st.title("🧪 Anya – A/B Test Performance Analytics")

st.write("""
This dashboard displays performance results for A/B tests related to resume scoring, 
skill extraction accuracy, tone variations, and more.
""")



abtests, err = fetch_abtests()

if err:
    st.error(f"Error loading A/B test analytics: {err}")
else:
    df = pd.DataFrame(abtests)

    
    st.subheader("📋 Raw A/B Test Results")
    st.dataframe(df, use_container_width=True)

 
    if "conversion" in df.columns:
        st.subheader("Conversion Rates by Variant")

        fig_conversion = px.bar(
            df,
            x="variant",
            y="conversion",
            color="test",
            title="Conversion Rate Comparison by Variant",
            labels={"conversion": "Conversion Rate", "variant": "Variant"},
            barmode="group"
        )
        st.plotly_chart(fig_conversion, use_container_width=True)

  
    st.subheader("Test Distribution")

    fig_distribution = px.pie(
        df,
        names="test",
        title="Distribution of A/B Test Types",
    )

    st.plotly_chart(fig_distribution, use_container_width=True)

