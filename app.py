import streamlit as st
from datetime import date, timedelta
from models.flight import FlightOffer
from services.flight_service import search_flights
from components.flight_card import display_flight_list, display_flight_card
from components.sidebar import render_sidebar
from utils.helpers import city_to_iata

st.set_page_config(
    page_title="LMT Flight | Uçak Bileti",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PROFESYONEL PREMIUM CSS
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    .premium-header {
        background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(15,15,30,0.9) 100%);
        backdrop-filter: blur(20px);
        padding: 20px 0;
        margin-bottom: 40px;
        border-bottom: 1px solid rgba(255,107,0,0.3);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .logo {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b00, #ffaa00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .logo-sub {
        font-size: 12px;
        color: rgba(255,255,255,0.5);
        margin-top: 4px;
    }
    
    .hero-premium {
        background: linear-gradient(135deg, rgba(255,107,0,0.15) 0%, rgba(255,140,0,0.05) 100%);
        border-radius: 40px;
        padding: 60px 40px;
        margin-bottom: 40px;
        text-align: center;
        border: 1px solid rgba(255,107,0,0.2);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-premium::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,107,0,0.08) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.3; }
    }
    
    .hero-title {
        font-size: 52px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b00, #ffaa00, #ffdd00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: rgba(255,255,255,0.7);
        position: relative;
        z-index: 1;
    }
    
    .search-card-premium {
        background: rgba(25, 25, 35, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 32px;
        padding: 32px;
        margin-bottom: 40px;
        border: 1px solid rgba(255,107,0,0.2);
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        animation: fadeInUp 0.6s ease-out 0.1s both;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        margin: 40px 0;
    }
    
    .stat-card-premium {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    .stat-card-premium:hover {
        transform: translateY(-8px);
        border-color: rgba(255,107,0,0.4);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .stat-number {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b00, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    .flight-card-custom {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.04) 100%);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        cursor: pointer;
    }
    
    .flight-card-custom:hover {
        transform: translateX(4px);
        border-color: rgba(255,107,0,0.4);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #ff6b00 0%, #ff8c00 50%, #ffaa00 100%);
        color: white;
        border: none;
        border-radius: 48px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        transition: all 0.3s;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255,107,0,0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(255,107,0,0.5);
    }
    
    .stButton button:active {
        transform: translateY(1px);
    }
    
    .stTextInput input, .stDateInput input, .stNumberInput input {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 12px 18px !important;
        font-size: 15px !important;
        transition: all 0.3s;
    }
    
    .stTextInput input:focus, .stDateInput input:focus {
        border-color: #ff6b00 !important;
        box-shadow: 0 0 20px rgba(255,107,0,0.2) !important;
    }
    
    .stRadio > div {
        background: rgba(255,255,255,0.05);
        border-radius: 48px;
        padding: 6px;
    }
    
    .stRadio label {
        padding: 8px 24px;
        border-radius: 40px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stRadio label:has(input:checked) {
        background: linear-gradient(135deg, #ff6b00, #ff8c00);
    }
    
    .premium-footer {
        background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(15,15,30,0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 40px;
        margin-top: 60px;
        text-align: center;
        border-top: 1px solid rgba(255,107,0,0.2);
        border-radius: 30px 30px 0 0;
    }
    
    .footer-text {
        color: rgba(255,255,255,0.4);
        font-size: 13px;
    }
    
    @media (max-width: 768px) {
        .hero-title { font-size: 32px; }
        .hero-premium { padding: 40px 20px; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
        .search-card-premium { padding: 20px; }
        .stat-number { font-size: 28px; }
        .stButton button { padding: 10px 20px; }
    }
    
    @media (max-width: 480px) {
        .stats-grid { grid-template-columns: 1fr; }
        .hero-title { font-size: 28px; }
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ff6b00;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ff8c00;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PREMIUM HEADER
# ============================================================
st.markdown("""
<div class="premium-header">
    <div style="max-width: 1400px; margin: 0 auto; padding: 0 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="logo">✈️ LMT Flight</div>
                <div class="logo-sub">Profesyonel Uçuş Arama Platformu</div>
            </div>
            <div style="display: flex; gap: 20px;">
                <span style="color: rgba(255,255,255,0.6);">✈️ Uçak</span>
                <span style="color: rgba(255,255,255,0.3);">🏨 Otel</span>
                <span style="color: rgba(255,255,255,0.3);">🚌 Otobüs</span>
                <span style="color: rgba(255,255,255,0.3);">🚗 Araç</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HERO BANNER
# ============================================================
st.markdown("""
<div class="hero-premium">
    <div class="hero-title">En Uygun Uçuşu Bul</div>
    <div class="hero-subtitle">100+ havayolu, gerçek zamanlı fiyatlar, anında rezervasyon</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
if 'currency' not in st.session_state:
    st.session_state.currency = "TRY"

target_currency = render_sidebar()

# ============================================================
# ANA ARAMA KARTI
# ============================================================
with st.container():
    st.markdown('<div class="search-card-premium">', unsafe_allow_html=True)
    st.markdown("### ✈️ Uçuş Ara")
    
    col1, col2 = st.columns(2)
    with col1:
        origin_input = st.text_input("Nereden", "İstanbul", placeholder="Şehir veya havalimanı")
    with col2:
        dest_input = st.text_input("Nereye", "Londra", placeholder="Şehir veya havalimanı")
    
    col1, col2 = st.columns(2)
    with col1:
        depart_date = st.date_input("Gidiş", min_value=date.today(), value=date.today() + timedelta(days=14))
    with col2:
        return_date = st.date_input("Dönüş", min_value=depart_date + timedelta(days=1), value=depart_date + timedelta(days=7))
    
    with st.expander("Yolcu ve Kabin Seçimi"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            adults = st.number_input("Yetişkin", min_value=1, max_value=9, value=1)
        with col_b:
            children = st.number_input("Çocuk", min_value=0, max_value=8, value=0)
        with col_c:
            infants = st.number_input("Bebek", min_value=0, max_value=6, value=0)
        cabin_class = st.selectbox("Kabin Sınıfı", ["Economy", "Premium Economy", "Business", "First Class"])
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_direct = st.checkbox("✈️ Aktarmasız", value=True)
    with col_f2:
        filter_1stop = st.checkbox("🔄 1 Aktarmalı", value=True)
    with col_f3:
        filter_2stop = st.checkbox("🔄 2+ Aktarmalı", value=False)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        flight_type = st.radio("Uçuş Tipi", ["Tek yön", "Gidiş-dönüş"], horizontal=True)
    with col_t2:
        mode = st.radio("Arama Hızı", ["fast", "full"], index=0, horizontal=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# İSTATİSTİK KARTLARI
# ============================================================
st.markdown("""
<div class="stats-grid">
    <div class="stat-card-premium">
        <div class="stat-number">100+</div>
        <div class="stat-label">Havayolu</div>
    </div>
    <div class="stat-card-premium">
        <div class="stat-number">1,000+</div>
        <div class="stat-label">Günlük Uçuş</div>
    </div>
    <div class="stat-card-premium">
        <div class="stat-number">₺0</div>
        <div class="stat-label">Komisyon</div>
    </div>
    <div class="stat-card-premium">
        <div class="stat-number">7/24</div>
        <div class="stat-label">Destek</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ARAMA BUTONU VE SONUÇLAR
# ============================================================
if st.button("🔍 Ucuz Bilet Ara", type="primary", use_container_width=True):
    origin = city_to_iata(origin_input)
    dest = city_to_iata(dest_input)
    
    if not origin:
        st.error(f"❌ '{origin_input}' için geçerli bir şehir bulunamadı")
    elif not dest:
        st.error(f"❌ '{dest_input}' için geçerli bir şehir bulunamadı")
    elif origin == dest:
        st.error("❌ Kalkış ve varış noktaları aynı olamaz")
    else:
        st.info(f"✈️ {origin_input} ({origin}) → {dest_input} ({dest})")
        
        with st.spinner("✈️ En uygun uçuşlar aranıyor..."):
            depart_result = search_flights(origin, dest, depart_date.strftime("%Y-%m-%d"), mode, "Gidiş")
            return_result = search_flights(dest, origin, return_date.strftime("%Y-%m-%d"), mode, "Dönüş")
        
        depart_offers = []
        if depart_result and 'offers' in depart_result:
            depart_offers = [FlightOffer(**o) for o in depart_result['offers']]
            depart_offers.sort(key=lambda x: x.price)
        
        return_offers = []
        if return_result and 'offers' in return_result:
            return_offers = [FlightOffer(**o) for o in return_result['offers']]
            return_offers.sort(key=lambda x: x.price)
        
        filtered_depart = [o for o in depart_offers if 
                          (o.stops == 0 and filter_direct) or
                          (o.stops == 1 and filter_1stop) or
                          (o.stops >= 2 and filter_2stop)]
        
        filtered_return = [o for o in return_offers if 
                          (o.stops == 0 and filter_direct) or
                          (o.stops == 1 and filter_1stop) or
                          (o.stops >= 2 and filter_2stop)]
        
        current_currency = st.session_state.currency
        
        if flight_type == "Gidiş-dönüş":
            st.markdown("## 🚀 Gidiş Uçuşları")
            if filtered_depart:
                display_flight_list(filtered_depart, "Gidiş", current_currency)
            else:
                st.warning("Bu tarihte gidiş uçuşu bulunamadı")
            
            st.markdown("## 🔄 Dönüş Uçuşları")
            if filtered_return:
                display_flight_list(filtered_return, "Dönüş", current_currency)
            else:
                st.warning("Bu tarihte dönüş uçuşu bulunamadı")
            
            if filtered_depart and filtered_return:
                total = filtered_depart[0].price + filtered_return[0].price
                st.info(f"🏆 **En ucuz kombinasyon:** {filtered_depart[0].main_airline} + {filtered_return[0].main_airline} = **{filtered_depart[0].currency} {total:,.2f}**")
        else:
            if filtered_depart:
                display_flight_list(filtered_depart, "Uçuşlar", current_currency)
            else:
                st.warning("Bu tarihte uçuş bulunamadı")

# ============================================================
# PREMIUM FOOTER
# ============================================================
st.markdown("""
<div class="premium-footer">
    <div class="footer-text">
        <p>✈️ <strong>LMT Flight</strong> | Profesyonel Uçuş Arama Motoru</p>
        <p style="margin-top: 10px;">© 2026 LMT Academy - Tüm Hakları Saklıdır.</p>
        <p style="margin-top: 5px; font-size: 11px;">🔒 Güvenli Ödeme | 256-bit SSL | Anlık Onay</p>
    </div>
</div>
""", unsafe_allow_html=True)