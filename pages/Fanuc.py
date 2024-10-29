import streamlit as st
from openai import OpenAI
import time
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Manufacturing Assistant", page_icon="🏭", layout="wide")

# Initialize session states if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Fanuc Robot Assistant. How can I help you today?"}
    ]
if "token_usage" not in st.session_state:
    st.session_state.token_usage = {"total": 1250, "current": 0}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize OpenAI client (assuming API key is in environment variables)
client = OpenAI(api_key=st.session_state.api_key)

# Custom CSS for better styling
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

# Create three columns layout
file_col, chat_col, stats_col = st.columns([1, 2, 1])

# Left column - RAG Files
with file_col:
    st.subheader("Available RAG Files")
    
    # File upload section
    uploaded_file = st.file_uploader("Upload New File", type=['pdf', 'txt'])
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
    
    # Available files list
    st.markdown("### Current Files")
    files = ["Fanuc_Manual_2024.pdf", "Error_Codes.pdf", "Maintenance_Guide.pdf"]
    for file in files:
        if st.button(f"📄 {file}", key=file):
            st.session_state.selected_file = file

# Middle column - Chat Interface
with chat_col:
    st.header("Fanuc Robot Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="chat-message user-message">
                        {message["content"]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message assistant-message">
                        {message["content"]}
                    </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    with st.container():
        user_input = st.text_area("Type your message:", key="user_input", height=100)
        if st.button("Send", key="send"):
            if user_input:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Simulate AI response (replace with actual OpenAI call)
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": user_input}],
                        temperature=0.7,
                        max_tokens=500,
                    )
                    
                    # Add assistant response
                    assistant_response = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                    # Update token usage
                    st.session_state.token_usage["current"] += response.usage.total_tokens
                    
                    # Add to chat history
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.chat_history.append(f"Chat at {timestamp}")
                    
                    # Clear input
                    st.experimental_rerun()
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Right column - Stats and History
with stats_col:
    # Token Usage
    st.subheader("Token Usage")
    st.metric("Current Session", st.session_state.token_usage["current"])
    st.metric("Total Available", st.session_state.token_usage["total"])
    
    # Progress bar for token usage
    progress = st.session_state.token_usage["current"] / st.session_state.token_usage["total"]
    st.progress(progress)
    
    # Chat History
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        if st.button(f"💬 {chat}", key=chat):
            st.session_state.selected_chat = chat

# Footer
st.sidebar.markdown("---")
st.sidebar.info("© 2024 AI Manufacturing Solutions")

# Error handling and notifications
if "error" in st.session_state:
    st.error(st.session_state.error)
    del st.session_state.error

if "success" in st.session_state:
    st.success(st.session_state.success)
    del st.session_state.success
      
