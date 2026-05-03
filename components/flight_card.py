import streamlit as st
from utils.helpers import convert_price, get_currency_symbol, enhance_airline_name, is_turkish_airline

def display_flight_card(offer, idx, target_currency="TRY"):
    """Uçuş kartı - Dinamik para birimi desteği"""
    
    airline = offer.main_airline
    airline_code = offer.main_airline_code
    price = offer.price
    source_currency = offer.currency
    booking_url = getattr(offer, 'booking_url', None)
    
    # source_name kontrolü
    source_name = getattr(offer, 'source_name', None)
    if not source_name:
        source_name = getattr(offer, 'source', 'Havayolu')
    
    # Kaynak site adını düzenle
    source_map = {
        "skiplagged_meta": "Skiplagged", "kiwi_connector": "Kiwi.com",
        "travelstart_ota": "Travelstart", "traveltrolley_ota": "TravelTrolley",
        "esky_ota": "eSky", "byojet_ota": "ByoJet", "auntbetty_ota": "Aunt Betty",
        "cleartrip_ota": "Cleartrip", "tripcom_ota": "Trip.com", "opodo_ota": "Opodo"
    }
    source_display = source_map.get(source_name, source_name)
    
    # Havayolu bilgisini zenginleştir
    enhanced_airline = enhance_airline_name(airline)
    
    # THY özel vurgu
    is_thy = airline_code == "TK" or "turk" in airline.lower()
    
    # Türk havayolu mu?
    is_turkish = is_turkish_airline(airline) or airline in ["TK", "PC", "VF", "XQ"]
    turkish_badge = "🇹🇷 " if is_turkish else ""
    
    # THY için özel yıldız badge
    thy_badge = "🌟 " if is_thy else ""
    
    # Fiyat dönüşümü (güncel kur ile)
    converted_price = convert_price(price, source_currency, target_currency)
    symbol = get_currency_symbol(target_currency)
    
    # ============================================================
    # AKTARMA ÖZETİ
    # ============================================================
    segments = offer.segments
    if offer.stops == 0:
        stop_summary = "✈️ Direkt uçuş"
    else:
        route_parts = []
        for i, seg in enumerate(segments):
            origin_code = seg.get('origin', '?')
            dest_code = seg.get('destination', '?')
            airline_code_seg = seg.get('airline', '?')
            
            if i == 0:
                route_parts.append(f"{origin_code} → {dest_code} ({airline_code_seg})")
            else:
                route_parts.append(f"→ {dest_code} ({airline_code_seg})")
        
        stop_summary = " 🔄 ".join(route_parts)
    
    # ============================================================
    # KART GÖSTERİMİ
    # ============================================================
    with st.container(border=True):
        # 1. SATIR: Havayolu ve fiyat
        col1, col2, col3 = st.columns([3, 2, 1.5])
        with col1:
            if is_thy:
                st.markdown(f"**{idx}.** ✈️ {thy_badge}{turkish_badge}**:green[**{enhanced_airline}**]**")
                st.caption("🇹🇷 Bayrak taşıyıcı | 4 yıldızlı havayolu | Star Alliance üyesi")
            else:
                st.markdown(f"**{idx}.** ✈️ {turkish_badge}**{enhanced_airline}**")
                st.caption(f"📡 Kaynak: {source_display}")
        with col2:
            st.markdown(f"### {symbol} {converted_price:,.2f}")
        with col3:
            if booking_url and booking_url != "#":
                st.markdown(
                    f'<a href="{booking_url}" target="_blank">'
                    f'<button style="background:#ff6b00; color:white; border:none; '
                    f'border-radius:20px; padding:8px 16px; cursor:pointer;">'
                    f'🎫 Satın Al</button></a>',
                    unsafe_allow_html=True
                )
        
        # 2. SATIR: Gidiş saatleri
        st.markdown(f"🕐 **Kalkış:** {offer.departure_time} → **Varış:** {offer.arrival_time}")
        st.markdown(f"⏱️ **Toplam süre:** {offer.total_duration_str}")
        
        # 3. SATIR: AKTARMA ÖZETİ
        if offer.stops == 0:
            st.markdown(f"✈️ **{stop_summary}**")
        else:
            st.markdown(f"🔄 **{stop_summary}**")
        
        # 4. SATIR: AYRINTILAR
        if offer.stops > 0:
            with st.expander("📋 **Aktarma ve rota detayları**", expanded=False):
                seg_details = offer.segment_details
                if seg_details:
                    st.markdown("**✈️ Uçuş Segmentleri:**")
                    for seg in seg_details:
                        city_info = ""
                        if seg.get('origin_city') and seg.get('destination_city'):
                            city_info = f"({seg['origin_city']} → {seg['destination_city']})"
                        
                        if seg['airline_code'] == "TK":
                            st.markdown(
                                f"**{seg['no']}. :green[🇹🇷 {seg['airline_code']}]** {seg['airline_name']}\n\n"
                                f"   ✈️ {seg['origin']} {city_info} **{seg['departure_time']}** → {seg['destination']} **{seg['arrival_time']}**"
                            )
                        else:
                            st.markdown(
                                f"**{seg['no']}. {seg['airline_code']}** {seg['airline_name']}\n\n"
                                f"   ✈️ {seg['origin']} {city_info} **{seg['departure_time']}** → {seg['destination']} **{seg['arrival_time']}**"
                            )
                
                layovers = offer.layover_details
                if layovers:
                    st.markdown("---")
                    st.markdown("**⏱️ Aktarma Bekleme Süreleri:**")
                    for i, layover in enumerate(layovers, 1):
                        st.markdown(
                            f"   **{i}. Aktarma:** {layover['city']} ({layover['airport']}) - "
                            f"Bekleme: {layover['duration_str']}"
                        )
                
                # Süre Analizi
                total_min = offer.total_duration_minutes
                flight_min = sum(seg.get('duration_seconds', 0) for seg in segments) // 60
                layover_min = total_min - flight_min
                
                if layover_min > 0:
                    st.markdown("---")
                    st.markdown(
                        f"**📊 Süre Analizi:**\n"
                        f"   • Toplam uçuş süresi: {flight_min} dakika\n"
                        f"   • Toplam bekleme süresi: {layover_min} dakika"
                    )


def display_flight_list(offers, title, target_currency="TRY", max_display=15):
    """Uçuş listesini göster - Türk havayolları öne çıkar"""
    if not offers:
        st.warning(f"⚠️ {title} uçuşu bulunamadı")
        return
    
    # Önce Türk havayollarını, sonra diğerlerini göster
    turkish_offers = []
    other_offers = []
    
    for offer in offers:
        airline = offer.main_airline
        airline_code = offer.main_airline_code
        
        if airline_code == "TK":
            turkish_offers.insert(0, offer)
        elif is_turkish_airline(airline) or airline_code in ["TK", "PC", "VF", "XQ"]:
            turkish_offers.append(offer)
        else:
            other_offers.append(offer)
    
    turkish_offers.sort(key=lambda x: x.price)
    other_offers.sort(key=lambda x: x.price)
    
    sorted_offers = turkish_offers + other_offers
    turkish_count = len(turkish_offers)
    
    if turkish_count > 0:
        st.success(f"✅ **{len(offers)}** {title} uçuşu bulundu (🇹🇷 Türk havayolları: {turkish_count})")
    else:
        st.success(f"✅ **{len(offers)}** {title} uçuşu bulundu")
    
    for idx, offer in enumerate(sorted_offers[:max_display], 1):
        display_flight_card(offer, idx, target_currency)