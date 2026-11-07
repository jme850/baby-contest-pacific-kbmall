import base64
from datetime import datetime, timedelta
import os
import requests
import streamlit as st

# Konfigurasi Page
st.set_page_config(
    page_title="Baby Contest PACIFIC KB Mall", page_icon="👶", layout="centered"
)

# URL SheetDB & Google Apps Script
SHEETDB_URL = "https://sheetdb.io/api/v1/hl16pu8rhve9t"
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxYyv_AELPBJz5v62dVbs-jPDXhjQNLVf2Lvg52gZdqRiZnBF-SWbddkDigCyXWni0wyQ/exec"

# CSS Khas (Tema Poster & Warna Cerah)
st.markdown(
    """
<style>
.stApp { background-color: #fff5f7; }
.stForm { background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #ffccd5; }
h1, h2, h3, h4, h5, h6, label, p, span, div { color: #2c3e50 !important; }
input, textarea, div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #000000 !important; -webkit-text-fill-color: #000000 !important; border: 1px solid #ccc !important; }

/* Kotak Muat Naik Fail */
[data-testid="stFileUploader"] { background-color: #ffffff !important; padding: 15px; border-radius: 8px; border: 1px solid #ffccd5; }
[data-testid="stFileUploader"] section { background-color: #faf0f2 !important; border: 2px dashed #e91e63 !important; }
[data-testid="stFileUploader"] section div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small { color: #2c3e50 !important; }

.stFormSubmitButton button { background-color: #e91e63 !important; color: white !important; font-weight: bold !important; width: 100% !important; border-radius: 8px !important; border: none !important; padding: 12px !important; }
.stFormSubmitButton button:hover { background-color: #d81b60 !important; color: white !important; }

.terms-box { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #e91e63; font-size: 13px; margin-bottom: 15px; line-height: 1.5; color: #333 !important; }
.period-badge { background-color: #ffe6eb; color: #e91e63 !important; padding: 8px 15px; border-radius: 8px; font-weight: bold; font-size: 15px; display: block; text-align: center; margin-bottom: 20px; border: 1px solid #ffccd5; }
.prizes-box { background-color: #fff0f3; padding: 15px; border-radius: 10px; border: 2px dashed #e91e63; margin-bottom: 20px; text-align: center; }
.prizes-box h4 { color: #d81b60 !important; margin-bottom: 10px; }
.criteria-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #ffccd5; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.criteria-box h4 { color: #d81b60 !important; margin-bottom: 10px; text-align: center; }
.dates-box { background-color: #fff8f9; padding: 15px; border-radius: 10px; border: 1px solid #ffccd5; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.dates-box h4 { color: #d81b60 !important; margin-bottom: 10px; text-align: center; }
</style>
""",
    unsafe_allow_html=True,
)

# Paparkan "Created By : Azmer" di bahagian paling atas kanan
st.markdown(
    "<div style='text-align: right; font-size: 11px; color: #888888;"
    " margin-bottom: -10px; font-weight: bold;'>Created By : Azmer</div>",
    unsafe_allow_html=True,
)

