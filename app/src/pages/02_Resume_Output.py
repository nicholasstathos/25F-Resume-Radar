import logging
logger = logging.getLogger(__name__)
import datetime as dt
import requests

import streamlit as st
from modules.nav import SideBarLinks
import base64


st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}")
user_id = st.session_state.get('user_id', None)
st.write('')
st.write('')

try:
    all_users_response = requests.get(f"http://host.docker.internal:4000/sarah/users")
    
    if all_users_response.status_code == 200:
        all_users = all_users_response.json()
        
        st.write(f'### All Users ({len(all_users)})')
        
        for i in range(0, len(all_users), 2):
            cols = st.columns(2)
            for idx, user in enumerate(all_users[i:i+2]):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="padding: 15px; border: 2px solid #444; border-radius: 10px; background-color: #f0f0f0; margin-bottom: 10px;">
                        <h4 style="color: #333;">{user.get('first_name', '')} {user.get('last_name', '')}</h4>
                        <p style="color: #666;">Email: {user.get('email', 'N/A')}</p>
                        <p style="color: #666;">User ID: {user.get('user_id', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error fetching all users: {str(e)}")

st.write('---')
st.write('### We took a look at your resume....')

try:
    user_id = st.session_state.get('user_id')  
    response = requests.get(f"http://host.docker.internal:4000/sarah/users/{user_id}")
    
    if response.status_code == 200:
        user_data = response.json()
        email = user_data.get('email')
        resumes = user_data.get('resumes', [])
        
        resume_score = resumes[0]['resume_score'] if resumes else 0
        score = st.metric(f'ResumeScore', f'{resume_score}%', str(dt.datetime.now()), delta_color='normal')
    else:
        st.error("Failed to fetch resume data")
        resume_score = 0
except Exception as e:
    st.error(f"Error calling API: {str(e)}")
    resume_score = 0

with open("assets/Nicholas_Stathos_Resume_Tech.pdf", "rb") as file:
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

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