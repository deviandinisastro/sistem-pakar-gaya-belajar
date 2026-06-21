# =============================================================================
# SISTEM PAKAR PENENTUAN GAYA BELAJAR SISWA
# Metode: Forward Chaining | Sumber: Aditasari dkk. (2020) ITJRD Vol.5 No.1
# Adaptasi berbasis Python + Streamlit (sistem asli jurnal menggunakan PHP/MySQL)
# Redesign UI/UX Modern - 2026
# =============================================================================

# ── 1. IMPORT ─────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import re
import base64
import os

# ── 2. KONFIGURASI ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kenali Gaya Belajarmu - Sistem Pakar Gaya Belajar Siswa",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ubah ke True untuk menampilkan menu akademik (Basis Pengetahuan & Metode)
SHOW_ACADEMIC_MODE = False

# ── 3. CSS MODERN & DESIGN SYSTEM ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

/* Force Light Mode and Set Global Typography */
:root {
    --bg-light: #EAF4F7;
    --bg-soft: #F7FBFD;
    --primary-blue: #2D9CDB;
    --primary-blue-2: #3B82F6;
    --navy: #07164A;
    --orange: #F28C28;
    --magenta: #C7356D;
    --white: #FFFFFF;
    --border: #D6E3EA;
    --muted: #64748B;
}

html, body, .stApp {
    color: var(--navy) !important;
}

/* Set font for all elements to match the button font */
* {
    font-family: 'Plus Jakarta Sans', 'Inter', 'Segoe UI', sans-serif !important;
}

/* Restore icon fonts using attribute selectors (higher specificity than *) */
[data-testid*="Icon"], 
[class*="Icon"],
[class*="icon"],
[class*="material"],
[data-testid="collapsedSidebarButton"] span {
    font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

.stApp {
    background-color: var(--bg-light) !important;
    background-image: 
        radial-gradient(rgba(7, 22, 74, 0.05) 1.2px, transparent 1.2px),
        radial-gradient(circle at 5% 15%, rgba(242, 140, 40, 0.08) 0%, transparent 22%),
        radial-gradient(circle at 95% 12%, rgba(199, 53, 109, 0.08) 0%, transparent 22%),
        radial-gradient(circle at 85% 85%, rgba(45, 156, 219, 0.06) 0%, transparent 28%),
        linear-gradient(135deg, #EAF4F7 0%, #F7FBFD 48%, #EEF2FF 100%) !important;
    background-repeat: repeat, no-repeat, no-repeat, no-repeat, no-repeat !important;
    background-size: 28px 28px, 100% 100%, 100% 100%, 100% 100%, 100% 100% !important;
}

/* Background decorative shapes */
.stApp::before {
    content: '';
    position: fixed;
    top: 5%;
    right: 5%;
    width: 250px;
    height: 250px;
    background-image: 
        radial-gradient(rgba(242, 140, 40, 0.15) 2px, transparent 2px);
    background-size: 16px 16px;
    mask-image: radial-gradient(circle, black, transparent 70%);
    -webkit-mask-image: radial-gradient(circle, black, transparent 70%);
    pointer-events: none;
    z-index: 0;
    opacity: 0.15;
}

.stApp::after {
    content: '';
    position: fixed;
    bottom: -100px;
    left: -100px;
    width: 450px;
    height: 450px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(199, 53, 109, 0.06) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* --- SIDEBAR CUSTOMIZATION --- */
[data-testid="stSidebar"] {
    background-color: var(--bg-soft) !important;
    border-right: 1px solid var(--border) !important;
    transition: min-width 0.3s ease, max-width 0.3s ease, transform 0.3s ease !important;
}

[data-testid="stSidebar"][aria-expanded="true"] {
    min-width: 260px !important;
    max-width: 260px !important;
}

/* Make Sidebar not scrollable */
[data-testid="stSidebarContent"], [data-testid="stSidebarUserContent"] {
    overflow: hidden !important;
}

/* Hide Radio Label */
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stWidgetLabel"] {
    display: none !important;
}

/* Sidebar Radio Wrapper */
[data-testid="stSidebar"] [data-testid="stRadio"] {
    width: 100% !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    padding: 4px 0 !important;
    width: 100% !important;
    margin: 0 !important;
}

/* Hide Streamlit Radio Circle Icons */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

/* Style Sidebar Radio Option as Full-Pill Buttons */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255, 255, 255, 0.7) !important;
    color: #07164A !important;
    border-radius: 999px !important;
    padding: 14px 20px !important;
    margin: 4px 0 !important;
    border: 1px solid rgba(214, 227, 234, 0.8) !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
    min-height: 52px !important;
    box-sizing: border-box !important;
    box-shadow: 0 2px 8px rgba(7, 22, 74, 0.06) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Radio Text Styling */
[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stRadio"] label span {
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: #07164A !important;
    opacity: 0.9 !important;
    transition: all 0.25s ease !important;
    margin: 0 !important;
    text-align: center !important;
    width: 100% !important;
    display: block !important;
    line-height: 1.3 !important;
}

/* Hover State for Non-Active Radio */
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #DFF2FA !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 18px rgba(45, 156, 219, 0.15) !important;
    border-color: #B8DCEF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover span {
    color: #07164A !important;
    opacity: 1 !important;
}

/* Active Radio Style — selected pill */
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #2D9CDB 0%, #3B82F6 55%, #C7356D 100%) !important;
    box-shadow: 0 8px 20px rgba(45, 156, 219, 0.3) !important;
    border-color: transparent !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked):hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 26px rgba(45, 156, 219, 0.38) !important;
}

/* --- BUTTONS --- */
/* Target all Streamlit standard, download, and form buttons */
div.stButton > button, 
div.stDownloadButton > button, 
div.stFormSubmitButton > button,
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, var(--primary-blue), var(--primary-blue-2)) !important;
    color: #FFFFFF !important;
    border: 1px solid transparent !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.6rem !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    box-shadow: 0 8px 20px rgba(45, 156, 219, 0.25) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: inline-block !important;
    cursor: pointer !important;
    width: 100% !important;
}

div.stButton > button:hover, 
div.stDownloadButton > button:hover, 
div.stFormSubmitButton > button:hover,
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(45, 156, 219, 0.35) !important;
    border-color: var(--orange) !important;
    color: #FFFFFF !important;
}

div.stButton > button:active, 
div.stDownloadButton > button:active, 
div.stFormSubmitButton > button:active {
    transform: translateY(0) !important;
}

/* Outline/Soft Blue Button for Back / Reset buttons */
.st-key-btn_kembali_tes button, 
.st-key-btn_ulangi_tes button {
    background: #EAF4F7 !important;
    color: var(--navy) !important;
    border: 1.5px solid var(--primary-blue) !important;
    box-shadow: none !important;
}
.st-key-btn_kembali_tes button:hover, 
.st-key-btn_ulangi_tes button:hover {
    background: #DFF2FA !important;
    border-color: var(--primary-blue-2) !important;
    color: var(--navy) !important;
    transform: translateY(-2px) !important;
}

/* Center Buttons Align */
.center-btn-container {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    padding: 16px 0 !important;
}

/* --- TYPOGRAPHY & LAYOUT --- */
.hero-container {
    background: linear-gradient(135deg, #EAF4F7 0%, #F7FBFD 55%, #E8ECFF 100%);
    border-radius: 24px;
    padding: 40px 30px;
    margin-bottom: 30px;
    border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(7, 22, 74, 0.03);
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(7, 22, 74, 0.02) 10px, rgba(7, 22, 74, 0.02) 11px);
    pointer-events: none;
    z-index: 0;
}

.hero-container::after {
    content: '•';
    color: var(--orange);
    font-size: 3rem;
    position: absolute;
    top: 10px;
    right: 20px;
    opacity: 0.8;
    pointer-events: none;
}

.hero-dot-pink {
    position: absolute;
    bottom: 15px;
    left: 25px;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--magenta);
    opacity: 0.6;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, var(--navy) 0%, var(--primary-blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.hero-sub {
    font-size: 1.15rem;
    font-weight: 500;
    text-align: center;
    color: var(--navy);
    opacity: 0.85;
    max-width: 750px;
    margin: 0 auto 10px;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.hero-desc {
    font-size: 1rem;
    text-align: center;
    color: var(--muted);
    max-width: 820px;
    margin: 0 auto 30px;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.sec-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--navy);
    border-left: 5px solid var(--magenta);
    padding-left: 14px;
    margin: 28px 0 16px;
}

/* --- CARDS & HOVER EFFECTS --- */
.card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 26px 30px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(7, 22, 74, 0.03);
    border: 1px solid var(--border);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    color: var(--navy);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 32px rgba(7, 22, 74, 0.06);
    border-color: rgba(45, 156, 219, 0.2);
}

