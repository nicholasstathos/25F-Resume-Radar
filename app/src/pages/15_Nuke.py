import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()
st.title(f"Welcome Admin {st.session_state['first_name']}")

st.write('### System Administration Dashboard')


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