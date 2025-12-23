import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Duygu Arkadaşı Tavşan", layout="centered")

# --- SES OLUŞTURMA (Hızlı ve Çocuksu) ---
def ses_olustur(metin):
    # slow=False sesi daha hızlı ve enerjik (çocuksu) yapar
    tts = gTTS(text=metin, lang='tr', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- DURUM YÖNETİMİ ---
if "notlar" not in st.session_state:
    st.session_state.notlar = []
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{"rol": "tavsan", "metin": "Merhaba arkadaşım! Bugün seninle oyun oynamak ve sohbet etmek için sabırsızlanıyorum. Günün nasıl geçti?"}]
    st.session_state.ilk_ses_caldi = False

# --- TAVŞAN GÖRSELLERİ (Emojiler yerine temiz ikonlar) ---
tavsan_resimleri = {
    "normal": "https://img.icons8.com/color/200/rabbit.png",
    "mutlu": "https://img.icons8.com/color/200/happy-rabbit.png",
    "uzgun": "https://img.icons8.com/color/200/sad-rabbit.png"
}

# --- ARAYÜZ ---
st.title("Duygu Arkadaşı")

# Tavşan Durumu Seçimi
durum = "normal"
if len(st.session_state.mesajlar) > 1:
    son_mesaj = st.session_state.mesajlar[-1]["metin"].lower()
    if any(k in son_mesaj for k in ["harika", "sevindim", "yaşasın"]): durum = "mutlu"
    if any(k in son_mesaj for k in ["anlıyorum", "yanındayım", "üzülme"]): durum = "uzgun"

st.image(tavsan_resimleri[durum], width=180)

# --- SOHBET AKIŞI ---
# İlk mesajı sesli oku (Sadece bir kere)
if not st.session_state.ilk_ses_caldi:
    st.write(f"**Tavşan:** {st.session_state.mesajlar[0]['metin']}")
    st.audio(ses_olustur(st.session_state.mesajlar[0]['metin']), format='audio/mp3', autoplay=True)
    st.session_state.ilk_ses_caldi = True

# Önceki mesajları göster
for mesaj in st.session_state.mesajlar[1:]:
    kim = "**Sen:** " if mesaj["rol"] == "cocuk" else "**Tavşan:** "
    st.write(kim + mesaj["metin"])

# --- SESLİ GİRDİ ---
st.write("---")
text = speech_to_text(language='tr', start_prompt="Konuşmak için dokun", stop_prompt="Dinliyorum...", key='recorder')

if text:
    # Çocuğun mesajını ekle
    st.session_state.mesajlar.append({"rol": "cocuk", "metin": text})
    st.session_state.notlar.append(f"{datetime.now().strftime('%H:%M')} - Çocuk: {text}")
    
    # Cevap üret (Basit Mantık)
    cevap = "Seni dinliyorum arkadaşım, anlatmaya devam et."
    if "iyi" in text.lower(): cevap = "Yaşasın! Bunu duyduğuma çok sevindim!"
    elif "üzgün" in text.lower() or "kötü" in text.lower(): cevap = "Canım arkadaşım, ben her zaman senin yanındayım. Bana her şeyi anlatabilirsin."
    
    st.session_state.mesajlar.append({"rol": "tavsan", "metin": cevap})
    st.rerun()

# --- VELİ PANELİ ---
with st.sidebar:
    st.header("Veli Alanı")
    if st.text_input("Şifre", type="password") == "1234":
        st.write("### Sohbet Kayıtları")
        for n in st.session_state.notlar:
            st.text(n)
