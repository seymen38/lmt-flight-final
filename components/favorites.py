import streamlit as st
import json
import os

FAVORITES_FILE = "favorites.json"

def load_favorites():
    """Kayıtlı favori rotaları yükle"""
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    """Favori rotaları kaydet"""
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f)

def add_favorite(origin, dest):
    """Yeni favori ekle"""
    favorites = load_favorites()
    new_fav = {"origin": origin, "dest": dest}
    if new_fav not in favorites:
        favorites.append(new_fav)
        save_favorites(favorites)
        return True
    return False

def remove_favorite(origin, dest):
    """Favori sil"""
    favorites = load_favorites()
    favorites = [f for f in favorites if not (f["origin"] == origin and f["dest"] == dest)]
    save_favorites(favorites)

def render_favorites_sidebar():
    """Sidebar'da favori rotaları göster"""
    favorites = load_favorites()
    
    if not favorites:
        st.caption("Henüz favori rota eklenmemiş")
        return None
    
    st.markdown("### ⭐ Favori Rotalar")
    for fav in favorites:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"✈️ {fav['origin']} → {fav['dest']}", key=f"fav_{fav['origin']}_{fav['dest']}"):
                return fav['origin'], fav['dest']
        with col2:
            if st.button("🗑️", key=f"del_{fav['origin']}_{fav['dest']}"):
                remove_favorite(fav['origin'], fav['dest'])
                st.rerun()
    return None