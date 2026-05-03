import streamlit as st

def render_passenger_selector():
    """Yolcu tipi seçici bileşeni"""
    
    with st.popover("👥 Yolcu Seçimi", use_container_width=True):
        st.markdown("### Yolcu Bilgileri")
        
        col1, col2 = st.columns(2)
        with col1:
            adults = st.number_input("👨 Yetişkin (12+ yaş)", min_value=1, max_value=9, value=1)
        with col2:
            children = st.number_input("🧒 Çocuk (2-11 yaş)", min_value=0, max_value=8, value=0)
        
        infants = st.number_input("👶 Bebek (0-2 yaş)", min_value=0, max_value=6, value=0, 
                                   help="Bebekler kucakta seyahat eder")
        
        # Kabin sınıfı
        cabin_class = st.selectbox(
            "💺 Kabin Sınıfı",
            ["Economy", "Premium Economy", "Business", "First Class"],
            index=0
        )
        
        total_passengers = adults + children + infants
        
        st.markdown(f"**Toplam Yolcu:** {total_passengers}")
        
        if infants > adults:
            st.warning("⚠️ Bebek sayısı yetişkin sayısını geçemez!")
        
        return {
            "adults": adults,
            "children": children,
            "infants": infants,
            "total": total_passengers,
            "cabin_class": cabin_class
        }

def display_passenger_summary(passenger_data):
    """Yolcu özetini göster"""
    parts = []
    if passenger_data["adults"] > 0:
        parts.append(f"{passenger_data['adults']} Yetişkin")
    if passenger_data["children"] > 0:
        parts.append(f"{passenger_data['children']} Çocuk")
    if passenger_data["infants"] > 0:
        parts.append(f"{passenger_data['infants']} Bebek")
    
    return ", ".join(parts)