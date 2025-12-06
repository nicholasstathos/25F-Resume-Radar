import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}")
st.write('### Job Search')

st.write('---')

keyword_search = st.text_input("Search by title or company for jobs!", placeholder="ex Engineer")

if st.button("Search Jobs", type="primary", use_container_width=True):
    if keyword_search:
        try:
            response = requests.get(f"http://host.docker.internal:4000/sarah/jobs/search/{keyword_search}")
            
            if response.status_code == 200:
                jobs = response.json()
                
                if jobs:
                    st.success(f"Found {len(jobs)} jobs matching {keyword_search}")
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
                    st.info(f"No jobs found matching {keyword_search}")
                    
            else:
                st.error(f"Error searching jobs: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cant connect to API server")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a keyword to search")

st.write('---')