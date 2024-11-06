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
st.title("AI at manufacturing 4.0 using upadate documents for a RAG")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
if "fanuc_chat_history" not in st.session_state:
    st.session_state.fanuc_chat_history = []
if "components_chat_history" not in st.session_state:
    st.session_state.components_chat_history = []
if "fanuc_total_tokens" not in st.session_state:
    st.session_state.fanuc_total_tokens = 0
if "components_total_tokens" not in st.session_state:
    st.session_state.components_total_tokens = 0
if "custom_components" not in st.session_state:
    st.session_state.custom_components = []
if "fanuc_context" not in st.session_state:
    st.session_state.fanuc_context = ""
if "components_context" not in st.session_state:
    st.session_state.components_context = ""

# Utility function for OpenAI API calls
def get_ai_response(prompt, model="gpt-3.5-turbo", temperature=1, max_tokens=126):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content, response.usage.total_tokens
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, 0

# Function to download chat history
def download_chat_history():
    data = {
        "fanuc_chat_history": st.session_state.fanuc_chat_history,
        "components_chat_history": st.session_state.components_chat_history,
        "fanuc_total_tokens": st.session_state.fanuc_total_tokens,
        "components_total_tokens": st.session_state.components_total_tokens
    }
    json_string = json.dumps(data, indent=2)
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="chat_history.json">Download Chat History</a>'
    return href

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
def get_key_points(text, num_points):
    prompt = f"Extract {num_points} key points from the following text:\n\n{text}"
    response, _ = get_ai_response(prompt, max_tokens=1000)
    return response

# Function for context-based chat
def chat_with_ai(context, question, chat_history):
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    response, tokens = get_ai_response(prompt, max_tokens=500)
    chat_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "answer": response
    })
    return response, tokens

# Page 1: Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.header("🤖 Fanuc Robot Assistant")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("👋 I'm your Fanuc Robot Assistant!")
        st.warning("Note: This AI assistant is still in development mode.")
    with col2:
        st.metric("Tokens Used", st.session_state.fanuc_total_tokens)

    # Document upload
    uploaded_file = st.file_uploader("Upload a document for context (PDF, DOCX, MD, TXT)", type=['pdf', 'docx', 'md', 'txt'])
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
        num_points = st.number_input("Number of key points", min_value=3, max_value=10, value=3, step=1)
        if st.button("Extract Key Points"):
            key_points = get_key_points(text, num_points)
            st.markdown("### Key Points:")
            st.write(key_points)

    # Chat functionality
    st.subheader("Chat with Fanuc Robot Assistant")
    question = st.text_input("Ask a question about Fanuc robots:")
    if st.button("Send"):
        if question:
            response, tokens = chat_with_ai(st.session_state.fanuc_context, question, st.session_state.fanuc_chat_history)
            st.markdown(f"**Answer:** {response}")
            st.session_state.fanuc_total_tokens += tokens

    # Chat history
    if st.session_state.fanuc_chat_history:
        st.subheader("Chat History")
        for chat in reversed(st.session_state.fanuc_chat_history):
            with st.expander(f"Q: {chat['question']} - {chat['timestamp']}"):
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Page 2: Electronic Components Assistant
def electronic_components_assistant():
    st.header("🔌 Electronic Components Assistant")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        This assistant helps with the setup and configuration of electronic components 
        used in manufacturing systems. It ensures optimal configurations for the best 
        performance and compatibility across different systems.
        """)
    with col2:
        st.metric("Tokens Used", st.session_state.components_total_tokens)
        
    new_component = st.sidebar.text_input("Add new component type:")
    if st.sidebar.button("Add Component"):
        if new_component and new_component not in st.session_state.custom_components:
            st.session_state.custom_components.append(new_component)  

    component_types = ["PLC", "HMI", "Servo Drive", "Sensor", "Other"] + st.session_state.custom_components
    component_type = st.selectbox("Select the type of electronic component:", component_types)
    
    # Document upload
    uploaded_file = st.file_uploader("Upload a document for context (PDF, DOCX, MD, TXT)", type=['pdf', 'docx', 'md', 'txt'])
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
        num_points = st.number_input("Number of key points", min_value=3, max_value=10, value=3, step=1)
        if st.button("Extract Key Points"):
            key_points = get_key_points(text, num_points)
            st.markdown("### Key Points:")
            st.write(key_points)

    # Chat functionality
    st.subheader("Chat with Electronic Components Assistant")
    question = st.text_input("Ask a question about electronic components:")
    if st.button("Send"):
        if question:
            response, tokens = chat_with_ai(st.session_state.components_context, question, st.session_state.components_chat_history)
            st.markdown(f"**Answer:** {response}")
            st.session_state.components_total_tokens += tokens

    # Chat history
    if st.session_state.components_chat_history:
        st.subheader("Chat History")
        for chat in reversed(st.session_state.components_chat_history):
            with st.expander(f"{chat['component'] if 'component' in chat else ''}: {chat['question']} - {chat['timestamp']}"):
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Page 3: Documentation
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

# Sidebar Navigation
with st.sidebar:
    st.title("AI AT MANUFACTURING 4.0")
    
    pages = {
        "Home": main_page,
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
