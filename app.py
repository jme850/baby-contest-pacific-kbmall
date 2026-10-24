import base64
from datetime import datetime, timedelta
import os
import requests
import streamlit as st

# Konfigurasi Page
st.set_page_config(
    page_title="Baby Contest PACIFIC KB Mall", page_icon="👶", layout="centered"
)

# URL SheetDB anda & URL Google Apps Script untuk simpan gambar ke Drive
SHEETDB_URL = "https://sheetdb.io/api/v1/hl16pu8rhve9t"
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxYyv_AELPBJz5v62dVbs-jPDXhjQNLVf2Lvg52gZdqRiZnBF-SWbddkDigCyXWni0wyQ/exec"

# CSS Khas (Tema Cerah / Terang - Paksa kotak uploader jadi putih bersih)
st.markdown(
    """
<style>
.stApp { background-color: #fff5f7; }
.stForm { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #ffccd5; }
h1, h2, h3, h4, h5, h6, label, p, span, div { color: #2c3e50 !important; }
input, textarea, div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #000000 !important; -webkit-text-fill-color: #000000 !important; border: 1px solid #ccc !important; }

/* Paksa kotak muat naik fail (file uploader) jadi warna cerah */
[data-testid="stFileUploader"] { background-color: #ffffff !important; padding: 15px; border-radius: 8px; border: 1px solid #ffccd5; }
[data-testid="stFileUploader"] section { background-color: #faf0f2 !important; border: 2px dashed #e91e63 !important; }
[data-testid="stFileUploader"] section div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small { color: #2c3e50 !important; }

.stFormSubmitButton button { background-color: #e91e63 !important; color: white !important; font-weight: bold !important; width: 100% !important; border-radius: 8px !important; border: none !important; padding: 10px !important; }
.stFormSubmitButton button:hover { background-color: #d81b60 !important; color: white !important; }
.terms-box { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #e91e63; font-size: 13px; margin-bottom: 15px; line-height: 1.5; color: #333 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# Kamus Terjemahan Bahasa (BM, English, 中文)
translations = {
    "Bahasa Melayu": {
        "title": "PACIFIC KB Mall Pendaftaran Si Manja SUPERSTAR",
        "desc": "Sila isi borang di bawah untuk menyertai peraduan.",
        "parent_name": "Nama Ibu / Bapa",
        "phone_no": "Nombor Telefon (WhatsApp)",
        "baby_name": "Nama Anak",
        "baby_age": "Umur Anak (Bulan)",
        "baby_photo": "Muat naik Gambar Baby",
        "receipt": "Muat naik Resit Pembelian",
        "terms": (
            "<b>C. PENGESAHAN IBU BAPA / PENJAGA</b><br>Saya mengesahkan bahawa"
            " maklumat yang diberikan adalah benar dan resit yang dikemukakan"
            " adalah sah serta belum digunakan untuk penyertaan lain. Saya"
            " memahami bahawa setiap resit pembelian minimum RM50 yang sah"
            " hanya melayakkan satu (1) penyertaan.<br>Saya memberi kebenaran"
            " kepada Pacific KBMall untuk menggunakan gambar bayi bagi tujuan"
            " pertandingan dan promosi berkaitan pertandingan ini melalui saluran"
            " rasmi penganjur."
        ),
        "agree": "Saya bersetuju dengan pengesahan dan kebenaran di atas.",
        "submit": "Hantar Penyertaan",
        "error_fill": (
            "Sila lengkapkan semua maklumat dan tandakan kotak persetujuan!"
        ),
        "spinner": (
            "Sedang memproses gambar ke Drive & hantar data ke SheetDB..."
        ),
        "success": "Tahniah! Penyertaan anda telah berjaya dihantar.",
        "error_db": "Ralat pelayan SheetDB: ",
        "error_fail": "Gagal menghantar data: ",
    },
    "English": {
        "title": "PACIFIC KB Mall SUPERSTAR Baby Contest Registration",
        "desc": "Please fill out the form below to join the contest.",
        "parent_name": "Parent's Name",
        "phone_no": "Phone Number (WhatsApp)",
        "baby_name": "Baby's Name",
        "baby_age": "Baby's Age (Months)",
        "baby_photo": "Upload Baby Photo",
        "receipt": "Upload Purchase Receipt",
        "terms": (
            "<b>C. PARENT / GUARDIAN CONFIRMATION</b><br>I confirm that the"
            " information provided is true and the receipt submitted is valid"
            " and has not been used for other entries. I understand that each"
            " valid minimum purchase receipt of RM50 entitles one (1) entry only.<br>I"
            " grant permission to Pacific KBMall to use the baby's photo for"
            " contest and promotional purposes through the organizer's official"
            " channels."
        ),
        "agree": "I agree to the above confirmation and authorization.",
        "submit": "Submit Entry",
        "error_fill": "Please complete all information and check the agreement box!",
        "spinner": "Processing image to Drive & sending data to SheetDB...",
        "success": "Congratulations! Your entry has been successfully submitted.",
        "error_db": "SheetDB server error: ",
        "error_fail": "Failed to send data: ",
    },
    "中文": {
        "title": "PACIFIC KB Mall 超级巨星宝宝大赛 报名表格",
        "desc": "请填写以下表格以参加比赛。",
        "parent_name": "父母姓名",
        "phone_no": "电话号码 (WhatsApp)",
        "baby_name": "宝宝姓名",
        "baby_age": "宝宝年龄 (个月)",
        "baby_photo": "上传宝宝照片",
        "receipt": "上传购买收据",
        "terms": (
            "<b>C. 父母/监护人确认</b><br>我确认所提供的信息属实，提交的收据有效且未用于其他参赛。我理解每张满"
            " RM50 的有效购物收据仅限获得一次 (1) 参赛资格。<br>我授权 Pacific"
            " KBMall 通过主办方官方渠道使用宝宝照片用于比赛及相关促销活动。"
        ),
        "agree": "我同意以上确认与授权。",
        "submit": "提交报名",
        "error_fill": "请填写所有信息并勾选同意条款！",
        "spinner": "正在处理照片并提交数据至服务器...",
        "success": "恭喜！您的参赛申请已成功提交。",
        "error_db": "服务器错误: ",
        "error_fail": "提交数据失败: ",
    },
}

# Pilihan Bahasa di Penjuru Kanan Atas & Logo di Kiri
col_logo, col_lang = st.columns([2, 2])

with col_logo:
  if os.path.exists("logo.png"):
    st.image("logo.png", width=140)

with col_lang:
  selected_lang = st.selectbox(
      "Language / Bahasa / 语言", ["Bahasa Melayu", "English", "中文"], index=0
  )
  st.markdown(
      "<div style='text-align: right; font-size: 11px; color: #666;'>Created"
      " by: Azmer</div>",
      unsafe_allow_html=True,
  )

t = translations[selected_lang]

st.title(t["title"])
st.write(t["desc"])


# Fungsi untuk simpan gambar/fail terus ke Google Drive & dapatkan URL
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
  parent_name = st.text_input(t["parent_name"])
  phone_no = st.text_input(t["phone_no"])
  baby_name = st.text_input(t["baby_name"])
  baby_age = st.number_input(t["baby_age"], min_value=0, max_value=36, value=12)

  st.markdown("---")
  uploaded_baby_photo = st.file_uploader(
      t["baby_photo"], type=["jpg", "jpeg", "png"]
  )
  uploaded_receipt = st.file_uploader(
      t["receipt"], type=["jpg", "jpeg", "png", "pdf"]
  )

  st.markdown("---")
  st.markdown(f"<div class='terms-box'>{t['terms']}</div>", unsafe_allow_html=True)

  agree = st.checkbox(t["agree"])
  submit_button = st.form_submit_button(label=t["submit"])

if submit_button:
  if (
      not parent_name
      or not phone_no
      or not baby_name
      or not uploaded_baby_photo
      or not uploaded_receipt
      or not agree
  ):
    st.error(t["error_fill"])
  else:
    with st.spinner(t["spinner"]):
      try:
        # Dapatkan URL fail dari Google Drive
        baby_photo_url = upload_to_drive(uploaded_baby_photo, "Baby_Photos")
        receipt_url = upload_to_drive(uploaded_receipt, "Receipts")

        # Tetapkan waktu mengikut zon masa Malaysia (UTC+8)
        malaysia_time = datetime.utcnow() + timedelta(hours=8)
        formatted_date = malaysia_time.strftime("'%Y-%m-%d %H:%M:%S")

        # Data yang dihantar ke SheetDB
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
          st.success(t["success"])
        else:
          st.error(t["error_db"] + response.text)

      except Exception as e:
        st.error(t["error_fail"] + str(e))
