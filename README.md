# Sistem Pakar Identifikasi Gaya Belajar Siswa
### Metode Forward Chaining — Implementasi Berbasis Python & Streamlit

> **Project Akhir Mata Kuliah Sistem Berbasis Pengetahuan / Sistem Pakar**  
> Pengembang: **Devi Andini Sastro**

---

## Deskripsi Proyek

Aplikasi ini merupakan implementasi ulang sistem pakar penentuan gaya belajar siswa menggunakan **Python** dan **Streamlit**, diadaptasi dari penelitian berikut:

> Aditasari, L. P., Novita, M., & Waliyansyah, R. R. (2020). *Sistem Pakar Penentuan Gaya Belajar Siswa Dengan Metode Forward Chaining Berbasis Web.* IT Journal Research and Development (ITJRD), Vol. 5, No. 1, hlm. 32–44. DOI: [10.25299/itjrd.2020.vol5(1).4740](https://doi.org/10.25299/itjrd.2020.vol5(1).4740)

Sistem asli pada jurnal dikembangkan berbasis web menggunakan PHP dan MySQL. Implementasi ini dibuat sebagai versi pembelajaran menggunakan Python dan Streamlit, dengan basis aturan dan kode fakta yang diadaptasi langsung dari tabel pada jurnal acuan.

Aplikasi mengidentifikasi **7 gaya belajar** berdasarkan **33 ciri perilaku belajar** (kode fakta C45–C79, dikecualikan C69) yang dikelompokkan ke dalam 4 kategori pertanyaan, menggunakan mesin inferensi Forward Chaining berbasis rule IF-THEN.

---

## Gaya Belajar yang Diidentifikasi

| No. | Gaya Belajar   | Kode Rule | Jumlah Fakta |
|-----|----------------|-----------|--------------|
| 1   | Visual         | R1        | 6 fakta      |
| 2   | Auditori       | R2        | 5 fakta      |
| 3   | Kinestetik     | R3        | 5 fakta      |
| 4   | Verbal         | R4        | 5 fakta      |
| 5   | Logis          | R5        | 4 fakta      |
| 6   | Interpersonal  | R6        | 5 fakta      |
| 7   | Intrapersonal  | R7        | 3 fakta      |

---

## Fitur Aplikasi

### 1. Beranda
Menampilkan penjelasan singkat aplikasi, ringkasan 7 gaya belajar dalam grid card, dan tombol langsung menuju tes.

### 2. Tes Gaya Belajar
Form interaktif berbasis langkah (*step-by-step*) yang dibagi dalam **4 tahap**:

| Langkah | Kategori                          |
|---------|-----------------------------------|
| 1       | Identitas siswa + Cara Menerima Informasi |
| 2       | Cara Belajar                      |
| 3       | Kebiasaan Sosial                  |
| 4       | Kecenderungan Berpikir            |

- Validasi wajib: nama lengkap harus diisi sebelum lanjut.
- Validasi akhir: minimal 1 ciri harus dipilih sebelum melihat hasil.
- Pilihan pengguna dipertahankan saat berpindah langkah (tidak hilang saat kembali).

### 3. Hasil & Rekomendasi
- Menampilkan **gaya belajar dominan** beserta persentase kecocokan terhadap rule.
- Jika dua atau lebih gaya memiliki skor tertinggi yang sama, sistem menampilkan status **campuran**.
- Progress bar horizontal perbandingan kecocokan seluruh 7 gaya belajar.
- **5 rekomendasi cara belajar** yang spesifik sesuai gaya dominan.
- Daftar semua ciri yang dipilih pengguna selama tes (expandable).
- Tombol **Download Laporan PDF** — laporan terstruktur berisi identitas, hasil, rekomendasi, dan disclaimer.
- Tombol **Ulangi Tes** untuk mereset seluruh sesi.

### 4. Tentang Aplikasi
- Penjelasan fungsi dan batasan aplikasi.
- Referensi lengkap jurnal acuan.
- Informasi akademik sistem: basis pengetahuan (tabel fakta) dan aturan inferensi IF-THEN (expandable, tanpa opsi download).
- Informasi pengembang.

---

## Mesin Inferensi: Forward Chaining

Sistem menggunakan **Forward Chaining** — inferensi dimulai dari fakta yang diberikan pengguna (data-driven) menuju kesimpulan gaya belajar.

**Alur kalkulasi (fungsi `hitung_hasil`):**

```
Untuk setiap rule R (R1–R7):
    cocok  = [k untuk k dalam fakta_rule[R] jika k ada di pilihan_pengguna]
    skor   = len(cocok) / len(fakta_rule[R]) × 100%

Gaya dominan = argmax(skor)
Jika terdapat lebih dari satu gaya dengan skor yang sama → status "campuran"
```

Sistem **tidak menggunakan ambang batas minimum** — gaya dengan persentase tertinggi selalu ditampilkan sebagai hasil, sesuai dengan logika pada jurnal acuan.

---

## Persyaratan & Instalasi

**Python 3.8 ke atas** wajib tersedia di sistem.

### Dependensi

| Pustaka     | Kegunaan                                      |
|-------------|-----------------------------------------------|
| `streamlit` | Framework antarmuka web interaktif            |
| `pandas`    | Manipulasi data tabel basis pengetahuan       |
| `fpdf2`     | Pembuatan laporan hasil dalam format PDF      |

### Langkah Instalasi

```bash
# 1. Clone atau unduh repository ini
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# 2. (Opsional) Buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Instal dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada: `http://localhost:8501`

---

## Struktur Proyek

```
streamlit_sistem_pakar/
│
├── app.py                  # Seluruh logika aplikasi (satu file)
│   ├── Konfigurasi halaman & CSS kustom
│   ├── Kamus fakta asli (fakta_asli) & tampilan (fakta_tampil)
│   ├── Kamus aturan rule base (aturan) — R1 s.d. R7
│   ├── Kamus rekomendasi belajar per gaya
│   ├── Mesin inferensi Forward Chaining (hitung_hasil)
│   ├── Generator laporan PDF (buat_pdf)
│   └── Routing halaman: Beranda, Tes, Hasil, Tentang
│
├── .streamlit/
│   └── config.toml         # Konfigurasi tema Streamlit (light mode)
│
├── requirements.txt        # Dependensi: streamlit, pandas, fpdf2
└── README.md               # Dokumentasi ini
```

> **Catatan arsitektur:** Seluruh aplikasi ditulis dalam satu file `app.py` (~1.590 baris) tanpa modul eksternal tambahan, sesuai pendekatan sederhana untuk keperluan pembelajaran.

---

## Batasan & Disclaimer

- Hasil identifikasi merupakan **kecenderungan awal** berdasarkan ciri yang dipilih pengguna, **bukan diagnosis psikologis klinis**.
- Basis pengetahuan diadaptasi dari penelitian pada siswa SD. Penggunaan pada jenjang pendidikan lain merupakan perluasan implementasi di luar validasi asal jurnal.
- Skor kecocokan dihitung secara proporsional terhadap jumlah fakta dalam setiap rule — semakin banyak ciri yang cocok, semakin tinggi persentase.
- Sistem tidak mempertimbangkan bobot atau prioritas antar fakta.

---

## Referensi

Aditasari, L. P., Novita, M., & Waliyansyah, R. R. (2020). Sistem Pakar Penentuan Gaya Belajar Siswa Dengan Metode Forward Chaining Berbasis Web. *IT Journal Research and Development*, 5(1), 32–44. https://doi.org/10.25299/itjrd.2020.vol5(1).4740