.gb-card {
    background: var(--white);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(7, 22, 74, 0.03);
    border: 1px solid var(--border);
    height: 100%;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

.gb-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 32px rgba(7, 22, 74, 0.08);
    border-color: rgba(45, 156, 219, 0.2);
}

/* Test page container and category header */
.test-container {
    width: 100% !important;
}

.category-header {
    background: rgba(255, 255, 255, 0.72) !important;
    border: 1px solid #D6E3EA !important;
    border-left: 5px solid #2D9CDB !important;
    border-radius: 18px !important;
    padding: 20px 24px !important;
    margin-bottom: 18px !important;
}

.category-header-title {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #172033 !important;
    margin-bottom: 6px !important;
}

.category-header-desc {
    font-size: 0.95rem !important;
    color: #64748B !important;
    margin: 0 !important;
}

/* Restrict the main content container to 1100px max width on the Test page */
[data-testid="stAppViewBlockContainer"]:has(.test-container) {
    max-width: 1100px !important;
    margin: 0 auto !important;
}

/* ── OPTION CARD GRID: equal-height columns ──────────────────────────────── */
[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) {
    align-items: stretch !important;
    margin-bottom: 12px !important;
}

/* L1 — column: force equal width via flex basis 0 */
[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) > [data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 0% !important;
    min-width: 0 !important;
}

/* L2 — stVerticalBlock (Streamlit inserts this between column and element-container) */
[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) > [data-testid="column"] > div {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}

/* L3 — element-container or any nested wrapper */
[data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) > [data-testid="column"] > div > div {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}

/* ── CHECKBOX CARD STYLE ─────────────────────────────────────────────────── */
div[data-testid="stCheckbox"] {
    background: #FFFFFF !important;
    border: 1.5px solid #D6E3EA !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 0 !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 14px rgba(7, 22, 74, 0.05) !important;
    /* FIXED dimensions — guarantees identical size for every card */
    width: 100% !important;
    min-width: 0 !important;
    height: 76px !important;        /* fixed, not min-height */
    max-height: 76px !important;
    overflow: hidden !important;    /* clip if text somehow overflows */
    flex: 1 1 auto !important;
    display: flex !important;
    align-items: center !important;
    box-sizing: border-box !important;
    cursor: pointer !important;
}

div[data-testid="stCheckbox"]:hover {
    transform: translateY(-2px) !important;
    border-color: #7CC7FF !important;
    box-shadow: 0 12px 24px rgba(45, 156, 219, 0.12) !important;
}

div[data-testid="stCheckbox"]:has(input:checked) {
    background: linear-gradient(135deg, #F8FCFF 0%, #EEF7FF 100%) !important;
    border-color: #4AA8FF !important;
    box-shadow: 0 12px 26px rgba(74, 168, 255, 0.16) !important;
}

div[data-testid="stCheckbox"] label {
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    height: 100% !important;
    gap: 14px !important;
    cursor: pointer !important;
}

/* Text span */
div[data-testid="stCheckbox"] label > span:last-child {
    flex: 1 !important;
    min-width: 0 !important;
    color: #24324A !important;
    font-size: 0.97rem !important;
    line-height: 1.48 !important;
    font-weight: 500 !important;
    margin: 0 !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
    white-space: normal !important;
}

/* Native checkbox: only safe overrides */
div[data-testid="stCheckbox"] label input[type="checkbox"] {
    accent-color: #2D9CDB !important;
    flex-shrink: 0 !important;
}

/* ── RESPONSIVE ──────────────────────────────────────────────────────────── */
@media (max-width: 900px) {
    [data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) {
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"]:has(div[data-testid="stCheckbox"]) > [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 auto !important;
    }
    div[data-testid="stCheckbox"] {
        height: 68px !important;
        max-height: 68px !important;
    }
}

/* Input Fields */
.stTextInput label, .stSelectbox label {
    color: var(--navy) !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    margin-bottom: 6px !important;
}

.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    padding: 2px 4px !important;
    font-size: 0.96rem !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
    border-color: var(--primary-blue) !important;
}

/* Progress bar container */
.prog-bg {
    background: var(--border);
    border-radius: 12px;
    height: 18px;
    overflow: hidden;
    margin: 4px 0 12px;
}

.prog-bar {
    height: 18px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 8px;
    font-size: 0.75rem;
    font-weight: 800;
    color: #FFFFFF;
    transition: width 0.3s ease;
}

/* Badges for status and levels */
.badge {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    margin: 4px 0;
}

