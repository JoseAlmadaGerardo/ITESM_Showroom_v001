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
st.title("AI at bussines units")

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
if "show_chat_history" not in st.session_state:
    st.session_state.show_chat_history = False
if "current_time" not in st.session_state:
    st.session_state.current_time = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

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
    
# Page 1: Document Analyzer
def customer_support():
    st.markdown("# 📄 Customer Support")
    st.markdown(
        """
        AI-powered customer support solutions can assist in handling inquiries, resolving issues, 
        and enhancing the overall customer experience. With AI chatbots, businesses can provide 
        24/7 support and quickly address customer needs.
        """
    )
    st.write("More details about AI in Customer Support will be added here.")
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
            messages=messages) #,temperature=1, max_tokens=300,
        
        st.session_state.total_tokens += response.usage.total_tokens
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred during the chat: {str(e)}")
        return None

st.title("File Analyzer with ChatGPT")

col_file, col_tokens = st.columns([3, 1])

with col_file:
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "md", "docx"])

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

    # Create two columns for chat and key points
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chat with AI about the Document")
        user_input = st.text_input("Ask a question about the document:", key="user_input")
        if st.button("Send"):
            if user_input:
                response = chat_with_ai(user_input, text)
                if response:
                    st.write("AI Response:")
                    st.write(response)
                    st.session_state.chat_history.append(("You", user_input, st.session_state.current_time))
                    st.session_state.chat_history.append(("AI", response, st.session_state.current_time))
                # Clear the chat input after sending
                #st.session_state.user_input = ""

    with col2:
        st.subheader("Key Points Min= 3 & Max=10")
        num_points = st.number_input("Number of key points", min_value=3, max_value=10, value=3, step=1)
        if st.button("Generate Key Points"):
            st.session_state.key_points = get_key_points(text, num_points)

        st.write(st.session_state.key_points)

    # Always visible chat history
    st.subheader("Chat History")
    chat_col1, chat_col2 = st.columns(2)
    for i, (role, message, timestamp) in enumerate(st.session_state.chat_history):
        with chat_col1 if i % 2 == 0 else chat_col2:
            st.write(f"**{role}** ({timestamp}):")
            st.write(message)

# Page 2: Sales
def sales():
    st.markdown("# 📄 Sales")
    st.markdown(
        """
        AI in sales can optimize the sales process by analyzing customer data, predicting customer 
        behavior, and recommending next best actions. This enables sales teams to focus on high-value 
        opportunities and close deals faster.
        """
    )
    st.write("More details about AI in Sales will be added here.")

# Page 3: Human Resources
def human_resources():
    st.markdown("# 📄 Human Resources")
    st.markdown(
        """
        AI tools in human resources can streamline recruitment, assist in talent management, 
        and improve employee engagement. AI can help match candidates with roles, automate 
        administrative tasks, and enhance workforce management.
        """
    )
    st.write("More details about AI in Human Resources will be added here.")

# Page 4: IT Support
def it_support():
    st.markdown("# 📄 IT Support")
    st.markdown(
        """
        AI in IT support helps diagnose issues, automate troubleshooting, and assist in monitoring 
        IT infrastructure. AI tools can provide real-time alerts, recommend fixes, and reduce 
        downtime for business operations.
        """
    )
    st.write("More details about AI in IT Support will be added here.")

# Page 5: Documentation
def documentation():
    st.markdown("# 📄 Documentation ")
    st.markdown(
        """
        At this section you will find the documentation about the cases explained for the Bussines units.
        """
    )
    st.write("Documentation will be added here.")

# Main Page Selection
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Customer Support": customer_support,
    "📄 Sales": sales,
    "📄 Human Resources": human_resources,
    "📄 IT Support": it_support,
    "📄 Documentation": documentation,
}

# Sidebar for Navigation
st.sidebar.header("AI AT BUSSINES UNITS")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())

# Render Main Introductory Content Only on Main Page
if demo_name == "—":
    st.markdown(
        """
        AI is transforming various business unit operations, from customer support and sales to human resources and IT support. 
        Explore how AI can improve efficiency, decision-making, and overall performance across these areas.
        
        **Explore Use Cases:**
        - 📄 Customer Support.
        - 📄 Sales.
        - 📄 Human Resources.
        - 📄 IT Support.
        - 📄 Documentation.
        """
    )
    st.write("👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

# Render Selected Page
page_names_to_funcs[demo_name]()
