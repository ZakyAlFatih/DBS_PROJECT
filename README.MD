# Dashboard Project

## Deskripsi

Project ini adalah dashboard berbasis Python yang menampilkan visualisasi data dari berbagai sumber CSV.

## Struktur Direktori

```
DBS_Project/
│-- .ipynb_checkpoints/
│-- Dashboard/
│   │-- app.py  # File utama untuk menjalankan dashboard
|-- Data # folder berisi data yang belum diolah
│-- cust_orders.csv
│-- geo_data_cleaned.csv
│-- product_data.csv
│-- Proyek_Analisis_Data_...
│-- requirements.txt  # File daftar dependensi
```

## Prasyarat

Pastikan Anda telah menginstal Python 3.x dan pip di sistem Anda.

## Instalasi Dependensi

Jalankan perintah berikut untuk menginstal pustaka yang dibutuhkan:

```sh
pip install -r requirements.txt
```

## Menjalankan Dashboard

Masuk ke direktori `Dashboard` dan jalankan perintah berikut:

```sh
cd Dashboard
streamlit run app.py
```

Setelah dijalankan, otomatis akan terbuka di browser :

```
atau klik link sesuai alamat yang ditampilkan di terminal.

```

## Sumber Data

Pastikan semua file CSV tersedia di root direktori proyek (`DBS_Project/`) dan berisi data yang diperlukan agar dashboard dapat berjalan dengan baik.
