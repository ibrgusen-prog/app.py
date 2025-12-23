import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
from pydub import AudioSegment
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Duygu Arkadaşı Tavşan", layout="centered")

def cocuk_sesi_olustur(metin):
    tts = gTTS(text=metin, lang='tr')
    raw_audio = io.BytesIO()
    tts.write_to_fp(raw_audio)
    raw_audio.seek(0)
    
    # Formatı açıkça belirtelim
    sound = AudioSegment.from_mp3(raw_audio)
    
    # Sesi inceltip hızlandır (Çocuk sesi efekti)
    yeni_sample_rate = int(sound.frame_rate * 1.35) 
    cocuk_sesi = sound._spawn(sound.raw_data, overrides={'frame_rate': yeni_sample_rate})
    cocuk_sesi = cocuk_sesi.set_frame_rate(sound.frame_rate)
    
    out_audio = io.BytesIO()
    cocuk_sesi.export(out_audio, format="mp3")
    return out_audio
    
    # 2. Pydub ile sesi çizgi film karakterine dönüştür
    sound = AudioSegment.from_file(raw_audio, format="mp3")
    
    # Sesi incelt (sample rate artırarak) ve biraz hızlandır
    yeni_sample_rate = int(sound.frame_rate * 1.25) 
    cocuk_sesi = sound._spawn(sound.raw_data, overrides={'frame_rate': yeni_sample_rate})
    cocuk_sesi = cocuk_sesi.set_frame_rate(sound.frame_rate)
    
    # 3. Sonucu gönder
    out_audio = io.BytesIO()
    cocuk_sesi.export(out_audio, format="mp3")
    return out_audio

# --- HAFIZA VE DURUM ---
if "notlar" not in st.session_state:
    st.session_state.notlar = []
if "basladi" not in st.session_state:
    st.session_state.basladi = False
if "durum" not in st.session_state:
    st.session_state.durum = "normal"

# --- TAVŞAN GÖRSELLERİ ---
# GitHub'ına yüklediğin tavşan dosyalarının isimlerini buraya yazmalısın
# Şimdilik hata vermemesi için senin için tasarladığım görsellerin linklerini simüle ediyoruz
tavsan_resimleri = {
    "normal": "https://raw.githubusercontent.com/google/fonts/main/ofl/notocoloremoji/noto_emoji_u1f430.png", # Tavşan emojisi (telifsiz)
    "mutlu": "https://raw.githubusercontent.com/google/fonts/main/ofl/notocoloremoji/noto_emoji_u1f430.png",
    "uzgun": "https://raw.githubusercontent.com/google/fonts/main/ofl/notocoloremoji/noto_emoji_u1f430.png"
}

# --- SOHBET MANTIĞI ---
def cevap_uret(metin):
    metin = metin.lower()
    if any(k in metin for k in ["merhaba", "selam", "naber"]):
        return "Selam arkadaşım! Bugün beraber neler yapalım? Seni gördüğüme çok sevindim!", "normal"
    elif any(k in metin for k in ["mutlu", "iyi", "harika", "süper"]):
        return "Yaşasın! Senin adına çok mutlu oldum, içim kıpır kıpır oldu!", "mutlu"
    elif any(k in metin for k in ["üzgün", "kötü", "canım sıkkın"]):
        return "Hımm, anlıyorum... Bazen bulutlar güneşin önüne geçer ama sonra yine açar. Anlatmak ister misin?", "uzgun"
    else:
        return "Anladım, çok ilginç! Peki sonra ne oldu? Seni dinlemeyi seviyorum.", "normal"

# --- ARAYÜZ ---
st.title("Duygu Arkadaşı")

# Tavşan Görseli
st.image(tavsan_resimleri[st.session_state.durum], width=200)

# İlk Karşılama
if not st.session_state.basladi:
    selam = "Merhaba! Ben senin duygu arkadaşınım. Bugün seninle sohbet etmek için sabırsızlanıyorum!"
    st.write(selam)
    audio = cocuk_sesi_olustur(selam)
    st.audio(audio, format='audio/mp3', autoplay=True)
    st.session_state.basladi = True

# Konuşma Alanı
st.write("---")
text = speech_to_text(language='tr', start_prompt="Bana anlatmak için dokun", stop_prompt="Dinliyorum...", key='recorder')

if text:
    st.write(f"**Sen:** {text}")
    yanit, yeni_durum = cevap_uret(text)
    
    st.session_state.durum = yeni_durum
    st.session_state.notlar.append(f"{datetime.now().strftime('%H:%M')} - Çocuk: {text}")
    
    st.write(f"**Tavşan:** {yanit}")
    
    # Çocuk sesi efektiyle yanıt ver
    audio_response = cocuk_sesi_olustur(yanit)
    st.audio(audio_response, format='audio/mp3', autoplay=True)

# --- VELİ PANELİ ---
with st.expander("Veli Bölümü"):
    sifre = st.text_input("Şifre", type="password")
    if sifre == "1234":
        st.write("### Günlük Özet")
        for n in st.session_state.notlar:
            st.write(n)
