import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="Accounting & Taxes", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.title("AI at accounting and taxes")

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

# Depreciation and Amortization Calculations
def calculate_straight_line_depreciation(initial_value, salvage_value, useful_life):
    annual_depreciation = (initial_value - salvage_value) / useful_life
    years = range(1, useful_life + 1)
    depreciation = [annual_depreciation] * useful_life
    accumulated_depreciation = [sum(depreciation[:i]) for i in range(1, useful_life + 1)]
    book_value = [initial_value - acc_dep for acc_dep in accumulated_depreciation]
    
    return pd.DataFrame({
        'Year': years,
        'Annual Depreciation': depreciation,
        'Accumulated Depreciation': accumulated_depreciation,
        'Book Value': book_value
    })

def calculate_declining_balance_depreciation(initial_value, salvage_value, useful_life, rate):
    years = range(1, useful_life + 1)
    book_value = [initial_value]
    annual_depreciation = []
    accumulated_depreciation = []
    
    for year in years:
        dep = min(book_value[-1] * rate, book_value[-1] - salvage_value) if year != useful_life else book_value[-1] - salvage_value
        annual_depreciation.append(dep)
        accumulated_depreciation.append(sum(annual_depreciation))
        book_value.append(book_value[-1] - dep)
    
    return pd.DataFrame({
        'Year': years,
        'Annual Depreciation': annual_depreciation,
        'Accumulated Depreciation': accumulated_depreciation,
        'Book Value': book_value[:-1]
    })

def calculate_amortization(principal, interest_rate, years):
    monthly_rate = interest_rate / 12 / 100
    num_payments = years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    schedule = []
    balance = principal

    for payment in range(1, num_payments + 1):
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        schedule.append({'Payment': payment, 'Principal': principal_payment, 'Interest': interest, 'Balance': max(0, balance)})
    
    return pd.DataFrame(schedule)

