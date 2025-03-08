import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import folium_static

# Load Data
@st.cache_data
def load_data():
    cust_orders_df = pd.read_csv("../cust_orders.csv")
    product_df = pd.read_csv("../product_data.csv")
    geo_df_cleaned = pd.read_csv("../geo_data_cleaned.csv")
    return cust_orders_df, product_df, geo_df_cleaned

cust_orders_df, product_df, geo_df_cleaned = load_data()

# Konversi kolom waktu ke format datetime
cust_orders_df['order_purchase_timestamp'] = pd.to_datetime(cust_orders_df['order_purchase_timestamp'])
cust_orders_df['order_month'] = cust_orders_df['order_purchase_timestamp'].dt.to_period('M')


st.sidebar.title("Dashboard E-Commerce")
st.sidebar.write("### by Zaky Al Fatih Nata Imam")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/zaky-al-fatih-nata-imam/)")
page = st.sidebar.radio("Pilih Halaman", ["📊 Data Overview", "📈 Visualisasi", "🗺️ Peta Geografis"])

# 1️⃣ Halaman Ringkasan Data
if page == "📊 Data Overview":
    st.title("📊 Ringkasan Data")

    st.subheader("📦 Data Pesanan Pelanggan")
    st.write(cust_orders_df.head())

    st.subheader("🛒 Data Produk")
    st.write(product_df.head())

    st.subheader("🌍 Data Geografis")
    st.write(geo_df_cleaned.head())

# 2️⃣ Halaman Visualisasi
elif page == "📈 Visualisasi":
    st.title("📈 Visualisasi Data")

    # Distribusi Status Pesanan
    st.subheader("📌 Distribusi Status Pesanan")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=cust_orders_df, x="order_status", 
                  order=cust_orders_df["order_status"].value_counts().index, 
                  hue="order_status", palette="viridis", legend=False)
    plt.xticks(rotation=45)
    plt.title("Distribusi Status Pesanan")
    plt.xlabel("Order Status")
    plt.ylabel("Jumlah Pesanan")
    st.pyplot(fig)

    # Tren Jumlah Pesanan per Bulan
    st.subheader("📅 Tren Jumlah Pesanan per Bulan")
    monthly_orders = cust_orders_df.groupby("order_month").size()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values)
    plt.xticks(rotation=45)
    plt.title("Tren Jumlah Pesanan per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pesanan")
    st.pyplot(fig)

    # 10 Kategori Produk Terpopuler
    st.subheader("🏆 10 Kategori Produk Terpopuler")
    product_category_counts = product_df["product_category_name_english"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=product_category_counts.values, y=product_category_counts.index, 
                palette="magma", hue=product_category_counts.index, legend=False)
    plt.title("10 Kategori Produk Terpopuler")
    plt.xlabel("Jumlah Produk")
    plt.ylabel("Kategori Produk")
    st.pyplot(fig)

    # Persebaran Lokasi Geografis Pelanggan
    st.subheader("🌎 Persebaran Lokasi Geografis Pelanggan")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(x=geo_df_cleaned['geolocation_lng'], 
                    y=geo_df_cleaned['geolocation_lat'], alpha=0.5)
    plt.title("Persebaran Lokasi Geografis Pelanggan")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    st.pyplot(fig)

# 3️⃣ Halaman Peta Geografis
elif page == "🗺️ Peta Geografis":
    st.title("🗺️ Peta Persebaran Pelanggan di Brazil")

    # Tentukan koordinat tengah Brazil
    brazil_center = [-14.2350, -51.9253]

    # Buat peta menggunakan Folium
    m = folium.Map(location=brazil_center, zoom_start=4)

    # Ambil sampel data untuk mempercepat render (misalnya, 10.000 titik)
    sample_data = geo_df_cleaned.sample(n=10000, random_state=42)

    # Tambahkan MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in sample_data.iterrows():
        folium.Marker(
            location=[row['geolocation_lat'], row['geolocation_lng']],
            popup=row['geolocation_city'],
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(marker_cluster)

    # Tambahkan Heatmap
    heat_data = list(zip(sample_data['geolocation_lat'], sample_data['geolocation_lng']))
    HeatMap(heat_data, radius=10).add_to(m)

    # Tampilkan peta
    folium_static(m)
