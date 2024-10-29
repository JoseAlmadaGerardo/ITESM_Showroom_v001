import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from openai import OpenAI

# Load the API key from secrets
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets["openai"]["api_key"]
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)

# Accounting Calculations (Depreciation, Amortization, etc.)
def accounting_calculations():
    calculation_type = st.sidebar.selectbox(
        'Select Calculation Type',
        ('Straight-Line Depreciation', 'Declining Balance Depreciation', 'Loan Amortization')
    )

    if calculation_type == 'Straight-Line Depreciation':
        st.header('Straight-Line Depreciation Calculator')
        initial_value = st.number_input('Initial Asset Value', min_value=0.0, value=10000.0, step=100.0)
        salvage_value = st.number_input('Salvage Value', min_value=0.0, value=1000.0, step=100.0)
        useful_life = st.number_input('Useful Life (years)', min_value=1, value=5, step=1)

        if st.button('Calculate Straight-Line Depreciation'):
            df = calculate_straight_line_depreciation(initial_value, salvage_value, useful_life)
            st.write(df)
            st.plotly_chart(plot_depreciation(df, 'Straight-Line Depreciation'))

    elif calculation_type == 'Declining Balance Depreciation':
        st.header('Declining Balance Depreciation Calculator')
        initial_value = st.number_input('Initial Asset Value', min_value=0.0, value=10000.0, step=100.0)
        salvage_value = st.number_input('Salvage Value', min_value=0.0, value=1000.0, step=100.0)
        useful_life = st.number_input('Useful Life (years)', min_value=1, value=5, step=1)
        rate = st.number_input('Depreciation Rate (as decimal)', min_value=0.0, max_value=1.0, value=0.2, step=0.05)

        if st.button('Calculate Declining Balance Depreciation'):
            df = calculate_declining_balance_depreciation(initial_value, salvage_value, useful_life, rate)
            st.write(df)
            st.plotly_chart(plot_depreciation(df, 'Declining Balance Depreciation'))

    elif calculation_type == 'Loan Amortization':
        st.header('Loan Amortization Calculator')
        principal = st.number_input('Loan Principal', min_value=0.0, value=100000.0, step=1000.0)
        interest_rate = st.number_input('Annual Interest Rate (%)', min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        years = st.number_input('Loan Term (years)', min_value=1, value=30, step=1)

        if st.button('Calculate Loan Amortization'):
            df = calculate_amortization(principal, interest_rate, years)
            st.write(df)
            st.plotly_chart(plot_amortization(df))

def calculate_straight_line_depreciation(initial_value, salvage_value, useful_life):
    # Define depreciation calculations
    # ...

def calculate_declining_balance_depreciation(initial_value, salvage_value, useful_life, rate):
    # Define declining balance calculations
    # ...

def calculate_amortization(principal, interest_rate, years):
    # Define amortization calculations
    # ...

def plot_depreciation(df, title):
    # Plotting depreciation
    # ...

def plot_amortization(df):
    # Plotting amortization
    # ...

# Page 3: Data Entry to Invoice Conversion
def data_entry_conversion():
    st.markdown("# 📄 Conversión de entrada de datos en facturas basadas en imágenes")
    st.write("More details about Data Entry to Invoice Conversion will be added here.")

# Page 4: Documentation
def documentation():
    st.markdown("# 📄 Documentation ")
    st.write("Documentation will be added here.")

# Main Page Selection
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Accounting Calculations": accounting_calculations,
    "📄 Data Entry to Invoice Conversion": data_entry_conversion,
    "📄 Documentation": documentation,
}

# Sidebar for Navigation
st.sidebar.header("AI in Accounting and Taxes")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())

# Render Main Introductory Content Only on Main Page
if demo_name == "—":
    st.markdown(
        """
        Welcome to the AI in Accounting and Taxes app. Select a feature to explore from the sidebar.
        """
    )

# Render Selected Page
page_names_to_funcs[demo_name]()
