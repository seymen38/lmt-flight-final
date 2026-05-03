import asyncio
import streamlit as st
from services.cache_service import cache
from letsfg.local import search_local
import os

os.environ["PLAYWRIGHT_HEADLESS"] = "1"
os.environ["BOOSTED_BROWSER_VISIBLE"] = "0"

async def search_async(origin: str, dest: str, date_str: str, mode: str = "fast"):
    try:
        result = await search_local(
            origin, dest, date_str,
            mode=mode,
            max_browsers=4
        )
        return result
    except Exception as e:
        print(f"Hata: {e}")
        return None

def search_flights(origin: str, dest: str, date_str: str, mode: str = "fast", label: str = "Uçuş"):
    cached = cache.get(origin, dest, date_str)
    if cached:
        st.toast(f"📦 {label} önbellekten alındı", icon="⚡")
        return cached
    
    with st.spinner(f"✈️ {label} uçuşları aranıyor (15-25 sn)..."):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(search_async(origin, dest, date_str, mode))
            loop.close()
            
            if result and isinstance(result, dict) and 'offers' in result and result['offers']:
                cache.set(result, origin, dest, date_str)
                st.toast(f"✅ {len(result['offers'])} uçuş bulundu!", icon="✈️")
                return result
            return None
        except Exception as e:
            st.error(f"Arama hatası: {str(e)}")
            return None