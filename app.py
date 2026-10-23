import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Pastikan folder untuk simpan gambar wujud
os.makedirs("uploads/baby_photos", exist_ok=True)
os.makedirs("uploads/receipts", exist_ok=True)

st.title("Pacific Kbmall Pendaftaran Si Manja SUPERSTAR")
st.write("Sila isi borang di bawah dan muat naik gambar baby serta resit pembelian RM100 ke atas.")

# Borang Pendaftaran
with st.form("baby_form"):
    parent_name = st.text_input("Nama Ibu / Bapa")
    phone_no = st.text_input("Nombor Telefon (WhatsApp)")
    baby_name = st.text_input("Nama Anak")
    baby_age = st.number_input("Umur Anak (Bulan)", min_value=0, max_value=36, value=12)
    
    st.markdown("---")
    
    # Bahagian Upload Fail
    uploaded_baby_photo = st.file_uploader("Muat naik Gambar Baby (JPG/PNG)", type=["jpg", "jpeg", "png"])
    uploaded_receipt = st.file_uploader("Muat naik Resit Pembelian RM100 ke atas (JPG/PNG/PDF)", type=["jpg", "jpeg", "png", "pdf"])
    
    submit_button = st.form_submit_button(label="Hantar Penyertaan")

# Proses bila customer tekan 'Hantar'
if submit_button:
    if not parent_name or not phone_no or not baby_name or not uploaded_baby_photo or not uploaded_receipt:
        st.error("Sila lengkapkan semua maklumat dan muat naik fail yang diperlukan!")
    else:
        # Simpan fail gambar baby
        baby_photo_path = os.path.join("uploads/baby_photos", f"{phone_no}_{uploaded_baby_photo.name}")
        with open(baby_photo_path, "wb") as f:
            f.write(uploaded_baby_photo.getbuffer())
            
        # Simpan fail resit
        receipt_path = os.path.join("uploads/receipts", f"{phone_no}_{uploaded_receipt.name}")
        with open(receipt_path, "wb") as f:
            f.write(uploaded_receipt.getbuffer())
            
        st.success("Tahniah! Penyertaan anda telah berjaya dihantar. Terima kasih menyertai Baby Contest Pacific KB Mall!")

# Bahagian bawah (Created by di sebelah kanan, saiz kecil)
st.markdown("---")
st.markdown("<p style='text-align: right; font-size: 12px; color: grey;'>Created by : Azmer</p>", unsafe_allow_html=True)
