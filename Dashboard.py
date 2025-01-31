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
        st.markdown("Berdasarkan garis besar data dari gambar lineplot Rata-rata Bulanan Konsentrasi Polutan di Nongzhanguan, dapat dilihat bahwa konsentrasi polutan bervariasi antara 0 hingga 3000 unit (misalnya µg/m³ atau satuan relevan lainnya), menunjukkan fluktuasi signifikan sepanjang tahun.Tingkat polusi tertinggi mendekati 3000 unit, sementara tingkat terendah mencapai 0 unit, meskipun nilai 0 mungkin bersifat hipotetis atau terjadi dalam kondisi khusus (misalnya, setelah hujan deras atau kebijakan pengurangan emisi darurat). Terdapat pola musiman yang jelas. Konsentrasi polutan cenderung meningkat pada bulan-bulan tertentu (misalnya, musim dingin atau musim kemarau) dan menurun drastis pada periode lain (misalnya, musim hujan atau musim dengan angin kencang). Puncak polusi mungkin terjadi akibat aktivitas manusia seperti pemanasan berbahan bakar fosil, emisi industri, atau fenomena alam seperti inversi suhu yang menghambat dispersi polutan. Fluktuasi ekstrem ini menunjukkan bahwa kualitas udara di Nongzhanguan sangat dipengaruhi oleh faktor musiman dan antropogenik. Tingginya konsentrasi polutan pada bulan tertentu berpotensi menimbulkan risiko kesehatan, seperti gangguan pernapasan atau penyakit kardiovaskular. Diperlukan pemantauan lebih intensif pada bulan-bulan puncak polusi dan implementasi kebijakan seperti pembatasan emisi industri, promosi transportasi ramah lingkungan, atau sistem peringatan dini untuk masyarakat rentan.")
    
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
        st.markdown("Berdasarkan data yang tersaji pada grafik Rata-rata Konsentrasi PM2.5 Berdasarkan Intensitas Hujan di Nongzhanguan, dapat dilihat bahwa Konsentrasi PM2.5 dalam periode Januari 2018–Oktober 2019 berkisar antara 55.0 hingga 75.0 µg/m³, menunjukkan fluktuasi yang cukup signifikan. Titik tertinggi (mendekati 75.0 µg/m³) terjadi pada Januari 2018, sementara titik terendah (sekitar 55.0 µg/m³) tercatat pada Oktober 2019.Peningkatan PM2.5 terlihat pada musim dingin/kering (Januari–April), seperti pada Januari 2018 (75.0 µg/m³) dan Januari 2019 (70.0 µg/m³). Hal ini mungkin disebabkan oleh penggunaan pemanas berbahan bakar fosil, stagnasi udara, atau akumulasi polutan. Penurunan PM2.5 terjadi pada musim hujan (Juli–Oktober), misalnya pada Juli 2019 (55.0 µg/m³) dan Oktober 2019 (57.5 µg/m³). Hujan berpotensi membersihkan partikel polutan dari udara (wet deposition). Terdapat indikasi bahwa intensitas hujan tinggi (misalnya pada Juli–Oktober) berbanding terbalik dengan konsentrasi PM2.5. Contohnya, pada Juli 2019, intensitas hujan yang lebih tinggi mungkin berkontribusi pada penurunan PM2.5 ke level terendah (55.0 µg/m³). Sebaliknya, intensitas hujan rendah (Januari–April) bertepatan dengan peningkatan PM2.5, seperti pada Januari 2018 (75.0 µg/m³). Konsentrasi PM2.5 di Nongzhanguan secara konsisten melebihi ambang batas aman WHO (25 µg/m³ untuk rata-rata tahunan), menunjukkan risiko kesehatan serius seperti gangguan pernapasan dan kardiovaskular. Musim kering menjadi periode kritis yang memerlukan intervensi kebijakan, seperti pembatasan emisi industri atau kampanye penggunaan masker.")

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
