# Import library yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import seaborn as sns


# Load data
df_customers = pd.read_csv("customers_dataset.csv")
df_geolocation = pd.read_csv("geolocation_dataset.csv")
df_order_items = pd.read_csv("order_items_dataset.csv")
df_order_payment = pd.read_csv("order_payments_dataset.csv")
df_reviews = pd.read_csv("order_reviews_dataset.csv")
df_orders = pd.read_csv("orders_dataset.csv")
df_product_category_name = pd.read_csv("product_category_name_translation.csv")
df_products = pd.read_csv("products_dataset.csv")
df_sellers = pd.read_csv("sellers_dataset.csv")


def AnalisisPertanyaan1():
    rating = list(df_reviews["review_score"])
    rekap_rating = {}
    for data in rating:
        if data in rekap_rating:
            rekap_rating[data] += 1
        else:
            rekap_rating[data] = 1
    st.write(
        "Menghitung Rating dari order_reviews dan Jumlah Value dari masing-masing rating"
    )
    st.write(rekap_rating)

    # Rating diurutkan secara Ascending Berdasarkan Keys
    st.write("Rating diurutkan secara Ascending Berdasarkan Keys")
    rekap_rating_sorted = dict(sorted(rekap_rating.items()))
    st.write(rekap_rating_sorted)

    # Rating diurutkan secara Descending Berdasarkan value
    st.write("Rating diurutkan secara Descending Berdasarkan value")
    rating_sorted_value = dict(
        sorted(rekap_rating.items(), key=lambda x: x[1], reverse=True)
    )
    st.write(rating_sorted_value)

    rata_rata_rating = df_reviews["review_score"].mean()
    st.write("Rata-rata Rating        : ", rata_rata_rating)
    st.write("Rata-rata dibulatkan    : ", np.round(rata_rata_rating, 1))

    # Menggabungkan 2 File csv menggunakan concat
    # Cetak nama kolom pada kedua DataFrame
    st.write("Columns in df_orders:", df_orders.columns)
    st.write("Columns in df_order_reviews:", df_reviews.columns)

    merged_df = pd.merge(df_orders, df_reviews, on="order_id")
    # Menampilkan kolom 'order_status' dan 'review_score' dalam satu DataFrame
    result_df = pd.concat(
        [merged_df["order_status"], merged_df["review_score"]], axis=1
    )
    # Menampilkan hasil
    st.write(result_df)

    # Melakukan penggabungan DataFrame
    merged_df = pd.merge(df_orders, df_reviews, on="order_id")

    # Mengelompokkan berdasarkan 'order_status' dan 'review_score', kemudian menghitung jumlahnya
    result_grouped = (
        merged_df.groupby(["order_status", "review_score"])
        .size()
        .reset_index(name="jumlah_review")
    )

    # Menampilkan hasil
    st.write(result_grouped)

    # Menggunakan .loc untuk memfilter baris dengan order_status "delivered"
    delivered_data = result_grouped.loc[result_grouped["order_status"] == "delivered"]

    # Menampilkan hasil
    st.write(delivered_data)

    return rekap_rating, rekap_rating_sorted


def visualisasi1(rekap_rating_sorted, rekap_rating):
    ratings = rekap_rating_sorted
    # Diagram batang rekapitulasi rating dari order_reviews_dataset
    ratings_descending = {5: 57328, 4: 19142, 1: 11424, 3: 8179, 2: 3151}
    # Membuat DataFrame dari dictionary
    df_descending = pd.DataFrame(
        list(ratings_descending.items()), columns=["Rating", "Jumlah"]
    )

    # Mengurutkan DataFrame berdasarkan kolom 'Jumlah' secara descending
    df_descending = df_descending.sort_values(by="Jumlah", ascending=False)
    # Plotting diagram batang
    df_descending.plot(kind="bar", x="Rating", y="Jumlah", legend=False)

    # Menambahkan label di atas setiap batang diagram
    for index, value in enumerate(df_descending["Jumlah"]):
        plt.annotate(
            str(value),
            (index, value),
            ha="center",
            va="bottom",
            xytext=(0, 1),
            textcoords="offset points",
        )
    # Menambahkan judul dan label pada sumbu-sumbu & Menampilkaan diagram batang
    plt.title("Rekapitulasi Review Score secara Descending")
    plt.xticks(rotation=360)
    plt.xlabel("Review_score")
    plt.ylabel("Jumlah")
    st.pyplot()
    st.set_option("deprecation.showPyplotGlobalUse", False)
    # Plotting diagram lingkaran
    plt.pie(ratings.values(), labels=ratings.keys(), autopct="%1.1f%%", startangle=140)
    # Menambahkan label di atas setiap diagram lingkaran & Menampilkaan diagram lingkaran
    plt.axis("equal")
    plt.title("Presentase Review Score Secara Descending")
    st.pyplot()
    st.set_option("deprecation.showPyplotGlobalUse", False)
    # Menghitung rata-rata review score
    rata_rata_rating = df_reviews["review_score"].mean()
    # Menampilkan hasil dengan pembulatan ke 1 desimal
    rata_rata_rating_bulat = round(rata_rata_rating, 1)
    st.write("Rata-rata Rating dari file order_reviews             :", rata_rata_rating)
    st.write(
        "Rata-rata Rating dari file order_reviews dibulatkan  :", rata_rata_rating_bulat
    )
    return rekap_rating, rekap_rating_sorted


