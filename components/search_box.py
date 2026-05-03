import streamlit as st
from datetime import date, timedelta

def render_search_box():
    """Arama kutusu bileşeni"""
    
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    
    # Uçuş tipi seçimi
    flight_type = st.radio(
        "",
        ["✈️ Tek yön", "🔄 Gidiş-dönüş", "⚡ Aktarmasız"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Ana arama satırı
    col1, col2 = st.columns(2)
    with col1:
        origin_input = st.text_input("", "İstanbul", placeholder="Nereden", label_visibility="collapsed")
    with col2:
        dest_input = st.text_input("", "Londra", placeholder="Nereye", label_visibility="collapsed")
    
    # Tarih ve yolcu satırı
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        depart_date = st.date_input(
            "Gidiş Tarihi",
            min_value=date.today(),
            value=date.today() + timedelta(days=14),
            label_visibility="collapsed"
        )
    
    with col2:
        if "dönüş" in flight_type.lower():
            return_date = st.date_input(
                "Dönüş Tarihi",
                min_value=depart_date + timedelta(days=1),
                value=depart_date + timedelta(days=7),
                label_visibility="collapsed"
            )
        else:
            return_date = None
            st.markdown('<div style="background: rgba(255,255,255,0.1); border-radius: 20px; padding: 12px 16px; text-align: center; color: rgba(255,255,255,0.6);">Dönüş seçilmedi</div>', unsafe_allow_html=True)
    
    with col3:
        adults = st.number_input("Yolcu", min_value=1, max_value=9, value=1, label_visibility="collapsed")
        
    with col4:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); border-radius: 20px; padding: 12px 16px; text-align: center; color: white;">
            💺 Ekonomi
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Arama butonu
    search_clicked = st.button("✈️ **Ucuz bilet bul >**", use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        "search_clicked": search_clicked,
        "origin_input": origin_input,
        "dest_input": dest_input,
        "depart_date": depart_date,
        "return_date": return_date,
        "adults": adults,
        "flight_type": flight_type
    }