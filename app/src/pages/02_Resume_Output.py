import logging
logger = logging.getLogger(__name__)
import datetime as dt

import streamlit as st
from modules.nav import SideBarLinks
from streamlit_pdf_viewer import pdf_viewer


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

#{st.session_state['affiliate']}

st.title(f"Welcome, {st.session_state['first_name']} from.")
st.write('')
st.write('')
st.write('### We took a look at your resume....')

score = st.metric(f'ResumeScore','91.4%',str(dt.datetime.now()),delta_color='normal')

with open("/Users/nicholas/Documents/GitHub/25F-Resume-Radar/app/src/assets/Nicholas_Stathos_Resume_Tech.pdf", "rb") as file:
    st.pdf(file.read(), height=700)

import streamlit as st

st.markdown("""
<style>
.div-box {
    padding: 15px;
    border: 1px solid #444;
    border-radius: 10px;
    color: white;
    min-height: 150px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="div-box" style="color: black;"><a style="text-decoration: none; font-size: 120%; color: red; font-weight: 800;">-3.6</a><br>"Performed QA tasks on existing company products, including mobile apps and chrome extensions."<br> <a style="text-decoration: none; font-size: 60%; color: red; font-weight: 800;">This item is very vague, consider making this more specific.</a></div>',
                unsafe_allow_html=True)

with col2:
    st.markdown('<div class="div-box" style="color: black;"><a style="text-decoration: none; font-size: 120%; color: red; font-weight: 800;">-4</a><br>"Prototyped a product idea pertaining to the takeout food business for company executives using SwiftUI."<br> <a style="text-decoration: none; font-size: 60%; color: red; font-weight: 800;">This means little to recruiters. People have ideas all the time. Your resume should focus on execution.</a></div>',
                unsafe_allow_html=True)

with col3:
    st.markdown('<div class="div-box" style="color: black;"><a style="text-decoration: none; font-size: 120%; color: red; font-weight: 800;">-1</a><br>"📍"<br> <a style="text-decoration: none; font-size: 60%; color: red; font-weight: 800;">Use of emojis can interact with AI resume filters in unpredictable ways, consider removing this.</a></div>',
                unsafe_allow_html=True)
