import streamlit as st
from utils.helpers import get_currency_symbol

def render_sidebar():
    """Yan menü - Para birimi seçimi"""
    with st.sidebar:
        st.markdown("### ⚙️ Ayarlar")
        st.markdown("---")
        
        # Para birimi seçimi (session_state ile kalıcı)
        if 'currency' not in st.session_state:
            st.session_state.currency = "TRY"
        
        currency = st.selectbox(
            "💰 Para Birimi",
            ["TRY", "USD", "EUR", "GBP"],
            index=["TRY", "USD", "EUR", "GBP"].index(st.session_state.currency),
            format_func=lambda x: f"{x} ({get_currency_symbol(x)})"
        )
        
        # Session state güncelle
        if currency != st.session_state.currency:
            st.session_state.currency = currency
            st.rerun()
        
        st.markdown("---")
        st.caption("📡 Kaynak: LetsFG")
        st.caption("🔄 Gerçek zamanlı fiyatlar")
        st.caption("🇹🇷 Türk havayolları öncelikli")
        st.caption("⚡ Ortalama 10-20 saniye")
        
        return st.session_state.currency