import streamlit as st
import json
import os
from PIL import Image

# File untuk menyimpan data
DATA_FILE = "dompet_digital.json"
PROFILE_PICS_DIR = "profile_pics"

# Fungsi untuk memuat data dari file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Fungsi untuk menyimpan data ke file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Fungsi untuk membuat direktori foto profil jika belum ada
if not os.path.exists(PROFILE_PICS_DIR):
    os.makedirs(PROFILE_PICS_DIR)

# Fungsi untuk format Rupiah
def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

# Fungsi untuk registrasi akun
def register():
    st.subheader("📝 Registrasi Akun")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("Buat PIN (6 digit)", type="password")
    if st.button("Buat Akun"):
        if username in data:
            st.error("Akun sudah ada!")
        elif len(pin) != 6 atau not pin.isdigit():
            st.error("PIN harus 6 digit angka!")
        else:
            data[username] = {"pin": pin, "saldo": 0, "riwayat": [], "profile_pic": ""}
            save_data(data)
            st.success("Akun berhasil dibuat!")

# Fungsi untuk login
def login():
    st.subheader("🔑 Login")
    username = st.text_input("Nama Pengguna")
    pin = st.text_input("PIN", type="password")
    if st.button("Login"):
        if username not in data:
            st.error("Akun tidak ditemukan!")
        elif data[username]["pin"] != pin:
            st.error("PIN salah!")
        else:
            st.session_state["username"] = username
            st.success(f"Selamat datang, {username}!")

# Fungsi untuk menambah saldo
def tambah_saldo():
    st.subheader("💰 Tambah Saldo")
    jumlah = st.number_input("Jumlah Saldo", min_value=0, step=1)
    if st.button("Tambah"):
        data[st.session_state["username"]]["saldo"] += jumlah
        save_data(data)
        saldo_terbaru = data[st.session_state["username"]]["saldo"]
        st.success(f"Saldo berhasil ditambahkan. Saldo saat ini: {format_rupiah(saldo_terbaru)}")

# Fungsi untuk transfer
def transfer():
    st.subheader("📤 Transfer")
    penerima = st.text_input("Nama Penerima")
    jumlah = st.number_input("Jumlah Transfer", min_value=0, step=1)
    pin = st.text_input("Konfirmasi PIN", type="password")
    if st.button("Kirim"):
        if penerima not in data:
            st.error("Penerima tidak ditemukan!")
        elif jumlah <= 0 atau jumlah > data[st.session_state["username"]]["saldo"]:
            st.error("Saldo tidak cukup atau jumlah tidak valid!")
        elif data[st.session_state["username"]]["pin"] != pin:
            st.error("PIN salah!")
        else:
            data[st.session_state["username"]]["saldo"] -= jumlah
            data[penerima]["saldo"] += jumlah
            data[st.session_state["username"]]["riwayat"].append(f"Transfer ke {penerima}: {format_rupiah(jumlah)}")
            data[penerima]["riwayat"].append(f"Diterima dari {st.session_state['username']}: {format_rupiah(jumlah)}")
            save_data(data)
            st.success(f"Transfer berhasil! Anda mengirim {format_rupiah(jumlah)} ke {penerima}.")

# Fungsi untuk cek saldo
def cek_saldo():
    st.subheader("📊 Cek Saldo")
    saldo = data[st.session_state["username"]]["saldo"]
    st.info(f"Saldo Anda saat ini: {format_rupiah(saldo)}")

# Fungsi untuk cek riwayat transfer
def cek_riwayat():
    st.subheader("🧾 Riwayat Transfer")
    riwayat = data[st.session_state["username"]]["riwayat"]
    if riwayat:
        for item in riwayat:
            st.write(f"- {item}")
    else:
        st.info("Belum ada riwayat transaksi.")

# Fungsi untuk logout
def logout():
    st.subheader("Logout")
    confirm = st.radio("Apakah Anda yakin ingin logout?", ("Tidak", "Ya"))
    if confirm == "Ya":
        st.session_state.clear()
        st.success("Anda telah logout.")

