import streamlit as st

def render_header():
    """Ana header bileşeni"""
    
    # CSS'i yükle
    with open("assets/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="logo">✈️ <span>LMT Flight</span></div>
                <div style="display: flex; gap: 10px;">
                    <a href="#" class="nav-link">✈️ Uçak Bileti</a>
                    <a href="#" class="nav-link">🏨 Otel</a>
                    <a href="#" class="nav-link">🚌 Otobüs</a>
                    <a href="#" class="nav-link">🚗 Araç</a>
                </div>
                <div>
                    <span style="color: white; background: rgba(255,107,0,0.3); padding: 6px 12px; border-radius: 20px;">🇹🇷 TRY</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)