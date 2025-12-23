import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import random
from datetime import datetime

# -------------------------------------------------
# SAYFA AYARLARI
# -------------------------------------------------
st.set_page_config(
    page_title="Duygu Arkadaşı Tavşan",
    layout="centered"
)

# -------------------------------------------------
# SES OLUŞTURMA
# -------------------------------------------------
def ses_olustur(metin):
    tts = gTTS(text=metin, lang="tr", slow=True)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# -------------------------------------------------
# CEVAPLAR
# -------------------------------------------------
CEVAPLAR = {
    "mutlu": [
        "Yaşaaasın! Buna çok sevindim!",
        "Vay canına! Bu çok güzel!"
    ],
    "uzgun": [
        "Hmmm… canın biraz acımış gibi.",
        "Ben buradayım, yalnız değilsin."
    ],
    "korkmus": [
        "Şu an güvendesin.",
        "Korku bazen gelir ama geçer."
    ],
    "ofkeli": [
        "Biraz kızgın hissediyorsun galiba.",
        "İstersen birlikte nefes alalım."
    ],
    "notr": [
        "Seni dinliyorum.",
        "Anlat bakalım."
    ]
}

def duygu_belirle(m):
    m = m.lower()
    if any(k in m for k in ["iyi", "mutlu", "güzel"]): return "mutlu"
    if any(k in m for k in ["üzgün", "kötü", "ağladım"]): return "uzgun"
    if any(k in m for k in ["korktum", "korkuyorum"]): return "korkmus"
    if any(k in m for k in ["kızdım", "sinirliyim"]): return "ofkeli"
    return "notr"

# -------------------------------------------------
# SESSION STATE (KRİTİK KISIM)
# -------------------------------------------------
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{
        "rol": "tavsan",
        "metin": "Merhaba. Ben Tavşan. Seninle sohbet etmeyi seviyorum. Nasılsın?"
    }]

if "ilk_ses" not in st.session_state:
    st.session_state.ilk_ses = False

if "notlar" not in st.session_state:
    st.session_state.notlar = []

# -------------------------------------------------
# ARAYÜZ
# -------------------------------------------------
st.title("🐰 Duygu Arkadaşı Tavşan")
st.image("https://img.icons8.com/color/200/rabbit.png", width=160)

# -------------------------------------------------
# İLK SES
# -------------------------------------------------
if not st.session_state.ilk_ses:
    ilk = st.session_state.mesajlar[0]["metin"]
    st.write("**Tavşan:**", ilk)
    st.audio(ses_olustur(ilk), autoplay=True)
    st.session_state.ilk_ses = True

# -------------------------------------------------
# SOHBET
# -------------------------------------------------
for m in st.session_state.mesajlar[1:]:
    if m["rol"] == "cocuk":
        st.write("**Sen:**", m["metin"])
    else:
        st.write("**Tavşan:**", m["metin"])

# -------------------------------------------------
# SESLİ GİRİŞ
# -------------------------------------------------
st.write("---")
konusma = speech_to_text(
    language="tr",
    start_prompt="🎤 Konuş",
    stop_prompt="Dinliyorum",
    key="mic"
)

if konusma:
    st.session_state.mesajlar.append({"rol": "cocuk", "metin": konusma})
    st.session_state.notlar.append(
        f"{datetime.now().strftime('%H:%M')} - {konusma}"
    )

    duygu = duygu_belirle(konusma)
    cevap = random.choice(CEVAPLAR[duygu])

    st.session_state.mesajlar.append({"rol": "tavsan", "metin": cevap})
    st.rerun()

# -------------------------------------------------
# VELİ PANELİ
# -------------------------------------------------
with st.sidebar:
    st.header("Veli Alanı")
    if st.text_input("Şifre", type="password") == "1234":
        for n in st.session_state.notlar:
            st.text(n)
