import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Function to load and chat with the assistant
def chat_with_assistant(assistant_id, user_message):
    try:
        # Create a new chat thread
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": f"Assistant ID: {assistant_id}"},
                {"role": "user", "content": user_message}
            ]
        )
        # Return the assistant's response
        return response.choices[0].message["content"]
    except Exception as e:
        st.error(f"Error chatting with assistant: {str(e)}")
        return None

# Streamlit app layout
st.title("Chat with OpenAI Assistant")

# Input field for the user message
user_message = st.text_input("Your message:")

# Button to send the message
if st.button("Send"):
    if user_message:
        # Load the assistant ID
        assistant_id = "asst_y1Nv3ALfFtxSHhsp3I6Knw1J"
        response = chat_with_assistant(assistant_id, user_message)
        
        # Display the assistant's response
        if response:
            st.markdown("### Assistant's Response:")
            st.write(response)
