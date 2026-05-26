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
        "pertanyaan": "Bhinneka Tunggal Ika adalah semboyan nasional. Makna utama semboyan tersebut adalah...",
        "opsi": ["A. Kesatuan dalam perbedaan", "B. Berbeda-beda tetapi tetap satu jua", "C. Persatuan suku bangsa", "D. Toleransi antar umat beragama"],
        "jawaban": "B. Berbeda-beda tetapi tetap satu jua"
    },
    {
        "id": 2, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Menurut Konvensi Montevideo 1933, unsur konstitutif (mutlak) berdirinya negara adalah...",
        "opsi": ["A. Wilayah, rakyat, pengakuan negara lain", "B. Wilayah, rakyat, pemerintah berdaulat", "C. Pemimpin, konstitusi, pengakuan de jure", "D. Konstitusi, wilayah, pengakuan negara lain"],
        "jawaban": "B. Wilayah, rakyat, pemerintah berdaulat"
    },
    {
        "id": 3, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Agama resmi yang diakui keberadaannya di Indonesia meliputi Islam, Kristen, Katolik, Hindu, Buddha, dan...",
        "opsi": ["A. Sunda Wiwitan", "B. Kejawen", "C. Khonghucu", "D. Animisme"],
        "jawaban": "C. Khonghucu"
    },
    {
        "id": 4, "level": "L1", "kategori": "Bab 5", "image": "https://via.placeholder.com/600x300.png?text=Ilustrasi+Peta+Batas+Laut+Indonesia",
        "pertanyaan": "Batas laut yang diukur dari garis pangkal kepulauan Indonesia sampai 12 mil laut ke laut lepas disebut...",
        "opsi": ["A. Zona Tambahan", "B. Zona Ekonomi Eksklusif", "C. Landas Kontinen", "D. Laut Teritorial"],
        "jawaban": "D. Laut Teritorial"
    },
    {
        "id": 5, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Berdasarkan data sensus, suku bangsa dengan populasi terbanyak di Indonesia (mencapai lebih dari 40%) adalah...",
        "opsi": ["A. Suku Sunda", "B. Suku Jawa", "C. Suku Batak", "D. Suku Madura"],
        "jawaban": "B. Suku Jawa"
    },
    {
        "id": 6, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pengakuan dari negara lain berdasarkan fakta bahwa sebuah negara telah memenuhi unsur mutlak disebut pengakuan...",
        "opsi": ["A. De facto", "B. De jure", "C. Konstitutif", "D. Deklaratif"],
        "jawaban": "A. De facto"
    },
    {
        "id": 7, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Bentuk kearifan lokal suku Bali dalam mengelola sistem pertanian yang menjaga keseimbangan alam adalah...",
        "opsi": ["A. Ngaben", "B. Seren Taun", "C. Subak", "D. Ruwatan"],
        "jawaban": "C. Subak"
    },
    {
        "id": 8, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pada sidang BPUPK, tokoh yang mengusulkan agar bentuk negara Indonesia berbentuk negara kesatuan atau integral adalah...",
        "opsi": ["A. Ir. Sukarno", "B. Drs. Mohammad Hatta", "C. Muhammad Yamin", "D. Soepomo"],
        "jawaban": "D. Soepomo"
    },
    {
        "id": 9, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Tempat ibadah yang digunakan oleh umat Buddha di Indonesia bernama...",
        "opsi": ["A. Pura", "B. Wihara", "C. Klenteng", "D. Gereja"],
        "jawaban": "B. Wihara"
    },
    {
        "id": 10, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Penegasan yuridis bahwa bentuk Negara Kesatuan Republik Indonesia tidak dapat dilakukan perubahan diatur dalam pasal...",
        "opsi": ["A. Pasal 1 ayat (1)", "B. Pasal 25 A", "C. Pasal 37 ayat (5)", "D. Pasal 18 ayat (1)"],
        "jawaban": "C. Pasal 37 ayat (5)"
    },
    {
        "id": 11, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Penduduk ras Melanesoid di Indonesia banyak mendiami wilayah bagian timur, di antaranya meliputi daerah...",
        "opsi": ["A. Sumatra, Jawa, dan Bali", "B. Kalimantan dan Sulawesi", "C. Papua, Maluku, dan NTT", "D. Aceh, Riau, dan Jambi"],
        "jawaban": "C. Papua, Maluku, dan NTT"
    },
    {
        "id": 12, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Wilayah selatan Indonesia berupa Laut Indonesia dan Laut Arafuru secara langsung berbatasan dengan negara...",
        "opsi": ["A. Filipina", "B. Australia", "C. Malaysia", "D. Papua Nugini"],
        "jawaban": "B. Australia"
    },
    {
        "id": 13, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Rumah adat suku Baduy Banten mencerminkan nilai budaya mereka, yaitu...",
        "opsi": ["A. Kemewahan ekonomi modern", "B. Menyatu dengan alam dan ramah lingkungan", "C. Pertahanan fisik dari serangan musuh", "D. Pengaruh dominan budaya asing"],
        "jawaban": "B. Menyatu dengan alam dan ramah lingkungan"
    },
    {
        "id": 14, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Negara kesatuan di mana semua urusan daerah dikendalikan sepenuhnya oleh pemerintah pusat dinamakan...",
        "opsi": ["A. Desentralisasi", "B. Serikat", "C. Sentralisasi", "D. Monarki"],
        "jawaban": "C. Sentralisasi"
    },
    {
        "id": 15, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Ras Asiatic Mongoloid yang berada di wilayah Indonesia umumnya berasal dari keturunan...",
        "opsi": ["A. India dan Timur Tengah", "B. Tionghoa, Jepang, dan Korea", "C. Eropa dan Amerika", "D. Afrika dan Arab"],
        "jawaban": "B. Tionghoa, Jepang, dan Korea"
    },
    {
        "id": 16, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Luas batas Zona Ekonomi Eksklusif (ZEE) Indonesia ditarik dari garis pangkal laut sejauh...",
        "opsi": ["A. 12 mil", "B. 24 mil", "C. 200 mil", "D. 350 mil"],
        "jawaban": "C. 200 mil"
    },
    {
        "id": 17, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Makanan khas tradisional suku Minangkabau (Sumatra Barat) yang sangat terkenal di dunia adalah...",
        "opsi": ["A. Rendang", "B. Colenak", "C. Rawon", "D. Ayam Betutu"],
        "jawaban": "A. Rendang"
    },
    {
        "id": 18, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Bentuk negara serikat (federal) pernah diterapkan di Indonesia pada tahun 1949 melalui sistem...",
        "opsi": ["A. Perjanjian Linggarjati", "B. Sidang BPUPK", "C. Republik Indonesia Serikat (RIS)", "D. Dekrit Presiden 5 Juli 1959"],
        "jawaban": "C. Republik Indonesia Serikat (RIS)"
    },
    {
        "id": 19, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Sikap yang menganggap budaya daerahnya sendiri lebih baik daripada budaya daerah lain disebut...",
        "opsi": ["A. Sukuisme", "B. Etnosentrisme", "C. Fanatisme", "D. Ekstremisme"],
        "jawaban": "B. Etnosentrisme"
    },
    {
        "id": 20, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Batas ketinggian ruang udara kedaulatan Indonesia yang diukur dari permukaan daratan dan perairan adalah...",
        "opsi": ["A. 12 km", "B. 24 km", "C. 110 km", "D. 200 km"],
        "jawaban": "C. 110 km"
    },
    {
        "id": 21, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Penggolongan masyarakat berdasarkan tingkatan jabatan seperti direktur, staf, dan buruh bersifat...",
        "opsi": ["A. Horizontal", "B. Setara", "C. Hierarki (Vertikal)", "D. Otonom"],
        "jawaban": "C. Hierarki (Vertikal)"
    },
    {
        "id": 22, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Sikap mementingkan diri sendiri secara berlebihan and cenderung menutup diri dari lingkungan sekitar disebut...",
        "opsi": ["A. Sukuisme", "B. Individualisme", "C. Nasionalisme", "D. Patriotisme"],
        "jawaban": "B. Individualisme"
    },
    {
        "id": 23, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Pakaian daerah bernama 'Ulee Balang' merupakan identitas pakaian adat yang berasal dari daerah...",
        "opsi": ["A. Sumatra Utara", "B. Jawa Barat", "C. Aceh", "D. Bali"],
        "jawaban": "C. Aceh"
    },
    {
        "id": 24, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Wilayah timur Indonesia, tepatnya di Pulau Papua, berbatasan darat secara langsung dengan negara...",
        "opsi": ["A. Australia", "B. Filipina", "C. Papua Nugini", "D. Timor Leste"],
        "jawaban": "C. Papua Nugini"
    },
    {
        "id": 25, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Agama resmi yang menjadikan kitab 'Weda' sebagai kitab suci utamanya adalah agama...",
        "opsi": ["A. Buddha", "B. Hindu", "C. Khonghucu", "D. Katolik"],
        "jawaban": "B. Hindu"
    },

    # --- LEVEL 2: Aplikasi (15 Soal) ---
    {
        "id": 26, "level": "L2", "kategori": "Bab 4", "image": "https://via.placeholder.com/600x300.png?text=Gotong+Royong+Beda+Suku",
        "pertanyaan": "Warga perumahan yang berbeda suku bekerja bakti membersihkan lingkungan selokan bersama. Tindakan ini menerapkan...",
        "opsi": ["A. Asimilasi budaya total", "B. Persatuan keberagaman suku", "C. Primordialisme daerah", "D. Etnosentrisme warga"],
        "jawaban": "B. Persatuan keberagaman suku"
    },
    {
        "id": 27, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Kapal asing ditangkap TNI AL karena mengambil ikan pada jarak 150 mil dari pantai Indonesia. Kapal ini melanggar batas...",
        "opsi": ["A. Laut Teritorial", "B. Perairan Pedalaman", "C. Zona Ekonomi Eksklusif", "D. Landasan Kontinen"],
        "jawaban": "C. Zona Ekonomi Eksklusif"
    },
    {
        "id": 28, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Andi merayakan Idulfitri dan Budi merayakan Natal. Mereka saling mengunjungi dengan rukun. Sikap ini menerapkan...",
        "opsi": ["A. Toleransi antarumat beragama", "B. Sinkretisme perayaan hari besar", "C. Memudarnya nilai ajaran asli", "D. Kompromi prinsip keyakinan"],
        "jawaban": "A. Toleransi antarumat beragama"
    },
    {
        "id": 29, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pemerintah Kota Banjar berwenang mengatur urusan rumah tangga daerahnya secara mandiri. Hal ini membuktikan penerapan sistem...",
        "opsi": ["A. Sentralisasi pusat", "B. Desentralisasi daerah", "C. Federalisme serikat", "D. Otoriter absolut"],
        "jawaban": "B. Desentralisasi daerah"
    },
    {
        "id": 30, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Indonesia menjadi jalur perdagangan dunia karena diapit dua benua dan samudra. Dampak kulturalnya adalah...",
        "opsi": ["A. Budaya lokal terisolasi", "B. Terbentuknya budaya tunggal", "C. Masuknya pengaruh budaya asing", "D. Terhentinya laju modernisasi"],
        "jawaban": "C. Masuknya pengaruh budaya asing"
    },
    {
        "id": 31, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Siswa yang membuang sampah pada tempatnya and merawat tanaman fasilitas sekolah mencerminkan sikap keutuhan negara berupa...",
        "opsi": ["A. Rela berkorban militer", "B. Cinta tanah air di sekolah", "C. Etnosentrisme kepemudaan", "D. Apatis terhadap lingkungan"],
        "jawaban": "B. Cinta tanah air di sekolah"
    },
    {
        "id": 32, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Perbedaan kondisi alam pesisir pantai dengan kawasan pegunungan tinggi memicu terjadinya keberagaman masyarakat dalam hal...",
        "opsi": ["A. Sistem keagamaan", "B. Mata pencaharian and rumah", "C. Konstitusi tata negara", "D. Kebijakan politik luar negeri"],
        "jawaban": "B. Mata pencaharian and rumah"
    },
    {
        "id": 33, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "RIS dibubarkan pada 17 Agustus 1950 and Indonesia kembali ke bentuk Negara Kesatuan Republik Indonesia (NKRI) karena...",
        "opsi": ["A. Desakan resmi dari PBB", "B. Belanda menarik dukungannya", "C. Keinginan sebagian besar rakyat", "D. RIS tidak memiliki parlemen"],
        "jawaban": "C. Keinginan sebagian besar rakyat"
    },
    {
        "id": 34, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Saat kerja kelompok PPKn anggotanya terdiri atas siswa beda suku dan agama. Langkah terbaik agar tugas lancar adalah...",
        "opsi": ["A. Membiarkan satu orang bekerja", "B. Menghargai perbedaan & kerja sama", "C. Menghindari anggota beda suku", "D. Mengerjakan tugas mandiri saja"],
        "jawaban": "B. Menghargai perbedaan & kerja sama"
    },
    {
        "id": 35, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Rasa cinta tanah air yang diwujudkan secara berlebihan dan memandang rendah bangsa lain dinamakan dengan paham...",
        "opsi": ["A. Nasionalisme luas", "B. Chauvinisme (Nasionalisme sempit)", "C. Patriotisme modern", "D. Individualisme sekuler"],
        "jawaban": "B. Chauvinisme (Nasionalisme sempit)"
    },
    {
        "id": 36, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Revolusi digital memicu perubahan gaya hidup remaja. Respons terbaik seorang pelajar untuk menghadapi tantangan global ini adalah...",
        "opsi": ["A. Menolak total internet", "B. Selektif, belajar hal positif", "C. Pasrah pada kondisi", "D. Mengikuti semua tren asing"],
        "jawaban": "B. Selektif, belajar hal positif"
    },
    {
        "id": 37, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Setiap pemerintah daerah provinsi di Indonesia dalam membuat peraturan hukum daerah wajib mengacu pada konstitusi tertinggi, yaitu...",
        "opsi": ["A. UUD NRI Tahun 1945", "B. Ketetapan MPR RI", "C. Peraturan Pemerintah", "D. Konstitusi RIS 1949"],
        "jawaban": "A. UUD NRI Tahun 1945"
    },
    {
        "id": 38, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Keragaman profesi masyarakat seperti petani, nelayan, and pedagang terjadi di lingkungan sekitar kita. Tujuan keragaman ini adalah...",
        "opsi": ["A. Menciptakan kasta sosial", "B. Memicu persaingan kelas", "C. Saling melengkapi kebutuhan", "D. Memisahkan kota dan desa"],
        "jawaban": "C. Saling melengkapi kebutuhan"
    },
    {
        "id": 39, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Jika ada oknum teman mengajak melakukan tindakan diskriminasi antarsuku di sekolah, perilaku benteng pertahanan terbaik kita adalah...",
        "opsi": ["A. Ikut bergabung dengan kompak", "B. Menolak tegas & berteman adil", "C. Diam dan mendukung pasif", "D. Menantang berkelahi fisik"],
        "jawaban": "B. Menolak tegas & berteman adil"
    },
    {
        "id": 40, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Kemajuan teknologi komunikasi and alat transportasi saat ini mempermudah interaksi masyarakat antarpulau. Manfaat utamanya adalah...",
        "opsi": ["A. Daerah asal menjadi sepi", "B. Pertukaran barang/informasi mudah", "C. Budaya lokal langsung punah", "D. Bahasa daerah tidak dipakai"],
        "jawaban": "B. Pertukaran barang/informasi mudah"
    },

    # --- LEVEL 3: Penalaran / HOTS (10 Soal) ---
    {
        "id": 41, "level": "L3", "kategori": "Bab 5", "image": "https://via.placeholder.com/600x300.png?text=Sidang+BPUPK+Bentuk+Negara",
        "pertanyaan": "Analisis argumen sidang BPUPK mengenai bentuk negara. Mengapa pendiri bangsa akhirnya sepakat menetapkan bentuk negara kesatuan?",
        "opsi": [
            "A. Sistem federal terlalu boros", 
            "B. Paling tepat mewadahi persatuan bangsa majemuk", 
            "C. SDM daerah belum siap mandiri", 
            "D. Adanya paksaan mutlak dari sekutu"
        ],
        "jawaban": "B. Paling tepat mewadahi persatuan bangsa majemuk"
    },
    {
        "id": 42, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Masuknya budaya global melalui internet tidak bisa dibendung. Jika remaja menerima hal tersebut tanpa filter, dampak buruknya bagi negara adalah...",
        "opsi": [
            "A. Kesadaran nasional meningkat", 
            "B. Hidup menjadi makin makmur", 
            "C. Lunturnya identitas budaya asli", 
            "D. Meningkatnya pariwisata daerah"
        ],
        "jawaban": "C. Lunturnya identitas budaya asli"
    },
    {
        "id": 43, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Evaluasi syarat Konvensi Montevideo 1933. Apa akibat hukum jika suatu negara merdeka secara de facto tetapi tidak diakui secara de jure?",
        "opsi": [
            "A. Negara otomatis batal berdiri", 
            "B. Wajib menggelar pemilu ulang", 
            "C. Kesulitan menjalin kerja sama sah", 
            "D. Wilayahnya diambil alih tetangga"
        ],
        "jawaban": "C. Kesulitan menjalin kerja sama sah"
    },
    {
        "id": 44, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Perbedaan kelas sosial and ekonomi rawan memicu konflik. Solusi mitigasi konflik tersebut berdasarkan nilai Bhinneka Tunggal Ika adalah...",
        "opsi": [
            "A. Menghapus semua hak pekerja", 
            "B. Membatasi mobilitas penduduk", 
            "C. Toleransi & gotong royong adil", 
            "D. Membagi harta secara paksa"
        ],
        "jawaban": "C. Toleransi & gotong royong adil"
    },
    {
        "id": 45, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Tindakan diskriminasi rasial di kelas merusak persatuan. Sebagai siswa, peran konkret apa yang bisa kalian lakukan untuk menghentikannya?",
        "opsi": [
            "A. Mengusulkan kelas khusus minoritas", 
            "B. Berteman dengan semua lintas suku", 
            "C. Menjauhi kawan yang memicu debat", 
            "D. Membuat kritik pedas di medsos"
        ],
        "jawaban": "B. Berteman dengan semua lintas suku"
    },
    {
        "id": 46, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Penerapan digitalisasi raport pendidikan memicu kejutan bagi guru tradisional. Berdasarkan tips respons sosial, langkah terbaik adalah...",
        "opsi": [
            "A. Menolak memakai aplikasi sistem", 
            "B. Meminta sistem kembali ke manual", 
            "C. Berpikir positif, belajar & adaptasi", 
            "D. Membiarkan data raport kosong"
        ],
        "jawaban": "C. Berpikir positif, belajar & adaptasi"
    },
    {
        "id": 47, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "UU No 43 Tahun 2008 menetapkan wilayah kedaulatan NKRI. Jika ditemukan minyak kedaulatan di perairan dalam nusantara, kepemilikannya ada pada...",
        "opsi":
