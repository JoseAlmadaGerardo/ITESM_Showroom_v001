import streamlit as st
from openai import OpenAI
import time
from datetime import datetime
import json
import base64
import PyPDF2
import docx
import markdown
import re

# Page Configuration
st.set_page_config(
    page_title="Manufacturing_4o_RAG", page_icon="🏭", layout="wide", initial_sidebar_state="expanded")
st.title("AI at manufacturing 4.0 using updated documents for a RAG")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

client = OpenAI(api_key=st.session_state.api_key)

# Initialize session state variables
if "fanuc_thread_id" not in st.session_state:
    st.session_state.fanuc_thread_id = None
if "components_thread_id" not in st.session_state:
    st.session_state.components_thread_id = None
if "fanuc_chat_history" not in st.session_state:
    st.session_state.fanuc_chat_history = []
if "components_chat_history" not in st.session_state:
    st.session_state.components_chat_history = []
if "fanuc_total_tokens" not in st.session_state:
    st.session_state.fanuc_total_tokens = 0
if "components_total_tokens" not in st.session_state:
    st.session_state.components_total_tokens = 0
if "fanuc_context" not in st.session_state:
    st.session_state.fanuc_context = ""
if "components_context" not in st.session_state:
    st.session_state.components_context = ""

# Function to interact with OpenAI Assistant
def chat_with_assistant(assistant_id, thread_id, user_message):
    if thread_id is None:
        thread = client.beta.threads.create()
        thread_id = thread.id

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_message = next((msg.content[0].text.value for msg in messages if msg.role == 'assistant'), None)

    return assistant_message, thread_id

# Text extraction functions
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_md(file):
    content = file.read().decode('utf-8')
    html = markdown.markdown(content)
    text = re.sub('<[^<]+?>', '', html)
    return text

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

# Function to extract key points
def get_key_points(assistant_id, thread_id, text, num_points):
    prompt = f"Extract {num_points} key points from the following text:\n\n{text}"
    response, thread_id = chat_with_assistant(assistant_id, thread_id, prompt)
    return response, thread_id

# Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.markdown("# 🤖 Fanuc Robot Assistant")
    st.markdown(
        """
        The Fanuc Robot Assistant supports automated operations, error troubleshooting, and 
        configuration management of industrial robots. It helps in diagnosing and resolving 
        common errors in Fanuc robotic systems for smooth manufacturing workflows.
        """
    )
    
    assistant_id = "asst_pHefU3EW9kDQwlKloWyl0jTn" 
    assistant_name = "Fanuc Robot Assistant" 
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"👋 I'm your {assistant_name}!")
        st.warning("Note: This AI assistant is still in development mode.")
    with col2:
        st.metric("Tokens Used", st.session_state.fanuc_total_tokens)

    # File upload
    uploaded_file = st.file_uploader("Upload a document for context (PDF, DOCX, MD, TXT)", type=['pdf', 'docx', 'md', 'txt'], key="fanuc_file_uploader")
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.type == "text/markdown":
            text = extract_text_from_md(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type")
            return

        st.session_state.fanuc_context = text
        st.success("Document uploaded and processed successfully!")

        # Key points extraction
        num_points = st.number_input("Number of key points", min_value=3, max_value=10, value=3, step=1, key="fanuc_num_points")
        if st.button("Extract Key Points", key="fanuc_extract_key_points"):
            key_points, st.session_state.fanuc_thread_id = get_key_points(assistant_id, st.session_state.fanuc_thread_id, text, num_points)
            st.markdown("### Key Points:")
            st.write(key_points)

    # Chat functionality
    st.subheader(f"Chat with {assistant_name}")
    question = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023 or a description of the issue)...",
    )
    if st.button("Send", key="fanuc_send"):
        if question:
            response, st.session_state.fanuc_thread_id = chat_with_assistant(
                assistant_id, 
                st.session_state.fanuc_thread_id, 
                question
            )
            st.markdown(f"**Answer:** {response}")
            st.session_state.fanuc_chat_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "question": question,
                "answer": response
            })
            # Note: Token counting might need to be implemented differently for the Assistants API

    # Chat history
    if st.session_state.fanuc_chat_history:
        st.subheader("Chat History")
        for chat in reversed(st.session_state.fanuc_chat_history):
            with st.expander(f"Q: {chat['question']} - {chat['timestamp']}"):
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Electronic Components Assistant
def electronic_components_assistant():
    st.header("🔌 Electronic Components Assistant")
    
    assistant_id = "asst_pHefU3EW9kDQwlKloWyl0jTn"  
    assistant_name = "Electronic Components Assistant" 
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        👋 I'm your {assistant_name}! I help with the setup and configuration of electronic components 
        used in manufacturing systems. I ensure optimal configurations for the best 
        performance and compatibility across different systems.
        """)
    with col2:
        st.metric("Tokens Used", st.session_state.components_total_tokens)

    # File upload
    uploaded_file = st.file_uploader("Upload a document for context (PDF, DOCX, MD, TXT)", type=['pdf', 'docx', 'md', 'txt'], key="components_file_uploader")
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.type == "text/markdown":
            text = extract_text_from_md(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type")
            return

        st.session_state.components_context = text
        st.success("Document uploaded and processed successfully!")

        # Key points extraction
        num_points = st.number_input("Number of key points", min_value=3, max_value=10, value=3, step=1, key="components_num_points")
        if st.button("Extract Key Points", key="components_extract_key_points"):
            key_points, st.session_state.components_thread_id = get_key_points(assistant_id, st.session_state.components_thread_id, text, num_points)
            st.markdown("### Key Points:")
            st.write(key_points)

    # Chat functionality
    st.subheader(f"Chat with {assistant_name}")
    question = st.text_area(
        "Describe your configuration question:",
        placeholder="E.g., How to set up communication between a Siemens S7-1200 PLC and an HMI panel?",
        height=100
    )
    if st.button("Send", key="components_send"):
        if question:
            response, st.session_state.components_thread_id = chat_with_assistant(
                assistant_id, 
                st.session_state.components_thread_id, 
                question
            )
            st.markdown(f"**Answer:** {response}")
            st.session_state.components_chat_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "question": question,
                "answer": response
            })
            # Note: Token counting might need to be implemented differently for the Assistants API

    # Chat history
    if st.session_state.components_chat_history:
        st.subheader("Chat History")
        for chat in reversed(st.session_state.components_chat_history):
            with st.expander(f"Q: {chat['question']} - {chat['timestamp']}"):
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Main Page
def main_page():
    st.markdown("""
        Welcome to the AI-powered Manufacturing 4.0 platform. This system integrates 
        artificial intelligence to optimize manufacturing processes and enhance productivity.
        
        **Available Features:**
        - 🤖 Fanuc Robot Assistant
        - 🔌 Electronic Components Assistant
        - 📚 Documentation Management
        
        Select a feature from the sidebar to get started.
    """)

# Documentation page (unchanged)
def documentation():
    st.header("📚 Documentation")
    st.markdown(
        """
        In this section, you will find comprehensive documentation about the use cases explained for the Business Units.
        """
    )
    
    st.subheader("Available Documentation:")
    doc_types = {
        "User Manuals": "https://example.com/user-manuals",
        "Technical Specifications": "https://example.com/tech-specs",
        "Troubleshooting Guides": "https://example.com/troubleshooting",
        "Best Practices": "https://example.com/best-practices"
    }
    for doc, link in doc_types.items():
        st.markdown(f"- [{doc}]({link})")
    
    st.info("For specific documentation requests, please contact your system administrator.")

# Sidebar Navigation
with st.sidebar:
    st.title("AI AT MANUFACTURING 4.0")
    
    pages = {
        "🏡 Home": main_page,
        "🤖 Fanuc Robot Assistant": fanuc_robot_assistant,
        "🔌 Electronic Components": electronic_components_assistant,
        "📚 Documentation": documentation
    }
    
    selected_page = st.radio("Navigation", list(pages.keys()))
    
    st.markdown("---")
    
    # Token Usage Summary
    st.subheader("Token Usage Summary")
    st.write(f"Fanuc: {st.session_state.fanuc_total_tokens}")
    st.write(f"Components: {st.session_state.components_total_tokens}")
    st.write(f"Total: {st.session_state.fanuc_total_tokens + st.session_state.components_total_tokens}")

# Render Selected Page
pages[selected_page]()
