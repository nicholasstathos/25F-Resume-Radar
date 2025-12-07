import streamlit as st
import requests
import logging
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Update Profile", layout="wide")

SideBarLinks()

st.title("Update Your Profile")
st.markdown("---")

if 'user_id' not in st.session_state:
    st.warning("Please log in to view your profile")
    st.stop()

user_id = st.session_state['user_id']

try:
    response = requests.get(f'http://host.docker.internal:4000/sarah/users/{user_id}')
    
    if response.status_code == 200:
        current_user = response.json()
        
        st.subheader(f"**Current Email:** {current_user.get('email', 'N/A')}")
        
        if current_user.get('resumes'):
            with st.expander(f"View Resumes ({len(current_user['resumes'])} total)"):
                for resume in current_user['resumes']:
                    st.write(f"- Resume ID: {resume['resume_id']} | Score: {resume['resume_score']} | Version: {resume['version_num']}")
        
        st.markdown("---")
        st.markdown("### Update Profile")
        
        with st.form("update_profile_form"):
            new_name = st.text_input(
                "Name", 
                placeholder="Enter your full name",
                help="This will update your name in the User table"
            )
            
            new_email = st.text_input(
                "New Email", 
                value=current_user.get('email', ''),
                placeholder="Enter your email address"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submit_button = st.form_submit_button("Update Profile", use_container_width=True)
            with col2:
                reset_button = st.form_submit_button("Reset", use_container_width=True)
            
            if submit_button:
                if not new_name or not new_email:
                    st.error("Name and email are required!")
                else:
                    update_data = {
                        "name": new_name,
                        "email": new_email
                    }
                    
                    try:
                        update_response = requests.put(
                            f'http://host.docker.internal:4000/sarah/users/{user_id}',
                            json=update_data
                        )
                        
                        if update_response.status_code == 200:
                            st.success("Profile updated successfully!")
                            st.balloons()
                            st.rerun()
                        elif update_response.status_code == 404:
                            st.error("User not found!")
                        elif update_response.status_code == 409:
                            st.error("Email already in use by another user!")
                        else:
                            error_msg = update_response.json().get('error', 'Unknown error')
                            st.error(f"Error: {error_msg}")
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {str(e)}")
                        logger.error(f"Failed to update profile: {e}")
            
            if reset_button:
                st.rerun()
    
    elif response.status_code == 404:
        st.error("User not found. Please check your account.")
    else:
        st.error(f"Error fetching user data: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Connection error: {str(e)}")
    logger.error(f"Failed to fetch user data: {e}")
