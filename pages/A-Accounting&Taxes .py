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

# Main Page Selection
page_names_to_funcs = {
    "—": lambda: st.write("Select a page from the sidebar."),
    "📄 Accounting Records Tracking": accounting_records_tracking,
    "📄 Accounting Calculations": accounting_calculations,
    "📄 Conversión de entrada de datos en facturas basadas en imágenes": data_entry_conversion,
}

# Sidebar for Navigation
st.sidebar.header("AI Applications in Accounting and Taxes")
demo_name = st.sidebar.selectbox("Choose a use case", page_names_to_funcs.keys())

# Render Selected Page
page_names_to_funcs[demo_name]()

# General Progress Bar and Placeholder (can be reused across pages)
st.write("👈 Select a page from the sidebar to explore AI use cases in Accounting.")
