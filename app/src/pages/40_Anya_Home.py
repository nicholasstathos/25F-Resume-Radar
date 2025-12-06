import streamlit as st

st.title("Anya: Data Analyst Home")

st.write("Select an analytics feature:")

if st.button("Hallucination & A/B Test Analytics", use_container_width=True):
    st.switch_page("pages/40_Anya_Hallucination_Analytics.py")

if st.button("Employer & University Analytics", use_container_width=True):
    st.switch_page("pages/41_Anya_Employer_University_Analytics.py")

if st.button("Feedback Viewer & Submission", use_container_width=True):
    st.switch_page("pages/42_Anya_Feedback_Page.py")
