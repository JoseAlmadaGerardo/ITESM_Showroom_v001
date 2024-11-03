import streamlit as st
import PyPDF2
import openai
import io

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
openai.api_key = st.session_state.api_key  # Set the API key globally for OpenAI

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8")

def get_key_points(text, num_points):
    # Check if text and num_points are provided before making API call
    if text and num_points:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key points from text."},
                {"role": "user", "content": f"Extract {num_points} key points from the following text:\n\n{text}"}
            ]
        )
        # Return the generated response text
        return response.choices[0].message['content']
    else:
        st.error("Text is empty or the number of key points is not set.")

st.title("File Analyzer with ChatGPT")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf"])
num_points = st.slider("Number of key points", min_value=5, max_value=10, value=5)

if uploaded_file is not None:
    st.write("Analyzing file...")
    
    # Extract text based on file type
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_txt(uploaded_file)
    
    st.write("Generating key points...")
    key_points = get_key_points(text, num_points)
    
    if key_points:
        st.write("Key Points:")
        st.write(key_points)

st.write("Note: Make sure to set your OpenAI API key in the Streamlit secrets.")
