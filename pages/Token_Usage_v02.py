import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Token Usage Dashboard", layout="wide")

# Function to load data
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.tsv'):
            df = pd.read_csv(file, sep='\t')
        elif file.name.endswith('.json'):
            df = pd.read_json(file)
        else:
            st.error("Unsupported file format. Please upload a CSV, TSV, or JSON file.")
            return None
        
        # Handle different date formats
        date_columns = ['date', 'created_at', 'timestamp']  # Possible date column names
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors='coerce')
                    df = df.rename(columns={col: 'date'})
                    break
                except:
                    continue
        
        if 'date' not in df.columns:
            st.error("Could not find a valid date column. Please ensure your file contains a column with dates.")
            return None
        
        # Ensure other required columns exist
        required_columns = ['total_tokens', 'total_cost', 'model', 'endpoint', 'user_id']
        for col in required_columns:
            if col not in df.columns:
                df[col] = 'Unknown'  # Add placeholder column if missing
        
        # Convert total_tokens and total_cost to numeric, replacing non-numeric values with 0
        df['total_tokens'] = pd.to_numeric(df['total_tokens'], errors='coerce').fillna(0)
        df['total_cost'] = pd.to_numeric(df['total_cost'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"An error occurred while loading the file: {str(e)}")
        return None

# Main app
def main():
    st.title("Token Usage Dashboard")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'tsv', 'json'])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.success("Data loaded successfully!")

            # Display raw data
            if st.checkbox("Show raw data"):
                st.write(df)

            # Sidebar for date range selection
            st.sidebar.header("Date Range")
            min_date = df['date'].min().date()
            max_date = df['date'].max().date()
            start_date = st.sidebar.date_input("Start date", min_date)
            end_date = st.sidebar.date_input("End date", max_date)

            # Filter data based on date range
            mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
            df_filtered = df.loc[mask]

            # Token & Cost Tracking
            st.header("Token & Cost Tracking")
            col1, col2 = st.columns(2)

            with col1:
                fig_tokens = px.area(df_filtered, x='date', y='total_tokens', title='Total Token Usage Over Time')
                st.plotly_chart(fig_tokens, use_container_width=True)

            with col2:
                fig_cost = px.line(df_filtered, x='date', y='total_cost', title='Total Cost Over Time')
                st.plotly_chart(fig_cost, use_container_width=True)

            # Model & Endpoint Analysis
            st.header("Model & Endpoint Analysis")
            col3, col4 = st.columns(2)

            with col3:
                model_usage = df_filtered.groupby('model')['total_tokens'].sum().reset_index()
                fig_model = px.pie(model_usage, values='total_tokens', names='model', title='Token Usage by Model')
                st.plotly_chart(fig_model, use_container_width=True)

            with col4:
                endpoint_usage = df_filtered.groupby('endpoint')['total_tokens'].sum().reset_index()
                fig_endpoint = px.bar(endpoint_usage, x='endpoint', y='total_tokens', title='Token Usage by Endpoint')
                st.plotly_chart(fig_endpoint, use_container_width=True)

            # User Segmentation
            st.header("User Segmentation")
            top_n = st.slider("Select number of top users to display", min_value=5, max_value=20, value=10)
            user_usage = df_filtered.groupby('user_id')['total_tokens'].sum().nlargest(top_n).reset_index()
            fig_users = px.bar(user_usage, x='user_id', y='total_tokens', title=f'Top {top_n} Users by Token Usage')
            st.plotly_chart(fig_users, use_container_width=True)

            # User details table
            st.subheader("User Details")
            selected_user = st.selectbox("Select a user to view details", options=user_usage['user_id'])
            user_data = df_filtered[df_filtered['user_id'] == selected_user]
            st.write(user_data)

    else:
        st.info("Please upload a CSV, TSV, or JSON file to begin.")

if __name__ == "__main__":
    main()
