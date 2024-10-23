import openai
import streamlit as st

# Set up your OpenAI API key
#openai.api_key = st.secrets["OPENAI_API_KEY"]
# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    openai.api_key = openai_api_key


# Function to interact with GPT-4.0
def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content']

# Streamlit UI
st.title("GPT-4 Chatbot")
st.write("Ask anything, and I will respond using GPT-4!")

# Text input from the user
user_input = st.text_input("You:", placeholder="Type your message here...")

# If the user inputs a message, call the GPT-4 API
if user_input:
    with st.spinner("Thinking..."):
        bot_response = ask_gpt(user_input)
        st.write(f"**Bot:** {bot_response}")
