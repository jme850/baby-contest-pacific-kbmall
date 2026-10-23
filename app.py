import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Konfigurasi Page
st.set_page_config(page_title="Baby Contest PACIFIC KB Mall", page_icon="👶", layout="centered")

# CSS Khas: Tetapkan Background Pink, Kotak Borang Putih, Kotak Upload Putih & Teks Hitam Jelas
st.markdown(
    """
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
    /* Paksa kotak input dan widget file uploader jadi latar belakang putih bersih & teks hitam */
    input, textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    /* Paksa kawasan tempat upload fail jadi warna putih cerah */
    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0;
        padding: 10px;
        border-radius: 8px;
    }
    [data-testid="stFileUploader"] section {
        background-color: #f8f9fa !important;
    }
    [data-testid="stFileUploader"] section * {
        color: #2c3e50 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Pastikan folder untuk simpan gambar wujud
os.makedirs("uploads/baby_photos", exist_ok=True)
os.makedirs("uploads/receipts", exist_ok=True)

# Susun Bahasa & "Created by" di bahagian atas sekali (Sebelah-menyebelah)
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    # Pilihan Bahasa (Language Selection)
    lang = st.selectbox("🌐 Choose Language / Pilih Bahasa / 选择语言", ["Bahasa Melayu", "English", "中文"])

with top_col2:
    # Paparan "Created by : Azmer" di penjuru kanan atas
    st.markdown("<div style='text-align: right; padding-top: 28px;'><span style='font-size: 11px; color: #7f8c8d; background-color: #ffffff; padding: 3px 8px; border-radius: 4px; border: 1px solid #f1f2f6;'>Created by : Azmer</span></div>", unsafe_allow_html=True)

# Kamus Teks Mengikut Bahasa
if lang == "English":
    title = "PACIFIC KB Mall Super Star Baby Contest Registration"
    period = "📅 Contest Period: 9 November - 29 November 2026"
    desc = "Please fill out the form below and upload your baby's photo along with a purchase receipt of RM100 and above."
    parent_label = "Parent's Name"
    phone_label = "Phone Number (WhatsApp)"
    baby_label = "Baby's Name"
    age_label = "Baby's Age (Months)"
    photo_label = "Upload Baby's Photo (JPG/PNG)"
    receipt_label = "Upload Receipt (RM100 & above) (JPG/PNG/PDF)"
    declaration_title = "C. PARENT / GUARDIAN DECLARATION"
    declaration_text = """
    I confirm that the information provided is true and the receipt submitted is valid and has not been used for other entries. I understand that each valid minimum purchase receipt is eligible for one (1) entry only.
    I give permission to PACIFIC KBMall to use the baby's photo for competition purposes and related promotions through the organizer's official channels.
    """
    checkbox_label = "I agree with the declaration and consent above."
    submit_label = "Submit Entry"
    error_msg = "Please complete all information, upload required files, and check the agreement box!"
    success_msg = "Congratulations! Your entry has been successfully submitted. Thank you for joining the PACIFIC KB Mall Baby Contest!"

elif lang == "中文":
    _ = lang # placeholder
    title = "PACIFIC KB Mall 超级星宝贝 婴儿比赛报名表格"
    period = "📅 比赛日期：2026年11月9日 - 11月29日"
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
    period = "📅 Tempoh Peraduan: 9 November - 29 November 2026"
    desc = "Sila isi borang di bawah dan muat naik gambar baby serta resit pembelian RM100 ke atas."
    parent_label = "Nama Ibu / Bapa"
    phone_label = "Nombor Telefon (WhatsApp)"
    baby_label = "Nama Anak"
    age_label = "Umur Anak (Bulan)"
    photo_label = "Muat naik Gambar Baby (JPG/PNG)"
    receipt_label = "Muat naik Resit Pembelian RM100 ke atas (JPG/PNG/PDF)"
    declaration_title = "C. PENGESAHAN IBU BAPA / PENJAGA"
    declaration_text = """
    Saya mengesahkan bahawa maklumat yang diberikan adalah benar dan resit yang dikemukakan adalah sah serta belum digunakan untuk penyertaan lain. Saya memahami bahawa setiap resit pembelian minimum yang sah hanya melayakkan satu (1) penyertaan.
    Saya memberi kebenaran kepada PACIFIC KBMall untuk menggunakan gambar bayi bagi tujuan pertandingan dan promosi berkaitan pertandingan ini melalui saluran rasmi penganjur.
    """
    checkbox_label = "Saya bersetuju dengan pengesahan dan kebenaran di atas."
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

# Proses bila customer tekan '
