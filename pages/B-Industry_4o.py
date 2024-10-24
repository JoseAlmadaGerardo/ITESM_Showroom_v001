import streamlit as st
from openai import OpenAI
# UCase_006(v002): Submit request PB was added

st.set_page_config(page_title="Indusrty_#001", page_icon="📊")
st.markdown("# AI at Industry 4.0 & Manufacturing  ")
st.sidebar.header("Industry 4.0 & Manufacturing")

st.title("Use Cases atIndustry 4.0 & Manufacturing")
st.subheader("Fanuc Robot Assistant")
st.write("📄 Enter an alarm code for Fanuc robots, and GPT will provide troubleshooting steps!")

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

    # Ask for the alarm code directly instead of uploading a document.
    st.write(" I'm Lucas_727, your Fanuc Robot Assistant powered by OpenAI API!")
    st.write(" I will provide you the explanation and road map for troubleshooting a robot alarm code.")
    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023 or a description of the issue)...",
    )

    # Add a Submit button to trigger the request
    if st.button("Submit"):
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
                model="gpt-4",
                messages=messages,
                stream=True,
            )

            # Display the response in the app using `st.write_stream`.
            st.write_stream(stream)
        else:
            st.error("Please enter a robot alarm code before submitting.")
