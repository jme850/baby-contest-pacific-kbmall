import streamlit as st
import pandas as pd
import os
import requests
import base64
from datetime import datetime

# Konfigurasi Page
st.set_page_config(page_title="Baby Contest PACIFIC KB Mall", page_icon="👶", layout="centered")

# URL Web App Google Apps Script anda
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz7Sj7TmmyYfa5tEv1Uy6WELAbrzClGsoU9mOs__DuKB1rQ6HaHt0a4PkVAu1Jf24kV/exec"

# CSS Khas: Tetapkan Background Pink, Kotak Borang Putih, Teks Hitam, & Cerahkan Kotak Upload serta Bahasa
st.markdown("""
<style>
.stApp {
    background-color: #fff0f3;
}
.stForm {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
/* Paksa semua tajuk, label, dan teks luar jadi warna hitam */
h1, h2, h3, h4, h5, h6, label, p, span, div {
    color: #2c3e50 !important;
}
/* Paksa kotak input, textarea, dan kotak selectbox jadi latar belakang putih bersih & teks hitam */
input, textarea, div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
/* Paksa teks di dalam kotak pilihan bahasa utama */
div[data-baseweb="select"] span {
    color: #000000 !important;
}
/* Paksa menu dropdown pilihan bahasa jadi putih cerah dan teks hitam */
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"], li[data-baseweb="option"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}
div[data-baseweb="popover"] *, div[data-baseweb="menu"] *, ul[data-baseweb="menu"] *, li[data-baseweb="option"] * {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
/* Kesan warna apabila sentuh/hover pada pilihan bahasa */
li[data-baseweb="option"]:hover {
    background-color: #ffe3ed !important;
    color: #000000 !important;
}
/* Paksa kawasan tempat upload fail jadi warna putih cerah sepenuhnya */
[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    border: 1px solid #dcdde1;
    padding: 12px;
    border-radius: 8px;
}
[data-testid="stFileUploader"] section {
    background-color: #ffffff !important;
    border: 2px dashed #ff4b4b !important;
}
[data-testid="stFileUploader"] section * {
    background-color: transparent !important;
    color: #2c3e50 !important;
    -webkit-text-fill-color: #2c3e50 !important;
}
/* Cantikkan dan tukar warna butang Hantar Penyertaan jadi warna tema menarik */
.stFormSubmitButton button {
    background-color: #e91e63 !important;
    color: white !important;
    font-weight: bold !important;
    width: 100% !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 10px !important;
}
.stFormSubmitButton button:hover {
    background-color: #d81b60 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Pastikan folder tempatan wujud (sebagai sandaran)
os.makedirs("uploads/baby_photos", exist_ok=True)
os.makedirs("uploads/receipts", exist_ok=True)

# Susun Bahasa & "Created by" di bahagian atas sekali (Sebelah-menyebelah)
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    # Pilihan Bahasa (Language Selection)
    lang = st.selectbox("🌐 Choose Language / Pilih Bahasa / 选择语言", ["Bahasa Melayu", "English", "中文"])
with top_col2:
    # Paparan "Created by : Azmer" diperkecilkan lagi saiznya (9px)
    st.markdown("<div style='text-align: right; padding-top: 30px;'><span style='font-size: 9px; color: #7f8c8d; background-color: #ffffff; padding: 2px 6px; border-radius: 3px; border: 1px solid #f1f2f6;'>Created by : Azmer</span></div>", unsafe_allow_html=True)

# Kamus Teks Mengikut Bahasa
if lang == "English":
    title = "PACIFIC KB Mall Super Star Baby Contest Registration"
    period = "Contest Period: 9 November - 29 November 2026"
    desc = "Please fill out the form below and upload your baby's photo along with a purchase receipt of RM100 and above."
    parent_label = "Parent's Name"
    phone_label = "Phone Number (WhatsApp)"
    baby_label = "Baby's Name"
    age_label = "Baby's Age (Months)"
    photo_label = "Upload Baby's Photo (JPG/PNG)"
    receipt_label = "Upload Receipt (RM100 & above) (JPG/PNG/PDF)"
    declaration_title = "C. PARENT / GUARDIAN DECLARATION"
    declaration_text = """
    I confirm that the information provided is true and the receipt submitted is valid and has not been used for other entries.
    I understand that each valid minimum purchase receipt is eligible for one (1) entry only.
    I give permission to PACIFIC KBMall to use the baby's photo for competition purposes and related promotions through the organizer's official channels.
    """
    checkbox_label = "I agree with the declaration and consent above."
    submit_label = "Submit Entry"
    error_msg = "Please complete all information, upload required files, and check the agreement box!"
    success_msg = "Congratulations! Your entry has been successfully submitted. Thank you for joining the PACIFIC KB Mall Baby Contest!"

elif lang == "中文":
    title = "PACIFIC KB Mall 超级星宝贝 婴儿比赛报名表格"
    period = "比赛日期：2026年11月9日 - 11月29日"
    desc = "请填写以下表格，并上传宝宝照片以及RM100或以上的购物收据。"
    parent_label = "家长姓名"
    phone_label = "电话号码 (WhatsApp)"
    baby_label = "宝宝姓名"
    age_label = "宝宝年龄 (个月)"
    photo_label = "上传宝宝照片 (JPG/PNG)"
    receipt_label = "上传购物收据 (RM100或以上) (JPG/PNG/PDF)"
    declaration_title = "C. 家长 / 监护人声明"
    declaration_text = """
    我确认所提供的信息真实有效，提交的收据有效且未用于其他参赛。我明白每张符合条件的最低消费收据仅享有一次（1）参赛资格。
    我授权 PACIFIC KBMall 通过主办方官方渠道使用宝宝照片用于比赛及相关促销活动。
    """
    checkbox_label = "我同意以上声明和授权。"
    submit_label = "提交报名"
    error_msg = "请填写所有资料、上传所需文件并勾选同意条款！"
    success_msg = "恭喜！您的报名已成功提交。感谢您参加 PACIFIC KB Mall 婴儿比赛！"

else:  # Default Bahasa Melayu
    title = "PACIFIC KB Mall Pendaftaran Si Manja SUPERSTAR"
    period = "Tempoh Peraduan: 9 November - 29 November 2026"
    desc = "Sila isi borang di bawah dan muat naik gambar baby serta resit pembelian RM100 ke atas."
    parent_label = "Nama Ibu / Bapa"
    phone_label = "Nombor Telefon (WhatsApp)"
    baby_label = "Nama Anak"
    age_label = "Umur Anak (Bulan)"
    photo_label = "Muat naik Gambar Baby (JPG/PNG)"
    receipt_label = "Muat naik Resit Pembelian RM100 ke atas (JPG/PNG/PDF)"
    declaration_title = "C. PENGESAHAN IBU BAPA / PENJAGA"
    declaration_text = """
    Ibu bapa/penjaga mengesahkan bahawa maklumat yang diberikan adalah benar dan resit yang dikemukakan adalah sah serta belum digunakan untuk penyertaan lain.
    Saya memahami bahawa setiap resit pembelian minimum yang sah hanya melayakkan satu (1) penyertaan.
    Ibu bapa/penjaga memberi kebenaran kepada PACIFIC KBMall untuk menggunakan gambar bayi bagi tujuan pertandingan dan promosi berkaitan pertandingan ini melalui saluran rasmi penganjur.
    """
    checkbox_label = "Ibu bapa/penjaga bersetuju dengan pengesahan dan kebenaran di atas."
    submit_label = "Hantar Penyertaan"
    error_msg = "Sila lengkapkan semua maklumat, muat naik fail yang diperlukan, dan tandakan kotak persetujuan!"
    success_msg = "Tahniah! Penyertaan anda telah berjaya dihantar. Terima kasih menyertai Baby Contest PACIFIC KB Mall!"

# Paparan Logo dan Tajuk Sebelah-Menyebelah
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo.png", width=140)
    except:
        st.write("")
with col2:
    st.title(title)
    st.markdown(f"### {period}")
    st.write(desc)

# Borang Pendaftaran
with st.form("baby_form"):
    parent_name = st.text_input(parent_label)
    phone_no = st.text_input(phone_label)
    baby_name = st.text_input(baby_label)
    baby_age = st.number_input(age_label, min_value=0, max_value=36, value=12)
    
    st.markdown("---")
    
    # Bahagian Upload Fail
    uploaded_baby_photo = st.file_uploader(photo_label, type=["jpg", "jpeg", "png"])
    uploaded_receipt = st.file_uploader(receipt_label, type=["jpg", "jpeg", "png", "pdf"])
    
    st.markdown("---")
    
    # Bahagian Pengesahan (Declaration)
    st.markdown(f"**{declaration_title}**")
    st.markdown(declaration_text)
    
    agree = st.checkbox(checkbox_label)
    submit_button = st.form_submit_button(label=submit_label)

# Proses bila customer tekan 'Hantar'
if submit_button:
    if not parent_name or not phone_no or not baby_name or not uploaded_baby_photo or not uploaded_receipt or not agree:
        st.error(error_msg)
    else:
        # Simpan fail sementara di server Streamlit
        baby_photo_path = os.path.join("uploads/baby_photos", f"{phone_no}_{uploaded_baby_photo.name}")
        with open(baby_photo_path, "wb") as f:
            f.write(uploaded_baby_photo.getbuffer())
            
        receipt_path = os.path.join("uploads/receipts", f"{phone_no}_{uploaded_receipt.name}")
        with open(receipt_path, "wb") as f:
            f.write(uploaded_receipt.getbuffer())

        # Hantar data dan fail ke Google Apps Script (Google Drive & Sheets)
        if GOOGLE_SCRIPT_URL != "MASUKKAN_URL_GOOGLE_APPS_SCRIPT_DI_SINI":
            try:
                baby_photo_bytes = uploaded_baby_photo.getvalue()
                baby_photo_base64 = base64.b64encode(baby_photo_bytes).decode('utf-8')
                
                receipt_bytes = uploaded_receipt.getvalue()
                receipt_base64 = base64.b64encode(receipt_bytes).decode('utf-8')
                
                payload = {
                    "parent_name": parent_name,
                    "phone_no": phone_no,
                    "baby_name": baby_name,
                    "baby_age": str(baby_age),
                    "baby_photo_name": uploaded_baby_photo.name,
                    "baby_photo_base64": baby_photo_base64,
                    "receipt_name": uploaded_receipt.name,
                    "receipt_base64": receipt_base64
                }
                requests.post(GOOGLE_SCRIPT_URL, json=payload)
            except Exception as e:
                st.error(f"Gagal hantar ke Google Drive: {e}")

        st.success(success_msg)
