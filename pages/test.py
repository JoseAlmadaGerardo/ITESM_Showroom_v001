import streamlit as st
import os
#from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Function to load and process documents
def process_document(file):
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension == ".pdf":
        loader = PyPDFLoader(file.name)
    elif file_extension == ".docx":
        loader = Docx2txtLoader(file.name)
    elif file_extension in [".txt", ".md"]:
        loader = TextLoader(file.name)
    else:
        st.error("Unsupported file format. Please upload PDF, DOCX, MD, or TXT files.")
        return None

    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore

# Function to generate content
def generate_content(vectorstore, prompt):
    llm = OpenAI(temperature=0.7)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    result = qa.run(prompt)
    return result

# Function to refine content
def refine_content(content, refinement_prompt):
    llm = OpenAI(temperature=0.5)
    refined_content = llm(f"{refinement_prompt}\n\nOriginal content:\n{content}")
    return refined_content

# Function to check brand consistency
def check_brand_consistency(content, brand_guidelines):
    llm = OpenAI(temperature=0.2)
    prompt = f"""
    Analyze the following content and check if it aligns with the brand guidelines.
    Provide feedback on consistency and suggestions for improvement.

    Content:
    {content}

    Brand Guidelines:
    {brand_guidelines}

    Feedback:
    """
    feedback = llm(prompt)
    return feedback

# Streamlit UI
st.title("Content Co-pilot for Marketing Teams")

# File upload
uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, MD, or TXT)", type=["pdf", "docx", "md", "txt"])

if uploaded_file:
    vectorstore = process_document(uploaded_file)
    
    if vectorstore:
        st.success("Document processed successfully!")

        # Content generation
        st.header("Content Generation")
        content_prompt = st.text_area("Enter a prompt for content generation:")
        if st.button("Generate Content"):
            generated_content = generate_content(vectorstore, content_prompt)
            st.subheader("Generated Content:")
            st.write(generated_content)

            # Content refinement
            st.header("Content Refinement")
            refinement_prompt = st.text_area("Enter refinement instructions:")
            if st.button("Refine Content"):
                refined_content = refine_content(generated_content, refinement_prompt)
                st.subheader("Refined Content:")
                st.write(refined_content)

            # Brand consistency check
            st.header("Brand Consistency Check")
            brand_guidelines = st.text_area("Enter your brand guidelines:")
            if st.button("Check Brand Consistency"):
                consistency_feedback = check_brand_consistency(generated_content, brand_guidelines)
                st.subheader("Brand Consistency Feedback:")
                st.write(consistency_feedback)

# Instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Upload a document (PDF, DOCX, MD, or TXT) containing relevant marketing information.
2. Enter a prompt to generate content based on the uploaded document.
3. Refine the generated content by providing specific instructions.
4. Check brand consistency by entering your brand guidelines.
""")

# About
st.sidebar.header("About")
st.sidebar.markdown("""
This Content Co-pilot app assists marketing teams in generating creative content. It uses LangChain and OpenAI to:
- Extract information from uploaded documents
- Generate content based on prompts
- Refine content with specific instructions
- Check brand consistency
""")