# Kamus Terjemahan Bahasa (BM, English, 中文, தமிழ்)
translations = {
    "Bahasa Melayu": {
        "title": "PACIFIC KB Mall - Si Manja SUPERSTAR!",
        "subtitle": "Show Your Baby, Let Them Shine! (BABY PHOTO CONTEST 2026)",
        "period": (
            "📅 Tarikh Peraduan: 9 November - 29 November 2026 (PACIFIC KB"
            " MALL KOTA BHARU)"
        ),
        "desc": (
            "Sila isi maklumat di bawah untuk pendaftaran penyertaan rasmi."
            " (Syarat Pembelian Minimum: RM100)"
        ),
        "prizes_title": "🏆 HADIAH MENARIK",
        "prizes_text": (
            "🥇 <b>Johan:</b> RM300 | 🥈 <b>Naib Johan:</b> RM200 | 🥉"
            " <b>Tempat Ketiga:</b> RM100<br>🎁 Serta Hadiah Saguhati x1 RM50"
        ),
        "criteria_title": "📊 KRITERIA PENILAIAN",
        "criteria_text": (
            "👶 Kecomelan & ekspresi: <b>40%</b><br>📸 Kreativiti gambar:"
            " <b>20%</b><br>🌟 Keunikan & daya tarikan: <b>10%</b><br>❤️ Undian"
            " media sosial: <b>30%</b>"
        ),
        "dates_title": "📅 TARIKH PENTING",
        "dates_text": (
            "📝 <b>9 - 25 November 2026:</b> Pendaftaran & pengesahan"
            " resit<br>📢 <b>26 - 28 November 2026:</b> Promosi peserta &"
            " penilaian<br>🏆 <b>29 November 2026:</b> Pengumuman pemenang"
        ),
        "parent_name": "Nama Ibu / Bapa",
        "phone_no": "Nombor Telefon (WhatsApp)",
        "baby_name": "Nama Anak",
        "baby_age": "Umur Anak (Bulan - Terbuka 0 hingga 36 bulan)",
        "baby_photo": "Muat naik Gambar Baby",
        "receipt": "Muat naik Resit Pembelian (Min. RM100 di Vendor Baby Fair)",
        "terms": (
            "<b>SYARAT & PENGESAHAN PENYERTAAN:</b><br>• Terbuka kepada bayi"
            " berumur 0 - 36 bulan.<br>• Setiap pembelian minimum RM100"
            " melayakkan satu (1) penyertaan sahaja.<br>• Setiap resit hanya"
            " boleh digunakan sekali dan wajib dikemukakan kepada admin untuk"
            " disahkan.<br>• Keputusan pihak penganjur adalah muktamad.<br>• Saya"
            " memberi kebenaran kepada Pacific KB Mall untuk menggunakan"
            " gambar bayi bagi tujuan promosi."
        ),
        "agree": "Saya bersetuju dengan terma dan syarat yang ditetapkan.",
        "submit": "Hantar Penyertaan Rasmi",
        "error_fill": (
            "Sila lengkapkan semua butiran dan tandakan kotak persetujuan!"
        ),
        "spinner": (
            "Sedang memproses gambar ke Drive & hantar data ke SheetDB..."
        ),
        "success": (
            "Tahniah! Penyertaan Si Manja anda telah berjaya dihantar."
        ),
        "error_db": "Ralat pelayan SheetDB: ",
        "error_fail": "Gagal menghantar data: ",
    },
    "English": {
        "title": "PACIFIC KB Mall - Si Manja SUPERSTAR!",
        "subtitle": "Show Your Baby, Let Them Shine! (BABY PHOTO CONTEST 2026)",
        "period": (
            "📅 Contest Period: November 9 - November 29, 2026 (PACIFIC KB MALL"
            " KOTA BHARU)"
        ),
        "desc": (
            "Please fill out the form below to register. (Minimum Purchase:"
            " RM100)"
        ),
        "prizes_title": "🏆 EXCITING PRIZES",
        "prizes_text": (
            "🥇 <b>Champion:</b> RM300 | 🥈 <b>1st Runner Up:</b> RM200 | 🥉"
            " <b>2nd Runner Up:</b> RM100<br>🎁 Consolation Prizes x1 RM50"
        ),
        "criteria_title": "📊 EVALUATION CRITERIA",
        "criteria_text": (
            "👶 Cuteness & Expression: <b>40%</b><br>📸 Photo Creativity:"
            " <b>20%</b><br>🌟 Uniqueness & Appeal: <b>10%</b><br>❤️ Social"
            " Media Votes: <b>30%</b>"
        ),
        "dates_title": "📅 IMPORTANT DATES",
        "dates_text": (
            "📝 <b>November 9 - 25, 2026:</b> Registration & receipt"
            " verification<br>📢 <b>November 26 - 28, 2026:</b> Participant"
            " promotion & evaluation<br>🏆 <b>November 29, 2026:</b> Winner"
            " announcement"
        ),
        "parent_name": "Parent's Name",
        "phone_no": "Phone Number (WhatsApp)",
        "baby_name": "Baby's Name",
        "baby_age": "Baby's Age (Months - Open 0 to 36 months)",
        "baby_photo": "Upload Baby Photo",
        "receipt": "Upload Purchase Receipt (Min. RM100 at Baby Fair vendors)",
        "terms": (
            "<b>CONTEST TERMS & CONFIRMATION:</b><br>• Open to babies aged 0 -"
            " 36 months.<br>• Every minimum purchase of RM100 entitles one (1)"
            " entry.<br>• Each receipt can only be used once and must be"
            " verified by admin.<br>• Organizer's decision is final.<br>• I"
            " grant permission to Pacific KB Mall to use the baby's photo for"
            " promotional purposes."
        ),
        "agree": "I agree to the terms and conditions above.",
        "submit": "Submit Official Entry",
        "error_fill": (
            "Please complete all details and check the agreement box!"
        ),
        "spinner": "Processing image to Drive & sending data to SheetDB...",
        "success": "Congratulations! Your baby's entry has been successfully sent.",
        "error_db": "SheetDB server error: ",
        "error_fail": "Failed to send data: ",
    },
    "中文": {
        "title": "PACIFIC KB Mall - 超级巨星宝宝大赛",
        "subtitle": "展现你的宝宝，让他们发光！(2026年宝宝摄影比赛)",
        "period": "📅 比赛日期: 2026年11月9日 - 11月29日 (哥打峇鲁 Pacific KB Mall)",
        "desc": "请填写以下表格进行正式报名。(最低消费: RM100)",
        "prizes_title": "🏆 丰富奖品",
        "prizes_text": (
            "🥇 <b>冠军:</b> RM300 | 🥈 <b>亚军:</b> RM200 | 🥉 <b>季军:</b>"
            " RM100<br>🎁 还有安慰奖 x1 RM50"
        ),
        "criteria_title": "📊 评选标准",
        "criteria_text": (
            "👶 可爱与表情: <b>40%</b><br>📸 照片创意: <b>20%</b><br>🌟 独特性与吸引力:"
            " <b>10%</b><br>❤️ 社交媒体投票: <b>30%</b>"
        ),
        "dates_title": "📅 重要日期",
        "dates_text": (
            "📝 <b>11月9日 - 25日:</b> 报名与收据验证<br>📢 <b>11月26日 - 28日:</b>"
            " 参赛者宣传与评选<br>🏆 <b>11月29日:</b> 公布获奖者"
        ),
        "parent_name": "父母姓名",
        "phone_no": "电话号码 (WhatsApp)",
        "baby_name": "宝宝姓名",
        "baby_age": "宝宝年龄 (个月 - 适合 0 至 36 个月)",
        "baby_photo": "上传宝宝照片",
        "receipt": "上传购买收据 (最低 RM100)",
        "terms": (
            "<b>比赛条款与确认:</b><br>• 开放给 0 至 36 个月的宝宝参加。<br>•"
            " 每次最低消费 RM100 仅可获得一次参赛资格。<br>• 每张收据仅限使用一次并需经管理员核实。<br>•"
            " 主办方的决定为最终决定。<br>• 我授权 Pacific KB"
            " Mall 使用宝宝照片用于促销活动。"
        ),
        "agree": "我同意以上条款与条件。",
        "submit": "提交正式报名",
        "error_fill": "请填写所有详情并勾选同意框！",
        "spinner": "正在处理照片并提交数据至服务器...",
        "success": "恭喜！您的宝宝参赛申请已成功发送。",
        "error_db": "服务器错误: ",
        "error_fail": "提交数据失败: ",
    },
    "தமிழ்": {
        "title": "PACIFIC KB Mall - சூப்பர் ஸ்டார் குழந்தை",
        "subtitle": (
            "உங்கள் குழந்தையைக் காட்டுங்கள், பிரகாசிக்கட்டும்! (குழந்தை"
            " புகைப்பட போட்டி 2026)"
        ),
        "period": (
            "📅 போட்டி காலம்: நவம்பர் 9 - நவம்பர் 29, 2026 (PACIFIC KB MALL கோத்தா"
            " பாரு)"
        ),
        "desc": (
            "பதிவு செய்ய கீழே உள்ள படிவத்தை நிரப்பவும். (குறைந்தபட்ச வாங்குதல்:"
            " RM100)"
        ),
        "prizes_title": "🏆 பரிசுகள்",
        "prizes_text": (
            "🥇 <b>முதலிடம்:</b> RM300 | 🥈 <b>இரண்டாம் இடம்:</b> RM200 | 🥉"
            " <b>மூன்றாம் இடம்:</b> RM100<br>🎁 ஆறுதல் பரிசுகள் x1 RM50"
        ),
        "criteria_title": "📊 மதிப்பீட்டு அளவுகோல்",
        "criteria_text": (
            "👶 அழகு மற்றும் வெளிப்பாடு: <b>40%</b><br>📸 புகைப்பட படைப்பாற்றல்:"
            " <b>20%</b><br>🌟 தனித்தன்மை: <b>10%</b><br>❤️ சமூக ஊடக வாக்குகள்:"
            " <b>30%</b>"
        ),
        "dates_title": "📅 முக்கியமான தேதிகள்",
        "dates_text": (
            "📝 <b>நவம்பர் 9 - 25:</b> பதிவு & ரசீது சரிபார்ப்பு<br>📢 <b>நவம்பர்"
            " 26 - 28:</b> பங்கேற்பாளர் விளம்பரம் & மதிப்பீடு<br>🏆 <b>நவம்பர்"
            " 29:</b> வெற்றியாளர் அறிவிப்பு"
        ),
        "parent_name": "பெற்றோர் பெயர்",
        "phone_no": "தொலைபேசி எண் (WhatsApp)",
        "baby_name": "குழந்தையின் பெயர்",
        "baby_age": "குழந்தையின் வயது (மாதங்கள் - 0 முதல் 36 மாதங்கள் வரை)",
        "baby_photo": "குழந்தையின் புகைப்படத்தைப் பதிவேற்றுக",
        "receipt": "விலைப்பட்டியலைப் பதிவேற்றுக (குறைந்தபட்சம் RM100)",
        "terms": (
            "<b>விதிமுறைகள் & நிபந்தனைகள்:</b><br>• 0 முதல் 36 மாதங்களுக்கு"
            " உட்பட்ட குழந்தைகளுக்கு மட்டுமே.<br>• குறைந்தபட்சம் RM100 வாங்குவது"
            " ஒரு பதிவுக்கு அனுமதிக்கப்படும்.<br>• ஒவ்வொரு ரசீதும் ஒருமுறை மட்டுமே"
            " பயன்படுத்தப்படும்.<br>• நடுவர்களின் முடிே இறுதியானது."
        ),
        "agree": "மேற்கண்ட நிபந்தனைகளை நான் ஏற்றுக்கொள்கிறேன்.",
        "submit": "பதிவை சமர்ப்பிக்கவும்",
        "error_fill": (
            "தயவுசெய்து அனைத்து விவரங்களையும் பூர்த்தி செய்து ஒப்புதல்"
            " பெட்டியை டிக் செய்யவும்!"
        ),
        "spinner": "படங்களை Drive-க்கு அனுப்பி தரவுகள் செயலாக்கப்படுகின்றன...",
        "success": "வாழ்த்துகள்! உங்கள் குழந்தையின் பதிவு வெற்றிகரமாக அனுப்பப்பட்டது.",
        "error_db": "SheetDB சேவையகப் பிழை: ",
        "error_fail": "தரவை அனுப்புவதில் தோல்வி: ",
    },
}

