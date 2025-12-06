import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}")
st.write('### Take a look at the jobs we have to offer!')

st.write('---')

try:
    response = requests.get("http://host.docker.internal:4000/sarah/jobs")
    
    if response.status_code == 200:
        jobs = response.json()
        
        if jobs:
            st.success(f"Found {len(jobs)} total jobs")
            st.write("")
            
            for job in jobs:
                job_id = job.get('JobID', 'N/A')
                title = job.get('Title', 'No title')
                company = job.get('Company', 'No company')
                user_id = job.get('UserID', 'N/A')
                avg_score = job.get('avg_resume_score')
                
                score_display = f"{avg_score}%" if avg_score else "No resumes"
                
                st.markdown(f"""
                <div style="
                    padding: 20px;
                    border-left: 5px solid #1976d2;
                    border-radius: 8px;
                    background-color: #f8f9fa;
                    margin-bottom: 15px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <h3 style="color: #333; margin-top: 0;">💼 {title}</h3>
                    <p style="color: #666; margin: 8px 0; font-size: 16px;">
                        <strong>Company:</strong> {company}
                    </p>
                    <p style="color: #666; margin: 8px 0;">
                        <strong>Job ID:</strong> {job_id}
                    </p>
                    <p style="color: #666; margin: 8px 0;">
                        <strong>Posted by User:</strong> {user_id}
                    </p>
                    <p style="color: #666; margin: 8px 0;">
                        <strong>Average Resume Score:</strong> {score_display}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No jobs found")
            
    else:
        st.error(f"Error loading jobs: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    st.error("Cant connect to API server")
except Exception as e:
    st.error(f"Error: {str(e)}")

st.write('---')