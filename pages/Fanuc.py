import streamlit as st
from openai import OpenAI
import time
import tiktoken

# Initialize OpenAI client
client = OpenAI(api_key=st.session_state.api_key)

# Initialize session state variables
if "fanuc_assistant" not in st.session_state:
    st.session_state.fanuc_assistant = None
if "fanuc_chat_history" not in st.session_state:
    st.session_state.fanuc_chat_history = []
if "fanuc_total_tokens" not in st.session_state:
    st.session_state.fanuc_total_tokens = 0

def load_assistants():
    try:
        assistants = client.beta.assistants.list()
        return assistants.data
    except Exception as e:
        st.error(f"Error loading assistants: {str(e)}")
        return []

def create_assistant(name, instructions, model):
    try:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
        return assistant
    except Exception as e:
        st.error(f"Error creating assistant: {str(e)}")
        return None

def upload_file(file):
    try:
        response = client.files.create(file=file, purpose='assistants')
        return response.id
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return None

def add_file_to_assistant(assistant_id, file_id):
    try:
        client.beta.assistants.files.create(assistant_id=assistant_id, file_id=file_id)
        st.success("File added to assistant successfully!")
    except Exception as e:
        st.error(f"Error adding file to assistant: {str(e)}")

def chat_with_assistant(assistant_id, user_message):
    try:
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        # Calculate and update token usage
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens_used = len(encoding.encode(user_message)) + len(encoding.encode(response))
        st.session_state.fanuc_total_tokens += tokens_used
        
        return response
    except Exception as e:
        st.error(f"Error chatting with assistant: {str(e)}")
        return None

def fanuc_robot_assistant():
    st.header("🤖 Fanuc Robot Assistant")
    st.markdown(
        """
        The Fanuc Robot Assistant supports automated operations, error troubleshooting, and 
        configuration management of industrial robots. It helps in diagnosing and resolving 
        common errors in Fanuc robotic systems for smooth manufacturing workflows.
        """
    )

    # Load or create Fanuc Robot Assistant
    assistants = load_assistants()
    fanuc_assistant = next((a for a in assistants if a.name == "Fanuc Robot Assistant"), None)
    
    if not fanuc_assistant:
        st.warning("Fanuc Robot Assistant not found. Creating a new one...")
        fanuc_assistant = create_assistant(
            name="Fanuc Robot Assistant",
            instructions="You are an expert in Fanuc robots. Assist with troubleshooting, configuration, and operations.",
            model="gpt-4"
        )
    
    st.session_state.fanuc_assistant = fanuc_assistant

    # File upload for RAG
    uploaded_file = st.file_uploader("Upload a file for RAG (optional)", type=['txt', 'pdf', 'csv'])
    if uploaded_file and st.button("Add File to Assistant"):
        file_id = upload_file(uploaded_file)
        if file_id:
            add_file_to_assistant(st.session_state.fanuc_assistant.id, file_id)

    st.info("👋 I'm Lucas_7, your Fanuc Robot Assistant!")
    st.write("I will provide you with an explanation and roadmap for troubleshooting a robot alarm code.")
    st.warning("Note: This AI assistant is still in development mode. Please consider that the answers may not be fully accurate yet.")

    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023) or a description of the issue...",
    )

    if st.button("Submit", key="fanuc_submit"):
        if alarm_code:
            with st.spinner("Generating response..."):
                response = chat_with_assistant(st.session_state.fanuc_assistant.id, alarm_code)
                if response:
                    st.markdown(response)
                    st.session_state.fanuc_chat_history.append({"question": alarm_code, "answer": response})

    # Display chat history and token consumption
    st.subheader("Chat History")
    for chat in st.session_state.fanuc_chat_history:
        st.text(f"Q: {chat['question']}")
        st.text(f"A: {chat['answer']}")
        st.markdown("---")
    
    st.sidebar.metric("Total Tokens Used (Fanuc)", st.session_state.fanuc_total_tokens)

# Main app
def main():
    st.set_page_config(page_title="Fanuc Robot Assistant", page_icon="🤖", layout="wide")
    st.title("AI AT MANUFACTURING 4.0 - Fanuc Robot Assistant")

    # Load API key
    if "api_key" not in st.session_state:
        st.session_state.api_key = st.secrets["openai"]["api_key"]

    fanuc_robot_assistant()

if __name__ == "__main__":
    main()