# Logo di Kiri & Pilihan Bahasa di Kanan
col_logo, col_lang = st.columns([2, 2])

with col_logo:
  if os.path.exists("logo.png"):
    st.image("logo.png", width=180)

with col_lang:
  selected_lang = st.selectbox(
      "Language / Bahasa / 语言 / தமிழ்",
      ["Bahasa Melayu", "English", "中文", "தமிழ்"],
      index=0,
  )

t = translations[selected_lang]

# Paparkan Banner Gambar Bayi di atas (Jika fail banner_baby.png diletakkan dalam folder)
if os.path.exists("banner_baby.png"):
  st.image("banner_baby.png", use_container_width=True)

st.title(t["title"])
st.markdown(
    f"<p style='text-align: center; color: #d81b60 !important; font-weight:"
    f" bold; margin-top: -10px;'>{t['subtitle']}</p>",
    unsafe_allow_html=True,
)
st.markdown(f"<div class='period-badge'>{t['period']}</div>", unsafe_allow_html=True)

# Kotak Hadiah Menarik
st.markdown(
    f"""
<div class='prizes-box'>
    <h4>{t['prizes_title']}</h4>
    <p style='margin: 0; font-size: 15px;'>{t['prizes_text']}</p>
</div>
""",
    unsafe_allow_html=True,
)

# Kotak Kriteria Penilaian
st.markdown(
    f"""
<div class='criteria-box'>
    <h4>{t['criteria_title']}</h4>
    <p style='margin: 0; font-size: 14px; line-height: 1.6;'>{t['criteria_text']}</p>
</div>
""",
    unsafe_allow_html=True,
)

# Kotak Tarikh Penting
st.markdown(
    f"""
<div class='dates-box'>
    <h4>{t['dates_title']}</h4>
    <p style='margin: 0; font-size: 14px; line-height: 1.6;'>{t['dates_text']}</p>
</div>
""",
    unsafe_allow_html=True,
)

st.write(t["desc"])


# Fungsi Upload ke Google Drive melalui Apps Script
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
        baby_photo_url = upload_to_drive(uploaded_baby_photo, "Baby_Photos")
        receipt_url = upload_to_drive(uploaded_receipt, "Receipts")

        malaysia_time = datetime.utcnow() + timedelta(hours=8)
        formatted_date = malaysia_time.strftime("'%Y-%m-%d %H:%M:%S")

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
