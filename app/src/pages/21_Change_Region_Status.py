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

st.title('Manual Override Region Status')

st.write('---')

region_id = st.text_input("Enter ID for region:", placeholder="region_001")

status = st.selectbox("Select New Status:", ["Running", "Error"])

if st.button("Update Status", type="primary", use_container_width=True):
    if region_id:
        try:
            response = requests.put(
                f"http://host.docker.internal:4000/jason/regions/{region_id}/status",
                json={"status": status}
            )
            
            if response.status_code == 200:
                st.success(f"Region {region_id} status changed to {status}")
            elif response.status_code == 404:
                st.error("Region not found")
            else:
                st.error(f"Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cant connect to API")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Enter a Region ID")