# Plotting Functions
def plot_depreciation(df, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Book Value'], mode='lines+markers', name='Book Value'))
    fig.add_trace(go.Bar(x=df['Year'], y=df['Annual Depreciation'], name='Annual Depreciation'))
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Amount')
    return fig

def plot_amortization(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Payment'], y=df['Balance'], mode='lines', name='Loan Balance'))
    fig.add_trace(go.Bar(x=df['Payment'], y=df['Principal'], name='Principal'))
    fig.add_trace(go.Bar(x=df['Payment'], y=df['Interest'], name='Interest'))
    fig.update_layout(title='Amortization Schedule', xaxis_title='Payment Number', yaxis_title='Amount')
    return fig

# Main Page Functions
def straight_line_depreciation():
    st.header('Straight-Line Depreciation Calculator')
    st.markdown(
    """
    **Straight-Line Depreciation** is a common method of allocating the cost of an asset evenly over its useful life.
    This method divides the initial cost of the asset, minus any expected salvage value, by its expected useful life 
    in years. This approach provides a simple, consistent expense amount each year, helping to represent the gradual 
    decrease in the asset’s value.
    Straight-line depreciation is commonly used for assets that experience a steady rate of usage over time, making 
    it an accessible choice for accounting and financial reporting.
    
    \n
    **Formula:**
    Annual Depreciation = (Initial Cost - Salvage Value) / Useful Life
    """
    )
    initial_value = st.number_input('Initial Asset Value', min_value=0.0, value=10000.0, step=100.0)
    salvage_value = st.number_input('Salvage Value', min_value=0.0, value=1000.0, step=100.0)
    useful_life = st.number_input('Useful Life (years)', min_value=1, value=5, step=1)
    if st.button('Calculate Straight-Line Depreciation'):
        df = calculate_straight_line_depreciation(initial_value, salvage_value, useful_life)
        st.write(df)
        st.plotly_chart(plot_depreciation(df, 'Straight-Line Depreciation'))

def declining_balance_depreciation():
    st.header('Declining Balance Depreciation Calculator')
    st.markdown(
    """
    **Declining Balance Depreciation** is an accelerated method of depreciation that applies a higher depreciation rate 
    at the beginning of an asset's useful life, which gradually decreases over time. This method is often used for assets 
    that quickly lose value or become obsolete, such as technology or vehicles.
    Each year, the book value decreases, resulting in a lower depreciation expense as the asset ages. This method 
    better reflects assets whose utility diminishes more rapidly in the initial years, aligning expenses with the 
    higher productivity or usage in early periods.
    
    \n
    The **formula** is based on a fixed depreciation rate applied to the asset’s **book value** at the beginning of each period:
    Annual Depreciation = Book Value at Start of Year × Depreciation Rate
    """)
    initial_value = st.number_input('Initial Asset Value', min_value=0.0, value=10000.0, step=100.0)
    salvage_value = st.number_input('Salvage Value', min_value=0.0, value=1000.0, step=100.0)
    useful_life = st.number_input('Useful Life (years)', min_value=1, value=5, step=1)
    rate = st.number_input('Depreciation Rate (as decimal)', min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    if st.button('Calculate Declining Balance Depreciation'):
        df = calculate_declining_balance_depreciation(initial_value, salvage_value, useful_life, rate)
        st.write(df)
        st.plotly_chart(plot_depreciation(df, 'Declining Balance Depreciation'))

def amortization_calculator():
    st.header('Loan Amortization Calculator')
    st.markdown(
    """
    **Loan Amortization** is the process of gradually paying off a debt over time through regular payments. Each payment 
    includes both **principal** (the original loan amount) and **interest** (the cost of borrowing). In the early stages 
    of the loan, a larger portion of each payment goes toward interest, while later payments contribute more to reducing 
    the principal balance.
        This method ensures a predictable payment schedule, helping borrowers understand their payment structure, manage their finances effectively, and reduce 
    their outstanding balance over the loan term. Amortization schedules provide transparency and planning by breaking down each payment 
    into interest, principal, and remaining balance.
    \n
    **Formula** for calculating monthly payments:
    Monthly Payment = Principal × (Monthly Rate × (1 + Monthly Rate) ^ Number of Payments) / ((1 + Monthly Rate) ^ Number of Payments - 1)
    """)
    principal = st.number_input('Loan Principal', min_value=0.0, value=100000.0, step=1000.0)
    interest_rate = st.number_input('Annual Interest Rate (%)', min_value=0.0, max_value=100.0, value=5.0, step=0.1)
    years = st.number_input('Loan Term (years)', min_value=1, value=30, step=1)
    if st.button('Calculate Loan Amortization'):
        df = calculate_amortization(principal, interest_rate, years)
        st.write(df)
        st.plotly_chart(plot_amortization(df))

def documentation():
    st.markdown("# 📄 Documentation ")
    st.markdown("Documentation details about the cases explained for the Business units will be added here.")

# Page Navigation
page_names_to_funcs = {
    "🏡 Home": lambda: st.write("Select a page from the sidebar."),
    "Straight-Line Depreciation": straight_line_depreciation,
    "Declining Balance Depreciation": declining_balance_depreciation,
    "Amortization Calculator": amortization_calculator,
    "Documentation": documentation,
}

# Sidebar for Navigation
st.sidebar.header("AI AT ACCOUNTING AND TAXES.")
demo_name = st.sidebar.radio("Choose a use case", page_names_to_funcs.keys())
#demo_name = st.radio("Navigation", list(pages.keys()))

# Render Main Introductory Content Only on Main Page
if demo_name == "Home":
    st.markdown(
        """
        Accounting, finance, and taxation in Mexico are critical areas that demand accuracy 
        and constant scrutiny. Cost of assets over their useful lives. This provides a clearer picture of the actual value 
        and utility of an asset over time..
        
        **Explore use cases for the calculator:**
        - Straight-Line Depreciation.
        - Declining Balance Depreciation.
        - Amortization.
        - Documentation.
        """
    )
    st.write("👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

# Render Selected Page
if demo_name:
    page_names_to_funcs[demo_name]()
