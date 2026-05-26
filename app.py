import streamlit as st
import pandas as pd
from datetime import datetime
import io
import time
import random  # Menambahkan pustaka untuk fitur pengacakan

# ==========================================
# KONFIGURASI HALAMAN & INFORMASI HAK CIPTA
# ==========================================
st.set_page_config(page_title="CBT PPKn - Media Pembelajaran", page_icon="🎓", layout="wide")

# DATA HAK CIPTA GURU
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
        "pertanyaan": "Bhinneka Tunggal Ika adalah semboyan atau motto nasional Indonesia. Makna utama dari semboyan tersebut adalah... [cite: 1138-1139]",
        "opsi": ["A. Kesatuan dalam perbedaan", "B. Berbeda-beda tetapi tetap satu jua", "C. Persatuan suku bangsa", "D. Toleransi antar umat beragama"],
        "jawaban": "B. Berbeda-beda tetapi tetap satu jua"
    },
    {
        "id": 2, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Menurut Konvensi Montevideo tahun 1933, unsur konstitutif (mutlak) berdirinya sebuah negara adalah... [cite: 93-94]",
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
        "pertanyaan": "Pengakuan dari negara lain yang didasarkan pada kenyataan (fakta) bahwa sebuah negara telah memenuhi unsur mutlak disebut pengakuan... [cite: 106-107]",
        "opsi": ["A. De facto", "B. De jure", "C. Konstitutif", "D. Deklaratif"],
        "jawaban": "A. De facto"
    },
    {
        "id": 7, "level": "L1", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Salah satu bentuk kearifan lokal suku Bali dalam mengelola sistem pertanian yang menjaga keseimbangan alam adalah... [cite: 1237-1238]",
        "opsi": ["A. Ngaben", "B. Seren Taun", "C. Subak", "D. Ruwatan"],
        "jawaban": "C. Subak"
    },
    {
        "id": 8, "level": "L1", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pada sidang BPUPK, tokoh yang mengusulkan agar bentuk negara Indonesia adalah negara kesatuan atau 'negara integral' adalah... [cite: 295-297]",
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
        "pertanyaan": "Rumah adat suku Baduy di Provinsi Banten yang terbuat dari bambu dan kayu mencerminkan nilai budaya mereka yaitu... [cite: 1211-1212]",
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
        "pertanyaan": "Ras Asiatic Mongoloid yang berada di wilayah Indonesia umumnya berasal dari bangsa... [cite: 1330-1331]",
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
        "pertanyaan": "Penggolongan masyarakat berdasarkan hierarki status sosial seperti pimpinan, staf, dan karyawan disebut sebagai penggolongan yang terbentuk secara... [cite: 1382-1383]",
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
        "pertanyaan": "Di sebuah kompleks perumahan, warga yang bersuku Batak, Jawa, dan Minang selalu bahu-membahu membersihkan lingkungan setiap bulan. Tindakan ini merupakan perwujudan dari... [cite: 1135-1143]",
        "opsi": ["A. Asimilasi total budaya lokal", "B. Persatuan dalam keberagaman suku di masyarakat", "C. Primordialisme antarsuku", "D. Etnosentrisme dalam satu lingkungan"],
        "jawaban": "B. Persatuan dalam keberagaman suku di masyarakat"
    },
    {
        "id": 27, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Sebuah kapal penangkap ikan dari negara Z ditangkap patroli TNI AL karena terbukti mencari ikan di perairan sejauh 150 mil dari garis pantai Indonesia. Kapal tersebut ditangkap karena melanggar batas perairan...",
        "opsi": ["A. Laut Teritorial", "B. Perairan Pedalaman", "C. Zona Ekonomi Eksklusif (ZEE)", "D. Landasan Kontinen"],
        "jawaban": "C. Zona Ekonomi Eksklusif (ZEE)"
    },
    {
        "id": 28, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Andi merayakan Idulfitri, sementara tetangganya Budi merayakan Natal. Keduanya saling mengunjungi dan menghargai perayaan agama masing-masing. Sikap ini merupakan penerapan langsung dari perilaku... [cite: 1297-1301]",
        "opsi": ["A. Toleransi beragama yang menciptakan keharmonisan", "B. Sinkretisme perayaan hari besar", "C. Memudarnya nilai-nilai ajaran asli agama", "D. Kompromi terhadap prinsip keyakinan"],
        "jawaban": "A. Toleransi beragama yang menciptakan keharmonisan"
    },
    {
        "id": 29, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Pemerintah daerah Kota Ambon saat ini memiliki wewenang untuk mengatur urusan rumah tangganya sendiri dan membangun fasilitas publik dari anggaran daerahnya. Ini menunjukkan negara Indonesia menerapkan sistem...",
        "opsi": ["A. Sentralisasi absolut", "B. Desentralisasi", "C. Federalisme murni", "D. Otoriterisme"],
        "jawaban": "B. Desentralisasi"
    },
    {
        "id": 30, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Indonesia menjadi jalur perdagangan internasional karena letak geografisnya yang diapit benua Asia dan Australia. Secara kultural, dampak dari kondisi ini adalah... [cite: 1153-1158]",
        "opsi": ["A. Masyarakat Indonesia sepenuhnya terisolasi dari kebudayaan global", "B. Terciptanya satu kebudayaan tunggal yang seragam di nusantara", "C. Indonesia sulit mencegah masuknya pengaruh budaya asing dan menjadi beragam", "D. Terhentinya laju modernisasi di sektor maritim"],
        "jawaban": "C. Indonesia sulit mencegah masuknya pengaruh budaya asing dan menjadi beragam"
    },
    {
        "id": 31, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Sebagai pelajar, tindakan seperti menjaga kebersihan lingkungan dan tidak merusak fasilitas umum merupakan salah satu cerminan sikap menjaga keutuhan negara melalui... [cite: 414-415]",
        "opsi": ["A. Rela berkorban di medan tempur", "B. Cinta tanah air di lingkungan masyarakat", "C. Etnosentrisme kepemudaan", "D. Sikap apatis terhadap perubahan lingkungan"],
        "jawaban": "B. Cinta tanah air di lingkungan masyarakat"
    },
    {
        "id": 32, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Kondisi alam pesisir yang subur dan kawasan pegunungan yang sejuk secara langsung akan melahirkan keberagaman masyarakat terutama pada sektor... [cite: 1172-1174]",
        "opsi": ["A. Pemilihan agama dan aliran kepercayaan", "B. Mata pencaharian dan desain arsitektur rumah", "C. Sistem hukum peradilan yang dianut", "D. Kebijakan hubungan luar negeri"],
        "jawaban": "B. Mata pencaharian dan desain arsitektur rumah"
    },
    {
        "id": 33, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Sesaat setelah Konferensi Meja Bundar, Indonesia terpaksa menjadi negara Republik Indonesia Serikat (RIS). Tak lama berselang, Presiden Sukarno membubarkan RIS pada 17 Agustus 1950 karena... [cite: 353-354]",
        "opsi": ["A. Adanya desakan dari pihak Perserikatan Bangsa-Bangsa", "B. Belanda secara resmi menarik dukungannya atas bentuk serikat", "C. Sebagian besar rakyat Indonesia menginginkan kembali ke bentuk negara kesatuan", "D. Sistem konstitusi RIS tidak memiliki parlemen perwakilan"],
        "jawaban": "C. Sebagian besar rakyat Indonesia menginginkan kembali ke bentuk negara kesatuan"
    },
    {
        "id": 34, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Dalam kerja kelompok PPKn, anggota kelompok terdiri atas teman-teman yang berbeda latar belakang agama dan suku bangsa. Langkah terbaik yang harus dilakukan untuk menyukseskan tugas adalah... [cite: 1388-1389]",
        "opsi": ["A. Menyerahkan semua tugas pada satu orang yang paling pintar", "B. Saling menghargai perbedaan tersebut dan bekerja sama menyelesaikan tugas", "C. Menghindari anggota yang berbeda suku agar tidak terjadi konflik", "D. Mengerjakan bagian tugas sendiri tanpa peduli hasil kelompok"],
        "jawaban": "B. Saling menghargai perbedaan tersebut dan bekerja sama menyelesaikan tugas"
    },
    {
        "id": 35, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Memiliki kebanggaan terhadap negara itu penting, tetapi jika perasaan cinta tanah air tersebut diwujudkan secara berlebihan hingga merendahkan negara lain, maka hal ini disebut sebagai...",
        "opsi": ["A. Nasionalisme dalam arti luas", "B. Nasionalisme dalam arti sempit (Chauvinisme)", "C. Patriotisme modern", "D. Individualisme progresif"],
        "jawaban": "B. Nasionalisme dalam arti sempit (Chauvinisme)"
    },
    {
        "id": 36, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Revolusi digital memberikan pengaruh yang sangat besar hingga memicu perubahan gaya hidup di kalangan remaja. Respons terbaik seorang pelajar untuk menghadapi perubahan global ini adalah... [cite: 1457-1473, 1482]",
        "opsi": ["A. Menolak total penggunaan internet demi menjaga tradisi", "B. Mengevaluasi peluang, menyerap informasi positif, dan terus belajar hal baru", "C. Menyerahkan semua permasalahan moral pada pemerintah", "D. Mengikuti tren apa saja tanpa batas agar terlihat kekinian"],
        "jawaban": "B. Mengevaluasi peluang, menyerap informasi positif, dan terus belajar hal baru"
    },
    {
        "id": 37, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Berbeda dengan negara bagian di sistem serikat, provinsi di Indonesia berkedudukan di bawah pemerintah pusat dan harus mengacu pada satu konstitusi utama, yakni...",
        "opsi": ["A. Undang-Undang Dasar Negara Republik Indonesia Tahun 1945", "B. Ketetapan Majelis Permusyawaratan Rakyat (TAP MPR)", "C. Peraturan Pemerintah Pengganti Undang-Undang (Perppu)", "D. Konstitusi Republik Indonesia Serikat"],
        "jawaban": "A. Undang-Undang Dasar Negara Republik Indonesia Tahun 1945"
    },
    {
        "id": 38, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Penggolongan profesi seperti petani, nelayan, buruh, dan pedagang menunjukkan keragaman antargolongan. Tujuan utama dari perbedaan profesi ini dalam masyarakat adalah untuk... [cite: 1386-1390]",
        "opsi": ["A. Menjadikan status pengusaha lebih tinggi dari kaum buruh", "B. Membangun persaingan antarkelas ekonomi", "C. Saling melengkapi kebutuhan hidup satu sama lain melalui kerja sama", "D. Memisahkan masyarakat desa dengan penduduk kota"],
        "jawaban": "C. Saling melengkapi kebutuhan hidup satu sama lain melalui kerja sama"
    },
    {
        "id": 39, "level": "L2", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Apabila ada oknum yang mengajak kalian untuk menyebarkan paham kebencian terhadap suatu kelompok budaya di sekolah, tindakan pencegahan ekstremisme yang paling tepat adalah... [cite: 406-407, 442-444]",
        "opsi": ["A. Ikut menyebarkannya jika banyak teman yang bergabung", "B. Menolak ajakan tersebut dan menjalin pertemanan dengan siapapun tanpa membedakan ras atau agama", "C. Mengabaikannya namun diam-diam setuju dengan paham tersebut", "D. Menantang oknum tersebut berkelahi"],
        "jawaban": "B. Menolak ajakan tersebut dan menjalin pertemanan dengan siapapun tanpa membedakan ras atau agama"
    },
    {
        "id": 40, "level": "L2", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Akibat isolasi geografis di masa lalu, penduduk antar pulau jarang berinteraksi sehingga bahasa mereka berbeda. Kini, dengan adanya kemajuan alat transportasi, interaksi antar masyarakat semakin tinggi. Manfaat utamanya adalah... [cite: 1175-1178]",
        "opsi": ["A. Daerah semakin tertinggal karena banyak warganya yang pindah", "B. Perpindahan orang dan pertukaran barang atau informasi antar wilayah menjadi lebih cepat dan mudah", "C. Seluruh budaya lokal otomatis terhapus", "D. Bahasa nasional tidak lagi dibutuhkan"],
        "jawaban": "B. Perpindahan orang dan pertukaran barang atau informasi antar wilayah menjadi lebih cepat dan mudah"
    },

    # --- LEVEL 3: Penalaran / HOTS (10 Soal) ---
    {
        "id": 41, "level": "L3", "kategori": "Bab 5", "image": "https://via.placeholder.com/600x300.png?text=Sidang+BPUPK+Bentuk+Negara",
        "pertanyaan": "Dalam sidang BPUPK, Mohammad Hatta menilai bentuk serikat cocok dengan keberagaman suku bangsa. Sebaliknya, Soepomo dan Muhammad Yamin meyakini bentuk kesatuanlah yang tepat. Berdasarkan sejarah ketatanegaraan kita, alasan paling filosofis mengapa negara kesatuan yang akhirnya menjadi pilihan permanen adalah... [cite: 313-316, 342-343]",
        "opsi": [
            "A. Negara serikat selalu membebani anggaran daerah", 
            "B. Negara kesatuan dianggap bentuk paling tepat untuk mewadahi ide persatuan sebuah bangsa yang majemuk sekaligus memperkuat kedaulatan", 
            "C. Indonesia belum memiliki SDM untuk memimpin negara-negara bagian", 
            "D. Undang-undang federal sangat sulit dirumuskan oleh panitia persiapan kemerdekaan"
        ],
        "jawaban": "B. Negara kesatuan dianggap bentuk paling tepat untuk mewadahi ide persatuan sebuah bangsa yang majemuk sekaligus memperkuat kedaulatan"
    },
    {
        "id": 42, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Pesatnya kemajuan teknologi informasi memungkinkan budaya global masuk tanpa hambatan. Jika masyarakat menerima hal asing (akulturasi) secara buta tanpa proses penyaringan nilai, konsekuensi sosial jangka panjang yang akan dialami bangsa Indonesia adalah... [cite: 1182-1192]",
        "opsi": [
            "A. Menguatnya kesadaran ber-Bhinneka Tunggal Ika", 
            "B. Terciptanya kehidupan sosial yang harmonis dan merata", 
            "C. Identitas nasional dan keaslian budaya luhur perlahan luntur dan tergantikan oleh budaya asing", 
            "D. Meningkatnya devisa negara dari sektor pariwisata luar negeri"
        ],
        "jawaban": "C. Identitas nasional dan keaslian budaya luhur perlahan luntur dan tergantikan oleh budaya asing"
    },
    {
        "id": 43, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Berdasarkan Konvensi Montevideo 1933, pengakuan de jure bersifat deklaratif namun krusial dalam percaturan global. Analisislah akibat hukum jika sebuah negara merdeka secara de facto (memiliki wilayah, rakyat, dan pemerintah) namun tidak kunjung mendapatkan pengakuan de jure dari masyarakat internasional! [cite: 93-94, 104-107]",
        "opsi": [
            "A. Negara tersebut batal berdiri dan rakyatnya kehilangan kewarganegaraan", 
            "B. Pemerintahannya tidak sah dan wajib melaksanakan pemilihan ulang di bawah PBB", 
            "C. Negara tersebut tetap ada secara fisik, namun akan sangat kesulitan melakukan hubungan kerja sama maupun perjanjian internasional secara sah", 
            "D. Kedaulatan negaranya langsung diambil alih oleh negara yang berbatasan dengannya"
        ],
        "jawaban": "C. Negara tersebut tetap ada secara fisik, namun akan sangat kesulitan melakukan hubungan kerja sama maupun perjanjian internasional secara sah"
    },
    {
        "id": 44, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Perbedaan tingkat ekonomi (pendapatan, status kelas sosial) sangat rawan memicu konflik di tengah masyarakat. Sebagai warga yang menjunjung tinggi Bhinneka Tunggal Ika, solusi sosiologis paling relevan untuk meredam kesenjangan tersebut adalah... [cite: 1150-1151]",
        "opsi": [
            "A. Menerapkan sistem otoriter yang menghapus kelas pekerja", 
            "B. Menghindari interaksi fisik antar wilayah kota dan desa", 
            "C. Menumbuhkan sikap saling menghormati, toleransi, dan kerja sama gotong royong tanpa memandang latar belakang materi", 
            "D. Mewajibkan golongan ekonomi atas untuk membiayai seluruh kebutuhan golongan bawah"
        ],
        "jawaban": "C. Menumbuhkan sikap saling menghormati, toleransi, dan kerja sama gotong royong tanpa memandang latar belakang materi"
    },
    {
        "id": 45, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Di lingkungan sekolah, tindakan membeda-bedakan kawan (diskriminasi) bertentangan dengan prinsip menjaga keutuhan wilayah. Pendekatan karakter yang paling solutif yang bisa kalian lakukan sebagai siswa adalah... [cite: 442-444]",
        "opsi": [
            "A. Melaporkan perbedaan teman kepada guru agar mereka diberikan kelas khusus", 
            "B. Menjalin hubungan pertemanan lintas batas (suku, ras, agama) serta mematuhi tata tertib sekolah", 
            "C. Membatasi pergaulan hanya pada teman yang memiliki budaya yang sama demi menjaga kedamaian", 
            "D. Menggunakan media sosial untuk mengkritik suku minoritas di sekolah"
        ],
        "jawaban": "B. Menjalin hubungan pertemanan lintas batas (suku, ras, agama) serta mematuhi tata tertib sekolah"
    },
    {
        "id": 46, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Dalam menghadapi perubahan sosial di era globalisasi (misalnya digitalisasi pendidikan pasca pandemi), sikap apatis sering kali memicu kemunduran. Berdasarkan tips manajemen krisis, langkah proaktif apa yang sebaiknya diambil oleh seorang pelajar? [cite: 1461-1474]",
        "opsi": [
            "A. Menyerah dan menunggu fasilitas yang sempurna", 
            "B. Melakukan protes dan menghindari belajar daring secara total", 
            "C. Menerima perubahan secara positif, mengevaluasi keadaan, dan terus belajar mengembangkan diri", 
            "D. Memaksakan diri menggunakan metode konvensional meski sudah dilarang"
        ],
        "jawaban": "C. Menerima perubahan secara positif, mengevaluasi keadaan, dan terus belajar mengembangkan diri"
    },
    {
        "id": 47, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Undang-Undang Nomor 43 Tahun 2008 memandang wilayah NKRI—baik darat, laut, maupun udara—sebagai satu kesatuan utuh. Jika suatu saat terjadi penemuan tambang mineral berharga di perairan kepulauan (archipelagic waters), maka secara yuridis hak kepemilikannya berada di tangan...",
        "opsi": [
            "A. Pihak asing yang berhasil menemukan wilayah tambang tersebut terlebih dahulu", 
            "B. Pemerintah provinsi setempat tanpa adanya campur tangan pemerintah pusat", 
            "C. Negara Kesatuan Republik Indonesia, termasuk seluruh sumber kekayaan yang terkandung di dalamnya", 
            "D. Perusahaan multinasional yang ditunjuk secara sepihak oleh gubernur setempat"
        ],
        "jawaban": "C. Negara Kesatuan Republik Indonesia, termasuk seluruh sumber kekayaan yang terkandung di dalamnya"
    },
    {
        "id": 48, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Berdasarkan tinjauan sosiologis, pemaksaan asimilasi atau penyeragaman kebudayaan seringkali gagal di Indonesia karena bertentangan dengan semboyan negara. Mengapa keberagaman budaya diklaim sebagai sebuah keunggulan, bukan kelemahan? [cite: 1133-1136, 1144-1146]",
        "opsi": [
            "A. Karena dapat memudahkan masuknya investasi asing tanpa harus memperhatikan adat", 
            "B. Karena keberagaman menyediakan banyak sumber daya pemikiran, kreativitas, dan inovasi yang vital bagi kemajuan nasional", 
            "C. Karena dengan keberagaman, pemerintah bisa lebih mudah memecah belah kekuatan politik rakyat", 
            "D. Karena keberagaman menekan biaya infrastruktur di wilayah yang masih tertinggal"
        ],
        "jawaban": "B. Karena keberagaman menyediakan banyak sumber daya pemikiran, kreativitas, dan inovasi yang vital bagi kemajuan nasional"
    },
    {
        "id": 49, "level": "L3", "kategori": "Bab 5", "image": None,
        "pertanyaan": "Penerapan hukum kelautan internasional yang menetapkan 200 mil sebagai Zona Ekonomi Eksklusif (ZEE) memberi Indonesia kewenangan berdaulat atas SDA. Apa implikasi pertahanan-keamanan (Hankam) atas perluasan batas ini? [cite: 139-142, 232]",
        "opsi": [
            "A. Angkatan bersenjata Indonesia kehilangan kendali atas lalu lintas kapal internasional di perairan sempit", 
            "B. Negara harus meningkatkan kapasitas diplomasi kelautan dan kemampuan patroli pengawasan batas perairan secara masif", 
            "C. Seluruh batas darat menjadi tidak penting karena anggaran difokuskan sepenuhnya ke laut lepas", 
            "D. Nelayan tradisional dilarang mencari ikan di perairan dekat pantai mereka sendiri"
        ],
        "jawaban": "B. Negara harus meningkatkan kapasitas diplomasi kelautan dan kemampuan patroli pengawasan batas perairan secara masif"
    },
    {
        "id": 50, "level": "L3", "kategori": "Bab 4", "image": None,
        "pertanyaan": "Jika diamati dari sejarah lahirnya Indische Partij (1912), perlawanan terhadap kolonial Belanda kala itu tidak sekadar menuntut kemerdekaan politik, tetapi juga didorong oleh perlawanan terhadap sistem golongan. Dari kasus tersebut, apa pelajaran yang bisa ditarik terkait stratifikasi (penggolongan) rasial di masa kini? [cite: 1429-1436]",
        "opsi": [
            "A. Stratifikasi rasial terbukti efisien untuk menjaga ketertiban masyarakat agraris", 
            "B. Penggolongan berbasis ras harus dipertahankan untuk melindungi keaslian suku bangsa dari ancaman luar", 
            "C. Diskriminasi antargolongan akan selalu melahirkan ketidakadilan (sosial, pendidikan, pekerjaan) yang memicu instabilitas dan penderitaan kemanusiaan", 
            "D. Kebijakan kolonial sebenarnya bermanfaat, namun cara penyampaiannya saja yang salah"
        ],
        "jawaban": "C. Diskriminasi antargolongan akan selalu melahirkan ketidakadilan (sosial, pendidikan, pekerjaan) yang memicu instabilitas dan penderitaan kemanusiaan"
    }
]

