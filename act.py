import streamlit as st
import datetime

st.set_page_config(page_title="SAFE LINK", page_icon=":heart:", layout="wide")

# --------------------------- Custom Style ---------------------------------
st.markdown("""
    <style>
    /* Import Poppins Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* General background */
    .stApp {
        background: linear-gradient(135deg, #ffe4e1, #fff0f5);
        font-family: 'Poppins', sans-serif;
        padding-bottom: 50px;
    }

    /* Floating Navbar */
    div[data-baseweb="tabs"] {
        background: rgba(255, 105, 180, 0.8);
        backdrop-filter: blur(8px);
        padding: 12px 20px;
        margin: 30px 80px 0px 80px;
        border-radius: 25px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
    }

    /* Tab Item */
    div[data-baseweb="tab"] {
        color: white;
        font-weight: 500;
        font-size: 16px;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }

    /* Tab Active */
    div[data-baseweb="tab"][aria-selected="true"] {
        background-color: white;
        color: #ff69b4;
        border-radius: 20px;
        font-weight: 600;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* Welcome Box */
    .welcome-box {
        background-color: white;
        padding: 40px 30px;
        margin: 50px auto 30px auto;
        width: 85%;
        border-radius: 30px;
        color: #ff69b4;
        text-align: center;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.1);
    }

    /* Form Container */
    .stForm {
        background-color: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.08);
        margin-top: 30px;
    }

    /* Input, Select, Textarea */
    input, textarea, select {
        background-color: #fff;
        border: 2px solid #ffb6c1;
        border-radius: 12px;
        padding: 12px;
        font-size: 14px;
    }

    /* Button */
    button {
        background: linear-gradient(135deg, #ff69b4, #ff85c1);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 20px;
        border: none;
        transition: background 0.3s ease;
    }
    button:hover {
        background: linear-gradient(135deg, #ff85c1, #ffa3d1);
        color: white;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff69b4, #ff85c1);
    }

    /* Comment Box */
    .comment-box {
        background-color: #fff0f5;
        padding: 20px;
        margin: 15px 0;
        border-radius: 20px;
        border: 1px solid #ffb6c1;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------- Logo Header ---------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("8442983a-8c2b-4de5-a763-e2365e3aad3f.png", use_container_width=True)

# --------------------------- Navigation ---------------------------
tab_home, tab_lapor, tab_status, tab_kasus, tab_faq = st.tabs(["🏠 HOME", "📝 LAPOR", "📈 STATUS", "🛡️ KASUS SEKITAR", "❓ FAQ"])

# --------------------------- Session State ---------------------------
if "reports" not in st.session_state:
    st.session_state.reports = []

if "comments_per_case" not in st.session_state:
    st.session_state.comments_per_case = {}

# --------------------------- HOME ---------------------------
with tab_home:
    st.markdown("""
    <div class='welcome-box'>
        <h2>Selamat Datang di SAFELINK!</h2>
        <p>Platform pelaporan kejadian di area BSD Link. Kami di sini untuk melindungi Anda! Jangan ragu untuk menghubungi kami.</p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------- LAPOR ---------------------------
with tab_lapor:
    st.header("Formulir Laporan Kejadian")

    with st.form("form_laporan", clear_on_submit=True):
        nama = st.text_input("Nama Pelapor (Opsional)")
        no_hp = st.text_input("Nomor Handphone (Wajib)")
        email = st.text_input("Email (Wajib)")
        tanggal = st.date_input("Tanggal Kejadian", datetime.date.today())
        waktu = st.time_input("Waktu Kejadian", datetime.datetime.now().time())
        lokasi = st.text_input("Lokasi Kejadian")
        jenis = st.selectbox("Jenis Kejadian", ["Pelecehan", "Pencurian", "Kekerasan", "Lainnya"])
        kronologi = st.text_area("Kronologi Kejadian")
        bukti = st.file_uploader("Upload Bukti (Opsional)", type=["jpg", "png", "mp4", "mov", "avi"])

        submit = st.form_submit_button("Kirim Laporan")

        if submit:
            with st.spinner("Mengirim laporan... Mohon tunggu 🙏"):
                laporan = {
                    "nama": nama if nama else "Anonim",
                    "no_hp": no_hp,
                    "email": email,
                    "tanggal": str(tanggal),
                    "waktu": str(waktu),
                    "lokasi": lokasi,
                    "jenis": jenis,
                    "kronologi": kronologi,
                    "bukti": bukti.name if bukti else None,
                    "status": "Diterima"
                }
                st.session_state.reports.append(laporan)
                st.success("✅ Laporan berhasil dikirim!")

# --------------------------- STATUS ---------------------------
with tab_status:
    st.header("Tracking Status Laporan")

    email_track = st.text_input("Masukkan Email Anda untuk Tracking")

    if st.button("Cek Status"):
        matched = [r for r in st.session_state.reports if r['email'].lower() == email_track.lower()]

        if matched:
            for idx, report in enumerate(matched):
                st.subheader(f"Laporan #{idx+1} - {report['jenis']}")
                st.write(f"Lokasi: {report['lokasi']}")
                st.write(f"Tanggal & Waktu: {report['tanggal']} {report['waktu']}")
                st.write(f"Status Saat Ini: **{report['status']}**")

                progress_map = {
                    "Diterima": (0.25, "Tahap 1/4: Diterima\nMasih ada 3 tahap lagi: Diproses → Dalam Investigasi → Selesai"),
                    "Diproses": (0.5, "Tahap 2/4: Diproses\nMasih ada 2 tahap lagi: Dalam Investigasi → Selesai"),
                    "Dalam Investigasi": (0.75, "Tahap 3/4: Dalam Investigasi\nMasih ada 1 tahap lagi: Selesai"),
                    "Selesai": (1.0, "Tahap 4/4: Selesai\nLaporan telah selesai ditangani.")
                }
                progress, label = progress_map.get(report["status"], (0.1, "Belum Diketahui"))
                st.progress(progress, text=label)

                if progress < 1.0:
                    st.info("🔄 Laporan Anda sedang dalam proses.")
                else:
                    st.success("✅ Laporan telah selesai ditindaklanjuti.")
        else:
            st.error("❌ Email tidak ditemukan dalam laporan kami.")

# --------------------------- KASUS SEKITAR ---------------------------
with tab_kasus:
    st.header("Kasus di Sekitar Anda ‼")

    kasus_list = [
        {"judul": "Silet tas di rute aeon the breeze", "waktu": "2 hari lalu", "keterangan" : "hati-hati ya guyss, barusan aku naik bsd link..."},
        {"judul": "Orang genit di rute Greenwhich sektor 1.3", "waktu": "5 hari lalu", "keterangan" : "be on the look out guys..."},
        {"judul": "Koko-koko satu geng duduk di kursi prioritas", "waktu": "6 hari lalu", "keterangan" : "ga abis pikir..."},
        {"judul": "Dicari earbuds hilang", "waktu": "1 minggu lalu", "keterangan" : "urgent! plis banget tolong guys..."}
    ] 

    search_query = st.text_input("🔎 Cari Kasus Berdasarkan Judul", "")

    filtered_kasus = [kasus for kasus in kasus_list if search_query.lower() in kasus['judul'].lower()]

    if filtered_kasus:
        for kasus in filtered_kasus:
            st.markdown(f"### 🛡️ {kasus['judul']}")
            st.caption(f"🕒 {kasus['waktu']}")
            st.write(f"{kasus['keterangan']}")

            st.subheader(f"💬 Komentar untuk {kasus['judul']}")
            form_key = f"form_komentar_{kasus['judul']}"
            with st.form(form_key, clear_on_submit=True):
                nama_komentar = st.text_input(f"Nama Anda ({kasus['judul']})")
                komentar = st.text_area(f"Komentar atau Dukungan Anda ({kasus['judul']})")
                kirim_komentar = st.form_submit_button("Kirim Komentar")

                if kirim_komentar and komentar:
                    if kasus['judul'] not in st.session_state.comments_per_case:
                        st.session_state.comments_per_case[kasus['judul']] = []
                    st.session_state.comments_per_case[kasus['judul']].append({
                        "nama": nama_komentar if nama_komentar else "Anonim",
                        "komentar": komentar
                    })
                    st.success("Komentar berhasil dikirim!")

            if kasus['judul'] in st.session_state.comments_per_case:
                for c in st.session_state.comments_per_case[kasus['judul']][::-1]:
                    st.markdown(f"""
                    <div class="comment-box">
                    <b>{c['nama']}</b><br>
                    {c['komentar']}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("Kasus tidak ditemukan. Coba kata kunci lain ya!")

# --------------------------- FAQ ---------------------------
with tab_faq:
    st.header("Frequently Asked Questions (FAQ)")
    with st.expander("Apakah ada nomor customer service yang bisa saya hubungi?"):
        st.write("Untuk saat ini belum ada nomor untuk customer service BSD Link, namun anda dapat menghubungi marketing office kami di +6221-5315-9000.")
    with st.expander("Berapa estimasi waktu tunggu tindak lanjut laporan?"):
        st.write("Penyelesaian kasus akan bervariasi tergantung kompleksitas kasus dan banyaknya kasus lain di saat itu. Namun, kasus akan mulai diinvestigasi selambat-lambatnya 5 hari kerja setelah laporan disampaikan.")
    with st.expander("Apakah saya boleh melaporkan tindak kejahatan yang dilakukan kepada penumpang lain?"):
        st.write("Ya, silakan dan silakan sertakan bukti kejadian juga.")
    with st.expander("Apakah saya bisa melapor secara anonim?"):
        st.write("Ya, Anda dapat menyamarkan nama Anda. Namun kontak (HP/Email) harus valid untuk keperluan follow up kasus.")
    with st.expander("Apa yang terjadi setelah saya melapor?"):
        st.write("Laporan Anda akan diverifikasi, diproses, dan ditindaklanjuti oleh tim terkait.")
    with st.expander("Apakah saya perlu mengunggah bukti?"):
        st.write("Ya, pengunggahan foto/video sangat disarankan sebagai bukti pendukung laporan, akan tetapi apabila tidak memungkinkan laporan tetap dapat disubmit.")
    with st.expander("Apa yang harus saya lakukan apabila saya difitnah?"):
        st.write("Silakan hubungi CS kami untuk pengaduan di nomor berikut 0812-3456-7890.")
