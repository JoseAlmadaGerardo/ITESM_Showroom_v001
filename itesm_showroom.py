import streamlit as st

# Set page configuration
st.set_page_config(page_title="Hello", page_icon="👋")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

st.write("# Welcome to the Data Science Hub Showroom at Tecnológico de Monterrey! 👋")
st.sidebar.success("Select a demo above.")


st.markdown(
        """This AI showroom showcases various use cases across different industrial applications. It is an open-source app built on the Streamlit framework, this showroom is specifically designed for AI agents utilizing RAG architecture from OpenAI.

👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!

        ### Want to learn more about streamlit?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### Want to learn more anout Assistant API use at this project?

        - Check out [AssistanAPI.openAI](https://platform.openai.com/docs/assistants/overview)

        ### See more complex demos
    """
    )
