import streamlit as st
from openai import OpenAI
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Industry_#004",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
if "rag_files" not in st.session_state:
    st.session_state.rag_files = {
        "fanuc": [],
        "components": [],
        "documentation": []
    }

# Initialize OpenAI client
client = OpenAI(api_key=st.session_state.api_key)

# Utility function for OpenAI API calls
def get_ai_response(prompt, model="gpt-4", temperature=0.7, max_tokens=500):
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

# File Management Function
def file_management_section(section_key):
    uploaded_file = st.file_uploader(f"Upload RAG File for {section_key}", type=['txt', 'csv', 'json'], key=f"uploader_{section_key}")
    if uploaded_file:
        file_details = {"name": uploaded_file.name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if file_details not in st.session_state.rag_files[section_key]:
            st.session_state.rag_files[section_key].append(file_details)
            st.success(f"File {uploaded_file.name} uploaded successfully!")

    if st.session_state.rag_files[section_key]:
        st.write("Available Files:")
        for file in st.session_state.rag_files[section_key]:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"{file['name']} - {file['timestamp']}")
            with col2:
                if st.button("Remove", key=f"remove_{section_key}_{file['name']}"):
                    st.session_state.rag_files[section_key].remove(file)
                    st.experimental_rerun()

# Page 1: Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.header("🤖 Fanuc Robot Assistant")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("👋 I'm Lucas_7, your Fanuc Robot Assistant!")
        st.warning("Note: This AI assistant is still in development mode.")
    with col2:
        st.metric("Tokens Used", st.session_state.fanuc_total_tokens)

    # RAG File Management
    with st.expander("Manage RAG Files"):
        file_management_section("fanuc")

    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023) or a description of the issue...",
        height=100
    )

    if st.button("Submit", key="fanuc_submit"):
        if alarm_code:
            question = f"Provide a detailed explanation and troubleshooting steps for: {alarm_code}"
            with st.spinner("Generating response..."):
                response, tokens = get_ai_response(question)
                if response:
                    st.markdown(response)
                    st.session_state.fanuc_chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "question": alarm_code,
                        "answer": response
                    })
                    st.session_state.fanuc_total_tokens += tokens

    if st.session_state.fanuc_chat_history:
        with st.expander("View Chat History"):
            for chat in reversed(st.session_state.fanuc_chat_history):
                st.markdown(f"**Time:** {chat['timestamp']}")
                st.markdown(f"**Q:** {chat['question']}")
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Page 2: Electronic Components Assistant
def electronic_components_assistant():
    st.header("🔌 Electronic Components Assistant")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("Configure and optimize electronic components with AI assistance.")
    with col2:
        st.metric("Tokens Used", st.session_state.components_total_tokens)

    # RAG File Management
    with st.expander("Manage RAG Files"):
        file_management_section("components")

    component_type = st.selectbox(
        "Select Component Type:",
        ["PLC", "HMI", "Servo Drive", "Sensor", "Other"]
    )
    
    query = st.text_area(
        "Describe your configuration question:",
        placeholder="E.g., How to set up communication between components?",
        height=100
    )
    
    if st.button("Get Assistance"):
        if query:
            prompt = f"Help with {component_type} configuration: {query}"
            with st.spinner("Generating response..."):
                response, tokens = get_ai_response(prompt)
                if response:
                    st.markdown(response)
                    st.session_state.components_chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "component": component_type,
                        "question": query,
                        "answer": response
                    })
                    st.session_state.components_total_tokens += tokens

    if st.session_state.components_chat_history:
        with st.expander("View Chat History"):
            for chat in reversed(st.session_state.components_chat_history):
                st.markdown(f"**Time:** {chat['timestamp']}")
                st.markdown(f"**Component:** {chat['component']}")
                st.markdown(f"**Q:** {chat['question']}")
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Page 3: Documentation
def documentation():
    st.header("📚 Documentation")
    
    # File Management
    st.subheader("Document Management")
    file_management_section("documentation")
    
    # View/Edit Documentation
    if st.session_state.rag_files["documentation"]:
        st.subheader("Available Documentation")
        for doc in st.session_state.rag_files["documentation"]:
            with st.expander(f"{doc['name']}"):
                st.text(f"Last Updated: {doc['timestamp']}")
                st.text_area("Edit Content", "", key=f"edit_{doc['name']}")
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.button("Save Changes", key=f"save_{doc['name']}")
                with col2:
                    st.button("Discard Changes", key=f"discard_{doc['name']}")

# Main Page
def main_page():
    st.title("AI AT MANUFACTURING 4.0")
    
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
    st.info("© 2024 AI Manufacturing Solutions")

# Render Selected Page
pages[selected_page]()
