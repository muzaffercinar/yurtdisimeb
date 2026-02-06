import streamlit as st
import random
import json

# Sayfa Yapısı - Mobil Odaklı
st.set_page_config(page_title="MC MEB PRO", page_icon="🚀", layout="centered")

# --- VERİ YÜKLEME ---
def load_data():
    try:
        with open('mc_soru_bankasi.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Veri yüklenemedi: {e}")
        return []

import hashlib
import hmac
import base64
import uuid

# --- CİHAZ KİLİTLEME SİSTEMİ ---
# Bu "SECRET_KEY", lisans_ureteci.py dosyasındaki ile AYNI olmalıdır!
SECRET_KEY = b"MUZAFFER_CINAR_2026_MASTER_KEY"

def get_device_id():
    """Tarayıcı oturumu için kalıcı olmayan ama session süresince sabit bir ID üretir"""
    if 'device_id' not in st.session_state:
        # Rastgele bir UUID üret (Gerçek uygulamada LocalStorage kullanılır)
        st.session_state.device_id = str(uuid.uuid4())[:8].upper()
    return st.session_state.device_id

def validate_license(device_id, input_key):
    """Girilen anahtarın, bu cihaz ID'si için geçerli olup olmadığını kontrol eder"""
    try:
        # Doğru anahtarı hesapla
        signature = hmac.new(SECRET_KEY, device_id.encode('utf-8'), hashlib.sha256).digest()
        license_key = base64.urlsafe_b64encode(signature).decode('utf-8').upper()
        
        import re
        clean_key = re.sub(r'[^A-Z0-9]', '', license_key)
        correct_key = clean_key[:6]
        
        return input_key.strip().upper() == correct_key
    except:
        return False

# --- GİRİŞ EKRANI ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

device_id = get_device_id()

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .stTextInput > div > div > input {text-align: center; letter-spacing: 5px; font-family: monospace;}
    .big-text {font-size: 24px; font-weight: bold; color: #1E88E5; text-align: center;}
    </style>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913133.png", width=100)
    st.title("🔐 Lisans Aktivasyonu")
    
    st.info("Bu eğitim seti **tek bir cihazda** kullanım için lisanslanmıştır.")
    
    st.markdown("### Adım 1: Cihaz Kodunuzu Kopyalayın")
    st.code(device_id, language="text")
    
    st.markdown("### Adım 2: Kodu Gönderin ve Şifre Alın")
    
    st.warning("⚠️ Güvenlik gereği otomatik mail butonu pasife alınmıştır.")
    st.info("Lütfen aşağıdaki Cihaz Kodunu kopyalayıp, şu adrese mail atınız:")
    st.code("muzaffercinarofficial@gmail.com", language="text")
    st.caption(f"(Konu kısmına 'Lisans Talebi - {device_id}' yazınız)")
    
    st.markdown("### Adım 3: Gelen Şifreyi Girin")
    license_input = st.text_input("Aktivasyon Şifresi", placeholder="XXXXXX")
    
    if st.button("🔓 GİRİŞ YAP"):
        if validate_license(device_id, license_input):
            st.session_state.authenticated = True
            st.success("Lisans Doğrulandı! Yönlendiriliyorsunuz...")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Hatalı Şifre! Bu şifre bu cihaza ait değil.")
            
    st.stop()




# --- GİRİŞ BAŞARILI İSE DEVAM ET ---
if st.session_state.questions:
    st.sidebar.success("✅ Giriş Başarılı - Hoş Geldiniz!")
    st.progress((st.session_state.index + 1) / len(st.session_state.questions))
    
    curr = st.session_state.questions[st.session_state.index]
    
    # JSON anahtarlarını, eski yapıya (q, a, hap) uygun hale getirelim
    soru_metni = curr.get('q', 'Soru Yok')
    cevap_metni = curr.get('a', 'Cevap Yok')
    hap_bilgi = curr.get('key', curr.get('hap', '')) # 'key' veya 'hap' kullan
    
    with st.container():
        st.markdown(f"### ❓ {soru_metni}")
        
        if st.button("👉 CEVABI VE HAP BİLGİYİ GÖR"):
            st.success(f"✅ **CEVAP:** {cevap_metni}")
            if hap_bilgi:
                st.warning(f"💡 **HAP BİLGİ:** {hap_bilgi}")

    
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Biliyorum (Puan Ver)"):
                st.session_state.correct_count += 1
                st.session_state.index = (st.session_state.index + 1) % len(st.session_state.questions)
                st.rerun()
        with col2:
            if st.button("❌ Tekrar Et (Atla)"):
                st.session_state.index = (st.session_state.index + 1) % len(st.session_state.questions)
                st.rerun()
    
    # --- ANALİZ PANELİ ---
    st.sidebar.title("📊 Rasyonel Analiz")
    st.sidebar.write(f"**Doğru Bilgi:** {st.session_state.correct_count}")
    st.sidebar.write(f"**Toplam Soru:** {len(st.session_state.questions)}")
    if len(st.session_state.questions) > 0:
        basari_orani = int((st.session_state.correct_count / len(st.session_state.questions)) * 100)
        st.sidebar.metric("Başarı Oranı", f"%{basari_orani}")
    
    if st.sidebar.button("🗑️ Verileri Sıfırla"):
        st.session_state.index = 0
        st.session_state.correct_count = 0
        random.shuffle(st.session_state.questions)
        st.rerun()

else:
    st.warning("Soru bankası yüklenemedi veya boş.")