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
# SES METNİ DÜZENLEME (DOĞAL DURAKLAMA)
# -------------------------------------------------
def ses_metin_duzelt(metin):
    metin = metin.strip()
    metin = metin.replace(".", "... ")
    metin = metin.replace("!", "! ")
    metin = metin.replace("?", "? ")
    return metin

# -------------------------------------------------
# SES OLUŞTURMA
# -------------------------------------------------
def ses_olustur(metin):
    metin = ses_metin_duzelt(metin)
    tts = gTTS(text=metin, lang="tr", slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# -------------------------------------------------
# CEVAPLAR
# -------------------------------------------------
CEVAPLAR = {
    "mutlu": [
        "Yaşaaasın... buna çok sevindim!",
        "Vay canına... bu harika!"
    ],
    "uzgun": [
        "Hmmm... biraz üzülmüş gibisin.",
        "Gel buraya... ben seninleyim."
    ],
    "korkmus": [
        "Şu an güvendesin... ben buradayım.",
        "Korku bazen gelir... sonra geçer."
    ],
    "ofkeli": [
        "Biraz kızgın hissediyorsun galiba.",
        "İstersen birlikte nefes alalım."
    ],
    "notr": [
        "Hımm... seni dinliyorum.",
        "Anlat bakalım."
    ]
}

# -------------------------------------------------
# DUYGU TESPİTİ
# -------------------------------------------------
def duygu_belirle(m):
    m = m.lower()
    if any(k in m for k in ["mutlu", "iyi", "güzel", "sevindim"]):
        return "mutlu"
    if any(k in m for k in ["üzgün", "kötü", "ağladım"]):
        return "uzgun"
    if any(k in m for k in ["korktum", "korkuyorum"]):
        return "korkmus"
    if any(k in m for k in ["kızdım", "sinirliyim"]):
        return "ofkeli"
    return "notr"

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "ilk_ses" not in st.session_state:
    st.session_state.ilk_ses = False

if "notlar" not in st.session_state:
    st.session_state.notlar = []

# -------------------------------------------------
# ARAYÜZ (SADE)
# -------------------------------------------------
st.image("https://img.icons8.com/color/200/rabbit.png", width=180)
st.markdown("### 🐰 Tavşan seni dinliyor")

# -------------------------------------------------
# İLK KARŞILAMA (SADECE SES)
# -------------------------------------------------
if not st.session_state.ilk_ses:
    ilk_mesaj = (
        "Merhaba... ben Tavşan. "
        "Seninle konuşmayı çok seviyorum. "
        "Hazırsan başlayabiliriz."
    )
    st.audio(ses_olustur(ilk_mesaj), autoplay=True)
    st.session_state.ilk_ses = True

# -------------------------------------------------
# SESLİ GİRİŞ
# -------------------------------------------------
st.write("---")
konusma = speech_to_text(
    language="tr",
    start_prompt="🎤 Konuşmak için dokun",
    stop_prompt="Dinliyorum...",
    key="mic"
)

if konusma:
    st.session_state.notlar.append(
        f"{datetime.now().strftime('%H:%M')} - {konusma}"
    )

    duygu = duygu_belirle(konusma)
    cevap = random.choice(CEVAPLAR[duygu])

    st.audio(ses_olustur(cevap), autoplay=True)

# -------------------------------------------------
# VELİ PANELİ (GİZLİ)
# -------------------------------------------------
with st.sidebar:
    st.header("Veli Alanı")
    if st.text_input("Şifre", type="password") == "1234":
        for n in st.session_state.notlar:
            st.text(n)
