# Page 1: Fanuc Robot Assistant
def fanuc_robot_assistant():
    st.header("🤖 Fanuc Robot Assistant")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("👋 I'm Lucas_7, your Fanuc Robot Assistant!")
        st.warning("Note: This AI assistant is still in development mode.")
    with col2:
        st.metric("Tokens Used", st.session_state.fanuc_total_tokens)

    # RAG File Management
    with st.expander("Manage RAG Files"):
        file_management_section("fanuc")

    alarm_code = st.text_area(
        "Describe the Robot Alarm Code:",
        placeholder="Enter the alarm code (e.g., SRVO-023) or a description of the issue...",
        height=100
    )

    if st.button("Submit", key="fanuc_submit"):
        if alarm_code:
            question = f"Provide a detailed explanation and troubleshooting steps for: {alarm_code}"
            with st.spinner("Generating response..."):
                response, tokens = get_ai_response(question)
                if response:
                    st.markdown(response)
                    st.session_state.fanuc_chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "question": alarm_code,
                        "answer": response
                    })
                    st.session_state.fanuc_total_tokens += tokens

    if st.session_state.fanuc_chat_history:
        with st.expander("View Chat History"):
            for chat in reversed(st.session_state.fanuc_chat_history):
                timestamp = chat.get("timestamp", "No timestamp available")
                st.markdown(f"**Time:** {timestamp}")
                st.markdown(f"**Q:** {chat['question']}")
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")

# Page 2: Electronic Components Assistant
def electronic_components_assistant():
    st.header("🔌 Electronic Components Assistant")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("Configure and optimize electronic components with AI assistance.")
    with col2:
        st.metric("Tokens Used", st.session_state.components_total_tokens)

    # RAG File Management
    with st.expander("Manage RAG Files"):
        file_management_section("components")

    component_type = st.selectbox(
        "Select Component Type:",
        ["PLC", "HMI", "Servo Drive", "Sensor", "Other"]
    )
    
    query = st.text_area(
        "Describe your configuration question:",
        placeholder="E.g., How to set up communication between components?",
        height=100
    )
    
    if st.button("Get Assistance"):
        if query:
            prompt = f"Help with {component_type} configuration: {query}"
            with st.spinner("Generating response..."):
                response, tokens = get_ai_response(prompt)
                if response:
                    st.markdown(response)
                    st.session_state.components_chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "component": component_type,
                        "question": query,
                        "answer": response
                    })
                    st.session_state.components_total_tokens += tokens

    if st.session_state.components_chat_history:
        with st.expander("View Chat History"):
            for chat in reversed(st.session_state.components_chat_history):
                timestamp = chat.get("timestamp", "No timestamp available")
                st.markdown(f"**Time:** {timestamp}")
                st.markdown(f"**Component:** {chat['component']}")
                st.markdown(f"**Q:** {chat['question']}")
                st.markdown(f"**A:** {chat['answer']}")
                st.markdown("---")
