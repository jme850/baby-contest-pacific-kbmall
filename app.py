import base64
from datetime import datetime
import os
import requests
import streamlit as st

# Konfigurasi Page
st.set_page_config(
    page_title="Baby Contest PACIFIC KB Mall", page_icon="👶", layout="centered"
)

# URL SheetDB anda & URL Google Apps Script untuk simpan gambar ke Drive
SHEETDB_URL = "https://sheetdb.io/api/v1/hl16pu8rhve9t"
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxHOtsTVHOvShwZgmkFh3I0Vtt17fPeIFGI5G28xJH0hShIQJvBbmR0nMn-jTmHrDQQ/exec"

# CSS Khas
st.markdown(
    """
<style>
.stApp { background-color: #fff0f3; }
.stForm { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
h1, h2, h3, h4, h5, h6, label, p, span, div { color: #2c3e50 !important; }
input, textarea, div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
.stFormSubmitButton button { background-color: #e91e63 !important; color: white !important; font-weight: bold !important; width: 100% !important; border-radius: 8px !important; border: none !important; padding: 10px !important; }
.stFormSubmitButton button:hover { background-color: #d81b60 !important; color: white !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("PACIFIC KB Mall Pendaftaran Si Manja SUPERSTAR")
st.write("Sila isi borang di bawah untuk menyertai peraduan.")


# Fungsi baru untuk simpan gambar/fail terus ke Google Drive & dapatkan URL
def upload_to_drive(uploaded_file, folder_name):
  if uploaded_file is None:
    return "Tiada fail"
  try:
    file_bytes = uploaded_file.getvalue()
    file_base64 = (
        f"data:{uploaded_file.type};base64,"
        + base64.b64encode(file_bytes).decode("utf-8")
    )

    payload = {
        "fileBase64": file_base64,
        "fileName": uploaded_file.name,
        "folderName": folder_name,
    }

    response = requests.post(APPS_SCRIPT_URL, json=payload)
    result = response.json()

    if result.get("status") == "success":
      return result.get("fileUrl")
    else:
      return "Gagal upload ke Drive"
  except Exception as e:
    return f"Ralat: {str(e)}"


with st.form("baby_form"):
  parent_name = st.text_input("Nama Ibu / Bapa")
  phone_no = st.text_input("Nombor Telefon (WhatsApp)")
  baby_name = st.text_input("Nama Anak")
  baby_age = st.number_input(
      "Umur Anak (Bulan)", min_value=0, max_value=36, value=12
  )

  st.markdown("---")
  uploaded_baby_photo = st.file_uploader(
      "Muat naik Gambar Baby", type=["jpg", "jpeg", "png"]
  )
  uploaded_receipt = st.file_uploader(
      "Muat naik Resit Pembelian", type=["jpg", "jpeg", "png", "pdf"]
  )

  agree = st.checkbox("Saya bersetuju dengan terma dan syarat peraduan.")
  submit_button = st.form_submit_button(label="Hantar Penyertaan")

if submit_button:
  if (
      not parent_name
      or not phone_no
      or not baby_name
      or not uploaded_baby_photo
      or not uploaded_receipt
      or not agree
  ):
    st.error("Sila lengkapkan semua maklumat dan tandakan kotak persetujuan!")
  else:
    with st.spinner(
        "Sedang memproses gambar ke Drive & hantar data ke SheetDB..."
    ):
      try:
        # Dapatkan URL fail dari Google Drive
        baby_photo_url = upload_to_drive(uploaded_baby_photo, "Baby_Photos")
        receipt_url = upload_to_drive(uploaded_receipt, "Receipts")

        # Format tarikh sebagai Teks Biasa supaya Google Sheets tidak tukar jadi nombor siri
        formatted_date = datetime.now().strftime("'%Y-%m-%d %H:%M:%S")

        # Data asal yang dihantar terus ke SheetDB anda
        data_to_send = {
            "Tarikh": formatted_date,
            "Parent Name": parent_name,
            "Phone No": str(phone_no),
            "Baby Name": baby_name,
            "Baby Age": str(baby_age),
            "Baby Photo": baby_photo_url,
            "Receipt": receipt_url,
        }

        response = requests.post(SHEETDB_URL, json=data_to_send)

        if response.status_code in [200, 201]:
          st.success("Tahniah! Penyertaan anda telah berjaya dihantar.")
        else:
          st.error(f"Ralat pelayan SheetDB: {response.text}")

      except Exception as e:
        st.error(f"Gagal menghantar data: {e}")
