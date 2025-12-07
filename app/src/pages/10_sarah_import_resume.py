import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}")
st.write('### Add Document')

st.write('---')

doc_id = st.text_input("Document ID:", placeholder="doc_sarah_001")

linkedin_url = st.text_input("LinkedIn URL:", placeholder="https://linkedin.com/in/yourprofile")

contents = st.text_area("Document Contents:", placeholder="Paste your resume or cover letter text here", height=300)

user_id = st.text_input("User ID:", value=st.session_state.get('user_id', '1'))

if st.button("Add Document", type="primary", use_container_width=True):
    if doc_id:
        try:
            response = requests.post(
                "http://host.docker.internal:4000/sarah/documents",
                json={
                    "doc_id": doc_id,
                    "linkedin_url": linkedin_url,
                    "contents": contents,
                    "user_id": user_id
                }
            )
            
            if response.status_code == 201:
                st.success(f"Document {doc_id} created successfully")
            elif response.status_code == 409:
                st.error("Document already exists")
            else:
                data = response.json()
                st.error(f"Error: {data.get('error', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cant connect to API")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Document ID is required")

st.write('---')