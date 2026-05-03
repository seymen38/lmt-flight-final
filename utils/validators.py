import re
from datetime import date

def validate_iata(code: str) -> bool:
    """IATA kodu validasyonu (3 harfli, büyük harf)"""
    if not code:
        return False
    return bool(re.match(r'^[A-Z]{3}$', code))

def validate_date_range(start_date: date, end_date: date) -> tuple:
    """Tarih aralığı validasyonu"""
    if not start_date or not end_date:
        return False, "Tarih boş olamaz"
    
    if start_date < date.today():
        return False, "Gidiş tarihi bugünden önce olamaz"
    
    if end_date <= start_date:
        return False, "Dönüş tarihi, gidiş tarihinden sonra olmalıdır"
    
    return True, ""

def validate_adults(count: int) -> tuple:
    """Yolcu sayısı validasyonu"""
    if count < 1:
        return False, "En az 1 yolcu olmalıdır"
    if count > 9:
        return False, "Maksimum 9 yolcu"
    return True, ""