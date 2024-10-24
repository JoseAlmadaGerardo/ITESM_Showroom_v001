import streamlit as st
import openai  # Import OpenAI API

# UCase_006(v002): Submit request PB was added

# Set global OpenAI API key
openai.api_key = "your-api-key-here"

# Set Streamlit page configuration
st.set_page_config(page_title="Industry_#003", page_icon="📊")

# Define individual pages for the finance services use cases
def redirection_forecasting_turnover():
    st.markdown("# 📄 Redirection/Forecasting Customer Turnover")
    # Example OpenAI interaction specific to this page
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="How can I forecast customer turnover using AI?"
    )
    st.write(response.choices[0].text)

def chatbots_customer_service():
    st.markdown("# 📄 Chatbots (Customer Service)")
    # Example OpenAI interaction for customer service chatbot use case
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="How can AI-powered chatbots improve customer service for finance companies?"
    )
    st.write(response.choices[0].text)

def copilot_market_scenario_planner():
    st.markdown("# 📄 Co-pilot Market Scenario Planner")
    # Example OpenAI interaction for market scenario planning
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="How can AI assist in market scenario planning for financial institutions?"
    )
    st.write(response.choices[0].text)

# Dictionary to map page names to functions
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Redirection/Forecasting Customer Turnover": redirection_forecasting_turnover,
    "📄 Chatbots (Customer Service)": chatbots_customer_service,
    "📄 Co-pilot Market Scenario Planner": copilot_market_scenario_planner,
}

# Sidebar for navigation
st.sidebar.header("Finances services")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()  # Render the selected page

# Main introductory section
st.markdown("# AI Finances Services")
st.write("👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

# Displaying the available use cases
st.title("Use Cases at Finances")
st.write(" - 📄 Redirection/Forecasting Customer Turnover.")
st.write(" - 📄 Chatbots (Customer Service).")
st.write(" - 📄 Co-pilot Market Scenario Planner.")
