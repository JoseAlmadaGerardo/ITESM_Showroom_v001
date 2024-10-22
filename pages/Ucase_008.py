import streamlit as st
import openai

st.set_page_config(page_title="UCase_008", page_icon="📊")
st.markdown("# UCase_008")
st.sidebar.header("UCase_008")

# Title.
st.title("Manufacturing: Use Case #8")
st.subheader("Factory Asset Effectiveness.​")
st.write("📄 Answers to questions about .TX, .MD, and .PDF documents. Upload a document below and ask a question about it – GPT will answer!")
st.write("Note: To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys).")

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    openai.api_key = openai_api_key

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display chat history
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Input for new message
    if prompt := st.chat_input("Ask a question:"):
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Call OpenAI API for a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"]
        )

        # Extract and display assistant's response
        msg = response.choices[0].message["content"]
        st.session_state["messages"].append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
