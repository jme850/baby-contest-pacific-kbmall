import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Pastikan folder untuk simpan gambar wujud
os.makedirs("uploads/baby_photos", exist_ok=True)
os.makedirs("uploads/receipts", exist_ok=True)

st.title("?? Pendaftaran Baby Contest")
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
            
        # Simpan data teks ke dalam fail CSV
        data = {
            "Tarikh Masa": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Nama Ibu/Bapa": [parent_name],
            "No Telefon": [phone_no],
            "Nama Baby": [baby_name],
            "Umur Baby (Bulan)": [baby_age],
            "Fail Gambar": [baby_photo_path],
            "Fail Resit": [receipt_path]
        }
        
        df = pd.DataFrame(data)
        csv_file = "submissions.csv"
        
        if not os.path.exists(csv_file):
            df.to_csv(csv_file, index=False)
        else:
            df.to_csv(csv_file, mode='a', header=False, index=False)
            
        st.success("Tahniah! Penyertaan anda telah berjaya dihantar. Semoga berjaya! ??")