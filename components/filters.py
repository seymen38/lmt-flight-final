import streamlit as st

def render_stop_filter(key_prefix=""):
    """Aktarma filtresi bileşeni"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nonstop = st.checkbox("✈️ Aktarmasız", value=True, key=f"{key_prefix}_nonstop")
    with col2:
        one_stop = st.checkbox("🔄 1 Aktarmalı", value=True, key=f"{key_prefix}_onestop")
    with col3:
        multi_stop = st.checkbox("🔄 2+ Aktarmalı", value=False, key=f"{key_prefix}_multistop")
    
    return {
        "nonstop": nonstop,
        "one_stop": one_stop,
        "multi_stop": multi_stop
    }

def apply_stop_filter(offers, filter_settings):
    """Aktarma filtresini uygula"""
    if not offers:
        return []
    
    filtered = []
    for offer in offers:
        stops = offer.stops
        if stops == 0 and filter_settings.get("nonstop", True):
            filtered.append(offer)
        elif stops == 1 and filter_settings.get("one_stop", True):
            filtered.append(offer)
        elif stops >= 2 and filter_settings.get("multi_stop", False):
            filtered.append(offer)
    
    return filtered

def get_stop_filter_summary(filter_settings):
    """Filtre özetini göster"""
    active = []
    if filter_settings.get("nonstop"):
        active.append("Aktarmasız")
    if filter_settings.get("one_stop"):
        active.append("1 aktarmalı")
    if filter_settings.get("multi_stop"):
        active.append("2+ aktarmalı")
    return ", ".join(active)