import streamlit as st
import openai

def run_use_case_5(api_key):
    # Set the page config and title
    st.markdown("# UCase_005")
    st.subheader("Factory Asset Effectiveness.​")
    st.write("📄 Answers to questions about .TX, .MD, and .PDF documents. Upload a document below and ask a question about it – GPT will answer!")

    # Allow the user to upload a file
    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

    # Ask the user to input a question
    question = st.text_area(
        "Ask a question about the document!",
        placeholder="Can you give me a brief summary?",
        disabled=not uploaded_file,
    )

    # If both a file is uploaded and a question is asked
    if uploaded_file and question:
        try:
            # Read the uploaded document
            document = uploaded_file.read().decode()

            # Prepare the messages for OpenAI
            messages = [
                {
                    "role": "user",
                    "content": f"Here is a document: {document} \n\n---\n\n {question}",
                }
            ]

            # Generate a response using OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
                api_key=api_key,
            )

            # Display the response
            for chunk in response:
                st.write(chunk['choices'][0]['delta']['content'])
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
