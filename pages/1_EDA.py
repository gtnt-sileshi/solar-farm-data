import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pdfplumber
from io import BytesIO
from scipy.stats import zscore

# Load the data from different file types
def load_data(uploaded_file):
    """
    Load data from an uploaded file.

    Args:
        uploaded_file (streamlit.uploaded_file_manager.UploadedFile): The uploaded file.

    Returns:
        pandas.DataFrame: The loaded data.
    """
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.pdf'):
            with pdfplumber.open(uploaded_file) as pdf:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                data = pd.read_csv(BytesIO(text.encode('utf-8')))  # Example, may need adjustments
        else:
            st.error("Unsupported file type")
            return None
        return data
    except Exception as e:
        st.error("Error loading data: " + str(e))
        return None

def display_data_preview(data):
    """
    Display the first few rows of the data.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Data Preview")
    st.write(data.head())

def display_data_types(data):
    """
    Display the data types of each column.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Data Types")
    st.write(data.dtypes)

def display_summary_statistics(data):
    """
    Display the summary statistics of the data.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Summary Statistics")
    st.write(data.describe())

def display_distribution(data, column_name):
    """
    Display the distribution of a column.

    Args:
        data (pandas.DataFrame): The data to display.
        column_name (str): The name of the column to display.
    """
    st.header(f"Distribution of {column_name}")
    if column_name in data.columns:
        fig = px.histogram(data, x=column_name)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Column '{column_name}' does not exist in the data.")
    """
    Display the sales by business unit.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Sales by Business Unit")
    if 'business_unit' in data.columns and 'Jan' in data.columns:
        business_unit_sales = data.groupby('business_unit')['Jan'].sum().reset_index()
        fig = px.bar(business_unit_sales, x='business_unit', y='Jan')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Required columns for business unit sales are missing.")
    """
    Display the monthly sales.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Monthly Sales")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if all(month in data.columns for month in months):
        monthly_sales = data[months].sum().reset_index()
        monthly_sales.columns = ['Month', 'Sales']
        fig = px.line(monthly_sales, x='Month', y='Sales')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Required columns for monthly sales are missing.")

def display_time_series(data):
    """
    Display time series analysis for selected columns.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Time Series Analysis")
    time_series_cols = ['GHI', 'DNI', 'DHI', 'Tamb']
    if 'Timestamp' in data.columns:
        for col in time_series_cols:
            if col in data.columns:
                fig = px.line(data, x='Timestamp', y=col, title=f'{col} Over Time')
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Timestamp column is missing for time series analysis.")

def display_correlation_analysis(data):
    """
    Display correlation analysis as a heatmap.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Correlation Analysis")
    correlation_cols = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS', 'WSgust']
    if all(col in data.columns for col in correlation_cols):
        corr_matrix = data[correlation_cols].corr()
        fig = plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        st.pyplot(fig)
    else:
        st.error("One or more columns for correlation analysis are missing.")

def display_wind_analysis(data):
    """
    Display wind analysis using polar plots.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Wind Analysis")
    if 'WD' in data.columns:
        fig = plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, projection='polar')
        ax.hist(data['WD'].dropna(), bins=30, density=True, alpha=0.75)
        ax.set_title('Wind Direction Distribution')
        st.pyplot(fig)
    else:
        st.error("Wind direction data (WD) is missing.")

def display_temperature_analysis(data):
    """
    Display temperature analysis scatter plot.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Temperature Analysis")
    if 'RH' in data.columns and 'Tamb' in data.columns:
        fig = plt.figure(figsize=(10, 6))
        sns.scatterplot(x='RH', y='Tamb', data=data)
        plt.title('Relative Humidity vs Temperature')
        st.pyplot(fig)
    else:
        st.error("Relative Humidity (RH) or Temperature (Tamb) data is missing.")

def display_histograms(data):
    """
    Display histograms for key variables.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Histograms")
    hist_cols = ['GHI', 'DNI', 'DHI', 'WS', 'Tamb']
    for col in hist_cols:
        if col in data.columns:
            st.write(f"### Histogram of {col}")
            fig = plt.figure(figsize=(10, 6))
            sns.histplot(data[col], bins=30)
            plt.title(f'Histogram of {col}')
            st.pyplot(fig)
        else:
            st.error(f"Column '{col}' is missing.")

def display_z_score_analysis(data):
    """
    Display Z-Score analysis to identify outliers.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Z-Score Analysis")
    z_cols = ['GHI', 'DNI', 'DHI', 'WS', 'WSgust']
    if all(col in data.columns for col in z_cols):
        df_z_scores = data[z_cols].apply(zscore)
        outliers = (df_z_scores.abs() > 3).any(axis=1)
        st.write("Rows with Z-scores > 3:")
        st.dataframe(data[outliers])
    else:
        st.error("One or more columns for Z-Score analysis are missing.")

def display_bubble_charts(data):
    """
    Display bubble charts to explore complex relationships.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.header("Bubble Charts")
    if 'GHI' in data.columns and 'Tamb' in data.columns and 'RH' in data.columns and 'WS' in data.columns:
        fig = px.scatter(data, x='GHI', y='Tamb', size='RH', color='WS', hover_name='Timestamp', title='GHI vs Tamb vs RH')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("One or more columns for bubble charts are missing.")

def eda_page(data):
    """
    Display the exploratory data analysis page.

    Args:
        data (pandas.DataFrame): The data to display.
    """
    st.title("Exploratory Data Analysis")

    display_data_preview(data)

    analysis_options = {
        "Data Types": display_data_types,
        "Summary Statistics": display_summary_statistics,
        "Distribution": display_distribution,
        "Time Series Analysis": display_time_series,
        "Correlation Analysis": display_correlation_analysis,
        "Wind Analysis": display_wind_analysis,
        "Temperature Analysis": display_temperature_analysis,
        "Histograms": display_histograms,
        "Z-Score Analysis": display_z_score_analysis,
        "Bubble Charts": display_bubble_charts
    }

    selected_analyses = st.multiselect("Select analyses to perform", list(analysis_options.keys()))

    for analysis in selected_analyses:
        if analysis == "Distribution":
            column_name = st.selectbox("Select column for distribution", data.columns)
            analysis_options[analysis](data, column_name)
        else:
            analysis_options[analysis](data)

def main():
    """
    The main function.
    """
    st.title("EDA Page")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            eda_page(data)
    else:
        st.info("Please upload a file to perform EDA")

if __name__ == "__main__":
    main()
