# Implementation Plan: Stakeholder Relationship Monitoring App (Decision Tree CART)

## 1. Project Overview
Aplikasi ini dirancang untuk memantau dan memprediksi status hubungan kerja sama antara BPMA dan Stakeholder (KKKS) menggunakan algoritma **Decision Tree CART (Classification and Regression Trees)**. Sistem akan memberikan penilaian otomatis (Harmonis/Kurang Harmonis) berdasarkan akumulasi skor interaksi bulanan (Komunikasi, Laporan, Rapat, dan Partisipasi).

## 2. Tech Stack (MVP Version)
- **Programming Language**: Python 3.10+
- **Data Analysis**: `pandas`, `numpy`
- **Machine Learning**: `scikit-learn` (Decision Tree Classifier)
- **API Framework**: `FastAPI` (Modern, fast, and auto-documented)
- **Web Server**: `uvicorn`
- **Exporting**: `joblib` (untuk menyimpan model dan encoder)

## 3. Data Architecture
Berdasarkan dataset `data/Dataset2.csv`:

### Fitur (X):
- **Nama KKKS**: Identitas stakeholder (Opsional untuk model, atau di-encode).
- **Skor_Komunikasi**: Nilai rata-rata/akumulasi efektivitas komunikasi.
- **Skor_Laporan**: Nilai kepatuhan dan kualitas pelaporan.
- **Skor_Rapat**: Nilai kehadiran dan proaktifitas dalam rapat.
- **Skor_Partisipasi**: Nilai keterlibatan dalam program tambahan.

### Target (y):
- **Label_Akhir**: Status hubungan (**Harmonis** vs **Kurang Harmonis**).

## 4. System Workflow
1.  **Data Ingestion**: Membaca dataset CSV.
2.  **Preprocessing**: 
    - Encoding fitur kategorikal menggunakan `LabelEncoder` atau `OneHotEncoder`.
    - Pembersihan data jika terdapat missing values.
3.  **Modeling**:
    - Split data (Training 80%, Testing 20%).
    - Inisialisasi `DecisionTreeClassifier` menggunakan algoritma **CART** (dengan kriteria default Gini Impurity).
    - Pelatihan model.
4.  **Prediction Engine**: Fungsi untuk menerima input interaksi baru dan memprediksi labelnya.
5.  **User Interface**:
    - **Dashboard**: Menampilkan statistik umum (jumlah interaksi, distribusi label).
    - **Monitoring Page**: Tabel interaktif performa tiap stakeholder.
    - **Prediction Form**: Form untuk menginput data interaksi baru secara manual.
    - **Tree Visualization**: Menampilkan visualisasi pohon keputusan agar model bersifat *explainable*.

## 5. MVP Roadmap & Milestones

### Milestone 1: Data Preparation & CART Modeling
- [x] Pembersihan dan agregasi data ke format `Dataset2.csv`.
- [x] Exploratory Data Analysis (EDA) untuk melihat korelasi antar skor.
- [x] Implementasi algoritma Decision Tree CART dengan hyperparameter tuning (max_depth, min_samples_split).
- [x] Evaluasi performa menggunakan Cross-Validation dan Confusion Matrix.
- [x] Export model dan metadata ke directory `models/`.

### Milestone 2: Backend Development (FastAPI)
- [x] Refactor `main.py` untuk mendukung skema input baru (4 kategori skor).
- [x] Pembuatan endpoint `/predict` yang mengembalikan label dan probabilitas.
- [x] Pembuatan endpoint `/visualize-tree` untuk menghasilkan file gambar/SVG dari pohon keputusan.
- [x] Implementasi sistem logging untuk melacak setiap prediksi yang dilakukan.

### Milestone 3: Frontend Development (Dashboard Premium)
- [ ] Inisialisasi Project Web App (Next.js/Vite).
- [ ] Pembuatan Dashboard Overview dengan grafik distribusi status KKKS.
- [ ] Halaman "Analisis Stakeholder" dengan input form skor interaktif.
- [ ] Integrasi visualisasi Decision Tree ke interface web.

### Milestone 4: Reporting & Explainability
- [ ] Fitur export hasil analisis ke format PDF untuk laporan manajemen.
- [ ] Implementasi "Feature Importance" chart untuk menjelaskan faktor utama penentu harmoni.
- [ ] Uji coba sistem dengan data real-time baru.
- [ ] Finalisasi dokumentasi teknis dan panduan penggunaan.

### Milestone 5: Deployment & Finalization
- [ ] Deployment API ke cloud (misal: Railway/Render).
- [ ] Deployment Frontend (misal: Vercel).
- [ ] Uji beban (Load Testing) sederhana.
- [ ] Serah terima project dan finalisasi laporan SKRIPSI.

## 6. Design Aesthetics (Preview)
- **Warna Utama**: Deep Blue & Emerald Green (melambangkan stabilitas dan harmoni).
- **Typography**: Inter / Roboto.
- **Interaksi**: Hover effects pada grafik dan transisi halus antar halaman.

---
*Dibuat untuk: Project SKRIPSI - Model Pemantauan Stakeholder*
