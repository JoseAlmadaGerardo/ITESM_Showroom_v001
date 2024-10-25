import streamlit as st
from openai import OpenAI

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

# Set page configuration
st.set_page_config(page_title="Industry_#003", page_icon="📊")

# Page 1: Redirection/Forecasting Customer Turnover
def customer_turnover_forecasting():
    st.markdown("# 📄 Redirection/Forecasting Customer Turnover")
    st.markdown(
        """
        Redirection and forecasting of customer turnover helps finance companies anticipate
        customer behavior and take proactive steps to retain customers and minimize churn.
        AI-based solutions can help forecast customer trends based on historical data.
        """
    )
    st.write("More details about customer turnover forecasting will be added here.")

# Page 2: Chatbots for Customer Service
def chatbots_customer_service():
    st.markdown("# 📄 Chatbots (Customer Service)")
    st.markdown(
        """
        Chatbots powered by AI can handle a variety of customer service tasks such as answering
        FAQs, resolving common issues, and providing personalized recommendations. These
        chatbots improve customer satisfaction while reducing operational costs.
        """
    )
    st.write("More details about chatbots for customer service will be added here.")

# Page 3: Co-pilot Market Scenario Planner
def copilot_market_scenario_planner():
    st.markdown("# 📄 Co-pilot Market Scenario Planner")
    st.markdown(
        """
        A co-pilot market scenario planner helps finance professionals explore different market
        conditions and predict possible outcomes. AI can simulate different market scenarios to
        support decision-making and risk assessment.
        """
    )
    st.write("More details about the co-pilot market scenario planner will be added here.")

# Page 4: Next Best Investment and Product Selection
def next_best_investment():
    st.markdown("# 📄 Next Best Investment and Product Selection")
    st.markdown(
        """
        AI can assist in identifying the next best investment opportunities by analyzing market trends,
        customer preferences, and financial data. This can help investors make more informed decisions
        and select the right products for their portfolios.
        """
    )
    st.write("More details about next best investment and product selection will be added here.")

# Main Page Selection
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Redirection/Forecasting Customer Turnover": customer_turnover_forecasting,
    "📄 Chatbots (Customer Service)": chatbots_customer_service,
    "📄 Co-pilot Market Scenario Planner": copilot_market_scenario_planner,
    "📄 Next Best Investment and Product Selection": next_best_investment,
}

# Sidebar for Navigation
st.sidebar.header("AI AT FINANCE SERVICES")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())
st.markdown("# AI AT FINANCE SERVICES")

# Render Main Introductory Content Only on Main Page
if demo_name == "—":
    st.markdown(
        """
        Financial services are leveraging AI to improve customer experiences, streamline operations, 
        and enhance decision-making processes.
        
        **Explore Use Cases:**
        - 📄 Redirection/Forecasting Customer Turnover.
        - 📄 Chatbots (Customer Service).
        - 📄 Co-pilot Market Scenario Planner.
        - 📄 Next Best Investment and Product Selection.
        """
    )
    st.write("👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

# Render Selected Page
page_names_to_funcs[demo_name]()
