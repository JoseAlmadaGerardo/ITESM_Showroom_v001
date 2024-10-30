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

# Utility function for OpenAI API calls
def get_ai_response(prompt, model="gpt-4", temperature=0.7, max_tokens=256):
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
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("👋 I'm your Fanuc Robot Assistant!")
        st.warning("Note: This AI assistant is still in development mode.")
    with col2:
        st.metric("Tokens Used", st.session_state.fanuc_total_tokens)

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
    
    query = st.text_area(
        "Describe your configuration question:",
        placeholder="E.g., How to set up communication between a Siemens S7-1200 PLC and an HMI panel?",
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
                        "component": component_type,
                        "question": query,
                        "answer": response
                    })
                    st.session_state.components_total_tokens += tokens

    if st.session_state.components_chat_history:
        with st.expander("View Chat History"):
            for chat in reversed(st.session_state.components_chat_history):
                st.markdown(f"**Component:** {chat['component']}")
                st.markdown(f"**Q:** {chat['question']}")
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
    
    # Placeholder for future documentation content
    st.info("Detailed documentation is currently being compiled. Check back soon for updates!")
    
    # Example structure for future documentation
    st.subheader("Available Documentation:")
    doc_types = ["User Manuals", "Technical Specifications", "Troubleshooting Guides", "Best Practices"]
    for doc in doc_types:
        st.write(f"- {doc}")
    
    st.write("For specific documentation requests, please contact your system administrator.")
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

    st.markdown("---")
    st.info("© 2024 AI Manufacturing Solutions")

# Render Selected Page
pages[selected_page]()
