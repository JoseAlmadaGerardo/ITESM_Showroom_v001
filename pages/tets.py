import streamlit as st
import PyPDF2
import openai
import io
from openai import OpenAI

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)
    
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def get_key_points(text, num_points):
    # Add submit button
    if st.button("Submit"):
        if uploaded_file and question:
            # Process uploaded file and question
            document = uploaded_file.read().decode()
            messages = [{"role": "system", "content": "You are a helpful assistant that extracts key points from text."},
            {"role": "user", "content": f"Extract {num_points} key points from the following text:\n\n{text}"}]

            # Generate response using OpenAI API
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )
             # Display the response
            st.write_stream(stream)
        else:
            st.error("Please upload a document and ask a question.")

st.title("File Analyzer with ChatGPT")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
num_points = st.slider("Number of key points", min_value=5, max_value=10, value=5)

if uploaded_file is not None:
    st.write("Analyzing file...")
    
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_txt(uploaded_file)
    
    st.write("Generating key points...")
    key_points = get_key_points(text, num_points)
    
    st.write("Key Points:")
    st.write(key_points)

st.write("Note: Make sure to set your OpenAI API key in the Streamlit secrets.")
