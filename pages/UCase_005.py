import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="UCase_005", page_icon="📊")
st.markdown("# UCase_005")
st.sidebar.header("UCase_005")

st.title("Manufacturing: Use Case #5")
st.subheader("Factory Asset Effectiveness")
st.write("📄 Upload a document below and ask a question about it – GPT will answer!")

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

    # Allow file upload
    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

    # Ask for a question
    question = st.text_area("Ask a question about the document", disabled=not uploaded_file)

    if uploaded_file and question:
        # Process uploaded file and question
        document = uploaded_file.read().decode()
        messages = [{"role": "user", "content": f"Document: {document} \n\n Question: {question}"}]

        # Generate response using OpenAI API
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Display the response
        st.write_stream(stream)
