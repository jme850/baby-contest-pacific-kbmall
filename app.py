import base64
from datetime import datetime
import os
import pandas as pd
import requests
import streamlit as st

# Konfigurasi Page
st.set_page_config(
    page_title="Baby Contest PACIFIC KB Mall", page_icon="👶", layout="centered"
)

# URL SheetDB anda
SHEETDB_URL = "https://sheetdb.io/api/v1/66qrdlbot0eln"

# CSS Khas
st.markdown(
    """
<style>
.stApp { background-color: #fff0f3; }
.stForm { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
h1, h2, h3, h4, h5, h6, label, p, span, div { color: #2c3e50 !important; }
input, textarea, div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
div[data-baseweb="select"] span { color: #000000 !important; }
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"], li[data-baseweb="option"] { background-color: #ffffff !important; color: #000000 !important; }
div[data-baseweb="popover"] *, div[data-baseweb="menu"] *, ul[data-baseweb="menu"] *, li[data-baseweb="option"] * { background-color: #ffffff !important; color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
li[data-baseweb="option"]:hover { background-color: #ffe3ed !important; color: #000000 !important; }
[data-testid="stFileUploader"] { background-color: #ffffff !important; border: 1px solid #dcdde1; padding: 12px; border-radius: 8px; }
[data-testid="stFileUploader"] section { background-color: #ffffff !important; border: 2px dashed #ff4b4b !important; }
[data-testid="stFileUploader"] section * { background-color: transparent !important; color: #2c3e50 !important; -webkit-text-fill-color: #2c3e50 !important; }
.stFormSubmitButton button { background-color: #e91e63 !important; color: white !important; font-weight: bold !important; width: 100% !important; border-radius: 8px !important; border: none !important; padding: 10px !important; }
.stFormSubmitButton button:hover { background-color: #d81b60 !important; color: white !important; }
</style>
""",
    unsafe_allow_html=True,
)

os.makedirs("uploads/baby_photos", exist_ok=True)
os.makedirs("uploads/receipts", exist_ok=True)

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
  lang = st.selectbox(
      "🌐 Choose Language / Pilih Bahasa / 选择语言",
      ["Bahasa Melayu", "English", "中文"],
  )
with top_col2:
  st.markdown(
      "<div style='text-align: right; padding-top: 30px;'><span style='font-size:"
      " 9px; color: #7f8c8d; background-color: #ffffff; padding: 2px 6px;"
      " border-radius: 3px; border: 1px solid #f1f2f6;'>Created by :"
      " Azmer</span></div>",
      unsafe_allow_html=True,
  )

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
  declaration_text = (
      "I confirm that the information provided is true and the receipt"
      " submitted is valid."
  )
  checkbox_label = "I agree with the declaration and consent above."
  submit_label = "Submit Entry"
  error_msg = "Please complete all information, upload required files, and check the agreement box!"
  success_msg = "Congratulations! Your entry has been successfully submitted."
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
  declaration_text = "我确认所提供的信息真实有效，提交的收据有效。"
  checkbox_label = "我同意以上声明和授权。"
  submit_label = "提交报名"
  error_msg = "请填写所有资料、上传所需文件并勾选同意条款！"
  success_msg = "恭喜！您的报名已成功提交。"
