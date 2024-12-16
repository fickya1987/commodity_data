import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
from streamlit_searchbox import Searchbox
import plotly.express as px

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Streamlit page
st.set_page_config(page_title="Analisis Ekspor Indonesia", layout="wide")
st.title("Analisis Data Ekspor Indonesia dan Insight")

# File uploader
st.sidebar.header("Unggah Data Ekspor Anda")
uploaded_file = st.sidebar.file_uploader("Unggah file Excel atau CSV", type=["csv", "xlsx"])

# GPT-4O Search and Analysis function
def analyze_data_with_gpt4o(data):
    if data.empty:
        return "Tidak ada data untuk dianalisis. Mohon unggah file."
    
    columns = ', '.join(data.columns)
    prompt = f"Analisis dataset dengan kolom: {columns}. Berikan wawasan tentang pola, anomali, atau tren yang terkait dengan tujuan ekspor atau produk Indonesia."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Anda adalah seorang analis data yang ahli dalam data ekspor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=1.0
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {e}"

# Visualize uploaded data
if uploaded_file is not None:
    try:
        # Load the data
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.write("### Data yang Diunggah")
        st.dataframe(data)

        # Interactive visualization
        st.write("### Grafik Interaktif")
        column_to_plot = st.selectbox("Pilih kolom untuk visualisasi", options=data.columns)
        if column_to_plot:
            fig = px.histogram(data, x=column_to_plot, title=f"Distribusi {column_to_plot}")
            st.plotly_chart(fig)

        # GPT-4O analysis
        st.write("### Analisis GPT-4O")
        analysis = analyze_data_with_gpt4o(data)
        st.write(analysis)
    except Exception as e:
        st.error(f"Error saat memuat file: {e}")

# GPT-4O Search feature
st.sidebar.header("Pencarian Data dengan GPT-4O")
search_query = st.sidebar.text_input("Masukkan pertanyaan pencarian Anda")
if search_query:
    try:
        search_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Anda adalah asisten pencarian data ekspor yang membantu."},
                {"role": "user", "content": search_query}
            ],
            max_tokens=2048,
            temperature=1.0
        )
        st.sidebar.write(search_response.choices[0].message['content'])
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

