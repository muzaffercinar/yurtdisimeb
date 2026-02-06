import streamlit as st
import random
import json
import time
import hashlib
import hmac
import base64
import re

# Sayfa Yapısı
st.set_page_config(page_title="MC MEB PRO", page_icon="🚀", layout="centered")

# --- VERİ YÜKLEME ---
@st.cache_data
def load_questions():
    try:
        with open('mc_soru_bankasi.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@st.cache_data
def load_ai_questions():
    try:
        with open('ai_questions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@st.cache_data
def load_hap_bilgiler():
    try:
        from cikmis_sorular import get_hap_bilgiler
        haplar = get_hap_bilgiler()
        questions = []
        for bilgi in haplar:
            if ':' in bilgi:
                q, a = bilgi.split(':', 1)
                questions.append({"q": q.strip() + "?", "a": a.strip(), "cat": "Hap Bilgi"})
            else:
                questions.append({"q": bilgi.strip(), "a": "", "cat": "Hap Bilgi"})
        return questions
    except:
        return []

# --- KULLANICI KODU LİSANS SİSTEMİ ---
SECRET_KEY = b"MUZAFFER_CINAR_2026_MASTER_KEY"

def validate_license(user_code, input_key):
    try:
        user_code = user_code.strip().upper()
        signature = hmac.new(SECRET_KEY, user_code.encode('utf-8'), hashlib.sha256).digest()
        license_key = base64.urlsafe_b64encode(signature).decode('utf-8').upper()
        clean_key = re.sub(r'[^A-Z0-9]', '', license_key)
        return input_key.strip().upper() == clean_key[:6]
    except:
        return False

# --- SESSION STATE BAŞLATMA ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_code' not in st.session_state:
    st.session_state.user_code = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "menu"
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'timer_end' not in st.session_state:
    st.session_state.timer_end = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# URL'den otomatik login
query_params = st.query_params
if not st.session_state.authenticated:
    if "user" in query_params and "key" in query_params:
        if validate_license(query_params["user"], query_params["key"]):
            st.session_state.authenticated = True
            st.session_state.user_code = query_params["user"]

# === LİSANS EKRANI ===
if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .stTextInput > div > div > input {text-align: center; letter-spacing: 3px; font-family: monospace;}
    </style>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913133.png", width=100)
    st.title("🔐 Lisans Aktivasyonu")
    st.info("Bu eğitim seti lisanslı kullanıcılar içindir.")
    
    st.markdown("### Adım 1: Kullanıcı Kodunuzu Girin")
    user_code_input = st.text_input("Kullanıcı Kodu", placeholder="MEB001")
    
    st.markdown("### Adım 2: Aktivasyon Şifrenizi Girin")
    license_input = st.text_input("Aktivasyon Şifresi", placeholder="XXXXXX", type="password")
    
    st.divider()
    st.info("📧 Şifre almak için kullanıcı kodunuzu **ufomath@gmail.com** adresine gönderin.")
    
    if st.button("🔓 GİRİŞ YAP", use_container_width=True):
        if not user_code_input.strip():
            st.error("❌ Kullanıcı Kodunu girin!")
        elif not license_input.strip():
            st.error("❌ Şifreyi girin!")
        elif validate_license(user_code_input, license_input):
            st.session_state.authenticated = True
            st.session_state.user_code = user_code_input.strip().upper()
            st.query_params["user"] = user_code_input.strip().upper()
            st.query_params["key"] = license_input.strip().upper()
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Hatalı şifre!")
    st.stop()

# === ANA UYGULAMA ===
all_questions = load_questions()
ai_questions = load_ai_questions()
hap_questions = load_hap_bilgiler()
categories = sorted(list(set(q.get("cat", "Genel") for q in all_questions)))

# --- YARDIMCI FONKSİYONLAR ---
def start_mode(mode, questions, timer_minutes=None):
    st.session_state.mode = mode
    st.session_state.questions = questions.copy()
    random.shuffle(st.session_state.questions)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.show_answer = False
    if timer_minutes:
        st.session_state.timer_end = time.time() + (timer_minutes * 60)
    else:
        st.session_state.timer_end = None

def go_home():
    st.session_state.mode = "menu"
    st.session_state.timer_end = None

def next_question(correct):
    if correct:
        st.session_state.score += 1
    st.session_state.index += 1
    st.session_state.show_answer = False
    if st.session_state.index >= len(st.session_state.questions):
        st.session_state.mode = "result"

# === ANA MENÜ ===
if st.session_state.mode == "menu":
    st.markdown("## 🎯 ÇALIŞMA MODUNU SEÇİN")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 GENEL SINAV\n(1360 Soru)", use_container_width=True, type="primary"):
            start_mode("exam", all_questions)
            st.rerun()
        
        if st.button("🤖 AI DESTEKLİ\n(Yüksek Olasılık)", use_container_width=True):
            if ai_questions:
                start_mode("exam", ai_questions, timer_minutes=45)
                st.rerun()
            else:
                st.error("AI soru dosyası bulunamadı!")
    
    with col2:
        if st.button("⏱️ DENEME SINAVI\n(100 Soru, 120 dk)", use_container_width=True):
            sample = random.sample(all_questions, min(100, len(all_questions)))
            start_mode("exam", sample, timer_minutes=120)
            st.rerun()
        
        if st.button("💡 HAP BİLGİ\n(Çıkmış Sorular)", use_container_width=True):
            if hap_questions:
                start_mode("exam", hap_questions)
                st.rerun()
            else:
                st.error("Hap bilgi dosyası bulunamadı!")
    
    st.divider()
    st.markdown("### 📂 Kategoriye Göre Çalış")
    selected_cat = st.selectbox("Kategori Seçin", ["Tümü"] + categories)
    if st.button("Seçili Kategori ile Başla"):
        if selected_cat == "Tümü":
            start_mode("exam", all_questions)
        else:
            filtered = [q for q in all_questions if q.get("cat") == selected_cat]
            start_mode("exam", filtered)
        st.rerun()
    
    st.sidebar.success(f"✅ Hoş geldiniz: {st.session_state.user_code}")
    st.sidebar.info(f"📊 Toplam Soru: {len(all_questions)}")

# === SINAV MODU ===
elif st.session_state.mode == "exam":
    questions = st.session_state.questions
    idx = st.session_state.index
    
    if idx >= len(questions):
        st.session_state.mode = "result"
        st.rerun()
    
    # Zamanlayıcı
    if st.session_state.timer_end:
        remaining = int(st.session_state.timer_end - time.time())
        if remaining <= 0:
            st.session_state.mode = "result"
            st.rerun()
        mins, secs = divmod(remaining, 60)
        st.sidebar.error(f"⏱️ Kalan Süre: {mins:02d}:{secs:02d}")
    
    # Üst bilgi
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress((idx + 1) / len(questions))
        st.caption(f"Soru {idx + 1} / {len(questions)}")
    with col2:
        if st.button("🏠 Ana Menü"):
            go_home()
            st.rerun()
    
    # Soru kartı
    q = questions[idx]
    st.markdown(f"### ❓ {q.get('q', 'Soru yok')}")
    
    if q.get("cat"):
        st.caption(f"📁 {q['cat']}")
    
    # Cevap göster butonu
    if not st.session_state.show_answer:
        if st.button("👁️ CEVABU GÖR", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.success(f"✅ **Cevap:** {q.get('a', '-')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ BİLDİM", use_container_width=True, type="primary"):
                next_question(True)
                st.rerun()
        with col2:
            if st.button("❌ BİLMEDİM", use_container_width=True):
                next_question(False)
                st.rerun()
    
    # Sidebar bilgi
    st.sidebar.metric("Doğru", st.session_state.score)
    st.sidebar.metric("Kalan", len(questions) - idx)

# === SONUÇ EKRANI ===
elif st.session_state.mode == "result":
    st.balloons()
    st.markdown("## 🏆 SINAV TAMAMLANDI!")
    
    total = len(st.session_state.questions)
    score = st.session_state.score
    percent = int((score / total) * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Doğru", score)
    col2.metric("❌ Yanlış", total - score)
    col3.metric("📊 Başarı", f"%{percent}")
    
    if percent >= 80:
        st.success("🎉 Mükemmel! Harika bir performans!")
    elif percent >= 60:
        st.info("👍 İyi! Biraz daha çalışarak daha iyi olabilirsin.")
    else:
        st.warning("📚 Daha fazla çalışman gerekiyor.")
    
    if st.button("🏠 Ana Menüye Dön", use_container_width=True):
        go_home()
        st.rerun()