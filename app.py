import streamlit as st
import pandas as pd
from datetime import datetime
import io
import time
import random

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="CBT PPKn - Media Pembelajaran", page_icon="🎓", layout="wide")

APP_AUTHOR = "Galuh Estu Putra"
APP_SCHOOL = "SMP Negeri 1 Banjar"
APP_CONTACT = "085227384085"

# ==========================================
# DATABASE SOAL (Dibagi per 10 untuk keamanan)
# ==========================================
soal_cbt = [
    {"id": 1, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Bhinneka Tunggal Ika artinya... [cite: 1138-1139]", "opsi": ["A. Kesatuan perbedaan", "B. Berbeda-beda tetap satu", "C. Persatuan suku", "D. Toleransi"], "jawaban": "B. Berbeda-beda tetap satu"},
    {"id": 2, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Unsur mutlak negara menurut Montevideo 1933 adalah... [cite: 93-94]", "opsi": ["A. Wilayah, rakyat, pengakuan", "B. Wilayah, rakyat, pemerintah berdaulat", "C. Pemimpin, konstitusi", "D. Konstitusi, wilayah"], "jawaban": "B. Wilayah, rakyat, pemerintah berdaulat"},
    {"id": 3, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Agama resmi di Indonesia meliputi Islam, Kristen, Katolik, Hindu, Buddha, dan...", "opsi": ["A. Sunda Wiwitan", "B. Kejawen", "C. Khonghucu", "D. Animisme"], "jawaban": "C. Khonghucu"},
    {"id": 4, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Batas laut 12 mil laut dari garis pangkal disebut...", "opsi": ["A. Zona Tambahan", "B. ZEE", "C. Landas Kontinen", "D. Laut Teritorial"], "jawaban": "D. Laut Teritorial"},
    {"id": 5, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Suku bangsa dengan populasi terbanyak di Indonesia adalah...", "opsi": ["A. Sunda", "B. Jawa", "C. Batak", "D. Madura"], "jawaban": "B. Jawa"},
    {"id": 6, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Pengakuan negara berdasarkan fakta disebut... [cite: 106-107]", "opsi": ["A. De facto", "B. De jure", "C. Konstitutif", "D. Deklaratif"], "jawaban": "A. De facto"},
    {"id": 7, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Sistem pertanian suku Bali yang menjaga keseimbangan alam adalah... [cite: 1237-1238]", "opsi": ["A. Ngaben", "B. Seren Taun", "C. Subak", "D. Ruwatan"], "jawaban": "C. Subak"},
    {"id": 8, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Tokoh sidang BPUPK pengusul negara kesatuan adalah... [cite: 295-297]", "opsi": ["A. Sukarno", "B. Hatta", "C. Yamin", "D. Soepomo"], "jawaban": "D. Soepomo"},
    {"id": 9, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Tempat ibadah umat Buddha di Indonesia adalah...", "opsi": ["A. Pura", "B. Wihara", "C. Klenteng", "D. Gereja"], "jawaban": "B. Wihara"},
    {"id": 10, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Pasal UUD 1945 tentang bentuk negara kesatuan yang tidak bisa diubah adalah...", "opsi": ["A. 1 ayat 1", "B. 25 A", "C. 37 ayat 5", "D. 18"], "jawaban": "C. 37 ayat 5"},
    
    # (Soal 11-50 ditambahkan dengan struktur yang sama agar tidak error)
    {"id": 11, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Ras Melanesoid di Indonesia banyak tinggal di...", "opsi": ["A. Jawa", "B. Kalimantan", "C. Papua & Maluku", "D. Sumatra"], "jawaban": "C. Papua & Maluku"},
    {"id": 12, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Batas selatan Indonesia berbatasan dengan negara...", "opsi": ["A. Filipina", "B. Australia", "C. Malaysia", "D. Papua Nugini"], "jawaban": "B. Australia"},
    {"id": 13, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Nilai budaya rumah adat Baduy adalah... [cite: 1211-1212]", "opsi": ["A. Mewah", "B. Menyatu alam", "C. Benteng", "D. Modern"], "jawaban": "B. Menyatu alam"},
    {"id": 14, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Sistem pemerintah pusat mengendalikan semua urusan daerah disebut...", "opsi": ["A. Desentralisasi", "B. Serikat", "C. Sentralisasi", "D. Monarki"], "jawaban": "C. Sentralisasi"},
    {"id": 15, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Ras Asiatic Mongoloid berasal dari... [cite: 1330-1331]", "opsi": ["A. India", "B. Tionghoa/Jepang/Korea", "C. Eropa", "D. Afrika"], "jawaban": "B. Tionghoa/Jepang/Korea"},
    {"id": 16, "level": "L1", "kategori": "Bab 5", "pertanyaan": "ZEE Indonesia sejauh...", "opsi": ["A. 12 mil", "B. 24 mil", "C. 200 mil", "D. 350 mil"], "jawaban": "C. 200 mil"},
    {"id": 17, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Makanan khas Sumatra Barat adalah...", "opsi": ["A. Rendang", "B. Colenak", "C. Rawon", "D. Ayam Betutu"], "jawaban": "A. Rendang"},
    {"id": 18, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Bentuk serikat RIS 1949 adalah hasil dari...", "opsi": ["A. Linggarjati", "B. BPUPK", "C. KMB", "D. Dekrit"], "jawaban": "C. KMB"},
    {"id": 19, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Sikap merasa budaya sendiri paling baik disebut...", "opsi": ["A. Sukuisme", "B. Etnosentrisme", "C. Fanatisme", "D. Ekstremisme"], "jawaban": "B. Etnosentrisme"},
    {"id": 20, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Batas ruang udara kedaulatan Indonesia adalah...", "opsi": ["A. 12 km", "B. 24 km", "C. 110 km", "D. 200 km"], "jawaban": "C. 110 km"},
    {"id": 21, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Jabatan pimpinan-staf termasuk penggolongan... [cite: 1382-1383]", "opsi": ["A. Horizontal", "B. Setara", "C. Vertikal", "D. Otonom"], "jawaban": "C. Vertikal"},
    {"id": 22, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Sikap egois menutup diri disebut...", "opsi": ["A. Sukuisme", "B. Individualisme", "C. Nasionalisme", "D. Patriotisme"], "jawaban": "B. Individualisme"},
    {"id": 23, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Pakaian 'Ulee Balang' berasal dari...", "opsi": ["A. Sumut", "B. Jabar", "C. Aceh", "D. Bali"], "jawaban": "C. Aceh"},
    {"id": 24, "level": "L1", "kategori": "Bab 5", "pertanyaan": "Papua berbatasan darat langsung dengan...", "opsi": ["A. Australia", "B. Filipina", "C. Papua Nugini", "D. Timor Leste"], "jawaban": "C. Papua Nugini"},
    {"id": 25, "level": "L1", "kategori": "Bab 4", "pertanyaan": "Agama dengan kitab Weda adalah...", "opsi": ["A. Buddha", "B. Hindu", "C. Khonghucu", "D. Katolik"], "jawaban": "B. Hindu"},
    {"id": 26, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Gotong royong beda suku adalah perwujudan... [cite: 1135-1143]", "opsi": ["A. Asimilasi", "B. Persatuan suku", "C. Primordialisme", "D. Etnosentrisme"], "jawaban": "B. Persatuan suku"},
    {"id": 27, "level": "L2", "kategori": "Bab 5", "pertanyaan": "Kapal asing mencari ikan 150 mil dari pantai melanggar...", "opsi": ["A. Laut Teritorial", "B. Pedalaman", "C. ZEE", "D. Kontinen"], "jawaban": "C. ZEE"},
    {"id": 28, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Saling menghargai Idulfitri & Natal adalah... [cite: 1297-1301]", "opsi": ["A. Toleransi", "B. Sinkretisme", "C. Memudar", "D. Kompromi"], "jawaban": "A. Toleransi"},
    {"id": 29, "level": "L2", "kategori": "Bab 5", "pertanyaan": "Pemerintah daerah mengatur urusan sendiri disebut...", "opsi": ["A. Sentralisasi", "B. Desentralisasi", "C. Federal", "D. Otoriter"], "jawaban": "B. Desentralisasi"},
    {"id": 30, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Letak strategis Indonesia membuat pengaruh asing... [cite: 1153-1158]", "opsi": ["A. Terisolasi", "B. Seragam", "C. Mudah masuk", "D. Terhenti"], "jawaban": "C. Mudah masuk"},
    {"id": 31, "level": "L2", "kategori": "Bab 5", "pertanyaan": "Membuang sampah pada tempatnya mencerminkan... [cite: 414-415]", "opsi": ["A. Rela berkorban", "B. Cinta tanah air", "C. Etnosentrisme", "D. Apatis"], "jawaban": "B. Cinta tanah air"},
    {"id": 32, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Kondisi alam memicu keberagaman... [cite: 1172-1174]", "opsi": ["A. Agama", "B. Mata pencaharian", "C. Konstitusi", "D. Politik"], "jawaban": "B. Mata pencaharian"},
    {"id": 33, "level": "L2", "kategori": "Bab 5", "pertanyaan": "RIS dibubarkan karena... [cite: 353-354]", "opsi": ["A. Desakan PBB", "B. Belanda dukung RIS", "C. Keinginan rakyat", "D. RIS tidak ada parlemen"], "jawaban": "C. Keinginan rakyat"},
    {"id": 34, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Tugas kelompok siswa beda suku harus... [cite: 1388-1389]", "opsi": ["A. Sendiri", "B. Kerja sama", "C. Hindari", "D. Memilih"], "jawaban": "B. Kerja sama"},
    {"id": 35, "level": "L2", "kategori": "Bab 5", "pertanyaan": "Nasionalisme berlebihan merendahkan negara lain disebut...", "opsi": ["A. Luas", "B. Chauvinisme", "C. Patriotisme", "D. Individualisme"], "jawaban": "B. Chauvinisme"},
    {"id": 36, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Respons remaja terhadap digitalisasi adalah... [cite: 1457-1473]", "opsi": ["A. Menolak", "B. Belajar positif", "C. Pasrah", "D. Ikut tren"], "jawaban": "B. Belajar positif"},
    {"id": 37, "level": "L2", "kategori": "Bab 5", "pertanyaan": "Konstitusi utama pemerintah daerah adalah...", "opsi": ["A. UUD 1945", "B. TAP MPR", "C. Peraturan Pemerintah", "D. Konstitusi RIS"], "jawaban": "A. UUD 1945"},
    {"id": 38, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Tujuan perbedaan profesi adalah... [cite: 1386-1390]", "opsi": ["A. Kasta", "B. Persaingan", "C. Saling melengkapi", "D. Memisah"], "jawaban": "C. Saling melengkapi"},
    {"id": 39, "level": "L2", "kategori": "Bab 5", "pertanyaan": "Tindakan saat teman mengajak diskriminasi...", "opsi": ["A. Ikut", "B. Menolak tegas", "C. Diam", "D. Berkelahi"], "jawaban": "B. Menolak tegas"},
    {"id": 40, "level": "L2", "kategori": "Bab 4", "pertanyaan": "Manfaat transportasi antar pulau... [cite: 1175-1178]", "opsi": ["A. Sepi", "B. Pertukaran mudah", "C. Punah", "D. Bahasa hilang"], "jawaban": "B. Pertukaran mudah"},
    {"id": 41, "level": "L3", "kategori": "Bab 5", "pertanyaan": "Alasan filosofis negara kesatuan... [cite: 313-316]", "opsi": ["A. Boros", "B. Persatuan majemuk", "C. SDM siap", "D. Sulit rumusnya"], "jawaban": "B. Persatuan majemuk"},
    {"id": 42, "level": "L3", "kategori": "Bab 4", "pertanyaan": "Akibat akulturasi buta budaya global... [cite: 1182-1192]", "opsi": ["A. Kesadaran naik", "B. Harmonis", "C. Lunturnya budaya", "D. Pariwisata naik"], "jawaban": "C. Lunturnya budaya"},
    {"id": 43, "level": "L3", "kategori": "Bab 5", "pertanyaan": "Akibat negara merdeka tanpa de jure... [cite: 93-94, 104-107]", "opsi": ["A. Batal berdiri", "B. Pemilu ulang", "C. Sulit kerja sama", "D. Diambil tetangga"], "jawaban": "C. Sulit kerja sama"},
    {"id": 44, "level": "L3", "kategori": "Bab 4", "pertanyaan": "Solusi kesenjangan ekonomi... [cite: 1150-1151]", "opsi": ["A. Otoriter", "B. Hindari interaksi", "C. Toleransi/gotong royong", "D. Paksa bagi harta"], "jawaban": "C. Toleransi/gotong royong"},
    {"id": 45, "level": "L3", "kategori": "Bab 5", "pertanyaan": "Peran siswa lawan diskriminasi... [cite: 442-444]", "opsi": ["A. Lapor guru", "B. Berteman lintas suku", "C. Menjauh", "D. Kritik medsos"], "jawaban": "B. Berteman lintas suku"},
    {"id": 46, "level": "L3", "kategori": "Bab 4", "pertanyaan": "Respons guru lawan digitalisasi... [cite: 1461-1474]", "opsi": ["A. Menolak", "B. Manual", "C. Adaptasi", "D. Kosong"], "jawaban": "C. Adaptasi"},
    {"id": 47, "level": "L3", "kategori": "Bab 5", "pertanyaan": "Penemuan tambang di perairan milik...", "opsi": ["A. Penemu", "B. Pemprov", "C. NKRI", "D. Swasta"], "jawaban": "C. NKRI"},
    {"id": 48, "level": "L3", "kategori": "Bab 4", "pertanyaan": "Mengapa penyeragaman gagal di Indonesia? [cite: 1133-1136]", "opsi": ["A. Investasi", "B. Fitrah/Inovasi", "C. Biaya", "D. PBB"], "jawaban": "B. Fitrah/Inovasi"},
    {"id": 49, "level": "L3", "kategori": "Bab 5", "pertanyaan": "Implikasi Hankam ZEE adalah...", "opsi": ["A. Kendali asing", "B. Patroli masif", "C. Batas darat hilang", "D. Nelayan dilarang"], "jawaban": "B. Patroli masif"},
    {"id": 50, "level": "L3", "kategori": "Bab 4", "pertanyaan": "Pelajaran sejarah Indische Partij...", "opsi": ["A. Kasta efisien", "B. Kasta dijaga", "C. Diskriminasi memicu konflik", "D. Kolonial adil"], "jawaban": "C. Diskriminasi memicu konflik"}
]

# (Sisa logika aplikasi tetap sama...)
# ...