def AnalisisPertanyaan2(df_orders, df_reviews):
    # Menghitung durasi pengiriman
    df_orders["order_purchase_timestamp"] = pd.to_datetime(
        df_orders["order_purchase_timestamp"]
    )
    df_orders["order_delivered_customer_date"] = pd.to_datetime(
        df_orders["order_delivered_customer_date"]
    )
    df_orders["delivery_duration"] = (
        df_orders["order_delivered_customer_date"]
        - df_orders["order_purchase_timestamp"]
    ).dt.days

    # Menggabungkan DataFrame df_orders dan df_reviews
    merged_df = pd.merge(df_orders, df_reviews, on="order_id")

    # Menghitung korelasi antara durasi pengiriman dan review score
    correlation = merged_df["delivery_duration"].corr(merged_df["review_score"])

    st.write("Korelasi antara Durasi Pengiriman dan Review Score: ", correlation)


def Visualisasi2(df_orders, df_reviews):
    # Menghitung durasi pengiriman
    df_orders["order_purchase_timestamp"] = pd.to_datetime(
        df_orders["order_purchase_timestamp"]
    )
    df_orders["order_delivered_customer_date"] = pd.to_datetime(
        df_orders["order_delivered_customer_date"]
    )
    df_orders["delivery_duration"] = (
        df_orders["order_delivered_customer_date"]
        - df_orders["order_purchase_timestamp"]
    ).dt.days

    # Menggabungkan DataFrame df_orders dan df_reviews
    st.write("Gabungin DataFrame df_orders dan df_reviews")
    merged_df = pd.merge(df_orders, df_reviews, on="order_id")
    st.write(merged_df.head())

    st.write("Tampil data df_orders")
    st.write(df_orders.head())

    # Pastikan panjang kedua kolom sama
    if len(merged_df["delivery_duration"]) != len(merged_df["review_score"]):
        st.write(
            "Panjang kolom 'delivery_duration' dan 'review_score' tidak sama. Cek data Anda."
        )
        return

    # Visualisasi diagram scatterplot untuk Durasi Pengiriman dan Review Score
    plt.scatter(merged_df["delivery_duration"], merged_df["review_score"], alpha=0.5)
    plt.title("Scatterplot Durasi Pengiriman vs Review Score")
    plt.xlabel("Durasi Pengiriman (hari)")
    plt.ylabel("Review Score")
    st.pyplot()

    st.write("Hasil Kesimpulan")
    st.write(
        "1. Korelasi negatif menunjukkan bahwa terdapat hubungan kebalikan antara durasi pengiriman dan review score. Dengan kata lain, semakin lama durasi pengiriman, cenderung review score semakin rendah, dan sebaliknya."
    )
    st.write(
        "2. Nilai -0.333 menunjukkan bahwa hubungan antara kedua variabel tidak sangat kuat, tetapi masih menunjukkan kecenderungan negatif yang signifikan. Semakin mendekati -1, hubungan akan semakin kuat negatif."
    )
    st.write(
        "2. Secara praktis, ini berarti bahwa pelanggan cenderung memberikan review score yang lebih rendah jika durasi pengiriman lebih lama. Ini bisa disebabkan oleh ketidakpuasan pelanggan terhadap waktu pengiriman yang lama, yang kemudian memengaruhi pandangan mereka terhadap pengalaman pembelian."
    )


def AnalisisPertanyaan3():
    df = pd.read_csv("order_payments_dataset.csv")

    # Memuat kolom payment_type dengan nilai "credit" dan "debit"
    credit_debit_payments = df[df["payment_type"].isin(["boleto", "voucher"])]
    st.write("Tampil data credit_debit_payments")
    st.write(credit_debit_payments.head())
    return credit_debit_payments  # Return the result for later use


