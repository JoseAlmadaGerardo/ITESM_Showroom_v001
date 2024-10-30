import streamlit as st
from openai import OpenAI

# UCase_005(v002): Submit request PB was added

st.set_page_config(page_title="UCase_005", page_icon="📊")
st.markdown("# template_005")
st.sidebar.header("Template")

st.title("Just a template")
st.subheader("Factory Asset Effectiveness")
st.write("📄 Upload a document below and ask a question about it – GPT will answer!")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

    # Allow file upload
    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

    # Ask for a question
    question = st.text_area("Ask a question about the document", disabled=not uploaded_file)

    # Add submit button
    if st.button("Submit"):
        if uploaded_file and question:
            # Process uploaded file and question
            document = uploaded_file.read().decode()
            messages = [{"role": "user", "content": f"Document: {document} \n\nQuestion: {question}"}]

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
