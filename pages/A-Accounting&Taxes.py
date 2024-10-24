import streamlit as st
import time
import numpy as np

#INTRO:
st.set_page_config(page_title="Indusrty_#001",  page_icon="1")
st.markdown("# AI applications at Accounting and taxes.")
st.sidebar.header("AI APPLICATIONS AT ACCOUNTING AND TAXES.")
st.markdown(
    """
    Accounting, finance, and taxation in Mexico are critical areas that demand accuracy 
    and constant scrutiny. Confirming accounting records is essential to ensure that all 
    financial transactions are properly documented and reflect the entity's economic reality. 
    Additionally, accounting calculations such as depreciation and amortization help distribute 
    asset costs over time, providing a more accurate view of their value and utility.
    """
)

st.title("Uses case at Accounting and Taxes")
st.write(" - 📄 Accounting records tracking.")
st.write(" - 📄 Accounting calculations (depreciation, amortization, among others).")

st.write(" 👈 Select a demo from the dropdown on the left to explore examples of what AI assistance can achieve!")

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
