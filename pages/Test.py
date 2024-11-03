import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import io  # Added import for io.StringIO()
from io import BytesIO
import requests

# Streamlit app
st.set_page_config(page_title="Accounting Data Autom", page_icon="📊", layout="")

def convertir_fecha(fecha_str):
    meses_es_en = {
        'enero': 'January', 'febrero': 'February', 'marzo': 'March',
        'abril': 'April', 'mayo': 'May', 'junio': 'June',
        'julio': 'July', 'agosto': 'August', 'septiembre': 'September',
        'octubre': 'October', 'noviembre': 'November', 'diciembre': 'December'
    }
    fecha_str = fecha_str.replace(' hs.', '')
    for mes_es, mes_en in meses_es_en.items():
        if mes_es in fecha_str:
            fecha_str = fecha_str.replace(mes_es, mes_en)
            break
    fecha_obj = datetime.strptime(fecha_str, "%d de %B de %Y %H:%M")
    return fecha_obj.strftime("%d/%m/%Y")

def process_data(df):
    # Remove specified columns
    columns_to_remove = [0, 2, 3, 4, 10, 12, 13, 14, 19, 20, 21, 25, 26, 27, 28, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40]
    df = df.drop(df.columns[columns_to_remove], axis=1)
    
    # Convert date
    df['1 Fecha de Venta'] = df['Fecha de Venta'].apply(convertir_fecha)
    
    # Fill NaN values
    df = df.fillna(0)
    
    return df

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return model, X_test, y_test, y_pred
def Component():
    st.title("Accounting Data Automation")

    # Google Sheets CSV export URL
    #sheet_id = "1za4GhpjjmdqW2dkx0qLiAtVarzEgPkYy"
    #gid = "1937746016"
    #csv_url = f"https://docs.google.com/spreadsheets/d/10Xc91vr4t5uLtwkdYZgDHNqlBWv0LJvR/edit?usp=sharing&ouid=117917482215490954026&rtpof=true&sd=true"
    #import requests

excel_url = f"https://docs.google.com/spreadsheets/d/1za4GhpjjmdqW2dkx0qLiAtVarzEgPkYy/edit?usp=sharing&ouid=102032149093714214712&rtpof=true&sd=true"
response = requests.get(excel_url)
if response.status_code == 200:
    with open('temp.xlsx', 'wb') as f:
        f.write(response.content)
    df = pd.read_excel('temp.xlsx')
else:
    st.error("Failed to retrieve data from Google Sheets.")

response = requests.get(excel_url)
if response.status_code == 200:
    df = pd.read_excel(BytesIO(response.content))
else:
    st.error("Failed to retrieve data from Google Sheets.")

    try:
        # Read the Google Sheet data into a DataFrame
        df = pd.read_csv(excel_url)

        st.write("Original Data:")
        st.write(df.head())

        processed_df = process_data(df)
        st.write("Processed Data:")
        st.write(processed_df.head())

        st.write("Data Info:")
        buffer = io.StringIO()
        processed_df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        # Simple visualization
        st.write("Total Sales by Date:")
        fig, ax = plt.subplots()
        processed_df.groupby('Fecha de Venta')['Total (MXN)'].sum().plot(ax=ax)
        st.pyplot(fig)

        # Model training and evaluation
        X = processed_df.drop(['Fecha de Venta', 'Total (MXN)'], axis=1)
        y = (processed_df['Total (MXN)'] > processed_df['Total (MXN)'].mean()).astype(int)
        model, X_test, y_test, y_pred = train_model(X, y)

        st.write("Model Evaluation:")
        st.text(classification_report(y_test, y_pred))

        st.write("Confusion Matrix:")
        fig, ax = plt.subplots()
        sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', ax=ax)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred while reading the Google Sheet: {e}")

Component()
