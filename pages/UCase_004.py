import streamlit as st
#import PyPDF2
from openai import OpenAI

st.set_page_config(page_title="UCase_004", page_icon="📊")
st.markdown("# UCase_004")
st.sidebar.header("UCase_004")

# Title.
st.title("Manufacturing: Use Case #4​")
st.subheader("Fanuc Robot Assistant.​")
st.write("📄 Answers questions about Alarm codes for the industrial robots of the brand Fanuc")
st.write(" Feed the robot assistant with the error code and it will give you back an explanation and a road map to troubleshoot the Robot alarm code!")
st.write("Note: To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Solicitar al usuario su clave de API de OpenAI mediante `st.text_input`.
# Alternativamente, puedes almacenar la clave de API en `./.streamlit/secrets.toml` y acceder a ella
# mediante `st.secrets`, ver https://docs.streamlit.io/develop/concepts/connections/secrets-management

# API key input
openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Ask for the alarm code directly instead of uploading a document.
    st.write(" I'm Lucas_727, your Fanuc Robot Assistant power by openAI API!")
    st.write(" I will provide you the explanation and road map for troubleshoot for a robot alarm's code")
    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023 or a description of the issue)...",
    )

    # Check if the user has provided the alarm code.
    if alarm_code:
        # Construct the specific prompt for the AI assistant.
        question = f"Can you give me the explanation and road map to troubleshoot the Robot alarm code: {alarm_code}"

        # Generate a response using the OpenAI API.
        messages = [
            {
                "role": "user",
                "content": question,
            }
        ]

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Display the response in the app using `st.write_stream`.
        st.write_stream(stream)