def Visualisasi3(credit_debit_payments):
    # Visualisasi dengan pie chart untuk persentase metode pembayaran
    st.write("Visualisasi Menggunakan Pie Chart Untuk Presentase Method Payment")
    payment_count = credit_debit_payments["payment_type"].value_counts()

    plt.pie(payment_count, labels=payment_count.index, autopct="%1.1f%%")
    plt.title("Persentase Jumlah Transaksi berdasarkan Metode Pembayaran")
    st.pyplot()

    # Visualisasi dengan histogram
    st.write("Visualisasi Menggunakan Historam")
    plt.figure(figsize=(10, 6))
    df_reviews["review_score"].plot(
        kind="hist", color="skyblue", edgecolor="black", bins=5
    )
    plt.title("Distribusi Skor Ulasan")
    plt.xlabel("Skor Ulasan")
    plt.ylabel("Jumlah Ulasan")
    st.pyplot()

    st.write("Kesimpulan")
    st.write(
        "kita bisa menyimpulkan bahwa orang-orang yang memakai jenis transaksi boleto 80% dan yang memakai jenis transaksi voucher adalah 20%"
    )


def AnalisisPertanyaan4(df_products):
    # Menghitung jumlah produk unik dalam dataset
    jumlah_produk_unik = df_products["product_id"].nunique()

    # Mendapatkan daftar produk unik
    unique_products = df_products[
        ["product_id", "product_category_name"]
    ].drop_duplicates()

    st.write(f"Jumlah produk unik dalam dataset adalah {jumlah_produk_unik}.")

    return jumlah_produk_unik, unique_products


def Visualisasi4(jumlah_produk_unik, unique_products):
    # Visualisasi dengan diagram batang
    plt.figure(figsize=(8, 6))
    sns.barplot(x=["Jumlah Produk Unik"], y=[jumlah_produk_unik], palette="viridis")
    plt.title("Jumlah Produk Unik dalam Dataset")
    plt.ylabel("Jumlah Produk")
    st.pyplot()

    # Menampilkan daftar produk unik
    st.write("Daftar Produk Unik:")
    st.table(unique_products.head(10))

    st.write("Kesimpulan")
    st.write(
        "Mengidentfikasi produk yang berbeda dan tidak ada duplikasi berdasarkan kolom atau atribut yang dianggap sebagai primary key"
    )


def AnalisisPertanyaan5(df_sellers):
    seller_counts = df_sellers["seller_city"].value_counts()
    top_cities_count = 10

    top_cities = seller_counts.head(top_cities_count)
    st.write("Top 10 kota dengan penjual terbanyak:")
    st.write(top_cities)

    return top_cities


def Visualisasi5(top_cities):
    plt.bar(top_cities.index, top_cities.values, color="red")
    plt.title(f"Top 10 Kota dengan Jumlah Penjual Terbanyak")
    plt.xlabel("Kota")
    plt.ylabel("Jumlah Penjual")
    plt.xticks(rotation=36, ha="right")
    plt.tight_layout()
    st.pyplot()

    st.write("Kesimpulan")
    st.write("10 penjual terbanyak yaitu dari kota sau paulo dengan 694 penjual")


def AnalisisPertanyaan6(customers_df):
    st.write("Nama Kolom yang Tersedia:", customers_df.columns)

    if "customer_country" in df_customers.columns:
        customer_countries = df_customers["customer_country"].to_numpy()

        unique_countries, counts = np.unique(customer_countries, return_counts=True)

        relative_frequencies = counts / len(customer_countries)

        top_countries = unique_countries[np.argsort(counts)[-5:]]
        top_country_counts = counts[np.argsort(counts)[-5:]]

        st.write("Top 5 countries:")
        for i, country in enumerate(top_countries):
            st.write(
                f"{i+1}. {country}: {top_country_counts[i]} ({relative_frequencies[i]:.2%})"
            )
    else:
        st.write("Kesalahan: Kolom 'customer_city' tidak ditemukan.")


