import streamlit as st
from openai import OpenAI

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)
    import streamlit as st
    
# Set page configuration
st.set_page_config(page_title="Industry_#004", page_icon="📊")

# Page 1: Content Co-pilot
def content_copilot():
    st.markdown("# 📄 Content Co-pilot")
    st.markdown(
        """
        The Content Co-pilot assists marketing teams in generating creative content. It helps 
        streamline the content creation process by offering suggestions, refining ideas, and 
        ensuring consistency with brand messaging.
        """
    )
    st.write("More details about Content Co-pilot will be added here.")

# Page 2: Content Localization
def content_localization():
    st.markdown("# 📄 Content Localization")
    st.markdown(
        """
        Content localization allows marketing teams to tailor content to different regions and 
        cultures, ensuring relevance and engagement across diverse markets. AI helps adapt content 
        by analyzing local preferences and language nuances.
        """
    )
    st.write("More details about Content Localization will be added here.")

# Page 3: Authenticity of the Content
def content_authenticity():
    st.markdown("# 📄 Authenticity of the Content")
    st.markdown(
        """
        Ensuring the authenticity of content is critical in today's digital world. AI tools can verify
        the originality of content and help maintain the trustworthiness of marketing materials.
        """
    )
    st.write("More details about Authenticity of the Content will be added here.")

# Page 4: Social Commitment
def social_commitment():
    st.markdown("# 📄 Social Commitment")
    st.markdown(
        """
        Social commitment refers to a brand's responsibility towards societal and environmental issues.
        AI can help monitor public sentiment and align marketing strategies with socially responsible 
        goals.
        """
    )
    st.write("More details about Social Commitment will be added here.")

# Dictionary to map page names to functions
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Content Co-pilot": content_copilot,
    "📄 Content Localization": content_localization,
    "📄 Authenticity of the Content": content_authenticity,
    "📄 Social Commitment": social_commitment,
}

# Sidebar for navigation
st.sidebar.header("Marketing Services")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())

# Render the selected page
page_names_to_funcs[demo_name]()

# Introductory content for the main page
st.markdown("# AI at Marketing")
st.write(
    """
    👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve in marketing.
    AI is revolutionizing marketing services by enhancing content creation, localization, and ensuring 
    the authenticity of brand messaging. Additionally, AI tools can help brands demonstrate their social commitment.
    """
)

st.title("Use Cases in Marketing")
st.write(" - 📄 Content Co-pilot.")
st.write(" - 📄 Content Localization.")
st.write(" - 📄 Authenticity of the Content.")
st.write(" - 📄 Social Commitment.")
st.write("👈 Select a page from the sidebar to explore AI use cases in marketing services.")
