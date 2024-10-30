import streamlit as st
import openai
import time
import tiktoken

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'assistants' not in st.session_state:
    st.session_state.assistants = []
if 'selected_assistant' not in st.session_state:
    st.session_state.selected_assistant = None
if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {}
if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0

def set_api_key():
    openai.api_key = st.session_state.api_key
    load_assistants()

def load_assistants():
    try:
        assistants = openai.beta.assistants.list()
        st.session_state.assistants = assistants.data
    except Exception as e:
        st.error(f"Error loading assistants: {str(e)}")

def create_assistant(name, instructions, model):
    try:
        assistant = openai.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
        st.session_state.assistants.append(assistant)
        return assistant
    except Exception as e:
        st.error(f"Error creating assistant: {str(e)}")
        return None

def upload_file(file):
    try:
        response = openai.files.create(file=file, purpose='assistants')
        return response.id
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return None

def add_file_to_assistant(assistant_id, file_id):
    try:
        openai.beta.assistants.files.create(assistant_id=assistant_id, file_id=file_id)
        st.success("File added to assistant successfully!")
    except Exception as e:
        st.error(f"Error adding file to assistant: {str(e)}")

def chat_with_assistant(assistant_id, user_message):
    try:
        thread = openai.beta.threads.create()
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        while run.status != 'completed':
            time.sleep(1)
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        # Calculate and update token usage
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens_used = len(encoding.encode(user_message)) + len(encoding.encode(response))
        st.session_state.total_tokens += tokens_used
        
        return response
    except Exception as e:
        st.error(f"Error chatting with assistant: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(layout="wide")
st.title("OpenAI assistant manager & dev.")

# Sidebar for configuration and assistant management
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password", on_change=set_api_key, key="api_key")
    
    if api_key:
        st.header("Manage Assistants")
        
        # Create new assistant
        with st.expander("Create New Assistant"):
            new_name = st.text_input("Assistant Name")
            new_instructions = st.text_area("Instructions")
            new_model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"])
            if st.button("Create Assistant"):
                new_assistant = create_assistant(new_name, new_instructions, new_model)
                if new_assistant:
                    st.success(f"Assistant '{new_name}' created successfully!")
        
        # Select assistant
        assistant_names = [a.name for a in st.session_state.assistants]
        selected_assistant_name = st.selectbox("Select an Assistant", assistant_names)
        st.session_state.selected_assistant = next((a for a in st.session_state.assistants if a.name == selected_assistant_name), None)
        
        # Upload file for RAG
        if st.session_state.selected_assistant:
            uploaded_file = st.file_uploader("Upload a file for RAG", type=['txt', 'pdf', 'csv'])
            if uploaded_file and st.button("Add File to Assistant"):
                file_id = upload_file(uploaded_file)
                if file_id:
                    add_file_to_assistant(st.session_state.selected_assistant.id, file_id)

# Main layout
if st.session_state.selected_assistant:
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.header(f"Chat with {st.session_state.selected_assistant.name}")
        
        # Initialize chat history for the selected assistant if not exists
        if st.session_state.selected_assistant.id not in st.session_state.chat_histories:
            st.session_state.chat_histories[st.session_state.selected_assistant.id] = []
        
        # Display chat history
        for message in st.session_state.chat_histories[st.session_state.selected_assistant.id]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        user_message = st.chat_input("Type your message here...")
        if user_message:
            st.session_state.chat_histories[st.session_state.selected_assistant.id].append({"role": "user", "content": user_message})
            with st.chat_message("user"):
                st.write(user_message)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = chat_with_assistant(st.session_state.selected_assistant.id, user_message)
                if full_response:
                    message_placeholder.markdown(full_response)
                    st.session_state.chat_histories[st.session_state.selected_assistant.id].append({"role": "assistant", "content": full_response})
    
    with col2:
        st.subheader("Conversation History")
        for assistant in st.session_state.assistants:
            if assistant.id in st.session_state.chat_histories:
                with st.expander(f"{assistant.name} History"):
                    for message in st.session_state.chat_histories[assistant.id]:
                        st.write(f"**{message['role'].capitalize()}:** {message['content'][:50]}...")
    
    with col3:
        st.subheader("Session Stats")
        st.metric("Total Tokens Used", st.session_state.total_tokens)
        st.write(f"Current Assistant: {st.session_state.selected_assistant.name}")
        st.write(f"Model: {st.session_state.selected_assistant.model}")
else:
    
    st.markdown(
        """
        Creating and deploying AI assistants has never been more accessible or versatile. With this tool, you can set up OpenAI-powered assistants to handle various
        tasks seamlessly. Simply provide your API key, and you’ll unlock options to browse existing AI assistants or create new ones tailored to your unique needs.
        Additionally, you can upload reference files for each assistant, enabling Retrieval-Augmented Generation (RAG) functionality to enrich responses with
        relevant contextual information.

        Once configured, the main column becomes your interactive space, where you can chat with your AI assistant and receive responses in real-time.From customer
        support bots to specialized advisors, this tool empowers you to design, manage, and interact with assistants that bring intelligent, responsive support to
        any task.
        """
        )
    st.write(" Note: To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys).")
    
    st.write("👈 Please select an assistant from the sidebar to start chatting.")

# Display total token usage at the bottom of the sidebar
with st.sidebar:
    st.metric("Total Session Tokens", st.session_state.total_tokens)