# ==========================================
# INISIALISASI SESSION STATE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "jawaban_user" not in st.session_state:
    st.session_state.jawaban_user = {q["id"]: None for q in soal_cbt}
if "db_nilai" not in st.session_state:
    cols = ["Waktu", "Nama Lengkap", "Kelas", "No Absen", "Asal Sekolah", "Nilai", "Benar", "Salah"]
    st.session_state.db_nilai = pd.DataFrame(columns=cols)
if "submit_status" not in st.session_state:
    st.session_state.submit_status = None
if "is_guru" not in st.session_state:
    st.session_state.is_guru = False
if "skor_siswa_saat_ini" not in st.session_state:
    st.session_state.skor_siswa_saat_ini = {"nilai": 0, "benar": 0, "salah": 0}
# Menyimpan urutan acak opsi agar tidak berubah-ubah saat radio button diklik siswa
if "opsi_acak_soal" not in st.session_state:
    st.session_state.opsi_acak_soal = {}

# ==========================================
# LOGIKA PERHITUNGAN & SINKRONISASI
# ==========================================
def hitung_nilai():
    benar = sum(
        1 for q in soal_cbt 
        if st.session_state.jawaban_user.get(q["id"]) == q["jawaban"]
    )
    salah = 50 - benar
    nilai = (benar / 50) * 100
    return round(nilai, 2), benar, salah

