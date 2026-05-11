# Implementation Plan: Stakeholder Relationship Monitoring App (Decision Tree)

## 1. Project Overview
Aplikasi ini dirancang untuk memantau dan memprediksi status hubungan kerja sama antara BPMA dan Stakeholder (KKKS) menggunakan algoritma **Decision Tree**. Sistem akan memberikan penilaian otomatis (Harmonis/Kurang Harmonis) berdasarkan data interaksi rutin.

## 2. Tech Stack (MVP Version)
- **Programming Language**: Python 3.10+
- **Data Analysis**: `pandas`, `numpy`
- **Machine Learning**: `scikit-learn` (Decision Tree Classifier)
- **API Framework**: `FastAPI` (Modern, fast, and auto-documented)
- **Web Server**: `uvicorn`
- **Exporting**: `joblib` (untuk menyimpan model dan encoder)

## 3. Data Architecture
Berdasarkan dataset `data/Dataset_Monitoring_BPMA_Interaksi_Lengkap.csv`:

### Fitur (X):
- **Nama KKKS**: Identitas stakeholder.
- **Jenis Interaksi**: Komunikasi, Laporan, Partisipasi, Rapat.
- **Detail Aktivitas**: Deskripsi spesifik kegiatan.
- **Keterangan**: Catatan performa (misal: "Respon sangat cepat", "Keterlambatan submit").
- **Skor**: Nilai numerik (1-3) dari interaksi tersebut.

### Target (y):
- **Label**: Status hubungan (**Harmonis** vs **Kurang Harmonis**).

## 4. System Workflow
1.  **Data Ingestion**: Membaca dataset CSV.
2.  **Preprocessing**: 
    - Encoding fitur kategorikal menggunakan `LabelEncoder` atau `OneHotEncoder`.
    - Pembersihan data jika terdapat missing values.
3.  **Modeling**:
    - Split data (Training 80%, Testing 20%).
    - Inisialisasi `DecisionTreeClassifier` dengan kriteria Gini atau Entropy.
    - Pelatihan model.
4.  **Prediction Engine**: Fungsi untuk menerima input interaksi baru dan memprediksi labelnya.
5.  **User Interface**:
    - **Dashboard**: Menampilkan statistik umum (jumlah interaksi, distribusi label).
    - **Monitoring Page**: Tabel interaktif performa tiap stakeholder.
    - **Prediction Form**: Form untuk menginput data interaksi baru secara manual.
    - **Tree Visualization**: Menampilkan visualisasi pohon keputusan agar model bersifat *explainable*.

## 5. MVP Roadmap & Milestones

### Minggu 1: Exploratory Data Analysis (EDA) & Modeling
- [ ] Implementasi script loading data dan preprocessing (Label Encoding).
- [ ] Pengembangan model Decision Tree Classifier.
- [ ] Evaluasi model (Accuracy, Confusion Matrix, Classification Report).
- [ ] Export model dan encoder ke format `.joblib`.

### Minggu 2: API Development (FastAPI)
- [ ] Setup boilerplate FastAPI dan struktur project.
- [ ] Pembuatan endpoint `/predict` (POST) untuk klasifikasi status stakeholder.
- [ ] Pembuatan endpoint `/train` (POST) untuk retraining model secara on-demand.
- [ ] Pembuatan endpoint `/stats` (GET) untuk melihat statistik model dan data.

### Minggu 3: API Security & Validation
- [ ] Implementasi request validation menggunakan Pydantic.
- [ ] Error handling untuk input data yang tidak valid.
- [ ] Dokumentasi API otomatis menggunakan Swagger UI (`/docs`).

### Minggu 4: Testing & Finalization
- [ ] Integration testing untuk alur prediksi.
- [ ] Optimalisasi performa model (Hyperparameter tuning).
- [ ] Dokumentasi lengkap instalasi dan penggunaan API.

## 6. Design Aesthetics (Preview)
- **Warna Utama**: Deep Blue & Emerald Green (melambangkan stabilitas dan harmoni).
- **Typography**: Inter / Roboto.
- **Interaksi**: Hover effects pada grafik dan transisi halus antar halaman.

---
*Dibuat untuk: Project SKRIPSI - Model Pemantauan Stakeholder*
