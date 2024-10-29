import streamlit as st
from openai import OpenAI
import time

# UCase_006(v003): Improved UI, error handling, and code structure
st.set_page_config(page_title="Industry_#003", page_icon="🏭", layout="wide")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

# Initialize OpenAI client
client = OpenAI(api_key=st.session_state.api_key)

# Utility function for OpenAI API calls
def get_ai_response(prompt, model="gpt-4", temperature=0.7, max_tokens=500):
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        return stream
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Page 1: Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.header("🤖 Fanuc Robot Assistant")
    st.markdown(
        """
        The Fanuc Robot Assistant supports automated operations, error troubleshooting, and 
        configuration management of industrial robots. It helps in diagnosing and resolving 
        common errors in Fanuc robotic systems for smooth manufacturing workflows.
        """
    )

    st.info("👋 I'm Lucas_7, your Fanuc Robot Assistant powered by OpenAI API!")
    st.write("I will provide you with an explanation and roadmap for troubleshooting a robot alarm code.")
    st.warning("Note: This AI assistant is still in development mode. Please consider that the answers may not be fully accurate yet.")

    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023) or a description of the issue...",
    )

    if st.button("Submit", key="fanuc_submit"):
        if alarm_code:
            question = f"Provide a detailed explanation and step-by-step troubleshooting roadmap for the Fanuc Robot alarm code: {alarm_code}. Include possible causes, safety precautions, and resolution steps."
            
            with st.spinner("Generating response..."):
                stream = get_ai_response(question)
                if stream:
                    response = st.empty()
                    full_response = ""
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            response.markdown(full_response + "▌")
                    response.markdown(full_response)
        else:
            st.error("Please enter a robot alarm code before submitting.")

# Page 2: Configurations of Electronic Components Assistant
def electronic_components_assistant():
    st.header("🔌 Configurations of Electronic Components Assistant")
    st.markdown(
        """
        This assistant helps with the setup and configuration of electronic components 
        used in manufacturing systems. It ensures optimal configurations for the best 
        performance and compatibility across different systems.
        """
    )
    
    component_type = st.selectbox(
        "Select the type of electronic component:",
        ["PLC", "HMI", "Servo Drive", "Sensor", "Other"]
    )
    
    configuration_query = st.text_area(
        "Describe your configuration question:",
        placeholder="E.g., How to set up communication between a Siemens S7-1200 PLC and an HMI panel?"
    )
    
    if st.button("Get Configuration Assistance", key="config_submit"):
        if configuration_query:
            prompt = f"Provide a detailed guide for configuring a {component_type} in the context of: {configuration_query}. Include step-by-step instructions, best practices, and any safety considerations."
            
            with st.spinner("Generating configuration guide..."):
                stream = get_ai_response(prompt, temperature=0.5)
                if stream:
                    response = st.empty()
                    full_response = ""
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            response.markdown(full_response + "▌")
                    response.markdown(full_response)
        else:
            st.error("Please enter a configuration question before submitting.")

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

# Main Page Selection
page_names_to_funcs = {
    "Home": lambda: main_page(),
    "🤖 Fanuc Robot Assistant": fanuc_robot_assistant,
    "🔌 Electronic Components Assistant": electronic_components_assistant,
    "📚 Documentation": documentation,
}

# Sidebar for Navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=AI+Manufacturing", width=150)
    st.header("AI AT MANUFACTURING 4.0")
    demo_name = st.selectbox("Choose a use case", list(page_names_to_funcs.keys()))

# Main page content
def main_page():
    st.title("AI AT MANUFACTURING 4.0")
    st.markdown(
        """
        Welcome to the AI-powered Manufacturing 4.0 platform. This system integrates artificial intelligence 
        to optimize manufacturing processes, enhance productivity, and streamline equipment monitoring.
        
        **Available Use Cases:**
        - 🤖 Fanuc Robot Assistant: Troubleshoot and manage Fanuc robotic systems.
        - 🔌 Electronic Components Assistant: Configure and optimize electronic components.
        - 📚 Documentation: Access comprehensive guides and technical information.
        
        Select a use case from the sidebar to explore how AI can revolutionize your manufacturing processes!
        """
    )
    st.image("https://via.placeholder.com/600x300?text=Manufacturing+4.0", use_column_width=True)

# Render Selected Page
page_names_to_funcs[demo_name]()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("© 2024 AI Manufacturing Solutions. All rights reserved.")