.b-visual      { background: #EAF4F7; color: #2D9CDB; border: 1px solid #2D9CDB55; }
.b-auditori    { background: #EEF2FF; color: #6C63FF; border: 1px solid #6C63FF55; }
.b-kinestetik  { background: #FFF7ED; color: #F28C28; border: 1px solid #F28C2855; }
.b-verbal      { background: #FFF0F6; color: #C7356D; border: 1px solid #C7356D55; }
.b-logis       { background: #ECFDF5; color: #10B981; border: 1px solid #10B98155; }
.b-interpersonal { background: #E6F9F9; color: #14A3A3; border: 1px solid #14A3A355; }
.b-intrapersonal { background: #EEF2FF; color: #07164A; border: 1px solid #07164A55; }

.b-ok   { background: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }
.b-part { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
.b-mix  { background: #EDE9FE; color: #5B21B6; border: 1px solid #C4B5FD; }

/* Ciri Chips */
.ciri-chip {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 10px 16px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    transition: all 0.2s ease !important;
}
.ciri-chip:hover {
    background: #E3F4FF !important;
    border-color: var(--primary-blue) !important;
    transform: translateY(-1px) !important;
}

/* --- SEMBUNYIKAN TOMBOL DOWNLOAD PADA TOOLBAR TABEL --- */
[data-testid="stElementToolbar"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── 4. FAKTA ASLI (Tabel 9 Jurnal) ───────────────────────────────────────────
# Rule diadaptasi dari Tabel 8 jurnal; daftar fakta dari Tabel 9 jurnal.
# C69 tidak digunakan (tidak ada dalam daftar fakta jurnal).
fakta_asli = {
    "C45":"Suka dengan diskusi kelompok",
    "C46":"Suka pelajaran yang berkelompok",
    "C47":"Lebih nyaman berkonsultasi dan berdiskusi",
    "C48":"Suka belajar mengutarakan ide atau argumen",
    "C49":"Suka bekerja di ruangan sendiri",
    "C50":"Lebih suka belajar sendiri",
    "C51":"Tidak mudah terganggu oleh keributan",
    "C52":"Dapat berkonsentrasi dengan mudah meskipun ada banyak orang",
    "C53":"Cenderung berpikir dengan menggunakan gambar",
    "C54":"Memiliki kemampuan dalam memodifikasi objek",
    "C55":"Menyukai permainan kata, puisi, pantun, dan menemukan arti kata",
    "C56":"Suka dengan warna, garis, dan seni",
    "C57":"Tertarik dengan hal yang berhubungan dengan matematika",
    "C58":"Menyukai aktivitas pembelajaran yang melibatkan tubuh",
    "C59":"Pandai menirukan suara",
    "C60":"Mudah berkomunikasi dengan orang lain",
    "C61":"Senang mendengarkan cerita",
    "C62":"Bosan dengan gaya pembelajaran yang hanya duduk diam",
    "C63":"Sering lupa saat berbicara",
    "C64":"Agak sulit berteman dengan orang lain",
    "C65":"Suka membaca, berbicara, dan menulis saat belajar",
    "C66":"Pasif dalam berdiskusi",
    "C67":"Kesulitan dalam menulis",
    "C68":"Memiliki kemampuan membedakan pola logika",
    "C70":"Menafsirkan suatu makna melalui isyarat nonverbal seperti perubahan irama, nada, dan intonasi, serta sering salah mengartikan makna",
    "C71":"Sangat sensitif terhadap perasaan orang lain",
    "C72":"Tidak suka yang berhubungan dengan hafalan",
    "C73":"Jarang dimintai nasihat teman",
    "C74":"Tidak pandai mengarang kata-kata",
    "C75":"Konsentrasi terhadap gangguan suara",
    "C76":"Belajar secara autodidak",
    "C77":"Pendengar yang baik",
    "C79":"Kurang cakap dalam mengarang",
}

# ── 5. FAKTA TAMPILAN (bahasa ramah siswa) ────────────────────────────────────
fakta_tampil = {
    "C45":"Saya suka belajar atau berdiskusi dalam kelompok",
    "C46":"Saya lebih nyaman dengan pelajaran yang dikerjakan berkelompok",
    "C47":"Saya lebih suka berkonsultasi dan berdiskusi daripada belajar sendiri",
    "C48":"Saya suka mengutarakan ide atau pendapat saat belajar",
    "C49":"Saya lebih suka bekerja atau belajar di ruangan sendiri",
    "C50":"Saya lebih suka belajar secara mandiri",
    "C51":"Saya tidak mudah terganggu oleh keributan di sekitar saya",
    "C52":"Saya bisa berkonsentrasi dengan baik meskipun banyak orang di sekitar",
    "C53":"Saya cenderung berpikir menggunakan gambar atau visualisasi",
    "C54":"Saya bisa memodifikasi atau merakit objek dengan baik",
    "C55":"Saya menyukai permainan kata, puisi, pantun, dan mencari arti kata",
    "C56":"Saya menyukai warna, garis, dan seni visual",
    "C57":"Saya tertarik dengan hal-hal yang berhubungan dengan matematika",
    "C58":"Saya menyukai kegiatan belajar yang melibatkan gerakan tubuh",
    "C59":"Saya pandai menirukan suara atau intonasi orang lain",
    "C60":"Saya mudah berkomunikasi dan berbaur dengan orang lain",
    "C61":"Saya senang mendengarkan cerita atau penjelasan lisan",
    "C62":"Saya cepat bosan jika hanya duduk diam saat belajar",
    "C63":"Saya sering lupa apa yang ingin saya katakan saat berbicara",
    "C64":"Saya agak sulit untuk berteman dengan orang yang baru saya kenal",
    "C65":"Saya suka membaca, berbicara, dan menulis saat belajar",
    "C66":"Saya cenderung pasif saat berdiskusi dalam kelompok",
    "C67":"Saya merasa kesulitan saat harus menulis",
    "C68":"Saya mampu membedakan dan mengenali pola logika",
    "C70":"Saya sering memahami makna dari nada bicara atau isyarat nonverbal, namun terkadang salah mengartikannya",
    "C71":"Saya sangat peka terhadap perasaan orang lain",
    "C72":"Saya tidak suka belajar dengan banyak hafalan",
    "C73":"Teman-teman jarang meminta nasihat atau pendapat dari saya",
    "C74":"Saya merasa kurang pandai dalam mengarang atau merangkai kata-kata",
    "C75":"Saya mudah kehilangan konsentrasi jika ada suara atau gangguan di sekitar",
    "C76":"Saya terbiasa belajar secara autodidak tanpa panduan khusus",
    "C77":"Saya adalah pendengar yang baik bagi orang-orang di sekitar saya",
    "C79":"Saya merasa kurang cakap dalam menulis atau mengarang",
}

# ── 6. KATEGORI PERTANYAAN ────────────────────────────────────────────────────
kategori_pertanyaan = {
    "Cara Menerima Informasi": ["C53","C56","C55","C57","C59","C61","C65","C70"],
    "Cara Belajar & Memproses Materi": ["C49","C50","C54","C58","C62","C67","C72","C74","C76","C79"],
    "Kebiasaan Sosial & Komunikasi": ["C45","C46","C47","C48","C60","C64","C66","C71","C73","C77"],
    "Kecenderungan Berpikir & Konsentrasi": ["C51","C52","C63","C68","C75"],
}

# ── 7. RULE BASE (Tabel 8 Jurnal) – JANGAN DIUBAH ────────────────────────────
aturan = {
    "Visual":        ["C53","C56","C49","C51","C66","C74"],
    "Auditori":      ["C45","C59","C61","C63","C79"],
    "Kinestetik":    ["C54","C58","C46","C62","C67"],
    "Verbal":        ["C55","C52","C65","C70"],
    "Logis":         ["C57","C68","C72","C76"],
    "Interpersonal": ["C60","C47","C48","C73","C75"],
    "Intrapersonal": ["C50","C64","C71","C77"],
}

# ── 8. INFO & WARNA GAYA BELAJAR ──────────────────────────────────────────────
# Memakai palette PPT: Visual (#2D9CDB), Auditori (#6C63FF), Kinestetik (#F28C28), Verbal (#C7356D), Logis (#10B981), Interpersonal (#14A3A3), Intrapersonal (#07164A)
info_gaya = {
    "Visual":        {"emoji":"🎨","hex":"#2D9CDB","badge":"b-visual",
                      "bg":"linear-gradient(135deg,#EAF4F7,#DFF2FA)",
                      "short":"Belajar lebih mudah lewat gambar, warna, diagram, dan visualisasi.",
                      "desk":"Kamu cenderung lebih mudah memahami materi melalui gambar, warna, diagram, peta konsep, video, dan tampilan visual."},
    "Auditori":      {"emoji":"🎧","hex":"#6C63FF","badge":"b-auditori",
                      "bg":"linear-gradient(135deg,#EEF2FF,#E0DDFF)",
                      "short":"Belajar lebih nyaman lewat suara, penjelasan lisan, dan diskusi.",
                      "desk":"Kamu cenderung lebih mudah memahami materi melalui suara, penjelasan lisan, diskusi, dan mendengarkan."},
    "Kinestetik":    {"emoji":"🏃","hex":"#F28C28","badge":"b-kinestetik",
                      "bg":"linear-gradient(135deg,#FFF7ED,#FFE8D1)",
                      "short":"Belajar lebih efektif lewat praktik, gerakan, dan aktivitas langsung.",
                      "desk":"Kamu cenderung lebih mudah belajar melalui gerakan, praktik, aktivitas langsung, dan pengalaman nyata."},
    "Verbal":        {"emoji":"📝","hex":"#C7356D","badge":"b-verbal",
                      "bg":"linear-gradient(135deg,#FFF0F6,#FFDEEB)",
                      "short":"Belajar kuat melalui membaca, menulis, berbicara, dan kata-kata.",
                      "desk":"Kamu cenderung menyukai kata-kata, membaca, menulis, berbicara, dan memahami makna bahasa."},
    "Logis":         {"emoji":"🧮","hex":"#10B981","badge":"b-logis",
                      "bg":"linear-gradient(135deg,#ECFDF5,#D1FAE5)",
                      "short":"Belajar nyaman dengan pola, angka, logika, dan sebab-akibat.",
                      "desk":"Kamu cenderung menyukai pola, angka, logika, matematika, dan hubungan sebab-akibat."},
    "Interpersonal": {"emoji":"👥","hex":"#14A3A3","badge":"b-interpersonal",
                      "bg":"linear-gradient(135deg,#E6F9F9,#CCF2F2)",
                      "short":"Belajar lebih baik melalui diskusi, kerja kelompok, dan interaksi.",
                      "desk":"Kamu cenderung lebih nyaman belajar bersama orang lain melalui diskusi, kerja kelompok, dan bertukar pendapat."},
    "Intrapersonal": {"emoji":"🌟","hex":"#07164A","badge":"b-intrapersonal",
                      "bg":"linear-gradient(135deg,#EEF2FF,#D5DBED)",
                      "short":"Belajar lebih fokus secara mandiri, tenang, dan reflektif.",
                      "desk":"Kamu cenderung lebih nyaman belajar sendiri, reflektif, dan memahami cara belajar pribadimu."},
}

# ── 9. REKOMENDASI BELAJAR ────────────────────────────────────────────────────
# Rekomendasi belajar merupakan tambahan praktis berdasarkan karakteristik gaya belajar, bukan rule utama jurnal.
rekomendasi = {
    "Visual": [
        "Gunakan mind map atau peta konsep untuk merangkum materi.",
        "Pakai warna untuk menandai poin penting saat mencatat.",
        "Belajar lewat gambar, tabel, diagram, atau tonton video edukatif.",
        "Buat flashcard visual dengan gambar atau simbol.",
        "Ringkas materi dalam bentuk bagan atau infografis sederhana.",
    ],
    "Auditori": [
        "Dengarkan penjelasan guru dengan fokus, minimalisir distraksi.",
        "Baca materi dengan suara pelan agar lebih mudah diingat.",
        "Diskusikan materi dengan teman secara lisan.",
        "Jelaskan ulang materi kepada orang lain untuk memastikan pemahamanmu.",
        "Gunakan rekaman suara jika perlu untuk mengulang materi.",
    ],
    "Kinestetik": [
        "Belajar sambil praktik atau melakukan eksperimen langsung.",
        "Gunakan alat peraga atau simulasi saat memahami konsep baru.",
        "Jangan belajar terlalu lama dalam posisi diam, selingi dengan gerakan ringan.",
        "Buat contoh nyata dari materi yang sedang dipelajari.",
        "Tulis ulang poin penting sambil bergerak atau berdiri.",
    ],
    "Verbal": [
        "Buat rangkuman tertulis dengan kata-katamu sendiri.",
        "Baca ulang materi secara bertahap dan berulang.",
        "Tulis poin penting setelah membaca setiap bagian.",
        "Jelaskan materi kepada teman atau anggota keluarga.",
        "Gunakan singkatan atau akronim untuk mengingat daftar informasi.",
    ],
    "Logis": [
        "Gunakan pola, tabel, dan langkah sistematis agar materi lebih mudah dipahami.",
        "Latihan soal bertahap dari mudah ke sulit.",
        "Cari hubungan dan keterkaitan antar konsep yang dipelajari.",
        "Buat daftar rumus, konsep, atau langkah penyelesaian secara sistematis.",
        "Gunakan skema untuk memahami struktur materi.",
    ],
    "Interpersonal": [
        "Belajar kelompok secara rutin bersama teman.",
        "Diskusi dan tanya jawab setelah membaca materi.",
        "Presentasikan materi secara singkat di depan teman.",
        "Saling menjelaskan materi dengan teman.",
        "Ikut kegiatan kerja sama atau proyek kelompok.",
    ],
    "Intrapersonal": [
        "Buat jadwal belajar pribadi dan patuhi dengan disiplin.",
        "Belajar di tempat yang tenang dan minim gangguan.",
        "Tulis target belajar harian dan evaluasi setiap hari.",
        "Buat catatan refleksi setelah selesai belajar.",
        "Evaluasi bagian yang sudah dan belum dipahami setiap sesi.",
    ],
}

# ── 10. SESSION STATE INITIALIZATION ─────────────────────────────────────────
if "menu" not in st.session_state:
    st.session_state["menu"] = "Beranda"
if "pilihan_user" not in st.session_state:
    st.session_state["pilihan_user"] = []
if "hasil_tes" not in st.session_state:
    st.session_state["hasil_tes"] = None
if "identitas" not in st.session_state:
    st.session_state["identitas"] = {"nama": "", "jenjang": "SMA/SMK", "kelas": ""}
if "step" not in st.session_state:
    st.session_state["step"] = 1

# ── 11. FUNGSI NAVIGASI ───────────────────────────────────────────────────────
def pindah_halaman(nama_menu):
    st.session_state["menu"] = nama_menu
    st.rerun()

# ── 12. FUNGSI INFERENSI FORWARD CHAINING ────────────────────────────────────
def hitung_hasil(pilihan_user):
    hasil = {}
    for gaya, daftar_kode in aturan.items():
        cocok = [k for k in daftar_kode if k in pilihan_user]
        persen = len(cocok) / len(daftar_kode) * 100
        hasil[gaya] = {
            "jumlah_cocok": len(cocok),
            "total_rule": len(daftar_kode),
            "persen": persen,
            "kode_cocok": cocok,
            "kode_belum": [k for k in daftar_kode if k not in pilihan_user],
        }
    return hasil

# ── 13. FUNGSI PDF ────────────────────────────────────────────────────────────
def bersihkan_teks_pdf(teks):
    # Hapus emoji dan karakter non-latin-1 agar PDF tidak error
    teks = re.sub(r'[^\x00-\xFF]', '', teks)
    return teks.encode("latin-1", errors="replace").decode("latin-1")

def buat_pdf():
    identitas = st.session_state["identitas"]
    hasil = st.session_state["hasil_tes"]
    sorted_hasil = sorted(hasil.items(), key=lambda x: x[1]["persen"], reverse=True)
    max_persen = sorted_hasil[0][1]["persen"]
    gaya_dominan = [g for g, d in sorted_hasil if d["persen"] == max_persen]
    g_dom = gaya_dominan[0]

    if max_persen == 100:
        status = "Seluruh ciri terpenuhi."
    elif len(gaya_dominan) > 1:
        status = "Kemungkinan gaya belajar campuran (skor tertinggi sama)."
    else:
        status = "Kecenderungan tertinggi berdasarkan ciri yang dipilih."

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(18, 20, 18)

    # Header Banner - Navy Dark (#07164A)
    pdf.set_fill_color(7, 22, 74)
    pdf.rect(0, 0, 210, 38, "F")
    
    # Accent Line - Orange (#F28C28)
    pdf.set_fill_color(242, 140, 40)
    pdf.rect(0, 38, 210, 1.5, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_y(12)
    pdf.cell(0, 8, "LAPORAN HASIL IDENTIFIKASI GAYA BELAJAR", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Adaptasi Jurnal Penelitian IT Journal Research and Development Vol. 5, No. 1, 2020", align="C")
    pdf.ln(18)

    # Identitas Section - Navy text on Soft Blue (#EAF4F7) background
    pdf.set_text_color(7, 22, 74)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(234, 244, 247)
    pdf.cell(0, 8, "  IDENTITAS PENGGUNA", fill=True)
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(2)
    for label, key in [("Nama Lengkap", "nama"), ("Jenjang Pendidikan", "jenjang"), ("Kelas / Tingkat", "kelas"), ("Tanggal Tes", "tanggal")]:
        val = bersihkan_teks_pdf(identitas.get(key, "-") or "-")
        pdf.cell(45, 7, f"  {label}")
        pdf.cell(5, 7, ":")
        pdf.cell(0, 7, f" {val}")
        pdf.ln(7)
    pdf.ln(4)

    # Hasil Identifikasi Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(234, 244, 247)
    pdf.cell(0, 8, "  HASIL IDENTIFIKASI GAYA BELAJAR", fill=True)
    pdf.ln(8)
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(45, 156, 219) # Primary Blue (#2D9CDB)
    label_gaya = bersihkan_teks_pdf(" & ".join(gaya_dominan) if len(gaya_dominan) > 1 else g_dom)
    pdf.cell(0, 9, f"  Gaya Belajar Dominan: {label_gaya}")
    pdf.ln(9)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(7, 22, 74)
    pdf.cell(45, 7, "  Persentase Kecocokan"); pdf.cell(5, 7, ":"); pdf.cell(0, 7, f" {max_persen:.0f}%"); pdf.ln(7)
    pdf.cell(45, 7, "  Status"); pdf.cell(5, 7, ":"); pdf.multi_cell(0, 7, f" {bersihkan_teks_pdf(status)}")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(7, 22, 74)
    # Combined description for PDF if mixed
    if len(gaya_dominan) > 1:
        desc_pdf = " ".join([info_gaya[g]["desk"] for g in gaya_dominan])
    else:
        desc_pdf = info_gaya[g_dom]["desk"]
    pdf.multi_cell(0, 6, f"  {bersihkan_teks_pdf(desc_pdf)}")
    pdf.ln(5)

    # Rekomendasi Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(234, 244, 247)
    pdf.set_text_color(7, 22, 74)
    pdf.cell(0, 8, "  REKOMENDASI CARA BELAJAR", fill=True)
    pdf.ln(8)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    # Loop over recommendations for dominant style (max 5 points)
    for s in rekomendasi[g_dom][:5]:
        pdf.multi_cell(0, 6, f"  - {bersihkan_teks_pdf(s)}")
        pdf.ln(1)
    pdf.ln(4)

    # Gaya Belajar Lain Section (if applicable)
    lain = [(g, d) for g, d in sorted_hasil if g not in gaya_dominan and d["persen"] > 0][:3]
    if lain:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(234, 244, 247)
        pdf.cell(0, 8, "  KECENDERUNGAN GAYA BELAJAR LAIN YANG MENONJOL", fill=True)
        pdf.ln(8)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        for g, d in lain:
            pdf.cell(0, 7, f"  - {g} ({d['persen']:.0f}% kecocokan)")
            pdf.ln(7)
        pdf.ln(4)

    # Ciri-Ciri Yang Dipilih Section (NEW REQUIREMENT)
    pilihan_user = st.session_state.get("pilihan_user", [])
    if pilihan_user:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(234, 244, 247)
        pdf.cell(0, 8, "  CIRI-CIRI GAYA BELAJAR YANG KAMU PILIH", fill=True)
        pdf.ln(8)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 10)
        for kode in pilihan_user:
            teks_ciri = fakta_tampil.get(kode, "")
            pdf.multi_cell(0, 6, f"  - {bersihkan_teks_pdf(teks_ciri)}")
            pdf.ln(1)
        pdf.ln(4)

    # Catatan & Disclaimer Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(254, 243, 199)
    pdf.set_text_color(146, 64, 14)
    pdf.cell(0, 8, "  CATATAN PENTING", fill=True)
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(7, 22, 74)
    pdf.ln(2)
    pdf.multi_cell(0, 6, "  1. Hasil identifikasi ini merupakan identifikasi awal kecenderungan gaya belajar berdasarkan tanggapan yang Anda berikan, bukan sebuah diagnosis psikologis klinis mutlak.")
    pdf.ln(1)
    pdf.multi_cell(0, 6, "  2. Gunakan rekomendasi belajar di atas untuk menunjang efektivitas belajar mandiri maupun berkelompok.")
    pdf.ln(1)
    pdf.multi_cell(0, 6, "  3. Sumber Jurnal Acuan: Aditasari, Novita, Waliyansyah (2020). Sistem Pakar Penentuan Gaya Belajar Siswa Dengan Metode Forward Chaining Berbasis Web. ITJRD Vol. 5 No. 1.")
    
    return bytes(pdf.output())

# ── 14. HALAMAN BERANDA ───────────────────────────────────────────────────────
def tampilkan_beranda():
    st.markdown("""
    <div class='hero-container'>
        <div class='hero-dot-pink'></div>
        <div class='hero-title'>Kenali Gaya Belajarmu</div>
        <div class='hero-sub'>Temukan cara belajar yang paling cocok untuk kamu melalui tes sederhana berbasis sistem pakar.</div>
        <div class='hero-desc'>Setiap orang punya cara belajar yang berbeda. Pilih ciri-ciri yang sesuai dengan kebiasaan belajarmu, lalu sistem akan membantu menampilkan gaya belajar dominan dan rekomendasi belajar yang sesuai.</div>
    </div>
    """, unsafe_allow_html=True)

    # Centered CTA Button
    c_left, c_middle, c_right = st.columns([2, 1.4, 2])
    with c_middle:
        st.markdown("<div class='center-btn-container'>", unsafe_allow_html=True)
        if st.button("Mulai Tes Sekarang", key="btn_mulai_home", use_container_width=True):
            pindah_halaman("Tes Gaya Belajar")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>7 Gaya Belajar yang Diidentifikasi</div>", unsafe_allow_html=True)

    # Display 7 learning style cards (3 columns grid layout)
    gaya_list = list(info_gaya.items())
    for baris in range(0, len(gaya_list), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = baris + i
            if idx < len(gaya_list):
                nama, info = gaya_list[idx]
                with col:
                    st.markdown(f"""
                    <div class='gb-card' style='border-top: 5px solid {info["hex"]};'>
                        <div style='font-size: 1.8rem; margin-bottom: 10px;'>{info["emoji"]}</div>
                        <div style='font-weight: 800; color: {info["hex"]}; font-size: 1.25rem; margin-bottom: 8px;'>{nama}</div>
                        <div style='font-size: 0.98rem; color: #4B5563; line-height: 1.6; margin-bottom: 0;'>{info["short"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top: 24px; padding: 14px 20px; background: rgba(254,243,199,0.7);
        border-radius: 16px; border: 1px solid #FCD34D; color: #92400E; font-size: 0.9rem; text-align: center; font-weight: 500;'>
        ℹ️ Hasil tes ini merupakan identifikasi awal, bukan diagnosis psikologis mutlak.
    </div>
    """, unsafe_allow_html=True)

# ── 15. HALAMAN TES GAYA BELAJAR ──────────────────────────────────────────────
def tampilkan_tes():
    st.markdown("<div class='test-container'>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title' style='font-size: 2.3rem; text-align: left;'>Tes Gaya Belajar</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub' style='text-align: left; margin-bottom: 24px; max-width: 100%;'>Isi data diri kamu dan jawab tes bertahap di bawah ini.</div>", unsafe_allow_html=True)

    # Progress bar and steps helper
    categories = list(kategori_pertanyaan.keys())
    step = st.session_state["step"]
    current_cat = categories[step - 1]

    # Progress Bar Horizontal
    pct = int((step) / 4 * 100)
    st.markdown(f"""
    <div style='margin-bottom: 26px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='font-size: 1.05rem; font-weight: 700; color: #6C4FF6;'>Langkah {step} dari 4: {current_cat}</span>
            <span style='font-size: 0.95rem; font-weight: 700; color: #3B82F6;'>{pct}% Selesai</span>
        </div>
        <div class='prog-bg'>
            <div class='prog-bar' style='width: {pct}%; background: linear-gradient(90deg, #6C4FF6, #3B82F6);'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 1: IDENTITY & FIRST CATEGORY ---
    if step == 1:
        st.markdown("<div class='sec-title' style='margin-top:0; border-left-color: var(--primary-blue);'>Identitas Siswa</div>", unsafe_allow_html=True)
        
        nama = st.text_input("Nama Lengkap *", placeholder="Masukkan nama lengkap kamu...",
                             value=st.session_state["identitas"].get("nama", ""))
        
        c1, c2 = st.columns(2)
        with c1:
            opsi = ["SD", "SMP", "SMA/SMK", "Mahasiswa", "Umum"]
            sj = st.session_state["identitas"].get("jenjang", "SMA/SMK")
            jenjang = st.selectbox("Jenjang Sekolah *", opsi, index=opsi.index(sj) if sj in opsi else 2)
        with c2:
            kelas = st.text_input("Kelas (opsional)", placeholder="Cth: XI IPA 2 atau Semester 4",
                                  value=st.session_state["identitas"].get("kelas", ""))
        
        # Save identity to session state live
        st.session_state["identitas"] = {
            "nama": nama,
            "jenjang": jenjang,
            "kelas": kelas,
            "tanggal": st.session_state["identitas"].get("tanggal", datetime.date.today().strftime("%d %B %Y"))
        }

    # Instruction Card for current step
    st.markdown(f"""
    <div class='category-header'>
        <div class='category-header-title'>{current_cat}</div>
        <div class='category-header-desc'>Pilih kebiasaan atau pernyataan di bawah ini yang paling menggambarkan dirimu:</div>
    </div>
    """, unsafe_allow_html=True)

    # Checkboxes rendered in 2 Columns row-by-row for neat layout
    kode_list = kategori_pertanyaan[current_cat]

    # Helper function to save choices on transition
    def simpan_pilihan_langkah_aktif(step_num):
        cat_name = categories[step_num - 1]
        for k in kategori_pertanyaan[cat_name]:
            cb_key = f"cb_{k}"
            if cb_key in st.session_state:
                state_val = st.session_state[cb_key]
                if state_val:
                    if k not in st.session_state["pilihan_user"]:
                        st.session_state["pilihan_user"].append(k)
                else:
                    if k in st.session_state["pilihan_user"]:
                        st.session_state["pilihan_user"].remove(k)

    # Render checkboxes in pairs of columns row-by-row
    for i in range(0, len(kode_list), 2):
        row_cols = st.columns(2)
        # Left item
        k1 = kode_list[i]
        checked1 = k1 in st.session_state["pilihan_user"]
        with row_cols[0]:
            st.checkbox(fakta_tampil[k1], value=checked1, key=f"cb_{k1}")
        
        # Right item
        if i + 1 < len(kode_list):
            k2 = kode_list[i + 1]
            checked2 = k2 in st.session_state["pilihan_user"]
            with row_cols[1]:
                st.checkbox(fakta_tampil[k2], value=checked2, key=f"cb_{k2}")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Navigation Buttons
    c_btn1, c_btn2 = st.columns([1, 1])

    with c_btn1:
        if step > 1:
            if st.button("Kembali", use_container_width=True, key="btn_kembali_tes"):
                simpan_pilihan_langkah_aktif(step)
                st.session_state["step"] = step - 1
                st.rerun()
        else:
            st.empty()

    with c_btn2:
        if step < 4:
            if st.button("Lanjut", use_container_width=True):
                # Validation on Step 1
                if step == 1:
                    nama_val = st.session_state["identitas"].get("nama", "").strip()
                    if not nama_val:
                        st.error("⚠️ Nama Lengkap wajib diisi sebelum melanjutkan.")
                        st.stop()
                
                simpan_pilihan_langkah_aktif(step)
                st.session_state["step"] = step + 1
                st.rerun()
        else:
            if st.button("Lihat Hasil Tes", use_container_width=True):
                simpan_pilihan_langkah_aktif(4)
                
                # Final validations
                nama_val = st.session_state["identitas"].get("nama", "").strip()
                pilihan = st.session_state["pilihan_user"]
                
                if not nama_val:
                    st.error("⚠️ Nama Lengkap wajib diisi.")
                elif not pilihan:
                    st.error("⚠️ Kamu belum memilih satu pun ciri. Pilih minimal 1 ciri untuk melihat hasil.")
                else:
                    # Perform Forward Chaining and navigate
                    st.session_state["hasil_tes"] = hitung_hasil(pilihan)
                    pindah_halaman("Hasil & Rekomendasi")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ── 16. HALAMAN HASIL & REKOMENDASI ──────────────────────────────────────────
def tampilkan_hasil():
    st.markdown("<div class='hero-title' style='font-size: 2.3rem; text-align: left;'>Hasil Identifikasi Gaya Belajar</div>", unsafe_allow_html=True)

    # Empty State Validation
    if not st.session_state["hasil_tes"] or not st.session_state["pilihan_user"]:
        st.markdown("""
        <div class='card' style='text-align: center; padding: 45px 30px; margin-top: 20px;'>
            <div style='font-size: 3.5rem; margin-bottom: 16px;'>🔍</div>
            <h3 style='color: #6C4FF6; margin: 0 0 10px; font-weight: 800; font-size: 1.5rem;'>Kamu belum mengikuti tes</h3>
            <p style='color: #64748B; font-size: 1.05rem; margin-bottom: 24px;'>Silakan isi kuesioner terlebih dahulu untuk mengenali gaya belajarmu.</p>
        </div>
        """, unsafe_allow_html=True)
        
        c_left, c_middle, c_right = st.columns([2, 1.4, 2])
        with c_middle:
            st.markdown("<div class='center-btn-container'>", unsafe_allow_html=True)
            if st.button("Mulai Tes Sekarang", key="btn_ke_tes_empty", use_container_width=True):
                st.session_state["step"] = 1
                pindah_halaman("Tes Gaya Belajar")
            st.markdown("</div>", unsafe_allow_html=True)
        return

    hasil = st.session_state["hasil_tes"]
    identitas = st.session_state["identitas"]
    pilihan = st.session_state["pilihan_user"]

    # Calculate top scoring styles
    sorted_hasil = sorted(hasil.items(), key=lambda x: x[1]["persen"], reverse=True)
    max_persen = sorted_hasil[0][1]["persen"]
    gaya_dominan = [g for g, d in sorted_hasil if d["persen"] == max_persen]
    
    g_dom = gaya_dominan[0]
    info = info_gaya[g_dom]

    # Warning if too few choices
    if len(pilihan) < 3:
        st.warning("⚠️ Ciri-ciri yang kamu pilih kurang dari 3. Hasil mungkin kurang akurat atau kurang kuat mendeskripsikan gaya belajarmu.")

    # Status Badges
    if max_persen == 100:
        status_txt, badge_class = "Seluruh ciri terpenuhi", "b-ok"
    elif len(gaya_dominan) > 1:
        status_txt, badge_class = "Kemungkinan gaya belajar campuran", "b-mix"
    else:
        status_txt, badge_class = "Kecenderungan tertinggi berdasarkan ciri yang dipilih", "b-part"

    # Identity Chip Row
    kelas_str = f"&nbsp;&nbsp;•&nbsp;&nbsp;🎒 Kelas {identitas.get('kelas')}" if identitas.get("kelas") else ""
    st.markdown(f"""
    <div class='card' style='padding: 16px 24px; font-size: 0.98rem; color: #4B5563; display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px;'>
        <span>👤 <b>{identitas.get("nama","")}</b></span>
        <span>&nbsp;&nbsp;•&nbsp;&nbsp;🏫 {identitas.get("jenjang","")}{kelas_str}</span>
        <span>&nbsp;&nbsp;•&nbsp;&nbsp;📅 {identitas.get("tanggal","")}</span>
    </div>
    """, unsafe_allow_html=True)

    # Style labels and description for mixed
    if len(gaya_dominan) > 1:
        label_gaya = " & ".join(gaya_dominan)
        desk_gabung = " ".join([info_gaya[g]["desk"] for g in gaya_dominan])
    else:
        label_gaya = g_dom
        desk_gabung = info["desk"]

    # Main Result Card
    st.markdown(f"""
    <div class='card' style='background: linear-gradient(135deg, #E3F8FF 0%, #FFFFFF 60%, #FFF4E6 100%); border-left: 6px solid {info["hex"]}; padding: 32px; border-radius: 24px; box-shadow: 0 12px 36px rgba(7, 22, 74, 0.06);'>
        <div style='font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--muted); margin-bottom: 8px;'>Gaya Belajar Dominan</div>
        <div style='font-size: 2.8rem; font-weight: 800; color: var(--navy); line-height: 1.1; margin-bottom: 12px; font-family: "Plus Jakarta Sans", sans-serif;'>
            {info["emoji"]} <span style='color: {info["hex"]};'>{label_gaya}</span>
        </div>
        <div style='display: flex; gap: 8px; align-items: center; margin-bottom: 20px; flex-wrap: wrap;'>
            <span class="badge" style="background: {info["hex"]}22; color: {info["hex"]}; border: 1px solid {info["hex"]}44; font-size: 0.9rem; padding: 6px 16px; border-radius: 30px; font-weight: 700;">Kecocokan {max_persen:.0f}%</span>
            <span class="badge {badge_class}" style="font-size: 0.9rem; padding: 6px 16px; border-radius: 30px;">{status_txt}</span>
        </div>
        <div style='font-size: 1.05rem; color: var(--navy); line-height: 1.7; margin-top: 10px;'>
            {desk_gabung}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recommendations Section
    st.markdown("<div class='sec-title'>Rekomendasi Cara Belajar</div>", unsafe_allow_html=True)
    rek_points = rekomendasi[g_dom]
    
    st.markdown("<div style='margin-bottom: 24px;'>", unsafe_allow_html=True)
    cols_rek = st.columns(min(len(rek_points), 5))
    for i, r_point in enumerate(rek_points[:5]):
        with cols_rek[i]:
            st.markdown(f"""
            <div class='card' style='height: 100%; padding: 20px; border-top: 4px solid #6C4FF6; margin-bottom: 0;'>
                <div style='font-weight: 800; color: #6C4FF6; font-size: 1.5rem; margin-bottom: 8px;'>0{i+1}</div>
                <div style='font-size: 0.93rem; color: #374151; line-height: 1.5;'>{r_point}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bar chart - Kecocokan Semua Gaya Belajar (Pertahankan logika/visual asli tapi perindah detailnya)
    st.markdown("<div class='sec-title'>Kecocokan Semua Gaya Belajar</div>", unsafe_allow_html=True)
    bars = ""
    for g, d in sorted_hasil:
        pct = d["persen"]
        hx = info_gaya[g]["hex"]
        em = info_gaya[g]["emoji"]
        pct_label = f"{pct:.0f}%" if pct >= 12 else ""
        bars += f"""
        <div style='margin-bottom: 14px;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.92rem; font-weight: 700; color: #374151; margin-bottom: 4px;'>
                <span>{em} {g}</span>
                <span style='color: {hx}; font-weight: 800;'>{pct:.1f}%</span>
            </div>
            <div class='prog-bg' style='height: 16px;'>
                <div class='prog-bar' style='width: {pct}%; background: {hx}; height: 16px; font-size: 0.75rem; font-weight: 800;'>{pct_label}</div>
            </div>
        </div>"""
    st.markdown(f"<div class='card' style='padding: 24px 28px;'>{bars}</div>", unsafe_allow_html=True)

    # Chips for Selected Characteristics (NEW REQUIREMENT - no Cxx)
    st.markdown("<div class='sec-title'>Ciri-Ciri yang Kamu Pilih</div>", unsafe_allow_html=True)
    with st.expander("Lihat semua ciri yang kamu pilih dalam tes ini", expanded=True):
        if pilihan:
            col_c1, col_c2 = st.columns(2)
            for idx, kode in enumerate(pilihan):
                teks_ciri = fakta_tampil[kode]
                with col_c1 if idx % 2 == 0 else col_c2:
                    st.markdown(f"""
                    <div class='ciri-chip'>
                        <span style='color: var(--primary-blue); font-size: 1.1rem; font-weight: 900;'>✓</span>
                        <span style='font-size: 0.92rem; color: var(--navy); line-height: 1.4; font-weight: 500;'>{teks_ciri}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.write("Tidak ada ciri yang dipilih.")

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # PDF Download and Reset Buttons Row
    c_dl, _, c_ul = st.columns([1.8, 2, 1.8])
    with c_dl:
        try:
            pdf_bytes = buat_pdf()
            # Sanitasi nama untuk file name
            nama_file = re.sub(r'[^a-z0-9_]', '', identitas.get("nama","pengguna").lower().replace(" ","_"))
            st.download_button(
                "📥 Download Hasil PDF",
                data=pdf_bytes,
                file_name=f"hasil_gaya_belajar_{nama_file}.pdf",
                mime="application/pdf",
                key="btn_download_pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning("⚠️ Gagal membuat PDF. Silakan coba sesaat lagi.")
            import traceback
            traceback.print_exc()

    with c_ul:
        if st.button("🔄 Ulangi Tes", key="btn_ulangi_tes", use_container_width=True):
            # Reset states and rerun
            st.session_state["pilihan_user"] = []
            st.session_state["hasil_tes"] = None
            st.session_state["identitas"] = {"nama": "", "jenjang": "SMA/SMK", "kelas": ""}
            st.session_state["step"] = 1
            for k in fakta_tampil.keys():
                st.session_state[f"cb_{k}"] = False
            pindah_halaman("Tes Gaya Belajar")

# ── 17. HALAMAN TENTANG APLIKASI ──────────────────────────────────────────────
def tampilkan_tentang_aplikasi():
    st.markdown("<div class='hero-title' style='font-size: 2.5rem; text-align: left; margin-bottom: 8px;'>Tentang Aplikasi</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub' style='text-align: left; margin-bottom: 24px; max-width: 100%;'>Informasi mengenai aplikasi, landasan teori, dan pengembang.</div>", unsafe_allow_html=True)
    
    col_kiri, col_kanan = st.columns(2)
    
    with col_kiri:
        st.markdown("""
        <div class='card' style='border-left: 5px solid var(--primary-blue); height: 100%; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
                <span style='font-size: 1.5rem;'>🎯</span>
                <span style='font-weight: 700; font-size: 1.25rem; color: var(--navy);'>Apa fungsi aplikasi ini?</span>
            </div>
            <p style='color: var(--navy); opacity: 0.85; font-size: 0.98rem; line-height: 1.65; margin: 0;'>
                Aplikasi ini membantu pengguna mengenali kecenderungan gaya belajar berdasarkan ciri-ciri yang dipilih. Hasil yang diberikan berupa <b>gaya belajar dominan</b> dan <b>rekomendasi cara belajar</b> yang lebih sesuai.
            </p>
            <div style='margin-top: 16px; display: flex; gap: 6px; flex-wrap: wrap;'>
                <span style='background: #EAF4F7; color: var(--primary-blue); font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(45, 156, 219, 0.2);'>Python</span>
                <span style='background: #EAF4F7; color: var(--primary-blue); font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(45, 156, 219, 0.2);'>Streamlit</span>
                <span style='background: #EAF4F7; color: var(--primary-blue); font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(45, 156, 219, 0.2);'>Forward Chaining</span>
                <span style='background: #EAF4F7; color: var(--primary-blue); font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(45, 156, 219, 0.2);'>Rule-Based Expert System</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card' style='border-left: 5px solid var(--orange); height: 100%; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
                <span style='font-size: 1.5rem;'>⚠️</span>
                <span style='font-weight: 700; font-size: 1.25rem; color: var(--navy);'>Batasan Penggunaan</span>
            </div>
            <p style='color: var(--navy); opacity: 0.85; font-size: 0.98rem; line-height: 1.65; margin: 0;'>
                Aplikasi ini merupakan alat bantu identifikasi awal gaya belajar berdasarkan ciri-ciri yang dipilih pengguna. Basis pengetahuan diadaptasi dari penelitian pada siswa SD, sehingga penggunaan pada jenjang lain perlu dipahami sebagai perluasan implementasi dan bukan hasil validasi psikologis mutlak.
        </div>
        """, unsafe_allow_html=True)
 
    with col_kanan:
        st.markdown("""
        <div class='card' style='border-left: 5px solid var(--navy); margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
                <span style='font-size: 1.5rem;'>📚</span>
                <span style='font-weight: 700; font-size: 1.25rem; color: var(--navy);'>Sumber Pengembangan</span>
            </div>
            <div style='color: var(--navy); opacity: 0.85; font-size: 0.95rem; line-height: 1.65;'>
                <div style='margin-bottom: 8px;'><b>Judul Jurnal:</b><br><span style='color: var(--navy); font-weight: 700;'>Sistem Pakar Penentuan Gaya Belajar Siswa Dengan Metode Forward Chaining Berbasis Web</span></div>
                <div style='margin-bottom: 8px;'><b>Penulis:</b><br><span style='color: var(--navy); font-weight: 700;'>Laelia Puti Aditasari, Mega Novita, Rahmat Robi Waliyansyah</span></div>
                <div style='margin-bottom: 8px;'><b>Jurnal:</b><br><span style='color: var(--navy); font-weight: 700;'>IT Journal Research and Development (ITJRD), Vol. 5, No. 1, 2020, hlm. 32–44</span></div>
                <div style='margin-bottom: 8px;'><b>DOI:</b> <span style='color: var(--navy); font-weight: 700;'>10.25299/itjrd.2020.vol5(1).4740</span></div>
            </div>
            <p style='color: var(--muted); font-size: 0.88rem; line-height: 1.6; border-top: 1px solid var(--border); padding-top: 12px; margin-top: 12px; margin-bottom: 0;'>
                Aplikasi ini dikembangkan sebagai implementasi ulang berbasis Streamlit dengan mengadaptasi konsep, basis aturan, dan metode Forward Chaining dari jurnal acuan. Sistem pada jurnal asli dikembangkan berbasis web menggunakan PHP dan MySQL, sedangkan aplikasi ini dibuat sebagai versi pembelajaran menggunakan Python dan Streamlit.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card' style='border-left: 4px solid #94A3B8; margin-bottom: 20px; padding: 16px 20px;'>
            <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 10px;'>
                <span style='font-size: 1.1rem;'>👤</span>
                <span style='font-weight: 700; font-size: 1rem; color: var(--navy);'>Pengembang</span>
            </div>
            <div style='font-size: 1rem; font-weight: 700; color: var(--navy); margin-bottom: 4px;'>Devi Andini Sastro</div>
            <div style='color: var(--muted); font-size: 0.82rem; line-height: 1.5;'>
                Project Akhir Mata Kuliah Sistem Berbasis Pengetahuan / Sistem Pakar
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── INFORMASI AKADEMIK SISTEM ──────────────────────────────────────────────
    st.markdown("""
    <div style='margin-top: 36px; margin-bottom: 18px;'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='width: 5px; height: 36px; background: linear-gradient(180deg, #2D9CDB, #6C4FF6); border-radius: 4px; flex-shrink: 0;'></div>
            <div>
                <div style='font-size: 1.35rem; font-weight: 800; color: #172033; line-height: 1.2;'>Informasi Akademik Sistem</div>
                <div style='font-size: 0.88rem; color: #64748B; margin-top: 3px;'>Bagian ini ditampilkan untuk kebutuhan akademik dan validasi sistem.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── EXPANDER 1: BASIS PENGETAHUAN ─────────────────────────────────────────
    with st.expander("📋 Lihat Basis Pengetahuan", expanded=False):
        st.markdown("""
        <div style='background: #F8FAFC; border: 1px solid #D6E3EA; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; font-size: 0.93rem; color: #334155; line-height: 1.6;'>
            Basis pengetahuan berisi fakta berupa ciri-ciri gaya belajar yang digunakan sistem untuk menentukan
            kecenderungan gaya belajar pengguna. Setiap ciri diberi kode tertentu sesuai daftar fakta pada jurnal.
           
        </div>
        """, unsafe_allow_html=True)

        # Build facts table from existing dictionaries
        rows_fakta = []
        # Map each code to its related learning style (from aturan dict)
        kode_ke_gaya = {}
        for gaya, kl in aturan.items():
            for k in kl:
                kode_ke_gaya[k] = gaya

        for kode in sorted(fakta_asli.keys()):
            rows_fakta.append({
                "Kode Fakta": kode,
                "Ciri dari Jurnal": fakta_asli[kode],
                "Versi Tampilan untuk Pengguna": fakta_tampil.get(kode, "-"),
                "Gaya Belajar Terkait": kode_ke_gaya.get(kode, "-"),
            })

        df_fakta = pd.DataFrame(rows_fakta)
        st.dataframe(df_fakta, use_container_width=True, hide_index=True)

    # ── EXPANDER 2: ATURAN INFERENSI ──────────────────────────────────────────
    with st.expander("⚙️ Lihat Aturan Inferensi", expanded=False):
        st.markdown("""
        <div style='background: #F8FAFC; border: 1px solid #D6E3EA; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; font-size: 0.93rem; color: #334155; line-height: 1.6;'>
            Aturan inferensi digunakan untuk menghubungkan kumpulan ciri belajar dengan hasil gaya belajar.
            Sistem menggunakan format <b>IF-THEN</b> sesuai aturan pada jurnal.
            Gaya belajar dengan persentase kecocokan tertinggi akan ditampilkan sebagai hasil dominan.
        </div>
        """, unsafe_allow_html=True)

        # Table of rules
        rows_rule = []
        rule_names = {"Visual": "R1", "Auditori": "R2", "Kinestetik": "R3",
                      "Verbal": "R4", "Logis": "R5", "Interpersonal": "R6", "Intrapersonal": "R7"}
        for gaya, kl in aturan.items():
            rows_rule.append({
                "Kode Rule": rule_names[gaya],
                "Kondisi IF (kode ciri)": " AND ".join(kl),
                "Hasil THEN": f"Gaya Belajar {gaya}",
            })
        df_rule = pd.DataFrame(rows_rule)
        st.dataframe(df_rule, use_container_width=True, hide_index=True)

        # Visual rule cards
        st.markdown("<div style='margin-top: 20px; margin-bottom: 8px; font-weight: 700; color: #172033; font-size: 0.95rem;'>Visualisasi Aturan IF-THEN:</div>", unsafe_allow_html=True)
        rule_colors = {
            "Visual": "#2D9CDB", "Auditori": "#6C63FF", "Kinestetik": "#F28C28",
            "Verbal": "#C7356D", "Logis": "#10B981", "Interpersonal": "#14A3A3", "Intrapersonal": "#07164A"
        }
        cards_html = "<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin-top: 4px;'>"
        for gaya, kl in aturan.items():
            rcode = rule_names[gaya]
            color = rule_colors[gaya]
            kode_str = " + ".join(kl)
            cards_html += f"""
            <div style='background: #FFFFFF; border: 1.5px solid #D6E3EA; border-left: 4px solid {color};
                        border-radius: 14px; padding: 14px 16px; box-shadow: 0 4px 12px rgba(7,22,74,0.05);'>
                <div style='font-size: 0.78rem; font-weight: 800; color: {color}; letter-spacing: 0.5px;
                            text-transform: uppercase; margin-bottom: 6px;'>{rcode} — {gaya}</div>
                <div style='font-size: 0.82rem; color: #475569; font-family: monospace; line-height: 1.6;
                            margin-bottom: 8px; word-break: break-word;'>{kode_str}</div>
                <div style='font-size: 0.85rem; font-weight: 700; color: {color};'>→ Gaya Belajar {gaya}</div>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

# ── 18. HALAMAN AKADEMIK (hanya jika SHOW_ACADEMIC_MODE = True) ───────────────
def tampilkan_basis_pengetahuan():
    st.markdown("<div class='hero-title' style='font-size:2rem;'>Basis Pengetahuan</div>", unsafe_allow_html=True)
    st.info("Halaman ini hanya ditampilkan dalam mode akademik.")
    with st.expander("Tabel Fakta", expanded=True):
        rows = []
        for gaya, kl in aturan.items():
            for k in kl:
                rows.append({"Kode":k,"Ciri Asli":fakta_asli[k],"Ciri Tampilan":fakta_tampil[k],"Gaya":gaya})
        st.dataframe(pd.DataFrame(rows).sort_values("Kode"), use_container_width=True, hide_index=True)
    with st.expander("Rule IF-THEN", expanded=False):
        rr = [{"Rule":f"R{i}","IF":" AND ".join(kl),"THEN":f"Gaya Belajar {g}"}
              for i,(g,kl) in enumerate(aturan.items(),1)]
        st.dataframe(pd.DataFrame(rr), use_container_width=True, hide_index=True)

def tampilkan_metode():
    st.markdown("<div class='hero-title' style='font-size:2rem;'>Metode Sistem Pakar</div>", unsafe_allow_html=True)
    st.info("Halaman ini hanya ditampilkan dalam mode akademik.")
    st.markdown("""
    <div class='card'>
        <b>Forward Chaining</b> adalah metode inferensi yang dimulai dari fakta yang diketahui menuju kesimpulan.<br><br>
        Pada aplikasi ini:<br>
        1. Ciri yang dipilih pengguna = fakta awal.<br>
        2. Sistem mencocokkan fakta dengan Rule IF-THEN (R1-R7).<br>
        3. Skor = jumlah ciri cocok / total ciri dalam rule x 100%.<br>
        4. Gaya belajar dengan skor tertinggi = hasil dominan.
    </div>
    """, unsafe_allow_html=True)

# ── 19. SIDEBAR & ROUTING ────────────────────────────────────────────────────
menu_utama = ["Beranda", "Tes Gaya Belajar", "Hasil & Rekomendasi", "Tentang Aplikasi"]
menu_akademik = ["Basis Pengetahuan", "Metode Sistem"]

menu_pilihan = menu_utama + (menu_akademik if SHOW_ACADEMIC_MODE else [])

with st.sidebar:
    # Circle Logo & Title Header
    _logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    try:
        with open(_logo_path, "rb") as _f:
            _logo_b64 = base64.b64encode(_f.read()).decode()
        _logo_html = f"<img src='data:image/png;base64,{_logo_b64}' style='width:105px; height:105px; border-radius:50%; object-fit:cover; border:2px solid #FFFFFF; box-shadow:0 8px 24px rgba(7,22,74,0.15);'>"
    except Exception:
        _logo_html = "<div style='width:105px;height:105px;border-radius:50%;background:linear-gradient(135deg,#07164A,#2D9CDB);display:flex;align-items:center;justify-content:center;margin:0 auto;box-shadow:0 8px 24px rgba(7,22,74,0.15);border:2px solid #FFFFFF;'><span style='color:#FFFFFF;font-weight:800;font-size:1.8rem;'>GB</span></div>"

    st.markdown(f"""
    <div style='text-align: center; padding: 8px 0 8px;'>
        <div style='margin: 0 auto; width: fit-content;'>
            {_logo_html}
        </div>
        <div style='font-weight: 800; font-size: 1.05rem; color: var(--navy); margin-top: 8px; line-height: 1.3;'>Sistem Pakar Gaya Belajar</div>
        <div style='font-size: 0.72rem; color: var(--primary-blue); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px;'>Forward Chaining Method</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 6px; border-bottom: 1px solid var(--border); margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    # Render Pills/Buttons using st.radio with custom CSS
    idx_aktif = menu_pilihan.index(st.session_state["menu"]) if st.session_state["menu"] in menu_pilihan else 0
    menu_terpilih = st.radio(
        "Menu", menu_pilihan, index=idx_aktif,
        label_visibility="collapsed"
    )
    if menu_terpilih != st.session_state["menu"]:
        st.session_state["menu"] = menu_terpilih
        st.rerun()

    # Footer section
    st.markdown("""
    <div style='font-size: 0.78rem; color: #64748B; text-align: center; line-height: 1.6; margin-top: 50px; border-top: 1px solid #E2E8F0; padding-top: 16px;'>
        <b>Dikembangkan oleh Devi Andini</b><br>
        <span style='color: #94A3B8;'>Project Akhir Sistem Pakar</span>
    </div>
    """, unsafe_allow_html=True)

# Routing Halaman
halaman = st.session_state["menu"]
if halaman == "Beranda":
    tampilkan_beranda()
elif halaman == "Tes Gaya Belajar":
    tampilkan_tes()
elif halaman == "Hasil & Rekomendasi":
    tampilkan_hasil()
elif halaman == "Tentang Aplikasi":
    tampilkan_tentang_aplikasi()
elif halaman == "Basis Pengetahuan" and SHOW_ACADEMIC_MODE:
    tampilkan_basis_pengetahuan()
elif halaman == "Metode Sistem" and SHOW_ACADEMIC_MODE:
    tampilkan_metode()
