# Şehir adı -> IATA dönüşümü
CITY_TO_IATA = {
    # Türkiye
    "istanbul": "IST", "ankara": "ESB", "izmir": "ADB", "antalya": "AYT",
    "adana": "ADA", "trabzon": "TZX", "kayseri": "ASR", "bursa": "YEI",
    "dalaman": "DLM", "bodrum": "BJV", "gaziantep": "GZT", "konya": "KYA",
    "samsun": "SZF", "erzurum": "ERZ", "van": "VAN", "diyarbakir": "DIY",
    "malatya": "MLX", "elazig": "EZS",
    
    # Avrupa
    "londra": "LHR", "paris": "CDG", "berlin": "BER", "munih": "MUC",
    "frankfurt": "FRA", "roma": "FCO", "milano": "MXP", "venedik": "VCE",
    "madrid": "MAD", "barcelona": "BCN", "amsterdam": "AMS", "brüksel": "BRU",
    "viyana": "VIE", "zürih": "ZRH",
    
    # Dünya
    "dubai": "DXB", "doha": "DOH", "new york": "JFK", "los angeles": "LAX",
    "singapur": "SIN", "tokyo": "HND", "seul": "ICN", "pekin": "PEK",
    
    # İngilizce isimler
    "london": "LHR", "paris": "CDG", "berlin": "BER", "munich": "MUC",
    "rome": "FCO", "milan": "MXP", "venice": "VCE", "amsterdam": "AMS",
    "brussels": "BRU", "vienna": "VIE", "zurich": "ZRH", "dubai": "DXB",
    "doha": "DOH", "new york": "JFK", "los angeles": "LAX", "singapore": "SIN",
    "tokyo": "HND", "seoul": "ICN", "beijing": "PEK",
}

# Para birimi sembolleri
CURRENCY_SYMBOLS = {
    "TRY": "₺", "USD": "$", "EUR": "€", "GBP": "£", "AED": "د.إ",
}

def city_to_iata(city_name: str) -> str:
    if not city_name:
        return None
    
    # Orijinali sakla
    original = city_name.strip()
    
    # Türkçe karakterleri dönüştür
    normalized = original
    normalized = normalized.replace('İ', 'I').replace('ı', 'i')
    normalized = normalized.replace('Ü', 'U').replace('ü', 'u')
    normalized = normalized.replace('Ğ', 'G').replace('ğ', 'g')
    normalized = normalized.replace('Ş', 'S').replace('ş', 's')
    normalized = normalized.replace('Ö', 'O').replace('ö', 'o')
    normalized = normalized.replace('Ç', 'C').replace('ç', 'c')
    
    normalized = normalized.lower()
    
    # ASCII dönüşümü
    import unicodedata
    normalized = unicodedata.normalize('NFKD', normalized).encode('ASCII', 'ignore').decode('ASCII')
    
    # Zaten IATA kodu mu?
    if len(normalized) == 3 and normalized.isalpha():
        return normalized.upper()
    
    # Önce tam eşleşme ara
    if normalized in CITY_TO_IATA:
        return CITY_TO_IATA[normalized]
    
    # Kısmi eşleşme
    for city, iata in CITY_TO_IATA.items():
        if city in normalized or normalized in city:
            return iata
    
    return None
    
    # Türkçe karakterleri İngilizce'ye çevir
    normalized = city_name.strip()
    normalized = normalized.replace('İ', 'I').replace('ı', 'i')
    normalized = normalized.replace('Ü', 'U').replace('ü', 'u')
    normalized = normalized.replace('Ğ', 'G').replace('ğ', 'g')
    normalized = normalized.replace('Ş', 'S').replace('ş', 's')
    normalized = normalized.replace('Ö', 'O').replace('ö', 'o')
    normalized = normalized.replace('Ç', 'C').replace('ç', 'c')
    
    normalized = normalized.lower()
    
    # ASCII dönüşümü
    import unicodedata
    normalized = unicodedata.normalize('NFKD', normalized).encode('ASCII', 'ignore').decode('ASCII')
    
    # Zaten IATA kodu mu?
    if len(normalized) == 3 and normalized.isalpha():
        return normalized.upper()
    
    # Şehir eşlemesi
    return CITY_TO_IATA.get(normalized)

def get_currency_symbol(currency: str) -> str:
    return CURRENCY_SYMBOLS.get(currency, "₺")

def convert_price(price: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return price
    # Yaklaşık kur
    rates = {"TRY": 1, "USD": 33, "EUR": 36, "GBP": 42}
    if from_currency in rates and to_currency in rates:
        in_try = price * rates.get(from_currency, 1)
        return in_try / rates.get(to_currency, 1)
    return price

def enhance_airline_name(airline_name: str) -> str:
    if airline_name in ["TK", "turkish"]:
        return "🇹🇷 Türk Hava Yolları (TK) - Bayrak taşıyıcı"
    elif airline_name in ["PC", "pegaus"]:
        return "🇹🇷 Pegasus (PC) - Düşük bütçeli"
    elif airline_name in ["VF", "ajet"]:
        return "🇹🇷 AJet (VF) - THY alt kuruluşu"
    elif airline_name in ["XQ", "sunexpress"]:
        return "🇹🇷 SunExpress (XQ) - THY & Lufthansa"
    elif airline_name in ["BA", "british"]:
        return "🇬🇧 British Airways (BA)"
    elif airline_name in ["LH", "lufthansa"]:
        return "🇩🇪 Lufthansa (LH)"
    elif airline_name in ["EK", "emirates"]:
        return "🇦🇪 Emirates (EK)"
    return airline_name

def is_turkish_airline(airline_name: str) -> bool:
    turkish = ["TK", "PC", "VF", "XQ", "XC", "4M", "FH", "TI"]
    return airline_name in turkish