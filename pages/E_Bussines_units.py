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
st.set_page_config(page_title="Industry_#005", page_icon="📊")

# Page 1: Customer Support
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
st.markdown("# AI AT BUSSINES UNITS")

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
