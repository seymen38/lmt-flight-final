import re
from datetime import date

def validate_iata(code: str) -> bool:
    return bool(re.match(r'^[A-Z]{3}$', code))

def validate_date_range(start_date: date, end_date: date) -> tuple:
    if start_date < date.today():
        return False, "Gidiş tarihi bugünden önce olamaz"
    if end_date <= start_date:
        return False, "Dönüş tarihi gidiş tarihinden sonra olmalı"
    return True, ""