import streamlit as st
import pandas as pd
from datetime import datetime
import io
import time
import random

# ==========================================
# KONFIGURASI HALAMAN & INFORMASI HAK CIPTA
# ==========================================
st.set_page_config(page_title="CBT PPKn - Media Pembelajaran", page_icon="🎓", layout="wide")

# DATA HAK CIPTA GURU (Sesuai Profil Kerja Bapak Galuh)
APP_AUTHOR = "Galuh Estu Putra"
APP_SCHOOL = "SMP Negeri 1 Banjar"
APP_CONTACT = "085227384085"

# ==========================================
# DATABASE SOAL PPKN (50 SOAL HOTS)
# ==========================================
soal_cbt = [
    # --- LEVEL 1: Pengetahuan & Pemahaman (25 Soal) ---
    {
        "id": 1, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Bhinneka Tunggal Ika adalah semboyan atau motto nasional Indonesia. Makna utama dari semboyan tersebut adalah...",
        "opsi": ["A. Kesatuan dalam perbedaan", "B. Berbeda-beda tetapi tetap satu jua", "C. Persatuan suku bangsa", "D. Toleransi antar umat beragama"],
        "jawaban": "B. Berbeda-beda tetapi tetap satu jua"
    },
    {
        "id": 2, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Menurut Konvensi Montevideo tahun 1933, unsur konstitutif (mutlak) berdirinya sebuah negara adalah...",
        "opsi": ["A. Wilayah, rakyat, pengakuan negara lain", "B. Wilayah, rakyat, pemerintahan yang berdaulat", "C. Pemimpin, konstitusi, pengakuan de jure", "D. Konstitusi, wilayah, pengakuan negara lain"],
        "jawaban": "B. Wilayah, rakyat, pemerintahan yang berdaulat"
    },
    {
        "id": 3, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Agama resmi yang diakui keberadaannya di Indonesia meliputi Islam, Kristen, Katolik, Hindu, Buddha, dan...",
        "opsi": ["A. Sunda Wiwitan", "B. Kejawen", "C. Khonghucu", "D. Animisme"],
        "jawaban": "C. Khonghucu"
    },
    {
        "id": 4, "level": "L1", "kategori": "Bab 5", "image": "https://via.placeholder.com/600x300.png?text=Ilustrasi+Peta+Batas+Laut+Indonesia",
        "pertanyaan": "Batas wilayah laut yang diukur mulai dari garis pangkal kepulauan Indonesia sampai dengan 12 mil laut ke arah laut lepas disebut...",
        "opsi": ["A. Zona Tambahan", "B. Zona Ekonomi Eksklusif", "C. Landas Kontinen", "D. Laut Teritorial"],
        "jawaban": "D. Laut Teritorial"
    },
    {
        "id": 5, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Berdasarkan data sensus, suku bangsa dengan populasi terbanyak di Indonesia yang penyebarannya mencapai lebih dari 40 persen adalah...",
        "opsi": ["A. Suku Sunda", "B. Suku Jawa", "C. Suku Batak", "D. Suku Madura"],
        "jawaban": "B. Suku Jawa"
    },
    {
        "id": 6, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pengakuan dari negara lain yang didasarkan pada kenyataan (fakta) bahwa sebuah negara telah memenuhi unsur mutlak disebut pengakuan...",
        "opsi": ["A. De facto", "B. De jure", "C. Konstitutif", "D. Deklaratif"],
        "jawaban": "A. De facto"
    },
    {
        "id": 7, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Salah satu bentuk kearifan lokal suku Bali dalam mengelola sistem pertanian yang menjaga keseimbangan alam adalah...",
        "opsi": ["A. Ngaben", "B. Seren Taun", "C. Subak", "D. Ruwatan"],
        "jawaban": "C. Subak"
    },
    {
        "id": 8, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pada sidang BPUPK, tokoh yang mengusulkan agar bentuk negara Indonesia adalah negara kesatuan atau 'negara integral' adalah...",
        "opsi": ["A. Ir. Sukarno", "B. Drs. Mohammad Hatta", "C. Muhammad Yamin", "D. Soepomo"],
        "jawaban": "D. Soepomo"
    },
    {
        "id": 9, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Tempat ibadah yang digunakan oleh umat Buddha di Indonesia adalah...",
        "opsi": ["A. Pura", "B. Wihara", "C. Klenteng", "D. Gereja"],
        "jawaban": "B. Wihara"
    },
    {
        "id": 10, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Bentuk Negara Kesatuan Republik Indonesia secara yuridis ditegaskan dan tidak dapat dilakukan perubahan, hal ini diatur dalam UUD NRI Tahun 1945 pasal...",
        "opsi": ["A. Pasal 1 ayat (1)", "B. Pasal 25 A", "C. Pasal 37 ayat (5)", "D. Pasal 18 ayat (1)"],
        "jawaban": "C. Pasal 37 ayat (5)"
    },
    {
        "id": 11, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Penduduk ras Melanesoid di Indonesia banyak mendiami wilayah bagian timur, di antaranya meliputi daerah...",
        "opsi": ["A. Sumatra, Jawa, dan Bali", "B. Kalimantan, Sulawesi, dan Lombok", "C. Papua, Maluku, dan Nusa Tenggara Timur", "D. Aceh, Riau, dan Jambi"],
        "jawaban": "C. Papua, Maluku, dan Nusa Tenggara Timur"
    },
    {
        "id": 12, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Wilayah selatan Indonesia berupa Laut Indonesia and Laut Arafuru secara langsung berbatasan dengan negara...",
        "opsi": ["A. Filipina", "B. Australia", "C. Malaysia", "D. Papua Nugini"],
        "jawaban": "B. Australia"
    },
    {
        "id": 13, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Rumah adat suku Baduy di Provinsi Banten yang terbuat dari bambu dan kayu mencerminkan nilai budaya mereka yaitu...",
        "opsi": ["A. Kemewahan ekonomi modern", "B. Menyatu dengan alam dan ramah lingkungan", "C. Pertahanan fisik dari serangan musuh", "D. Pengaruh dominan budaya asing"],
        "jawaban": "B. Menyatu dengan alam dan ramah lingkungan"
    },
    {
        "id": 14, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Negara kesatuan di mana semua urusan dan peraturan daerahnya dikendalikan sepenuhnya oleh pemerintah pusat dinamakan bersistem...",
        "opsi": ["A. Desentralisasi", "B. Serikat", "C. Sentralisasi", "D. Monarki"],
        "jawaban": "C. Sentralisasi"
    },
    {
        "id": 15, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Ras Asiatic Mongoloid yang berada di wilayah Indonesia umumnya berasal dari bangsa...",
        "opsi": ["A. India, Timur Tengah, dan Eropa", "B. Tionghoa, Jepang, dan Korea", "C. Eropa, Amerika, dan Australia", "D. Afrika, Arab, dan Persia"],
        "jawaban": "B. Tionghoa, Jepang, dan Korea"
    },
    {
        "id": 16, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Luas Zona Ekonomi Eksklusif (ZEE) Indonesia ditarik dari garis pangkal laut sejauh...",
        "opsi": ["A. 12 mil", "B. 24 mil", "C. 200 mil", "D. 350 mil"],
        "jawaban": "C. 200 mil"
    },
    {
        "id": 17, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Makanan khas tradisional suku Minangkabau yang sangat terkenal adalah...",
        "opsi": ["A. Rendang", "B. Colenak", "C. Rawon", "D. Ayam Betutu"],
        "jawaban": "A. Rendang"
    },
    {
        "id": 18, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Bentuk negara serikat (federal) di Indonesia pernah diterapkan pada tahun 1949 melalui Republik Indonesia Serikat (RIS) sebagai hasil dari...",
        "opsi": ["A. Perjanjian Linggarjati", "B. Sidang BPUPK", "C. Konferensi Meja Bundar (KMB)", "D. Dekrit Presiden 5 Juli 1959"],
        "jawaban": "C. Konferensi Meja Bundar (KMB)"
    },
    {
        "id": 19, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Sikap etnosentrisme merupakan ancaman bagi persatuan nasional karena sikap ini berarti...",
        "opsi": ["A. Selalu mementingkan diri sendiri secara egois", "B. Menganggap budaya bangsanya lebih baik daripada budaya bangsa lain", "C. Memaksakan perubahan dengan tindakan ekstrem", "D. Fanatik terhadap agama tertentu saja"],
        "jawaban": "B. Menganggap budaya bangsanya lebih baik daripada budaya bangsa lain"
    },
    {
        "id": 20, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Berdasarkan peraturan yang berlaku, batas ketinggian ruang udara wilayah kedaulatan Indonesia yang diukur dari permukaan daratan dan perairan adalah...",
        "opsi": ["A. 12 km", "B. 24 km", "C. 110 km", "D. 200 km"],
        "jawaban": "C. 110 km"
    },
    {
        "id": 21, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Penggolongan masyarakat berdasarkan hierarki status sosial seperti pimpinan, staf, dan karyawan disebut sebagai penggolongan yang terbentuk secara...",
        "opsi": ["A. Horizontal", "B. Setara", "C. Vertikal", "D. Otonom"],
        "jawaban": "C. Vertikal"
    },
    {
        "id": 22, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Sikap mementingkan suku sendiri secara berlebihan dan menganggapnya lebih unggul daripada suku lain dinamakan...",
        "opsi": ["A. Sukuisme", "B. Individualisme", "C. Nasionalisme", "D. Patriotisme"],
        "jawaban": "A. Sukuisme"
    },
    {
        "id": 23, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Pakaian daerah bernama 'Ulee Balang' merupakan identitas budaya dari daerah...",
        "opsi": ["A. Sumatra Utara", "B. Jawa Barat", "C. Aceh", "D. Bali"],
        "jawaban": "C. Aceh"
    },
    {
        "id": 24, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Wilayah timur Indonesia, tepatnya di Pulau Papua, berbatasan daratan secara langsung dengan negara...",
        "opsi": ["A. Australia", "B. Filipina", "C. Papua Nugini", "D. Timor Leste"],
        "jawaban": "C. Papua Nugini"
    },
    {
        "id": 25, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Agama yang menjadikan 'Weda' sebagai kitab suci utamanya adalah agama...",
        "opsi": ["A. Buddha", "B. Hindu", "C. Khonghucu", "D. Katolik"],
        "jawaban": "B. Hindu"
    },

    # --- LEVEL 2: Aplikasi (15 Soal) ---
    {
        "id": 26, "level": "L2", "kategori": "Bab 4", "image": "https://via.placeholder.com/600x300.png?text=Gotong+Royong+Beda+Suku",
        "pertanyaan": "Di sebuah kompleks perumahan, warga yang bersuku Batak, Jawa, dan Minang selalu bahu-membahu membersihkan lingkungan setiap bulan. Tindakan ini merupakan perwujudan dari...",
        "opsi":
