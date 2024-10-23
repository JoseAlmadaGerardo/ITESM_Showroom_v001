import streamlit as st

# Set page configuration
st.set_page_config(page_title="Hello", page_icon="👋", layout="wide")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

st.write("# Welcome to the Data Science Hub Showroom at Tecnológico de Monterrey! 👋")
st.sidebar.success("Select a demo above.")

# Use the full page instead of a narrow central column

st.markdown(
        """
        ### AI Use Cases
        This showroom showcases various AI use cases across different industries applications, and is an app built
        on the Streamlit framework specifically designed for AI agents utilizing RAG architecture from OpenAI.

        👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!
        """
    )


# Create 2 columns
col1, col2 = st.columns((1.5,1))

with col1:
    st.markdown(
        """
        ## Objetives.
        Analyze different industrial sectors to identify potential opportunities
        where it is feasible to develop AI-based assistants using RAG architecture.
        The industries to explore are the next, Accounting & Tax, Industry 4.0,
        Finance, Marketing and Business Units.
        
        These assistants will be able to incorporate personalized knowledge & integrate
        call functions!
        """
    )

with col2:
    st.markdown(
        """
        ### Learn About Streamlit, Assistant API and More Demos
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community forums](https://discuss.streamlit.io)
        - Check out [Assistant API by OpenAI](https://platform.openai.com/docs/assistants/overview)
        - Explore additional complex demos and industry use cases.
        """
    )
