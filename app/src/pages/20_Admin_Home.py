import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome Admin {st.session_state['first_name']}")

st.write('### System Administration Dashboard')

st.write('---')


status_types = ["Running", "Error"]

status_colors = {
    "Running": "#28a745",
    "Error": "#dc3545",
}

all_regions = []
errors = []

for status in status_types:
    try:
        response = requests.get(f"http://host.docker.internal:4000/jason/regions/status/{status}")
        
        if response.status_code == 200:
            regions = response.json()
            for region in regions:
                region['Status'] = status 
            all_regions.extend(regions)
        elif response.status_code == 404:
            st.info(f"Cant find any regions with {status}")
        else:
            st.warning(f"Unexpected response {status}:for{response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError as e:
        error_msg = f"❌ Connection error for status '{status}'and cant reach API"
        st.error(error_msg)
        errors.append(error_msg)
    except Exception as e:
        error_msg = f"❌ Error fetching {status} regions: {str(e)}"
        st.error(error_msg)

if all_regions:
    regions_by_status = {}
    for region in all_regions:
        status = region.get('Status', 'Unknown')
        if status not in regions_by_status:
            regions_by_status[status] = []
        regions_by_status[status].append(region)
    
    for status, regions in regions_by_status.items():
        st.markdown(f"### Your {status} Regions ({len(regions)})")
        
        for i in range(0, len(regions), 3):
            cols = st.columns(3)
            
            for idx, region in enumerate(regions[i:i+3]):
                with cols[idx]:
                    color = status_colors.get(status, "#6c757d")
                    
                    status_emoji = {
                        "Running": "✅",
                        "Error": "❌",
                    }.get(status, "📍")
                    
                    st.markdown(f"""
                    <div style="
                        padding: 20px;
                        border-left: 5px solid {color};
                        border-radius: 8px;
                        background-color: #f8f9fa;
                        margin-bottom: 15px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    ">
                        <h4 style="color: #333; margin-top: 0;">
                            {status_emoji} {region.get('Name', 'Unknown Region')}
                        </h4>
                        <p style="color: #666; margin: 5px 0;">
                            <strong>Region ID:</strong> {region.get('RegionID', 'N/A')}
                        </p>
                        <p style="color: #666; margin: 5px 0;">
                            <strong>Status:</strong> 
                            <span style="
                                background-color: {color};
                                color: white;
                                padding: 3px 10px;
                                border-radius: 12px;
                                font-size: 12px;
                                font-weight: bold;
                            ">{status}</span>
                        </p>
                        <p style="color: #666; margin: 5px 0;">
                            <strong>Admin ID:</strong> {region.get('AdminID', 'N/A')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.write('')
else:
    st.info("No regions found for this administrator")
    if errors:
        st.error("Error occurred while fetching data above")

st.markdown("---")
st.markdown("### Master Switch")
st.warning("The Nuclear Button will turn all LLM outputs to snowlike ash. This action is irreversible (unless you rebuild the database in the demo....)")

confirm = st.checkbox("I understand this will delete all cached outputs permanently")

st.markdown("""
<style>
div.stButton > button[kind="secondary"] {
    background-color: #ff0000;
    color: white;
    font-size: 24px;
    font-weight: bold;
    padding: 20px 40px;
    border: 3px solid #990000;
    border-radius: 10px;
    width: 100%;
}
div.stButton > button[kind="secondary"]:hover {
    background-color: #cc0000;
    border: 3px solid #660000;
}
</style>
""", unsafe_allow_html=True)

if st.button("NUCLEAR BUTTON - DELETE ALL OUTPUTS", 
             type="secondary",
             disabled=not confirm,
             use_container_width=True):
    
    with st.spinner("☢️ Initiating nuclear protocol..."):
        try:
            response = requests.delete("http://host.docker.internal:4000/jason/nuclear-button")
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ {data.get('outputs_destroyed', 0)} {data.get('message', 'Success')}")
                st.snow()
            else:
                st.error(f"❌ Failed to execute nuclear button. Status code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API server on port 4000")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")