def proses_kirim_jawaban():
    try:
        with st.spinner("Sistem sedang mengamankan data ujian..."):
            time.sleep(1.5)
            nilai, benar, salah = hitung_nilai()
            
            st.session_state.skor_siswa_saat_ini = {
                "nilai": nilai,
                "benar": benar,
                "salah": salah
            }
            
            data_baru = {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nama Lengkap": st.session_state.user_data["Nama Lengkap"],
                "Kelas": st.session_state.user_data["Kelas"],
                "No Absen": st.session_state.user_data["No Absen"],
                "Asal Sekolah": st.session_state.user_data["Asal Sekolah"],
                "Nilai": nilai,
                "Benar": benar,
                "Salah": salah
            }
            
            df_baru = pd.DataFrame([data_baru])
            st.session_state.db_nilai = pd.concat([st.session_state.db_nilai, df_baru], ignore_index=True)
            st.session_state.submit_status = "Berhasil"
    except Exception as err:
        st.session_state.submit_status = "Gagal"

# ==========================================
# INTERFACE HALAMAN
# ==========================================
def halaman_login_siswa():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>CBT KEMDIKBUD LITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Aplikasi Penilaian Sumatif Pendidikan Pancasila Kelas VII</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("form_login"):
            st.markdown("### 👤 Form Login Peserta")
            
            input_nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap")
            pilihan_kelas = ["Pilih Kelas", "7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "7I"]
            input_kelas = st.selectbox("Kelas", pilihan_kelas)
            
            pilihan_absen = ["Pilih Absen"] + [str(i) for i in range(1, 41)]
            input_absen = st.selectbox("Nomor Absen", pilihan_absen)
            input_sekolah = st.text_input("Asal Sekolah", value="SMP Negeri 1 Banjar")
            
            tombol_masuk = st.form_submit_button("Masuk Ujian", use_container_width=True)
            
            if tombol_masuk:
                if not input_nama.strip() or input_kelas == "Pilih Kelas" or input_absen == "Pilih Absen" or not input_sekolah.strip():
                    st.error("Silakan lengkapi seluruh isian data login!")
                else:
                    st.session_state.user_data = {
                        "Nama Lengkap": input_nama,
                        "Kelas": input_kelas,
                        "No Absen": input_absen,
                        "Asal Sekolah": input_sekolah
                    }
                    
                    # PROSES PENGACAKAN OPSI JAWABAN SAAT LOGIN BERHASIL (Setiap siswa unik)
                    st.session_state.opsi_acak_soal = {}
                    for q in soal_cbt:
                        list_opsi = list(q["opsi"])
                        random.shuffle(list_opsi) # Mengacak posisi A, B, C, D
                        st.session_state.opsi_acak_soal[q["id"]] = list_opsi
                        
                    st.session_state.logged_in = True
                    st.rerun()

def halaman_ujian():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"**Peserta:** {st.session_state.user_data['Nama Lengkap']} | **Kelas:** {st.session_state.user_data['Kelas']}")
    with c2:
        st.markdown("**Mata Pelajaran:** PPKn")
    st.divider()

    if st.session_state.submit_status == "Berhasil":
        st.balloons()
        st.success("✔ JAWABAN BERHASIL DIKIRIM KE DATABASE GURU!")
        
        st.markdown("""
            <div style='background-color: #F0FDF4; border: 2px solid #16A34A; padding: 25px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
                <h2 style='color: #16A34A; margin-top: 0;'>📝 HASIL SKOR UJIAN ANDA</h2>
                <p style='font-size: 1.1rem; color: #374151;'>Terima kasih telah menyelesaikan ujian dengan jujur.</p>
                <hr style='border-top: 1px solid #BBF7D0;'>
                <div style='display: flex; justify-content: space-around; margin-top: 20px;'>
                    <div>
                        <span style='font-size: 1rem; color: #6B7280;'>Benar</span><br>
                        <span style='font-size: 2rem; font-weight: bold; color: #16A34A;'>{}</span>
                    </div>
                    <div>
                        <span style='font-size: 1.2rem; color: #374151; font-weight: bold;'>NILAI AKHIR</span><br>
                        <span style='font-size: 3.5rem; font-weight: bold; color: #1E3A8A;'>{}</span>
                    </div>
                    <div>
                        <span style='font-size: 1rem; color: #6B7280;'>Salah</span><br>
                        <span style='font-size: 2rem; font-weight: bold; color: #DC2626;'>{}</span>
                    </div>
                </div>
            </div>
        """.format(
            st.session_state.skor_siswa_saat_ini["benar"],
            st.session_state.skor_siswa_saat_ini["nilai"],
            st.session_state.skor_siswa_saat_ini["salah"]
        ), unsafe_allow_html=True)
        
        if st.button("Keluar dan Selesai", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            st.session_state.jawaban_user = {q["id"]: None for q in soal_cbt}
            st.session_state.submit_status = None
            st.session_state.skor_siswa_saat_ini = {"nilai": 0, "benar": 0, "salah": 0}
            st.session_state.opsi_acak_soal = {}
            st.rerun()
            
    elif st.session_state.submit_status == "Gagal":
        st.error("✖ PENGIRIMAN GAGAL! Silakan klik kembali tombol di bawah untuk mengulang pengiriman jawaban.")
        if st.button("Ulangi Pengiriman Jawaban", type="primary"):
            proses_kirim_jawaban()
            st.rerun()
            
    else:
        st.markdown("### Lembar Kerja Soal Pilihan Ganda")
        
        for i, q in enumerate(soal_cbt):
            st.markdown(f"**Soal No. {i+1}** (Level: {q['level']} - {q['kategori']})")
            if q["image"]:
                st.image(q["image"], width=400)
            st.write(q["pertanyaan"])
            
            # MENGAMBIL OPSI YANG SUDAH DIACAK KHUSUS SISWA INI SAAT LOGIN
            opsi_siswa = st.session_state.opsi_acak_soal.get(q["id"], q["opsi"])
            
            jawaban_saat_ini = st.session_state.jawaban_user.get(q["id"])
            idx_opsi = opsi_siswa.index(jawaban_saat_ini) if jawaban_saat_ini in opsi_siswa else None
                
            hasil_pilihan = st.radio(
                label=f"Pilihan untuk soal {q['id']}", 
                options=opsi_siswa, 
                index=idx_opsi,
                key=f"radio_{q['id']}",
                label_visibility="collapsed"
            )
            st.session_state.jawaban_user[q["id"]] = hasil_pilihan
            st.markdown("---")

        if st.button("KUMPULKAN JAWABAN", type="primary", use_container_width=True):
            proses_kirim_jawaban()
            st.rerun()

def halaman_guru():
    st.markdown("### 🔐 Akses Terbatas Khusus Guru")
    
    if not st.session_state.is_guru:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            with st.form("form_akses_guru"):
                st.write("Silakan masukkan PIN/Password Guru untuk mengunduh rekapitulasi nilai.")
                password_input = st.text_input("Password Guru", type="password")
                tombol_verifikasi = st.form_submit_button("Buka Data Rekap", use_container_width=True)
                
                if tombol_verifikasi:
                    if password_input == "guru123":
                        st.session_state.is_guru = True
                        st.rerun()
                    else:
                        st.error("Password salah! Akses ditolak.")
    else:
        st.success("Akses Terverifikasi. Selamat datang, Guru.")
        
        if st.button("Kunci Kembali Panel Guru"):
            st.session_state.is_guru = False
            st.rerun()
            
        st.divider()
        st.markdown("#### Tabel Database Hasil Kerja Siswa")
        df_data = st.session_state.db_nilai
        
        if not df_data.empty:
            st.dataframe(df_data, use_container_width=True)
            
            memori_excel = io.BytesIO()
            with pd.ExcelWriter(memori_excel, engine="openpyxl") as penulis:
                df_data.to_excel(penulis, index=False, sheet_name="Rekap Nilai Siswa")
                
            st.download_button(
                label="📥 Download Format Excel (.xlsx)",
                data=memori_excel.getvalue(),
                file_name=f"Nilai_CBT_PPKn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
        else:
            st.warning("Database kosong. Belum ada siswa yang mengirimkan lembar jawaban kuis.")

# ==========================================
# ROUTING UTAMA SISTEM
# ==========================================
def main():
    tab_peserta, tab_guru = st.tabs(["💻 Sesi Ujian (Siswa)", "📝 Sasis Dokumen (Guru Only)"])
    
    with tab_peserta:
        if st.session_state.logged_in:
            halaman_ujian()
        else:
            halaman_login_siswa()
            
    with tab_guru:
        halaman_guru()

    # Footer Identitas Hak Cipta
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='text-align: center; color: #888; font-size: 0.9em; border-top: 1px solid #ccc; padding-top: 15px;'>
            <strong>Hak Cipta &copy; 2026 - Aplikasi Media Pembelajaran CBT PPKn</strong><br>
            Instansi: {APP_SCHOOL} | Pengembang Utama: {APP_AUTHOR}<br>
            Layanan Pengaduan Sistem: {APP_CONTACT}
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()