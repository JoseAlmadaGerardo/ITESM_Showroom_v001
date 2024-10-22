import streamlit as st
from openai import OpenAI
import openai

st.set_page_config(page_title="UCase_004", page_icon="📊")
st.markdown("# UCase_004")
st.sidebar.header("UCase_004")

st.title("Manufacturing: Use Case #4")
st.subheader("Fanuc Robot Assistant")

st.write("📄 Enter an alarm code for Fanuc robots, and GPT will provide troubleshooting steps!")

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    openai.api_key = openai_api_key

    # Ask for an alarm code
    alarm_code = st.text_area("Describe the Robot Alarm Code", placeholder="Enter the alarm code (e.g., SRVO-023)...")

    if alarm_code:
        # Generate a response using OpenAI API
        question = f"Can you give me the explanation and road map to troubleshoot the Robot alarm code: {alarm_code}"
        messages = [{"role": "user", "content": question}]

        # Create a placeholder to display the output
        output_placeholder = st.empty()

        # Stream the response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            stream=True
        )

        # Iterate over the streamed responses and display them
        for chunk in response:
            if "choices" in chunk:
                chunk_message = chunk["choices"][0]["delta"].get("content", "")
                output_placeholder.write(chunk_message)
