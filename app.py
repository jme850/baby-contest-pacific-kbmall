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

# CSS Khas (Tema Cerah / Terang)
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
.period-badge { background-color: #ffe6eb; color: #e91e63 !important; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block; margin-bottom: 15px; border: 1px solid #ffccd5; }
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

# Paparkan "Created By : Azmer" di bahagian paling atas (Kecil, tidak bold, warna lembut)
st.markdown(
    "<div style='text-align: right; font-size: 10px; color: #888888;"
    " margin-bottom: -15px;'>Created By : Azmer</div>",
    unsafe_allow_html=True,
)

# Kamus Terjemahan Bahasa (BM, English, 中文, தமிழ்) dengan Tarikh Penting
translations = {
    "Bahasa Melayu": {
        "title": "PACIFIC KB Mall Pendaftaran Si Manja SUPERSTAR",
        "period": "📅 Tempoh Peraduan: 9 November - 29 November 2026",
        "desc": (
            "Sila isi borang di bawah untuk menyertai peraduan. (Syarat"
            " Pembelian Minimum: RM100)"
        ),
        "prizes_title": "🏆 HADIAH MENARIK UNTUK DIMENANGI!",
        "prizes_text": (
            "🥇 <b>Johan:</b> RM300 | 🥈 <b>Naib Johan:</b> RM200 | 🥉"
            " <b>Tempat Ketiga:</b> RM100<br>🎁 Serta Hadiah Saguhati RM50"
            " menanti anda!"
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
        "baby_age": "Umur Anak (Bulan)",
        "baby_photo": "Muat naik Gambar Baby",
        "receipt": "Muat naik Resit Pembelian (Min. RM100)",
        "terms": (
            "<b>C. PENGESAHAN IBU BAPA / PENJAGA</b><br>Saya mengesahkan bahawa"
            " maklumat yang diberikan adalah benar dan resit bernilai minimum"
            " RM100 yang dikemukakan adalah sah serta belum digunakan untuk"
            " penyertaan lain. Setiap resit hanya boleh digunakan sekali dan"
            " melayakkan satu (1) penyertaan sahaja.<br>Saya memberi kebenaran"
            " kepada Pacific KBMall untuk menggunakan gambar bayi bagi tujuan"
            " pertandingan dan promosi melalui saluran rasmi penganjur."
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
        "period": "📅 Contest Period: November 9 - November 29, 2026",
        "desc": (
            "Please fill out the form below to join the contest. (Minimum"
            " Purchase: RM100)"
        ),
        "prizes_title": "🏆 EXCITING PRIZES TO BE WON!",
        "prizes_text": (
            "🥇 <b>Champion:</b> RM300 | 🥈 <b>1st Runner Up:</b> RM200 | 🥉"
            " <b>2nd Runner Up:</b> RM100<br>🎁 Consolation Prizes RM50 await"
            " you!"
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
        "baby_age": "Baby's Age (Months)",
        "baby_photo": "Upload Baby Photo",
        "receipt": "Upload Purchase Receipt (Min. RM100)",
        "terms": (
            "<b>C. PARENT / GUARDIAN CONFIRMATION</b><br>I confirm that the"
            " information provided is true and the minimum RM100 receipt"
            " submitted is valid and has not been used for other entries. Each"
            " receipt can only be used once for one (1) entry.<br>I grant"
            " permission to Pacific KBMall to use the baby's photo for contest"
            " and promotional purposes through official channels."
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
        "period": "📅 比赛日期: 2026年11月9日 - 11月29日",
        "desc": "请填写以下表格以参加比赛。(最低消费: RM100)",
        "prizes_title": "🏆 丰富奖品等着你！",
        "prizes_text": (
            "🥇 <b>冠军:</b> RM300 | 🥈 <b>亚军:</b> RM200 | 🥉 <b>季军:</b>"
            " RM100<br>🎁 还有安慰奖 RM50 等着您！"
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
        "baby_age": "宝宝年龄 (个月)",
        "baby_photo": "上传宝宝照片",
        "receipt": "上传购买收据 (最低 RM100)",
        "terms": (
            "<b>C. 父母/监护人确认</b><br>我确认所提供的信息属实，提交的最低 RM100"
            " 收据有效且未用于其他参赛。每张收据仅限使用一次并获得一次 (1) 参赛资格。<br>我授权"
            " Pacific KBMall 通过官方渠道使用宝宝照片用于比赛及促销活动。"
        ),
        "agree": "我同意以上确认与授权。",
        "submit": "提交报名",
        "error_fill": "请填写所有信息并勾选同意条款！",
