import streamlit as st
import PyPDF2
from openai import OpenAI
import io

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

# Initialize the OpenAI client
client = OpenAI(api_key=st.session_state.api_key)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "key_points" not in st.session_state:
    st.session_state.key_points = ""

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def get_key_points(text, num_points):
    if text and num_points:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts key points from text."},
                    {"role": "user", "content": f"Extract {num_points} key points from the following text:\n\n{text}"}
                ]
            )
            st.session_state.total_tokens += response.usage.total_tokens
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"An error occurred while generating key points: {str(e)}")
            return None
    else:
        st.error("Text is empty or the number of key points is not set.")
        return None

def chat_with_ai(user_input, context):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant answering questions about a document."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_input}"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        st.session_state.total_tokens += response.usage.total_tokens
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred during the chat: {str(e)}")
        return None

st.title("Advanced File Analyzer with ChatGPT")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])

if uploaded_file is not None:
    st.write("Analyzing file...")
    
    # Extract text based on file type
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_txt(uploaded_file)
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col2:
        st.subheader("Key Points")
        num_points = st.number_input("Number of key points", min_value=5, max_value=10, value=5, step=1)
        if st.button("Generate Key Points"):
            st.session_state.key_points = get_key_points(text, num_points)
        
        if st.session_state.key_points:
            st.write(st.session_state.key_points)
    
    with col1:
        st.subheader("Chat with AI about the Document")
        user_input = st.text_input("Ask a question about the document:")
        if st.button("Send"):
            if user_input:
                response = chat_with_ai(user_input, text)
                if response:
                    st.session_state.chat_history.append(("You", user_input))
                    st.session_state.chat_history.append(("AI", response))
        
        # Display chat history
        st.subheader("Chat History")
        for role, message in st.session_state.chat_history:
            st.write(f"**{role}:** {message}")
    
    # Display token usage
    st.sidebar.subheader("Token Usage")
    st.sidebar.write(f"Total tokens used: {st.session_state.total_tokens}")

st.write("Note: Make sure to set your OpenAI API key in the Streamlit secrets.")

# CSS to improve the layout
st.markdown("""
<style>
.stButton>button {
    width: 100%;
}
.stTextInput>div>div>input {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)