# Fungsi untuk mengubah tema dan background
def change_theme():
    st.subheader("Ganti Tema dan Background")
    theme = st.selectbox("Pilih Tema", ["Default", "Dark Mode", "Light Mode", "Blue Theme", "Green Theme"])
    if st.button("Terapkan Tema"):
        if theme == "Dark Mode":
            st.markdown(
                """
                <style>
                body {
                    background-color: #181818;
                    color: #FFFFFF;
                }
                .main {
                    background-color: #181818;
                    color: #FFFFFF;
                }
                .sidebar .sidebar-content {
                    background-color: #181818;
                    color: #FFFFFF;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        elif theme == "Light Mode":
            st.markdown(
                """
                <style>
                body {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                .main {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                .sidebar .sidebar-content {
                    background-color: #FFFFFF;
                    color: #000000;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        elif theme == "Blue Theme":
            st.markdown(
                """
                <style>
                body {
                    background-color: #e0f7fa;
                    color: #00796b;
                }
                .main {
                    background-color: #e0f7fa;
                    color: #00796b;
                }
                .sidebar .sidebar-content {
                    background-color: #e0f7fa;
                    color: #00796b;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        elif theme == "Green Theme":
            st.markdown(
                """
                <style>
                body {
                    background-color: #d0f0c0;
                    color: #4caf50;
                }
                .main {
                    background-color: #d0f0c0;
                    color: #4caf50;
                }
                .sidebar .sidebar-content {
                    background-color: #d0f0c0;
                    color: #4caf50;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <style>
                body {
                    background: linear-gradient(to right, #ff758c, #ff7eb3);
                }
                .main {
                    background: rgba(255, 255, 255, 0.8);
                    border-radius: 10px;
                    padding: 20px;
                }
                .sidebar .sidebar-content {
                    background: linear-gradient(to right, #ff758c, #ff7eb3);
                    color: #FFFFFF;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

# Fungsi untuk mengganti foto profil
def change_profile_pic():
    st.subheader("Ganti Foto Profil")
    uploaded_file = st.file_uploader("Pilih file gambar", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        profile_pic_path = os.path.join(PROFILE_PICS_DIR, f
                                                profile_pic_path = os.path.join(PROFILE_PICS_DIR, f"{st.session_state['username']}.png")
        with open(profile_pic_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image = Image.open(profile_pic_path)
        image = image.resize((200, 200))
        image = image.convert("RGBA")
        circle_image = Image.new("L", (200, 200), 0)
        Image.Draw.Draw(circle_image).ellipse((0, 0, 200, 200), fill=255)
        circular_image = Image.new("RGBA", (200, 200))
        circular_image.paste(image, (0, 0), mask=circle_image)
        circular_image.save(profile_pic_path)
        data[st.session_state['username']]["profile_pic"] = profile_pic_path
        save_data(data)
        st.success("Foto profil berhasil diubah!")

# Inisialisasi data
data = load_data()

# Streamlit: Header dengan latar belakang animasi uang
st.markdown("""
    <div style="background: linear-gradient(to right, #ff758c, #ff7eb3); padding: 15px; border-radius: 10px;">
        <h1 style="color: white; text-align: center;">🌐 Dompet Digital</h1>
    </div>
    <style>
        body {
            background: url('https://media.giphy.com/media/11ISwbgCxEzMyY/giphy.gif') no-repeat center center fixed;
            background-size: cover;
        }
        .main > div {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Nama pengguna di atas sidebar
if "username" in st.session_state:
    st.sidebar.subheader(f"Selamat datang, {st.session_state['username']}!")

    # Menampilkan foto profil
    profile_pic_path = data[st.session_state['username']].get("profile_pic", "")
    if profile_pic_path and os.path.exists(profile_pic_path):
        st.sidebar.image(profile_pic_path, caption="Foto Profil", use_column_width=True, output_format="PNG", clamp=True)

    # Menu profil dengan pengaturan, bantuan, dan ganti password
    with st.sidebar.expander("🔧 Profil"):
        with st.expander("Pengaturan"):
            change_theme()
            change_profile_pic()
        with st.expander("Bantuan"):
            st.write("Silakan pilih opsi berikut jika Anda membutuhkan bantuan:")
            if st.button("Saran"):
                st.write("Terima kasih atas saran Anda!")
            if st.button("Ajukan"):
                st.write("Silakan ajukan pertanyaan Anda!")
        if st.button("Ganti Password"):
            new_pin = st.text_input("PIN Baru (6 digit)", type="password")
            if st.button("Simpan PIN Baru"):
                if len(new_pin) != 6 atau not new_pin.isdigit():
                    st.error("PIN harus 6 digit angka!")
                else:
                    data[st.session_state['username']]["pin"] = new_pin
                    save_data(data)
                    st.success("PIN berhasil diganti!")

    menu = st.sidebar.radio("Menu", ["Tambah Saldo", "Transfer", "Cek Saldo", "Riwayat Transfer", "Logout"])
    
    if menu == "Tambah Saldo":
        tambah_saldo()
    elif menu == "Transfer":
        transfer()
    elif menu == "Cek Saldo":
        cek_saldo()
    elif menu == "Riwayat Transfer":
        cek_riwayat()
    elif menu == "Logout":
        logout()
else:
    menu = st.sidebar.radio("Menu", ["Login", "Registrasi"])
    
    if menu == "Login":
        login()
    elif menu == "Registrasi":
        register()
