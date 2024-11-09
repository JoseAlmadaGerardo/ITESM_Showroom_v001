import streamlit as st
import PyPDF2
from openai import OpenAI
import io
import docx
import markdown
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="# Bussines_units",page_icon="📈", layout="wide",initial_sidebar_state="expanded")
st.title("AI at bussines units Using Document Analyzer")
st.markdown(
        """
        This AI-powered document analyzer utilizing the OpenAI API 3.5 turbo extracts insights, summarizes content, 
        and identifies key points from documents, enabling efficient data processing and knowledge extraction.
        This tool aids users in quickly understanding and analyzing text, streamlining document review, and 
        facilitating informed decision-making. 
        """ 
        """
        In sales, AI optimizes processes by analyzing customer data, 
        predicting behavior, and recommending actions, allowing teams to focus on high-value opportunities. 
        In human resources, AI streamlines recruitment, assists in talent management, and enhances employee engagement by matching candidates with roles and automating tasks. 
        In IT support, AI diagnoses issues, automates troubleshooting, and monitors infrastructure, providing real-time alerts and reducing downtime. 
        AI-powered customer support solutions handle inquiries, resolve issues, and enhance the customer experience through 24/7 chatbot assistance.
        """
    )

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
if "current_time" not in st.session_state:
    st.session_state.current_time = ""

# Update current time
st.session_state.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def extract_text_from_md(file):
    md_text = file.getvalue().decode("utf-8")
    html = markdown.markdown(md_text)
    return html

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

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
            messages=messages)

        st.session_state.total_tokens += response.usage.total_tokens
        answer = response.choices[0].message.content
        st.session_state.chat_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_input,
            "answer": answer
        })
        return answer
    except Exception as e:
        st.error(f"An error occurred during the chat: {str(e)}")
        return None

# File uploader and text extraction
col_file, col_tokens = st.columns([3, 1])

with col_file:
    uploaded_file = st.file_uploader("Choose a file to explore our key points tool and chat with the AI assistant about the document. Note:Maximum size allowed 5MB.", 
                                     type=["txt", "pdf", "md", "docx", "(The Real tool limit per file is 5MB)."])

with col_tokens:
    st.subheader("Token Usage")
    st.write(f"Total tokens used: {st.session_state.total_tokens}")

if uploaded_file is not None:
    # Clear previous key points
    st.session_state.key_points = ""

    st.write("Analyzing file...")

    # Extract text based on file type
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "text/markdown":
        text = extract_text_from_md(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)
    else:
        text = extract_text_from_txt(uploaded_file)

    # Chat and key points extraction sections
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chat with AI about the Document")
        user_input = st.text_input("Ask a question about the document:")
        if st.button("Send"):
            if user_input:
                response = chat_with_ai(user_input, text)
                if response:
                    st.markdown(f"**Answer:** {response}")

    with col2:
        st.subheader("Key Points Min=3 & Max=10")
        num_points = st.number_input("Number of key points", min_value=3, max_value=10, value=3, step=1)
        if st.button("Generate Key Points"):
            st.session_state.key_points = get_key_points(text, num_points)
        st.write(st.session_state.key_points)

# Main Page Selection
page_names_to_funcs = {
    "🏡 Home": lambda: st.write("😊"),
}

# Sidebar for Navigation
st.sidebar.header("AI AT BUSSINES UNITS")
demo_name = st.sidebar.radio("Choose a use case", page_names_to_funcs.keys())

# Render Main Introductory Content Only on Main Page
if demo_name == "🏡 Home":
    st.write("Thanks!")

# Render Selected Page
page_names_to_funcs[demo_name]()
