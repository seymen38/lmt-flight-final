import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

def generate_price_trend(origin, dest, start_date):
    """Fiyat trendi verisi üret"""
    dates = []
    prices = []
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        dates.append(current_date.strftime("%d.%m"))
        
        # Gerçekçi fiyat dalgalanması
        base_price = random.randint(2000, 6000)
        trend = random.randint(-500, 500)
        prices.append(base_price + trend)
    
    return dates, prices

def display_price_chart(origin, dest, start_date):
    """Fiyat grafiğini göster"""
    dates, prices = generate_price_trend(origin, dest, start_date)
    
    df = pd.DataFrame({
        "Tarih": dates,
        "En Düşük Fiyat (₺)": prices
    })
    
    st.line_chart(df.set_index("Tarih"), use_container_width=True)
    
    # En iyi günü bul
    best_idx = prices.index(min(prices))
    best_date = dates[best_idx]
    best_price = prices[best_idx]
    
    st.info(f"💡 **En ucuz gün:** {best_date} - **{best_price:,.0f} ₺**")