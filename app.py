import os
import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Streamlit page
st.set_page_config(page_title="Analisis Ekspor Indonesia", layout="wide")
st.title("Analisis Data Ekspor Indonesia dan Insight")

# File uploader
st.sidebar.header("Unggah Data Ekspor Anda")
uploaded_files = st.sidebar.file_uploader("Unggah hingga 5 file Excel atau CSV", type=["csv", "xlsx"], accept_multiple_files=True)

# GPT-4O Analysis function
def analyze_data_with_gpt4o(data):
    if data.empty:
        return "Tidak ada data untuk dianalisis. Mohon unggah file."
    
    columns = ', '.join(data.columns)
    prompt = f"Analisis dataset dengan kolom: {columns}. Berikan wawasan tentang pola, anomali, atau tren yang terkait dengan tujuan ekspor atau produk Indonesia."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Anda adalah seorang analis data yang ahli dalam data ekspor."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2048,
            temperature=1.0
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {e}"

# Visualize uploaded data
def visualize_data(data):
    st.write("### Pilih Jenis Visualisasi")
    chart_type = st.selectbox("Jenis Grafik", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot", "Heatmap", "Treemap", "Area Chart", "Sunburst Chart"])

    st.write("### Pilih Kolom untuk Visualisasi")
    x_axis = st.selectbox("Kolom X", data.columns)
    y_axis = st.selectbox("Kolom Y", data.columns)

    if chart_type == "Bar Chart":
        fig = px.bar(data, x=x_axis, y=y_axis)
    elif chart_type == "Line Chart":
        fig = px.line(data, x=x_axis, y=y_axis)
    elif chart_type == "Scatter Plot":
        fig = px.scatter(data, x=x_axis, y=y_axis)
    elif chart_type == "Pie Chart":
        fig = px.pie(data, names=x_axis, values=y_axis)
    elif chart_type == "Histogram":
        fig = px.histogram(data, x=x_axis)
    elif chart_type == "Box Plot":
        fig = px.box(data, x=x_axis, y=y_axis)
    elif chart_type == "Heatmap":
        fig = px.imshow(data.corr())
    elif chart_type == "Treemap":
        fig = px.treemap(data, path=[x_axis], values=y_axis)
    elif chart_type == "Area Chart":
        fig = px.area(data, x=x_axis, y=y_axis)
    elif chart_type == "Sunburst Chart":
        fig = px.sunburst(data, path=[x_axis], values=y_axis)

    st.plotly_chart(fig)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Load the data
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            st.write(f"### Data dari {uploaded_file.name}")
            st.dataframe(data)

            # Visualization menu
            visualize_data(data)

            # AI Analysis Options
            st.write("### Pelindo AI Data Analysis")
            analysis_type = st.radio("Pilih jenis analisis:", ["Analisis Berdasarkan Data", "Pencarian Global Pelindo AI"])
            analysis_query = st.text_area("Deskripsi analisis atau detail pencarian:")
            if st.button("Generate Pelindo AI") and analysis_query:
                try:
                    if analysis_type == "Analisis Berdasarkan Data":
                        prompt = (
                            f"Berdasarkan dataset berikut, lakukan analisis mendalam tentang '{analysis_query}'.Gunakan bahasa Indonesia.Fokuskan analisis pada tren ekspor dan peluang untuk Indonesia:\n"
                            + data.to_csv(index=False)
                        )
                    else:
                        prompt = (
                            f"Cari informasi lengkap tentang '{analysis_query}' yang relevan dengan data ekspor Indonesia. Tambahkan referensi sumber terpercaya."
                        )

                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        max_completion_tokens= 2048,
                        messages=[{"role": "system", "content": "Anda adalah analis data berpengalaman. Gunakan bahasa Indonesia"},
                                  {"role": "user", "content": prompt}]
                    )
                    result = response['choices'][0]['message']['content']
                    st.write("#### Hasil Analisis AI:")
                    st.write(result)

                except Exception as e:
                    st.error(f"Error generating analysis: {e}")

        except Exception as e:
            st.error(f"Error saat memuat file {uploaded_file.name}: {e}")




