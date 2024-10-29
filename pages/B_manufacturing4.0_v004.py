import streamlit as st
from openai import OpenAI
import time
import os
from datetime import datetime

# Configuration
st.set_page_config(page_title="Manufacturing Assistant", page_icon="🏭", layout="wide")

# Initialize session states
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your Fanuc Robot Assistant. How can I help you today?"}
        ]
    if "token_usage" not in st.session_state:
        st.session_state.token_usage = {"total": 1250, "current": 0}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

initialize_session_state()

# Load OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# CSS for styling
def apply_custom_css():
    st.markdown("""
        <style>
        .stApp {
            max-width: 100%;
            padding: 1rem;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .user-message {
            background-color: #2e7d32;
            color: white;
            margin-left: 20%;
        }
        .assistant-message {
            background-color: #f0f2f6;
            margin-right: 20%;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# Helper function to simulate AI response
def get_ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.7,
            max_tokens=500,
        )
        assistant_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.session_state.token_usage["current"] += response.usage.total_tokens
        return assistant_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# File Management Section
def file_management():
    st.subheader("Available RAG Files")
    uploaded_file = st.file_uploader("Upload New File", type=['pdf', 'txt'])
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
    
    st.markdown("### Current Files")
    files = ["Fanuc_Manual_2024.pdf", "Error_Codes.pdf", "Maintenance_Guide.pdf"]
    for file in files:
        if st.button(f"📄 {file}", key=file):
            st.session_state.selected_file = file

# Chat Interface Section
def chat_interface():
    st.header("Fanuc Robot Assistant")
    for message in st.session_state.messages:
        role_class = "user-message" if message["role"] == "user" else "assistant-message"
        st.markdown(f"""<div class="chat-message {role_class}">{message["content"]}</div>""", unsafe_allow_html=True)
    
    user_input = st.text_area("Type your message:", key="user_input", height=100)
    if st.button("Send", key="send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        assistant_response = get_ai_response(user_input)
        if assistant_response:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.chat_history.append(f"Chat at {timestamp}")
            st.experimental_rerun()

# Stats and History Section
def stats_and_history():
    st.subheader("Token Usage")
    st.metric("Current Session", st.session_state.token_usage["current"])
    st.metric("Total Available", st.session_state.token_usage["total"])
    
    progress = st.session_state.token_usage["current"] / st.session_state.token_usage["total"]
    st.progress(progress)
    
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        if st.button(f"💬 {chat}", key=chat):
            st.session_state.selected_chat = chat

# Layout for page sections
file_col, chat_col, stats_col = st.columns([1, 2, 1])

with file_col:
    file_management()

with chat_col:
    chat_interface()

with stats_col:
    stats_and_history()

# Sidebar and Footer
st.sidebar.markdown("---")
st.sidebar.info("© 2024 AI Manufacturing Solutions")
