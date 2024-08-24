import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pdfplumber
from scipy.stats import zscore
from io import BytesIO

# Set up Streamlit page
st.set_page_config(page_title="Solar Farm Data Analysis Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")
st.title("Solar Farm Data Analysis Dashboard")

@st.cache_data
def load_data(file):
    # Determine file type and load data accordingly
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    elif file.name.endswith('.pdf'):
        # Extract text from the PDF and return as DataFrame
        with pdfplumber.open(file) as pdf:
            # Assuming the first page contains the data
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            # Convert text to DataFrame (assuming tabular format)
            # This part needs customization based on the PDF's text format
            data = pd.read_csv(BytesIO(text.encode('utf-8')))  # Example, may need adjustments
        return data
    else:
        st.error("Unsupported file type")
        st.stop()

# Sidebar for file upload
with st.sidebar:
    upload_file = st.file_uploader("Choose a file", type=["csv", "xlsx", 'pdf'])

    if upload_file is None:
        st.info("Upload file", icon="ℹ️")
        st.stop()

    df = load_data(upload_file)

# Display Data
st.subheader("Data Overview")
st.write("### First few rows of the dataframe")
st.dataframe(df.head())

st.write("### Shape of the dataframe")
st.write(df.shape)

st.write("### Data Description")
st.write(df.describe())

st.write("### Unique values in 'Comments' column")
if 'Comments' in df.columns:
    st.write(df['Comments'].unique())

st.write("### Unique values in 'Cleaning' column")
if 'Cleaning' in df.columns:
    st.write(df['Cleaning'].unique())

st.write("### Missing values in each column")
st.write(df.isnull().sum())

# Data Quality Check
st.subheader("Data Quality Check")

# Check for incorrect entries
st.write("### Incorrect Entries")
incorrect_entries = df[(df[['GHI', 'DNI', 'DHI']] < 0).any(axis=1)]
st.write("Rows with negative GHI, DNI, or DHI values:")
st.dataframe(incorrect_entries)

# Check for outliers using Z-scores
st.write("### Z-Score Analysis")
numeric_cols = ['GHI', 'DNI', 'DHI', 'WS', 'WSgust', 'Tamb']
df_z_scores = df[numeric_cols].apply(zscore)
outliers = (df_z_scores.abs() > 3).any(axis=1)
st.write("Rows with Z-scores > 3:")
st.dataframe(df[outliers])

# Data Cleaning
st.subheader("Data Cleaning")
df_cleaned = df.dropna(subset=['Comments'])
st.write("### Data after removing rows where 'Comments' is null")
st.dataframe(df_cleaned.head())

# Time Series Analysis
st.subheader("Time Series Analysis")
time_series_cols = ['GHI', 'DNI', 'DHI', 'Tamb']
for col in time_series_cols:
    if 'Timestamp' in df.columns:
        st.write(f"### {col} Over Time")
        fig = px.line(df, x='Timestamp', y=col, title=f'{col} Over Time')
        st.plotly_chart(fig, use_container_width=True)