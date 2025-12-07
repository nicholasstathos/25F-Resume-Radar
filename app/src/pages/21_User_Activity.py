import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

st.title(f"Welcome Admin {st.session_state['first_name']}")

st.write('### System Administration Dashboard')

st.write('---')


SideBarLinks()

st.write('### User Activity Search')

user_id_search = st.text_input("Enter User ID:", placeholder="1 (use for demo)")

if st.button("Search", use_container_width=True):
    if user_id_search:
        try:
            response = requests.get(f"http://host.docker.internal:4000/jason/fetch_activity/{user_id_search}")
            
            if response.status_code == 200:
                activities = response.json()
                st.write(f"**{len(activities)} activities**")
                st.write("")
                
                for activity in activities:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Input** `{activity.get('InputID')}`")
                        st.text(f"Time: {activity.get('InputTime')}")
                        st.text(f"Region: {activity.get('RegionID')}")
                        st.text(f"Content: {activity.get('InputContent')}")
                
                    
                    st.divider()
                    
            elif response.status_code == 404:
                st.warning(f"Cant find any activity for {user_id_search}")
            else:
                st.error(f"Error {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to API")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Enter a User ID")

st.markdown("---")