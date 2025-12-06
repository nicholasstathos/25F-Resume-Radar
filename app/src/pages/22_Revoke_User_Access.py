import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Admin {st.session_state['first_name']}")

st.write('### System Administration Dashboard')

st.write('---')

st.write('Revoke User Access')
st.warning("This permenantly deletes a user and all associated data.")

user_id = st.text_input("Enter User ID", placeholder="1")


if st.button("Revoke Access", type="secondary", use_container_width=True):
    if user_id:
        try:
            response = requests.delete(
                f"http://host.docker.internal:4000/jason/users_delete/{user_id}"
            )
            
            if response.status_code == 200:
                st.success(f"User {user_id} access revoked successfully")
            elif response.status_code == 404:
                st.error(f"User {user_id} not found")
            else:
                st.error(f"Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cant connect to API")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Enter a User ID")