else:
  title = "PACIFIC KB Mall Pendaftaran Si Manja SUPERSTAR"
  period = "Tempoh Peraduan: 9 November - 29 November 2026"
  desc = (
      "Sila isi borang di bawah dan muat naik gambar baby serta resit pembelian"
      " RM100 ke atas."
  )
  parent_label = "Nama Ibu / Bapa"
  phone_label = "Nombor Telefon (WhatsApp)"
  baby_label = "Nama Anak"
  age_label = "Umur Anak (Bulan)"
  photo_label = "Muat naik Gambar Baby (JPG/PNG)"
  receipt_label = "Muat naik Resit Pembelian RM100 ke atas (JPG/PNG/PDF)"
  declaration_title = "C. PENGESAHAN IBU BAPA / PENJAGA"
  declaration_text = (
      "Ibu bapa/penjaga mengesahkan bahawa maklumat yang diberikan adalah benar."
  )
  checkbox_label = "Ibu bapa/penjaga bersetuju dengan pengesahan dan kebenaran di atas."
  submit_label = "Hantar Penyertaan"
  error_msg = "Sila lengkapkan semua maklumat, muat naik fail yang diperlukan, dan tandakan kotak persetujuan!"
  success_msg = "Tahniah! Penyertaan anda telah berjaya dihantar."

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


# Fungsi untuk hantar imej ke pelayan ImgBB dan pastikan dapat URL
def upload_to_imgbb(uploaded_file):
  if uploaded_file is None:
    return "Tiada fail"
  try:
    url = "https://api.imgbb.com/1/upload"
    file_bytes = uploaded_file.getvalue()
    payload = {
        "key": "6d207e02c9842a22533b3d57d2a57173",
        "image": base64.b64encode(file_bytes).decode("utf-8"),
    }
    response = requests.post(url, data=payload)
    result = response.json()
    if result.get("success"):
      return result["data"]["url"]
    else:
      # Paparkan mesej ralat sebenar jika gagal dari ImgBB
      error_msg = result.get("error", {}).get("message", "Gagal upload")
      return f"Ralat: {error_msg}"
  except Exception as e:
    return f"Ralat: {str(e)}"


with st.form("baby_form"):
  parent_name = st.text_input(parent_label)
  phone_no = st.text_input(phone_label)
  baby_name = st.text_input(baby_label)
  baby_age = st.number_input(age_label, min_value=0, max_value=36, value=12)

  st.markdown("---")
  uploaded_baby_photo = st.file_uploader(
      photo_label, type=["jpg", "jpeg", "png"]
  )
  uploaded_receipt = st.file_uploader(
      receipt_label, type=["jpg", "jpeg", "png", "pdf"]
  )

  st.markdown("---")
  st.markdown(f"**{declaration_title}**")
  st.markdown(declaration_text)

  agree = st.checkbox(checkbox_label)
  submit_button = st.form_submit_button(label=submit_label)

if submit_button:
  if (
      not parent_name
      or not phone_no
      or not baby_name
      or not uploaded_baby_photo
      or not uploaded_receipt
      or not agree
  ):
    st.error(error_msg)
  else:
    # Simpan salinan lokal
    baby_photo_path = os.path.join(
        "uploads/baby_photos", f"{phone_no}_{uploaded_baby_photo.name}"
    )
    with open(baby_photo_path, "wb") as f:
      f.write(uploaded_baby_photo.getbuffer())

    receipt_path = os.path.join(
        "uploads/receipts", f"{phone_no}_{uploaded_receipt.name}"
    )
    with open(receipt_path, "wb") as f:
      f.write(uploaded_receipt.getbuffer())

    with st.spinner("Sedang memproses dan menghantar ke Google Sheets..."):
      try:
        # Dapatkan URL imej dari ImgBB
        baby_photo_url = upload_to_imgbb(uploaded_baby_photo)
        receipt_url = upload_to_imgbb(uploaded_receipt)

        # Hantar data ke SheetDB
        data_to_send = {
            "Tarikh": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Parent Name": parent_name,
            "Phone No": phone_no,
            "Baby Name": baby_name,
            "Baby Age": str(baby_age),
            "Baby Photo": baby_photo_url,
            "Receipt": receipt_url,
        }

        response = requests.post(SHEETDB_URL, json=data_to_send)

        if response.status_code in [200, 201]:
          st.success(success_msg)
        else:
          st.error(f"Ralat pelayan: {response.text}")

      except Exception as e:
        st.error(f"Gagal menghantar data: {e}")
