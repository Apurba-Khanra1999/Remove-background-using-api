import streamlit as st
import pandas as pd
from datetime import date


today = str(date.today())
# Function to read the Excel file and extract URLs from specified column and rows
def extract_urls(file, column, start_row, end_row):
    df = pd.read_excel(file)
    urls = df.iloc[start_row - 1:end_row, column].tolist()  # Extract specified rows and column
    return urls


# Function to save URLs to a text file in the desired format
def save_to_textfile(urls, filename=f'disallow_{today}.txt'):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(f"Disallow: {url}\n")
    return filename


# Streamlit app
st.title("URL Extractor and Formatter")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Preview of the uploaded file:")
    st.write(df)

    # Input for column selection
    column = st.number_input("Column index (starting from 0)", min_value=0, max_value=len(df.columns) - 1, value=0)

    # Input for row selection
    start_row = st.number_input("Start row (starting from 1)", min_value=1, max_value=len(df), value=1)
    end_row = st.number_input("End row (inclusive)", min_value=start_row, max_value=len(df), value=len(df))

    if st.button("Generate Text File"):
        urls = extract_urls(uploaded_file, column, start_row, end_row)
        text_file = save_to_textfile(urls)
        st.success(f"Text file {text_file} generated successfully!")
        with open(text_file, 'r') as file:
            st.download_button('Download text file', file, file_name=text_file)
