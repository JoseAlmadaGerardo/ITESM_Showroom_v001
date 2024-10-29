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
if "custom_components" not in st.session_state:
    st.session_state.custom_components = []

# Initialize OpenAI client
client = OpenAI(api_key=st.session_state.api_key)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .user-message {
        background-color: #f8f9fa;
    }
    .assistant-message {
        background-color: #e8f4f9;
    }
    .token-counter {
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

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

# Page 1: Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.header("🤖 Fanuc Robot Assistant")
    
    # Description
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        The Fanuc Robot Assistant supports automated operations, error troubleshooting, and 
        configuration management of industrial robots. It helps in diagnosing and resolving 
        common errors in Fanuc robotic systems for smooth manufacturing workflows.
        </div>
    """, unsafe_allow_html=True)

    # AI Assistant Selection
    col1, col2 = st.columns([3, 1])
    with col1:
        ai_option = st.radio("Choose AI Assistant:", ["GPT-4", "Custom AI Assistant"])
    with col2:
        st.metric("Tokens Used", st.session_state.fanuc_total_tokens)

    # Main Interface
    st.info("👋 I'm Lucas_7, your Fanuc Robot Assistant!")
    st.warning("Note: This AI assistant is still in development mode.")

    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023) or a description of the issue...",
        height=100
    )

    if st.button("Submit", key="fanuc_submit"):
        if alarm_code:
            question = f"Provide a detailed explanation and step-by-step troubleshooting roadmap for the Fanuc Robot alarm code: {alarm_code}. Include possible causes, safety precautions, and resolution steps."
            
            with st.spinner("Generating response..."):
                response, tokens = get_ai_response(question)
                if response:
                    st.markdown(f"""
                        <div class='chat-message assistant-message'>
                        {response}
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.fanuc_chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "question": alarm_code,
                        "answer": response
                    })
                    st.session_state.fanuc_total_tokens += tokens

    # Chat History
    if st.session_state.fanuc_chat_history:
        st.subheader("Chat History")
        for chat in reversed(st.session_state.fanuc_chat_history):
            with st.expander(f"Query from {chat['timestamp']}"):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")

# Page 2: Electronic Components Assistant
def electronic_components_assistant():
    st.header("🔌 Configurations of Electronic Components Assistant")
    
    # Description
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        This assistant helps with the setup and configuration of electronic components 
        used in manufacturing systems. It ensures optimal configurations for the best 
        performance and compatibility across different systems.
        </div>
    """, unsafe_allow_html=True)

    # Component Management
    col1, col2 = st.columns([3, 1])
    with col1:
        new_component = st.text_input("Add new component type:")
        if st.button("Add Component"):
            if new_component and new_component not in st.session_state.custom_components:
                st.session_state.custom_components.append(new_component)
                st.success(f"Added {new_component} to component types!")
    with col2:
        st.metric("Tokens Used", st.session_state.components_total_tokens)

    # Component Selection and Query
    component_types = ["PLC", "HMI", "Servo Drive", "Sensor", "Other"] + st.session_state.custom_components
    component_type = st.selectbox("Select the type of electronic component:", component_types)
    
    configuration_query = st.text_area(
        "Describe your configuration question:",
        placeholder="E.g., How to set up communication between a Siemens S7-1200 PLC and an HMI panel?",
        height=100
    )
    
    if st.button("Get Configuration Assistance"):
        if configuration_query:
            prompt = f"Provide a detailed guide for configuring a {component_type} in the context of: {configuration_query}. Include step-by-step instructions, best practices, and any safety considerations."
            
            with st.spinner("Generating configuration guide..."):
                response, tokens = get_ai_response(prompt, temperature=0.5)
                if response:
                    st.markdown(f"""
                        <div class='chat-message assistant-message'>
                        {response}
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.components_chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "component": component_type,
                        "question": configuration_query,
                        "answer": response
                    })
                    st.session_state.components_total_tokens += tokens

    # Chat History
    if st.session_state.components_chat_history:
        st.subheader("Configuration History")
        for chat in reversed(st.session_state.components_chat_history):
            with st.expander(f"{chat['component']} Configuration - {chat['timestamp']}"):
                st.markdown(f"**Component:** {chat['component']}")
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Solution:** {chat['answer']}")

# Page 3: Documentation
def documentation():
    st.header("📚 Documentation")
    
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        Access comprehensive documentation about the use cases explained for the Business Units.
        This section provides detailed guides, specifications, and best practices.
        </div>
    """, unsafe_allow_html=True)
    
    # Documentation Categories
    doc_categories = {
        "User Manuals": ["Fanuc Robot Operation", "PLC Programming", "HMI Configuration"],
        "Technical Specifications": ["Robot Models", "Component Specifications", "System Requirements"],
        "Troubleshooting Guides": ["Common Error Codes", "Network Issues", "Safety Systems"],
        "Best Practices": ["Operation Guidelines", "Maintenance Schedules", "Safety Protocols"]
    }
    
    selected_category = st.selectbox("Select Documentation Category:", list(doc_categories.keys()))
    
    st.subheader(f"{selected_category} Available:")
    for doc in doc_categories[selected_category]:
        with st.expander(doc):
            st.info("Documentation content is being updated. Please check back soon.")
            st.button(f"Download {doc} PDF", key=f"download_{doc}")

# Main Page
def main_page():
    st.title("AI AT MANUFACTURING 4.0")
    
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem;'>
        <h2>Welcome to the AI-powered Manufacturing 4.0 platform</h2>
        <p>This system integrates artificial intelligence to optimize manufacturing processes, 
        enhance productivity, and streamline equipment monitoring.</p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background-color: #e8f4f9; padding: 1rem; border-radius: 0.5rem; height: 200px;'>
            <h3>🤖 Fanuc Robot Assistant</h3>
            <p>Troubleshoot 
