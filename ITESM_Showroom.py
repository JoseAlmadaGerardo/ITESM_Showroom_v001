import streamlit as st

# Set page configuration
st.set_page_config(page_title="Hello", page_icon="👋", layout="wide")
st.write("# Welcome to the Data Science Hub Showroom at Tecnológico de Monterrey! 👋🐏")
st.sidebar.success("Select a demo above.")
st.markdown(
        """
        A Streamlit app AI showroom design to research and showcases various use cases across different industrial applications !


        This app explore multiple AI use cases across different industries applications, and is an built
        on the Streamlit framework specifically designed for AI agents utilizing RAG architecture from OpenAI.

        👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!
        """
    )

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]

# Create 2 columns
col1, col2 = st.columns((1.5,1))

with col1:
    st.markdown(
        """
        ## Objectives. 🔎
        Analyze different industrial sectors to identify potential opportunities where it is feasible to develop AI-based assistants 
        using RAG architecture.
        
        AI Assistant Developer: A program has been developed capable of creating AI assistants using OpenAI's Assistant GPT-3.5 Turbo (beta). 
        For the 3.5 Turbo model, these assistants can be transformed into RAG (Retrieve-Augmented Generative) models by adding one to five documents, 
        which are converted into a vector database to enhance the model's responses on specific topics and areas. To create assistants within the 
        application, it is necessary to provide the corresponding account's API key. Additionally, the program allows displaying a gallery of available 
        AI assistants in the account and testing their functionality.
        
        AI in Accounting and Taxes: In the accounting and tax area, a depreciation and amortization calculator has been developed that can also graph 
        the calculations performed. The projection of this application is to integrate a GPT assistant to advise the user on the appropriate values to use 
        for calculating depreciations according to the type of asset. Furthermore, more functionalities and other calculations that could be integrated in 
        the future are being explored.
        
        Manufacturing 4.0: In the Manufacturing 4.0 area, an assistant has been implemented using the OpenAI Assistant GPT-3.5 Turbo (beta) API. This assistant
        is useful for tracking failures in Fanuc industrial robots. Additionally, another assistant with similar features has been developed to help plan and 
        configure automatic production lines.

        Financial Services: In the financial services area, a customer turnover forecasting feature has been developed. This tool uses machine learning models, 
        such as RandomForestClassifier, to analyze and predict the likelihood of a customer leaving. Thanks to the use of optimized functions like @st.cache_resource, 
        the prediction model is trained efficiently, and the results can help businesses make proactive decisions to retain customers. Additionally, improvements and 
        more features are being explored to further optimize financial analysis in the future.
        
        Marketing Services: In this area, use cases are explored, such as assistants that help creators generate engaging content (Content Co-Pilot), adapting material 
        to different languages and cultures (Content Localization), and verifying that brand messages are authentic and reflect their values (Content Authenticity). 
        These cases are processed through a GPT-3.5 Turbo API, complemented with a text extraction system that facilitates the RAG (Retrieval-Augmented Generation) function. 
        This combination enables generating more precise responses on specific topics, improving content quality and the consumer experience.
        
        Business Units: For this area, a document analyzer is developed that extracts key points from a text and answers questions related to its content. This tool will be 
        applied to demonstrate its use in cases such as Sales, Human Resources, IT Support, and Customer Support. By processing information effectively, the analyzer facilitates 
        decision-making and improves document management efficiency, providing precise and relevant answers to the needs of each area.
        
        These assistants will be able to incorporate personalized knowledge & integrate call functions!
        """
    )

with col2:
    st.markdown(
        """
        📝 Learn About Streamlit, Assistant API and More Demos:
        - Check out [Streamlit.io](https://streamlit.io)
        - Jump into [Streamlit documentation](https://docs.streamlit.io)
        - Ask a question in [Streamlit community](https://discuss.streamlit.io)
        - Check out [Assistant API by OpenAI](https://platform.openai.com/docs/assistants/overview)
        - Explore additional complex demos and industry use cases.
        """
    )
