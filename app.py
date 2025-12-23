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
# SES OLUŞTURMA (YUMUŞAK / ÇOCUK DOSTU)
# -------------------------------------------------
def ses_olustur(metin):
    tts = gTTS(
        text=metin,
        lang="tr",
        slow=True  # ÇOCUKLAR İÇİN ÇOK ÖNEMLİ
    )
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# -------------------------------------------------
# CEVAP HAVUZLARI (ÇOCUK PSİKOLOJİSİNE UYGUN)
# -------------------------------------------------
CEVAPLAR = {
    "mutlu": [
        "Yaşaaasın! Buna çok sevindim!",
        "Vay canına! Bu çok güzel!",
        "Kalbin pır pır mı ediyor?"
    ],
    "uzgun": [
        "Hmmm… canın biraz acımış gibi.",
        "Gel buraya, ben seninleyim.",
        "Üzgün olmak bazen olur."
    ],
    "korkmus": [
        "Korku bazen minicik bir canavar gibidir.",
        "Şu an güvendesin, ben buradayım.",
        "İstersen korkuyu küçültelim."
    ],
    "ofkeli": [
        "Öfke bazen hop diye gelir.",
        "Birlikte yavaşça nefes alalım mı?",
        "İçindeki sıcak topu hissediyor musun?"
    ],
    "notr": [
        "Hımm… seni dinliyorum.",
        "Anlat bakalım.",
        "Ben buradayım."
    ]
}

# -------------------------------------------------
# DUYGU TESPİTİ (BASİT AMA ETKİLİ)
# -------------------------------------------------
def duygu_belirle(metin):
    m = metin.lower()
    if any(k in m for k in ["mutlu", "iyi", "güzel", "sevindim", "harika"]):
        return "mutlu"
    if any(k in m for k in ["üzgün", "kötü", "ağladım", "canım acıdı"]):
        return "uzgun"
    if any(k in m for k in ["korktum", "korkuyorum", "karanlık"]):
        return "korkmus"
    if any(k in m for k in ["kızdım", "sinirliyim", "öfkeliyim"]):
        return "ofkeli"
    return "notr"

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{
        "rol": "tavsan",
        "metin": (
            "Merhaba arkadaşım. Ben Tavşan. "
            "Seninle oyun oynamayı ve sohbet etmeyi seviyorum. "
            "Bugün nasılsın?"
        )
    }]
    st.session_state.ilk_ses = False

if "notlar" not in st.session_state:
    st.session_state.notlar = []

# -------------------------------------------------
# GÖRSELLER
# -------------------------------------------------
TAVSAN_RESIMLERI = {
    "normal": "https://img.icons8.com/color/200/rabbit.png",
    "mutlu": "https://img.icons8.com/color/200/happy-rabbit.png",
    "uzgun": "https://img.icons8.com/color/200/sad-rabbit.png"
}

# -------------------------------------------------
# ARAYÜZ
# -------------------------------------------------
st.title("🐰 Duygu Arkadaşı Tavşan")

st.image(TAVSAN_RESIMLERI["normal"], width=160)

# -------------------------------------------------
# İLK MESAJI SESLİ OKU (SADECE 1 KEZ)
# -------------------------------------------------
if not st.session_state.ilk_ses:
    ilk = st.session_state.mesajlar[0]["metin"]
    st.write("**Tavşan:**", ilk)
    st.audio(ses_olustur(ilk), format="audio/mp3", autoplay=True)
    st.session_state.ilk_ses = True

# -------------------------------------------------
# ÖNCEKİ MESAJLAR
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
    start_prompt="🎤 Konuşmak için dokun",
    stop_prompt="Dinliyorum...",
    key="mic"
)

if konusma:
    st.session_state.mesajlar.append({
        "rol": "cocuk",
        "metin": konusma
    })

    st.session_state.notlar.append(
        f"{datetime.now().strftime('%H:%M')} - Çocuk: {konusma}"
    )

    duygu = duygu_belirle(konusma)
    cevap = random.choice(CEVAPLAR[duygu])

    st.session_state.mesajlar.append({
        "rol": "tavsan",
        "metin": cevap
    })

    st.rerun()

# -------------------------------------------------
# VELİ PANELİ (OPSİYONEL)
# -------------------------------------------------
with st.sidebar:
    st.header("Veli Alanı")
    sifre = st.text_input("Şifre", type="password")
    if sifre == "1234":
        st.subheader("Sohbet Kayıtları")
        for n in st.session_state.notlar:
            st.text(n)
