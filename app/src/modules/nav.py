# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


def sarahNav():
    st.sidebar.page_link("pages/02_Resume_Output.py", label="Our Feedback", icon="🧠")
    st.sidebar.page_link("pages/13_Job_Search.py", label="Job Search Tool", icon="🔍")
    st.sidebar.page_link("pages/04_All_Jobs.py", label="All Jobs", icon="🕵")
    st.sidebar.page_link("pages/10_sarah_import_resume.py", label="Add Document", icon="📄")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------

def usaidWorkerHomeNav():
    st.sidebar.page_link(
      "pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠"
    )

def NgoDirectoryNav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")

def AddNgoNav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")

def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")

def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )

def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )





#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="User Activity Search", icon="🏢"
    )
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Manage Outputs", icon="➕")
    st.sidebar.page_link("pages/21_Change_Region_Status.py", label="Change Region Status", icon="🔄")
    st.sidebar.page_link("pages/22_Revoke_User_Access.py", label="Revoke User Access", icon="🚫")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    st.sidebar.image("assets/logo.png", width=150)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        HomeNav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "pol_strat_advisor":
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()
        if st.session_state["role"] == "usaid_worker":
            usaidWorkerHomeNav()
            NgoDirectoryNav()
            AddNgoNav()
            PredictionNav()
            ApiTestNav()
            ClassificationNav()
        if st.session_state["role"] == "Student":
            sarahNav()
        if st.session_state["role"] == "administrator":
            AdminPageNav()
        if st.session_state["role"] == "Analyst":
            st.sidebar.page_link("pages/40_Anya_Home.py", label="Analyst Home", icon="📊")

    AboutPageNav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")