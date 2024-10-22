import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

# UCase_007(v002): Submit request PB was added
st.set_page_config(page_title="UCase_007", page_icon="📊")
st.markdown("# UCase_007")
st.sidebar.header("UCase_007")

st.title("🦜🔗 Quickstart App")
st.subheader("Learn how to use the Langchain OpenAI model")
st.write("📄 Enter a text prompt below and GPT will provide a response!")

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key

    # Function to generate a response using Langchain's ChatOpenAI model
    def generate_response(input_text):
        model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
        response = model.invoke(input_text)
        st.info(response)

    # Ask for input
    text = st.text_area(
        "Enter text:",
        placeholder="What are the three key pieces of advice for learning how to code?",
    )

    # Submit button
    if st.button("Submit"):
        # Check if API key is valid and process the input
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        else:
            generate_response(text)
