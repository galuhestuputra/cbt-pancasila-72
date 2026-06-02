import streamlit as st
import pandas as pd
from datetime import datetime
import io
import random

# --- KONFIGURASI ---
st.set_page_config(page_title="CBT PPKn", layout="wide")

# --- INISIALISASI SESSION STATE ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "db_nilai" not in st.session_state: st.session_state.db_nilai = pd.DataFrame(columns=["Waktu", "Nama", "Kelas", "Absen", "Nilai"])
if "is_guru" not in st.session_state: st.session_state.is_guru = False

# --- HALAMAN GURU (Database) ---
def halaman_guru():
    st.header("🔐 Panel Guru")
    if not st.session_state.is_guru:
        password = st.text_input("Password Guru", type="password")
        if st.button("Login Guru"):
            if password == "guru123":
                st.session_state.is_guru = True
                st.rerun()
            else:
                st.error("Password Salah!")
    else:
        st.success("Akses Diterima")
        if not st.session_state.db_nilai.empty:
            st.dataframe(st.session_state.db_nilai)
            # Tombol Download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                st.session_state.db_nilai.to_excel(writer, index=False)
            st.download_button("Download Excel", data=output.getvalue(), file_name="Data_Nilai.xlsx")
        else:
            st.warning("Belum ada data nilai.")

# --- HALAMAN SISWA (Login & Ujian) ---
def halaman_siswa():
    if not st.session_state.logged_in:
        st.header("Login Siswa")
        nama = st.text_input("Nama Lengkap")
        kelas = st.selectbox("Kelas", ["7A", "7B", "7C"])
        absen = st.number_input("Nomor Absen", 1, 40)
        if st.button("Mulai"):
            st.session_state.user = {"nama": nama, "kelas": kelas, "absen": absen}
            st.session_state.logged_in = True
            st.rerun()
    else:
        st.write(f"Selamat mengerjakan, {st.session_state.user['nama']}")
        # Simulasi 1 Soal
        jawaban = st.radio("Semboyan Indonesia adalah...", ["Bhinneka Tunggal Ika", "Pancasila"])
        if st.button("Kumpulkan"):
            nilai = 100 if jawaban == "Bhinneka Tunggal Ika" else 0
            st.write(f"Skor Anda: {nilai}")
            # Simpan ke DB
            data = {"Waktu": datetime.now(), "Nama": st.session_state.user['nama'], 
                    "Kelas": st.session_state.user['kelas'], "Absen": st.session_state.user['absen'], "Nilai": nilai}
            st.session_state.db_nilai = pd.concat([st.session_state.db_nilai, pd.DataFrame([data])], ignore_index=True)

# --- MAIN ---
tab1, tab2 = st.tabs(["💻 Siswa", "📝 Guru"])
with tab1: halaman_siswa()
with tab2: halaman_guru()
