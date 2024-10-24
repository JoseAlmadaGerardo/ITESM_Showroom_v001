import streamlit as st
from openai import OpenAI

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)
    import streamlit as st
    
st.set_page_config(page_title="Proyect_documentation", page_icon="📊")
st.markdown("# X_Documentation")
st.sidebar.header("Project documentation")

st.title("Project Documentation")
st.subheader("Project documentation will be here.")
