import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat dan menggabungkan dataset
@st.cache_data  # Mengganti st.cache dengan st.cache_data
def load_data():
    # Memuat dataset Aotizhongxin, Changping, Dingling
    df_all = pd.read_csv("https://raw.githubusercontent.com/satya-permadi/dicoding_airquality-project/refs/heads/main/AirQuality_Dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
    # Tambahkan kolom 'date_time'
    df_all['date_time'] = pd.to_datetime(df_all[['year', 'month', 'day', 'hour']])
    return df_all

# Panggil fungsi untuk memuat data
df_all = load_data()

# Sidebar untuk navigasi
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Analisis:", ["Home", "Pertanyaan 1", "Pertanyaan 2"])

# Home Section
if menu == "Home":
    st.title("Pengaruh Polutan terhadap Kualitas Udara di Nongzhanguan")
    st.markdown("""
Pengaruh Polutan terhadap Kualitas Udara di Nongzhanguan\n
Nama: Komang Satya Permadi\n
Email: satyaintershuty@gmail.com\n
ID Dicoding: satyapermadi
    """)

elif menu == "Pertanyaan 1":
    st.title("Bagaimana pengaruh konsentrasi NO2 dan CO sebagai polutan yang dihasilkan kendaraan bermotor terhadap kualitas udara di Nongzhanguan?")
    # Cek apakah dataset berhasil dimuat
    if df_all.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Konsentrasi CO dan NO2 Selama Beberapa Tahun (Rata-rata Bulanan)")
    
        df_all['date_time_month'] = df_all['date_time'].dt.to_period('M')

        monthly_avg = df_all.groupby('date_time_month').agg({
            'CO': 'mean', 
            'NO2': 'mean',
            'PM2.5': 'mean',
            'PM10': 'mean',
            'SO2': 'mean',
            'O3': 'mean'
        }).reset_index()

        monthly_avg['date_time_month'] = monthly_avg['date_time_month'].dt.to_timestamp()

        fig, ax = plt.subplots(figsize=(14, 8))

        sns.lineplot(x='date_time_month', y='CO', data=monthly_avg, label='CO', color='blue', ax=ax)
        sns.lineplot(x='date_time_month', y='NO2', data=monthly_avg, label='NO2', color='red', ax=ax)
        sns.lineplot(x='date_time_month', y='PM2.5', data=monthly_avg, label='PM2.5', color='green', ax=ax)
        sns.lineplot(x='date_time_month', y='PM10', data=monthly_avg, label='PM10', color='purple', ax=ax)
        sns.lineplot(x='date_time_month', y='SO2', data=monthly_avg, label='SO2', color='orange', ax=ax)
        sns.lineplot(x='date_time_month', y='O3', data=monthly_avg, label='O3', color='cyan', ax=ax)

        ax.set_title('Konsentrasi CO dan NO2 Selama Beberapa Tahun (Rata-rata Bulanan)')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Konsentrasi Polutan')

        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(fig)
 
elif menu == "Pertanyaan 2":
    st.title("Bagaimana pengaruh hujan terhadap polutan penyebab polusi udara di nongzhanguan?")

    # Cek apakah dataset berhasil dimuat
    if df_all.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Bagaimana pengaruh hujan terhadap polutan penyebab polusi udara?")

        df_all['RAIN_GROUP'] = pd.cut(df_all['RAIN'], bins=[0, 1, 4, 8, 10], labels=['Tidak Ada Hujan', 'Hujan Ringan', 'Hujan Sedang', 'Hujan Lebat'])

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.boxplot(x='RAIN_GROUP', y='PM2.5', data=df_all, ax=ax)
        ax.set_title('Visualisasi Data dengan Box Plot antara PM2.5 dengan Intensitas Hujan di Nongzhanguan')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        rain_group_avg = df_all.groupby('RAIN_GROUP')['PM2.5'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x='RAIN_GROUP', y='PM2.5', data=rain_group_avg, marker='o', color='blue', ax=ax)

        ax.set_title('Rata-rata Konsentrasi PM2.5 Berdasarkan Intensitas Hujan')
        ax.set_xlabel('Kelompok Intensitas Hujan')
        ax.set_ylabel('Rata-rata Konsentrasi PM2.5')

        st.pyplot(fig)

        st.subheader("Kesimpulan")
        st.markdown("""
        Dari analisis di atas, dapat disimpulkan bahwa:
        
        1. **Peningkatan konsentrasi CO dan NO₂** Tingkat karbon monoksida (CO) dan nitrogen dioksida (NO₂) yang meningkat di Nongzhanguan mengindikasikan adanya aktivitas kendaraan bermotor atau pembakaran bahan bakar fosil yang intensif. Hal ini menegaskan bahwa kedua sumber tersebut merupakan kontributor utama polutan udara di wilayah tersebut.

        2. **Hujan dengan Peningkatan PM2.5** data penelitian di Nongzhanguan membuktikan bahwa hujan berperan menurunkan kadar polutan, salah satunya PM2.5. Fenomena ini terjadi karena air hujan membawa serta polutan, sehingga distribusi PM2.5 mengalami penurunan drastis. Hujan berpotensi membersihkan partikel polutan dari udara (wet deposition). Intensitas hujan yang lebih tinggi berkontribusi pada penurunan PM2.5 ke level terendah. Sebaliknya, intensitas hujan rendah dapat meningkatkan intensitas PM2.5 di Nongzhanguan.
        """)
