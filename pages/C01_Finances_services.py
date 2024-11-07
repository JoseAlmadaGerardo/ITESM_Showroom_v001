import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="# AI at finance services",page_icon="💰", layout="wide",initial_sidebar_state="expanded")
st.title(" AI at finance services")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

# Page 1: Redirection/Forecasting Customer Turnover
def customer_turnover_forecasting():
    st.markdown("# Redirection/forecasting customer turnover")
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
    st.markdown("# Chatbots (Customer Service)")
    st.markdown(
        """
        Chatbots powered by AI can handle a variety of customer service tasks such as answering
        FAQs, resolving common issues, and providing personalized recommendations. These
        chatbots improve customer satisfaction while reducing operational costs.
        """
    )
    
    # Simple chatbot functionality
    user_input = st.text_input("Ask a question about our financial services:")
    if user_input:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial services chatbot."},
                {"role": "user", "content": user_input}
            ]
        )
        st.write("Chatbot:", response.choices[0].message.content)

# Page 3: Co-pilot Market Scenario Planner
def copilot_market_scenario_planner():
    st.markdown("# Co-pilot Market Scenario Planner")
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
    st.markdown("# Next Best Investment and Product Selection")
    st.markdown(
        """
        AI can assist in identifying the next best investment opportunities by analyzing market trends,
        customer preferences, and financial data. This can help investors make more informed decisions
        and select the right products for their portfolios.
        """
    )
    st.write("More details about next best investment and product selection will be added here.")

# Page 5: Documentation
def documentation():
    st.markdown("# Documentation ")
    st.markdown(
        """
        In this section, you will find the documentation about the cases explained for the Business units.
        """
    )
    st.write("Documentation will be added here.")

# Main app
def main():
    st.sidebar.header("AI AT FINANCE SERVICES")
    
    # Radio button for navigation
    pages = [
        "🏡  Home",
        "Churn_Forecasting",
        "Customer Service",
        "Co-pilot Market Planner",
        "Next Best Investment",
        "Documentation"
    ]
    
    page = st.sidebar.radio("Choose a use case", pages)

    if page == "🏡 Home":
        st.markdown(
            """
            Financial services are leveraging AI to improve customer experiences, streamline operations, 
            and enhance decision-making processes.
            
            **Explore Use Cases:**
            - 📄 Redirection/Forecasting Customer Turnover
            - 📄 Chatbots (Customer Service)
            - 📄 Co-pilot Market Scenario Planner
            - 📄 Next Best Investment and Product Selection
            - 📄 Documentation
            """
        )
        st.write("👈 Select a use case from the radio buttons on the left to explore examples of what AI assistance can achieve!")
    elif page == "Churn_Forecasting":
        customer_turnover_forecasting()
    elif page == "Customer Service":
        chatbots_customer_service()
    elif page == "Co-pilot Market Planner":
        copilot_market_scenario_planner()
    elif page == "Next Best Investment":
        next_best_investment()
    elif page == "Documentation":
        documentation()

if __name__ == "__main__":
    main()
