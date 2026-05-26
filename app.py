import streamlit as st
import pandas as pd
from datetime import datetime
import io
import time
import random

st.set_page_config(page_title="CBT PPKn", page_icon="🎓", layout="wide")
APP_SCHOOL = "SMP Negeri 1 Banjar"
APP_AUTHOR = "Galuh Estu Putra"
APP_CONTACT = "085227384085"

soal_cbt = [
    {"id": 1, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Bhinneka Tunggal Ika artinya... [cite: 1138-1139]", "opsi": ["A. Kesatuan perbedaan", "B. Berbeda-beda tetap satu", "C. Persatuan suku", "D. Toleransi"], "jawaban": "B. Berbeda-beda tetap satu"},
    {"id": 2, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Unsur mutlak negara menurut Montevideo 1933... [cite: 93-94]", "opsi": ["A. Wilayah, rakyat, pengakuan", "B. Wilayah, rakyat, pemerintah berdaulat", "C. Pemimpin, konstitusi", "D. Konstitusi, wilayah"], "jawaban": "B. Wilayah, rakyat, pemerintah berdaulat"},
    {"id": 3, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Agama resmi di Indonesia meliputi Islam, Kristen, Katolik, Hindu, Buddha, dan...", "opsi": ["A. Sunda Wiwitan", "B. Kejawen", "C. Khonghucu", "D. Animisme"], "jawaban": "C. Khonghucu"},
    {"id": 4, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Batas laut 12 mil dari garis pangkal disebut...", "opsi": ["A. Zona Tambahan", "B. ZEE", "C. Landas Kontinen", "D. Laut Teritorial"], "jawaban": "D. Laut Teritorial"},
    {"id": 5, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Suku bangsa dengan populasi terbanyak di Indonesia adalah...", "opsi": ["A. Sunda", "B. Jawa", "C. Batak", "D. Madura"], "jawaban": "B. Jawa"},
    {"id": 6, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Pengakuan negara berdasarkan fakta disebut... [cite: 106-107]", "opsi": ["A. De facto", "B. De jure", "C. Konstitutif", "D. Deklaratif"], "jawaban": "A. De facto"},
    {"id": 7, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Sistem pertanian suku Bali adalah... [cite: 1237-1238]", "opsi": ["A. Ngaben", "B. Seren Taun", "C. Subak", "D. Ruwatan"], "jawaban": "C. Subak"},
    {"id": 8, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Tokoh pengusul negara kesatuan... [cite: 295-297]", "opsi": ["A. Sukarno", "B. Hatta", "C. Yamin", "D. Soepomo"], "jawaban": "D. Soepomo"},
    {"id": 9, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Tempat ibadah umat Buddha...", "opsi": ["A. Pura", "B. Wihara", "C. Klenteng", "D. Gereja"], "jawaban": "B. Wihara"},
    {"id": 10, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Pasal UUD 1945 tentang bentuk negara tidak diubah...", "opsi": ["A. 1 ayat 1", "B. 25 A", "C. 37 ayat 5", "D. 18"], "jawaban": "C. 37 ayat 5"}
]
## ==========================================
# INISIALISASI & HALAMAN
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
# ... (Masukkan sisa logika halaman_login_siswa, halaman_ujian, halaman_guru, dan main() dari kode terakhir saya) (Lanjutkan daftar soal 11-50 di sini dengan format yang sama)
