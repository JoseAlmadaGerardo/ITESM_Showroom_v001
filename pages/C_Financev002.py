import streamlit as st
import openai  # Import OpenAI API

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)
    import streamlit as st
    
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

# Dictionary to map page names to functions
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Redirection/Forecasting Customer Turnover": customer_turnover_forecasting,
    "📄 Chatbots (Customer Service)": chatbots_customer_service,
    "📄 Co-pilot Market Scenario Planner": copilot_market_scenario_planner,
    "📄 Next Best Investment and Product Selection": next_best_investment,
}

# Sidebar for navigation
st.sidebar.header("Finance Services")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())

# Render the selected page
page_names_to_funcs[demo_name]()

# Introductory content for the main page
st.markdown("# AI in Financial Services")
st.write(
    """
    👈 Select a use case from the dropdown on the left to explore how AI can enhance financial services.
    Financial services are leveraging AI to improve customer experiences, streamline operations, 
    and enhance decision-making processes.
    """
)

st.title("Use Cases in Finance Services")
st.write(" - 📄 Redirection/Forecasting Customer Turnover.")
st.write(" - 📄 Chatbots (Customer Service).")
st.write(" - 📄 Co-pilot Market Scenario Planner.")
st.write(" - 📄 Next Best Investment and Product Selection.")
st.write("👈 Select a page from the sidebar to explore AI use cases in finance services.")

