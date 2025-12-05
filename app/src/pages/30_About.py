import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About Resume Radar...")

st.markdown(
    """
    As CS and DS majors, we know the job market at the moment is “cooked”. 
    
    Hundreds of applications and hundreds fewer replies make you question every aspect of your application. 
    
    What if there was a way you could see what resumes got people the jobs you want and get feedback based on them for yours? 
    
    Introducing ResumeRadar, the platform that allows you to see what resumes work and replicate them for yourself. 
    
    While many Resume improvement tools exist, ResumeRadar would be the first of its kind to base feedback on user data and outcomes rather than simple grammatical conventions. 
    
    ResumeRadar allows you to understand what it takes to get hired and see in real time what works for other users. 
    
    When someone uploads a resume to ResumeRadar, their resume gets added to our dataset of applicants. 
    
    When a user gets hired, we make note of what worked for them and relay that feedback to you. 
    """
)

# Add a button to return to home page
if st.button("Home", type="primary"):
    st.switch_page("Home.py")
