import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import base64
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Duygu Arkadaşı", page_icon="🐰")

# --- CSS İLE GÜZELLEŞTİRME ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F8FF; }
    .tavsan-container { display: flex; justify-content: center; margin-bottom: 20px; }
    .chat-box { background: white; padding: 20px; border-radius: 15px; border: 2px solid #87CEEB; }
    </style>
    """, unsafe_allow_html=True)

# --- ASİSTAN MANTIĞI ---
if "notlar" not in st.session_state:
    st.session_state.notlar = []

def cevap_uret(metin):
    metin = metin.lower()
    if "mutlu" in metin or "iyi" in metin:
        return "Harika! Senin mutlu olman beni de zıplatıyor! 🐰✨", "mutlu"
    elif "üzgün" in metin or "kötü" in metin:
        return "Üzülme arkadaşım, yanındayım. Bir sarılmaya ne dersin? 🫂", "uzgun"
    elif "korku" in metin or "korkuyorum" in metin:
        return "Derin bir nefes al... Ben buradayım, güvendesin. 🌟", "korku"
    else:
        return "Seni dinliyorum, anlatmak istediğin başka bir şey var mı? 😊", "normal"

# --- TAVŞAN GÖRSELİ (URL veya Yerel Dosya) ---
# Buraya internetten bulduğun hareketli tavşan GIF linklerini ekleyebilirsin
tavsan_gifleri = {
    "normal": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ2VudGlmaWVyJmN0PWc/3o7TKSjP6S5fthJCuQ/giphy.gif",
    "mutlu": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ2VudGlmaWVyJmN0PWc/l41lTfuxV5wWvJv9S/giphy.gif",
    "uzgun": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6bmR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZ2VudGlmaWVyJmN0PWc/3o7TKMGpxx7UuF4U5W/giphy.gif"
}

# --- ARAYÜZ ---
st.title("🐰 Duygu Arkadaşı Tavşan")

# Tavşanı Göster
durum = st.session_state.get("durum", "normal")
st.image(tavsan_gifleri.get(durum, tavsan_gifleri["normal"]), width=300)

st.write("### Hadi Konuşalım!")
# Sesli Kayıt Butonu
text = speech_to_text(language='tr', start_prompt="🎤 Konuşmak için bas", stop_prompt="⏹️ Durdur", key='recorder')

if text:
    st.write(f"**Sen:** {text}")
    cevap, yeni_durum = cevap_uret(text)
    st.session_state.durum = yeni_durum
    
    # Notları Kaydet (Veli için)
    st.session_state.notlar.append(f"{datetime.now().strftime('%H:%M')} - Çocuk: {text} | Duygu: {yeni_durum}")
    
    st.write(f"**Tavşan:** {cevap}")
    
    # Sese Çevir ve Oynat
    tts = gTTS(text=cevap, lang='tr')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    st.audio(audio_fp, format='audio/mp3', autoplay=True)

# --- VELİ BÖLÜMÜ ---
with st.sidebar:
    st.header("🔐 Veli Paneli")
    sifre = st.text_input("Şifre", type="password")
    if sifre == "1234":
        st.write("### Görüşme Analizi")
        for not_item in st.session_state.notlar:
            st.text(not_item)
        if st.button("Raporu İndir"):
            rapor = "\n".join(st.session_state.notlar)
            st.download_button("Dosyayı Kaydet", rapor, file_name="analiz.txt")
