import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Hello", page_icon="👋")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["general"]["OpenAI_key"]

st.write("# Welcome to the Data Science Hub Showroom at Tecnológico de Monterrey! 👋")
st.sidebar.success("Select a demo above.")

st.markdown(
    """This AI showroom showcases various use cases across different industrial applications.
    
    👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!"""
)

# Import the page function for Use Case #5
from use_case_5 import run_use_case_5

# Call the function based on user selection
page = st.sidebar.selectbox("Choose a page:", ["Home", "Use Case #5"])
if page == "Use Case #5":
    run_use_case_5(st.session_state.api_key)
