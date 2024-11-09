import streamlit as st
from openai import OpenAI
import PyPDF2
import docx
import markdown
import re
import json
import base64
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Content Co-pilot",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Content Co-pilot for Marketing Teams")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

openai_api_key = st.session_state.api_key
client = OpenAI(api_key=openai_api_key)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "context" not in st.session_state:
    st.session_state.context = ""

# Utility function for OpenAI API calls
def get_ai_response(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=500):
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

# Text extraction functions
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_md(file):
    content = file.read().decode('utf-8')
    html = markdown.markdown(content)
    text = re.sub('<[^<]+?>', '', html)
    return text

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

# Function to extract key points
def get_key_points(text, num_points):
    prompt = f"Extract {num_points} key points from the following text:\n\n{text}"
    response, tokens = get_ai_response(prompt, max_tokens=1000)
    st.session_state.total_tokens += tokens
    return response

# Function for content generation
def generate_content(context, prompt, target_audience):
    full_prompt = f"""
    Context: {context}
    Target Audience: {target_audience}
    Task: {prompt}

    Generate creative marketing content based on the given context and target audience. Ensure the content is engaging, relevant, 
    and tailored to the specified audience.
    """
    response, tokens = get_ai_response(full_prompt, max_tokens=1000)
    st.session_state.total_tokens += tokens
    return response

# Function for content localization
def localize_content(content, target_locale, target_culture):
    prompt = f"""
    Original Content: {content}
    Target Locale: {target_locale}
    Target Culture: {target_culture}

    Task: Adapt the given content for the target locale and culture. Consider language nuances, cultural references, and local preferences. 
    Ensure the localized content maintains the original message while being culturally appropriate and engaging for the target audience.
    """
    response, tokens = get_ai_response(prompt, max_tokens=1000)
    st.session_state.total_tokens += tokens
    return response

# Main application
def main():
    st.sidebar.title("Content Co-pilot")
    
    # Document upload
    uploaded_file = st.sidebar.file_uploader("Upload a document for context (PDF, DOCX, MD, TXT)", type=['pdf', 'docx', 'md', 'txt'])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.type == "text/markdown":
            text = extract_text_from_md(uploaded_file)
        elif uploaded_file.type == "text/plain":
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type")
            return

        st.session_state.context = text
        st.sidebar.success("Document uploaded and processed successfully!")

        # Key points extraction
        num_points = st.sidebar.number_input("Number of key points to extract", min_value=3, max_value=10, value=5)
        if st.sidebar.button("Extract Key Points"):
            key_points = get_key_points(text, num_points)
            st.sidebar.subheader("Key Points:")
            st.sidebar.write(key_points)

    # Content Generation
    st.header("Content Generation")
    st.markdown(
        """
        The Content Co-pilot assists in generating creative content. It helps 
        streamline the content creation process by offering suggestions, refining ideas, and 
        ensuring consistency with brand messaging.
        """
    )
    st.write("Add target audience and contente prompt to create a custom marketing content.")
    target_audience = st.text_input("Target Audience", placeholder="E.g., Young professionals in urban areas")
    content_prompt = st.text_area("Content Prompt", placeholder="E.g., Create a social media post about our new eco-friendly product line")
    
    if st.button("Generate Content"):
        if content_prompt:
            generated_content = generate_content(st.session_state.context, content_prompt, target_audience)
            st.subheader("Generated Content:")
            st.write(generated_content)
            st.session_state.chat_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "content_generation",
                "prompt": content_prompt,
                "result": generated_content
            })

    # Content Localization
    st.header("Content Localization")
    content_to_localize = st.text_area("Content to Localize", placeholder="Paste the content you want to localize")
    target_locale = st.text_input("Target Locale", placeholder="E.g., fr-FR, es-ES, de-DE")
    target_culture = st.text_input("Target Culture", placeholder="E.g., French, Spanish, German")
    
    if st.button("Localize Content"):
        if content_to_localize and target_locale and target_culture:
            localized_content = localize_content(content_to_localize, target_locale, target_culture)
            st.subheader("Localized Content:")
            st.write(localized_content)
            st.session_state.chat_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "content_localization",
                "original": content_to_localize,
                "locale": target_locale,
                "culture": target_culture,
                "result": localized_content
            })

    # Display token usage
    st.sidebar.metric("Total Tokens Used", st.session_state.total_tokens)

    # Display chat history
    if 'type' in item and 'timestamp' in item:
    with st.expander(f"{item['type']} - {item['timestamp']}"):
    st.header("Activity History")
    for item in reversed(st.session_state.chat_history):
        with st.expander(f"{item['type']} - {item['timestamp']}"):
            if item['type'] == 'content_generation':
                st.write(f"**Prompt:** {item['prompt']}")
                st.write(f"**Generated Content:** {item['result']}")
            elif item['type'] == 'content_localization':
                st.write(f"**Original:** {item['original']}")
                st.write(f"**Locale:** {item['locale']}")
                st.write(f"**Culture:** {item['culture']}")
                st.write(f"**Localized Content:** {item['result']}")
    else:
    # Handle the case where keys are missing
    st.write("Missing 'type' or 'timestamp' in item data.")

if __name__ == "__main__":
    main()
