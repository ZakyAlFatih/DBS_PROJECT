import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import folium_static

# Load Data dengan Caching
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

# Sidebar untuk Navigasi
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

# 2️⃣ Halaman Visualisasi dengan Filter Interaktif
elif page == "📈 Visualisasi":
    st.title("📈 Visualisasi Data")

    # 🔹 Filter Interaktif: Rentang Tanggal
    st.sidebar.subheader("📅 Filter Tanggal")
    min_date = cust_orders_df['order_purchase_timestamp'].min()
    max_date = cust_orders_df['order_purchase_timestamp'].max()
    start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date])

    # Filter Data berdasarkan Tanggal
    filtered_orders = cust_orders_df[
        (cust_orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
        (cust_orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))
    ]

    # 🔹 Distribusi Status Pesanan
    st.subheader("📌 Distribusi Status Pesanan")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(data=filtered_orders, x="order_status", 
                  order=filtered_orders["order_status"].value_counts().index, 
                  hue="order_status", palette="viridis", legend=False)
    plt.xticks(rotation=45)
    plt.title("Distribusi Status Pesanan")
    plt.xlabel("Order Status")
    plt.ylabel("Jumlah Pesanan")
    st.pyplot(fig)

    # 🔹 Tren Jumlah Pesanan per Bulan
    st.subheader("📅 Tren Jumlah Pesanan per Bulan")
    monthly_orders = filtered_orders.groupby("order_month").size()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(x=monthly_orders.index.astype(str), y=monthly_orders.values)
    plt.xticks(rotation=45)
    plt.title("Tren Jumlah Pesanan per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pesanan")
    st.pyplot(fig)

    # 🔹 Filter Interaktif: Pilih Kategori Produk
    st.sidebar.subheader("📌 Filter Kategori Produk")
    all_categories = product_df["product_category_name_english"].unique().tolist()
    selected_category = st.sidebar.selectbox("Pilih Kategori Produk", ["Semua"] + all_categories)

    # Filter Produk berdasarkan Kategori
    if selected_category != "Semua":
        filtered_product_df = product_df[product_df["product_category_name_english"] == selected_category]
    else:
        filtered_product_df = product_df

    # 🔹 10 Kategori Produk dengan Variasi Terbanyak
    st.subheader("🏆 10 Produk dengan Variasi Terbanyak")
    product_category_counts = filtered_product_df["product_category_name_english"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=product_category_counts.values, y=product_category_counts.index, 
                palette="magma", hue=product_category_counts.index, legend=False)
    plt.title("10 Produk dengan Variasi Terbanyak")
    plt.xlabel("Jumlah Produk")
    plt.ylabel("Kategori Produk")
    st.pyplot(fig)

# 3️⃣ Halaman Peta Geografis dengan Filter Berdasarkan State
elif page == "🗺️ Peta Geografis":
    st.title("🗺️ Peta Persebaran Pelanggan di Brazil")

    # 🔹 Filter Interaktif: Pilih State
    st.sidebar.subheader("📍 Filter Lokasi")
    all_states = geo_df_cleaned["geolocation_state"].unique().tolist()
    selected_state = st.sidebar.selectbox("Pilih State", ["Semua"] + all_states)

    # Filter Data Geografis berdasarkan State
    if selected_state != "Semua":
        filtered_geo_df = geo_df_cleaned[geo_df_cleaned["geolocation_state"] == selected_state]
    else:
        filtered_geo_df = geo_df_cleaned

    # Tentukan koordinat tengah Brazil
    brazil_center = [-14.2350, -51.9253]

    # Buat peta menggunakan Folium
    m = folium.Map(location=brazil_center, zoom_start=4)

    # Ambil sampel data untuk mempercepat render (misalnya, 10.000 titik)
    sample_data = filtered_geo_df.sample(n=min(10000, len(filtered_geo_df)), random_state=42)

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
