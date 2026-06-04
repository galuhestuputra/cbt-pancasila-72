import streamlit as st
import pandas as pd
from datetime import datetime
import io
import time
import random
# MEMANGGIL BANK SOAL SECARA MODULAR (ANTI-DARK-SCREEN)
from bank_soal import soal_cbt

# ==========================================
# KONFIGURASI HALAMAN & INFORMASI HAK CIPTA
# ==========================================
st.set_page_config(page_title="CBT PPKn - Media Pembelajaran", page_icon="🎓", layout="wide")

APP_AUTHOR = "Galuh Estu Putra"
APP_SCHOOL = "SMP Negeri 1 Banjar"
APP_CONTACT = "085227384085"

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
if "opsi_acak_soal" not in st.session_state:
    st.session_state.opsi_acak_soal = {}

# ==========================================
# LOGIKA PERHITUNGAN JAWABAN
# ==========================================
def hitung_nilai():
    benar = 0
    for q in soal_cbt:
        jawaban_terpilih = st.session_state.jawaban_user.get(q["id"])
        if jawaban_terpilih == q["jawaban"]:
            benar += 1
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
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #E0F2FE 0%, #ECFDF5 100%);
        }
        .kotak-login {
            background-color: #FFFFFF;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.1);
            border: 2px solid #A7F3D0;
            margin-top: 20px;
        }
        .judul-utama {
            color: #1E3A8A !important;
            font-weight: 800;
            text-align: center;
            margin-bottom: 5px;
        }
        .sub-judul {
            color: #1E3A8A !important;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='judul-utama'>🎓 CBT PANCASILA CERIA</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-judul'>Media Pembelajaran Interaktif Kelas VII - {APP_SCHOOL}</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div class='kotak-login'>", unsafe_allow_html=True)
        with st.form("form_login"):
            st.markdown("<h3 style='color: #1E3A8A; text-align:center; margin-bottom:20px;'>👋 Selamat Datang! Silakan Login</h3>", unsafe_allow_html=True)
            
            input_nama = st.text_input("📝 Nama Lengkap", placeholder="Ketik nama lengkapmu di sini...")
            pilihan_kelas = ["Pilih Kelas", "7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "7I"]
            input_kelas = st.selectbox("🏫 Pilih Kelasmu", pilihan_kelas)
            
            pilihan_absen = ["Pilih Absen"] + [str(i) for i in range(1, 41)]
            input_absen = st.selectbox("🔢 Nomor Absen", pilihan_absen)
            input_sekolah = st.text_input("📍 Asal Sekolah", value=APP_SCHOOL)
            
            st.markdown("<br>", unsafe_allow_html=True)
            tombol_masuk = st.form_submit_button("🚀 MULAI UJIAN SEKARANG", use_container_width=True)
            
            if tombol_masuk:
                if not input_nama.strip() or input_kelas == "Pilih Kelas" or input_absen == "Pilih Absen" or not input_sekolah.strip():
                    st.error("Ops! Silakan lengkapi semua data loginmu dulu ya! 🎯")
                else:
                    st.session_state.user_data = {
                        "Nama Lengkap": input_nama,
                        "Kelas": input_kelas,
                        "No Absen": input_absen,
                        "Asal Sekolah": input_sekolah
                    }
                    
                    st.session_state.opsi_acak_soal = {}
                    for q in soal_cbt:
                        list_opsi = list(q["opsi"])
                        random.shuffle(list_opsi)
                        st.session_state.opsi_acak_soal[q["id"]] = list_opsi
                        
                    st.session_state.logged_in = True
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
        
        # Kotak Skor Langsung untuk Peserta
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
        
        # --- REVIEW KUNCI JAWABAN (WARNA BERBEDA & ACAK) ---
        st.markdown("### 🔍 Tinjauan Hasil & Kunci Jawaban")
        st.caption("Pilihan jawaban Anda bertanda bulat, sedangkan kunci jawaban yang benar berwarna hijau tebal.")
        
        for i, q in enumerate(soal_cbt):
            st.markdown(f"**Soal No. {i+1}** ({q['kategori']})")
            st.write(q["pertanyaan"])
            
            jawaban_kamu = st.session_state.jawaban_user.get(q["id"])
            kunci_benar = q["jawaban"]
            
            for opsi in st.session_state.opsi_acak_soal.get(q["id"], q["opsi"]):
                if opsi == kunci_benar:
                    if opsi == jawaban_kamu:
                        st.markdown(f"<span style='color: #16A34A; font-weight: bold;'>🟢 {opsi} (Jawaban Anda - BENAR)</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='color: #16A34A; font-weight: bold;'>✅ {opsi} (Kunci Jawaban yang Benar)</span>", unsafe_allow_html=True)
                elif opsi == jawaban_kamu:
                    st.markdown(f"<span style='color: #DC2626; font-weight: bold;'>🔴 {opsi} (Jawaban Anda - SALAH)</span>", unsafe_allow_html=True)
                else:
                    st.text(f"⚪ {opsi}")
                    
            st.markdown("---")
            
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
        st.markdown("### Lembar Kerja Soal Pilihan Ganda (Opsi Diacak)")
        
        for i, q in enumerate(soal_cbt):
            st.markdown(f"**Soal No. {i+1}** (Level: {q['level']} - {q['kategori']})")
            if q["image"]:
                st.image(q["image"], width=400)
            st.write(q["pertanyaan"])
            
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
    tab_peserta, tab_guru = st.tabs(["💻 Sesi Ujian (Siswa)", "📝 Panel Dokumen Nilai (Guru Only)"])
    
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
            Layanan Dukungan Teknis: {APP_CONTACT}
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
