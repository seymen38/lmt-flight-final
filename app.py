import streamlit as st

st.set_page_config(page_title="LMT Flight", layout="wide")

# Basit stil. Emoji yok, karmaşık CSS yok.
st.markdown(
    """
    <style>
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3, p, .stText, label { color: white !important; }
    .stButton > button { background-color: #ff6b00; color: white; border-radius: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("LMT Flight")
st.markdown("Profesyonel Uçuş Arama Motoru (Test Sürümü)")

if st.button("Test Butonu"):
    st.success("Bağlantı başarılı! Altyapı çalışıyor.")