def Visualisasi6(customers_df):
    st.write("Visualisasi Distribusi Pelanggan Berdasarkan Kode Pos dan Kota:")

    zip_code_counts = customers_df.groupby("customer_zip_code_prefix").size()
    city_zip_code_counts = (
        customers_df.groupby(["customer_zip_code_prefix", "customer_city"])
        .size()
        .reset_index(name="counts")
    )
    state_zip_code_counts = (
        customers_df.groupby(["customer_zip_code_prefix", "customer_state"])
        .size()
        .reset_index(name="counts")
    )

    # Plotting bar chart untuk distribusi pelanggan berdasarkan kode pos
    plt.figure(figsize=(12, 6))
    plt.bar(zip_code_counts.index, zip_code_counts.values)
    plt.xlabel("Zip Code Prefix")
    plt.ylabel("Number of Customers")
    plt.title("Distribution of Customers by Zip Code Prefix")
    plt.xticks(rotation=45, ha="right")
    st.pyplot()

    # Plotting stack plot untuk distribusi pelanggan berdasarkan kode pos dan kota
    plt.figure(figsize=(12, 6))
    plt.stackplot(
        city_zip_code_counts["customer_zip_code_prefix"], city_zip_code_counts["counts"]
    )
    plt.xlabel("Zip Code Prefix")
    plt.ylabel("Number of Customers")
    plt.title("Distribution of Customers by Zip Code Prefix and City")
    plt.xticks(rotation=45, ha="right")
    st.pyplot()

    # Plotting stack plot untuk distribusi pelanggan berdasarkan kode pos dan negara bagian
    plt.figure(figsize=(12, 6))
    plt.stackplot(
        state_zip_code_counts["customer_zip_code_prefix"],
        state_zip_code_counts["counts"],
    )
    plt.xlabel("Zip Code Prefix")
    plt.ylabel("Number of Customers")
    plt.title("Distribution of Customers by Zip Code Prefix and State")
    plt.xticks(rotation=45, ha="right")
    st.pyplot()

    st.write("Kesimpulan")
    st.write(
        "disimpulkan dari data pelanggan, kita mendapatkan beberapa informasi kunciyaitu Lokasi Pelangganan: distribusi pelanggan dapat dilihat dari kode pos menggunakan histogram, Sebaran Kota dan Negara Bagiang Jumlah pelanggan di berbagai kota dan negara bagian ditampilkan dalam grafik batang, Pola Distribusi: Pola distribusi pelanggan lebih lanjut dieksplorasi dengan stack plot. plot.gocios "
    )


# Main function
def main():
    st.sidebar.title("List Pertanyaan")
    selected_tab = st.sidebar.radio(
        "Pertanyaan",
        [
            "Pertanyaan 1 - 10122276 - Fikri Defi Wulanto",
            "Pertanyaan 2 - 10122279 - Syadzwana Akbar Ramadhan",
            "Pertanyaan 3 - 10122288 - Muhammad Rafli Fazrin",
            "Pertanyaan 4 - 10122291 - Gomgom Parulian Nainggolan",
            "Pertanyaan 5 - 10122296 - Muhamad Taufik Arifin",
            "Pertanyaan 6 - 10122311 - Aldi Naufal",
        ],
    )

    if selected_tab == "Pertanyaan 1 - 10122276 - Fikri Defi Wulanto":
        st.title("Analisis Review Page")
        rekap_rating, rekap_rating_sorted = AnalisisPertanyaan1()
        visualisasi1(rekap_rating_sorted, rekap_rating)
    elif selected_tab == "Pertanyaan 2 - 10122279 - Syadzwana Akbar Ramadhan":
        st.title("Analisis Durasi Pengiriman dan Review Score")
        AnalisisPertanyaan2(df_orders, df_reviews)
        Visualisasi2(df_orders, df_reviews)
    elif selected_tab == "Pertanyaan 3 - 10122288 - Muhammad Rafli Fazrin":
        st.title(
            "Mencari persenan dari metode pembayaran menggunakan boleto dan voucher"
        )
        credit_debit_payments = AnalisisPertanyaan3()
        Visualisasi3(credit_debit_payments)
    elif selected_tab == "Pertanyaan 4 - 10122291 - Gomgom Parulian Nainggolan":
        st.title("Analisis Jumlah Produk Unik dalam Dataset")
        jumlah_produk_unik, unique_products = AnalisisPertanyaan4(df_products)
        Visualisasi4(jumlah_produk_unik, unique_products)
    elif selected_tab == "Pertanyaan 5 - 10122296 - Muhamad Taufik Arifin":
        st.title("Top 10 Penjual Terbanyak")
        top_cities = AnalisisPertanyaan5(df_sellers)
        Visualisasi5(top_cities)
    elif selected_tab == "Pertanyaan 6 - 10122311 - Aldi Naufal":
        st.title(
            "Seberapa banyak pelanggan yang berasal dari setiap kode pos dan bagaimana distribusinya di berbagai kota dan negara bagian "
        )
        AnalisisPertanyaan6(df_customers)
        Visualisasi6(df_customers)


if __name__ == "__main__":
    main()
