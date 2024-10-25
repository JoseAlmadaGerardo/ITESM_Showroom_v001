import streamlit as st
from openai import OpenAI

# Use API key from session state
if "api_key" not in st.session_state:
    st.error("API key is missing. Please configure it in the main page.")
else:
    openai_api_key = st.session_state.api_key
    client = OpenAI(api_key=openai_api_key)
    import streamlit as st
    
# Page 1: Accounting Records Tracking
def accounting_records_tracking():
    st.markdown("# 📄 Accounting Records Tracking")
    st.markdown(
        """
        Accounting records tracking is crucial for ensuring accurate financial documentation.
        Monitoring financial transactions ensures that an entity's financial statements reflect 
        its true financial position.
        """
    )
    st.write("More details about Accounting Records Tracking will be added here.")

# Page 2: Accounting Calculations (Depreciation, Amortization, etc.)
def accounting_calculations():
    st.markdown("# 📄 Accounting Calculations")
    st.markdown(
        """
        Accounting calculations such as depreciation and amortization are vital for spreading the
        cost of assets over their useful lives. This provides a clearer picture of the actual value 
        and utility of an asset over time.
        """
    )
    st.write("More details about Accounting Calculations will be added here.")

# Page 3: Data Entry to Invoice Conversion via Image
def data_entry_conversion():
    st.markdown("# 📄 Conversión de entrada de datos en facturas basadas en imágenes")
    st.markdown(
        """
        Converting input data into invoices based on images allows for automation of billing processes. 
        Using AI, scanned images can be transformed into structured data for creating invoices.
        """
    )
    st.write("More details about Data Entry to Invoice Conversion will be added here.")
# Modificacion
# Main Page Selection
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Accounting records tracking": accounting_records_tracking,
    "📄 Accounting calculations": accounting_calculations,
    "📄 Data entry conversion": data_entry_conversion,
}

# Sidebar for Navigation
st.sidebar.header("AI AT ACCOUNTING AND TAXES.")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())
st.markdown("# AI AT ACCOUNTING AND TAXES.")

# Render Main Introductory Content Only on Main Page
if demo_name == "—":
    st.markdown(
    """
    Accounting, finance, and taxation in Mexico are critical areas that demand accuracy 
    and constant scrutiny. Confirming accounting records is essential to ensure that all 
    financial transactions are properly documented and reflect the entity's economic reality. 
    Additionally, accounting calculations such as depreciation and amortization help distribute 
    asset costs over time, providing a more accurate view of their value and utility.
        
        **Explore Use Cases:**
        - 📄 Accounting records tracking.
        - 📄 Accounting calculations (depreciation, amortization, among others.
        - 📄 Converting data entry into image-based invoices.
        """
    )
    st.write("👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

# Render Selected Page
page_names_to_funcs[demo_name]()
