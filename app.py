import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Duygu Arkadaşı", layout="centered")

# Görsel ve Yazı Fontu Ayarları (Daha temiz bir görünüm)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .stMarkdown { font-family: 'Comic Sans MS', cursive, sans-serif; }
    div.stButton > button { border-radius: 20px; border: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI ---
if "notlar" not in st.session_state:
    st.session_state.notlar = []
if "basladi" not in st.session_state:
    st.session_state.basladi = False
if "durum" not in st.session_state:
    st.session_state.durum = "normal"

# --- TAVŞAN GÖRSELLERİ ---
# Güvenilir olması için direkt resim linkleri (Hata verirse buradaki URL'leri değiştirmen yeterli)
tavsan_resimleri = {
    "normal": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png", # Örnek: Sevimli karakter
    "mutlu": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
    "uzgun": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
}

# --- YARDIMCI FONKSİYONLAR ---
def ses_cal(metin):
    tts = gTTS(text=metin, lang='tr')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    st.audio(audio_fp, format='audio/mp3', autoplay=True)

def cevap_ve_analiz(metin):
    metin = metin.lower()
    if any(k in metin for k in ["merhaba", "selam", "günaydın"]):
        return "Merhaba arkadaşım! Bugün seninle vakit geçirmek için sabırsızlanıyorum.", "normal"
    elif any(k in metin for k in ["mutlu", "iyi", "güzel", "harika"]):
        return "Bunu duyduğuma çok sevindim! Seninle beraber ben de kendimi çok iyi hissediyorum.", "mutlu"
    elif any(k in metin for k in ["üzgün", "kötü", "canım sıkkın", "ağladım"]):
        return "Seni çok iyi anlıyorum. Bazen böyle hissetmekte sorun yok. Bana biraz daha anlatmak ister misin?", "uzgun"
    else:
        return "Seni çok dikkatli dinliyorum. Anlattıkların benim için çok değerli.", "normal"

# --- UYGULAMA BAŞLANGICI ---
st.title("Duygu Arkadaşı")

# Tavşanı Göster
st.image(tavsan_resimleri[st.session_state.durum], width=250)

# İlk Açılış Hoşgeldin Mesajı
if not st.session_state.basladi:
    hosgeldin = "Merhaba arkadaşım! Ben senin duygu arkadaşınım. Bugün neler yaptın? Seninle konuşmak için buradayım."
    st.write(hosgeldin)
    ses_cal(hosgeldin)
    st.session_state.basladi = True

# Sesli Kayıt Sistemi
st.write("---")
text = speech_to_text(language='tr', start_prompt="Konuşmak için dokun", stop_prompt="Durmak için dokun", key='recorder')

if text:
    st.write(f"Sen: {text}")
    cevap, yeni_durum = cevap_ve_analiz(text)
    
    # Hafıza güncelleme
    st.session_state.durum = yeni_durum
    st.session_state.notlar.append(f"{datetime.now().strftime('%H:%M')} - Çocuk: {text}")
    
    # Yanıt verme
    st.write(f"Arkadaşın: {cevap}")
    ses_cal(cevap)

# --- GİZLİ VELİ PANELİ (SAYFA SONUNDA) ---
with st.expander("Veli Notları"):
    sifre = st.text_input("Şifre", type="password")
    if sifre == "1234":
        for n in st.session_state.notlar:
            st.text(n)
