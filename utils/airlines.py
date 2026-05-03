"""
Türk Hava Yolları ve Türkiye merkezli havayolları veritabanı
"""

AIRLINES_DB = {
    # Tarifeli Havayolları
    "AJet": {
        "iata": "VF", "icao": "TKJ", "callsign": "AJET",
        "name_tr": "AJet", "hub": "Sabiha Gökçen (SAW)",
        "type": "Düşük bütçeli alt havayolu", "parent": "Türk Hava Yolları"
    },
    "Pegasus": {
        "iata": "PC", "icao": "PGT", "callsign": "SUNTURK",
        "name_tr": "Pegasus", "hub": "Sabiha Gökçen (SAW)",
        "type": "Düşük bütçeli havayolu", "parent": None
    },
    "SunExpress": {
        "iata": "XQ", "icao": "SXS", "callsign": "SUNEXPRESS",
        "name_tr": "SunExpress", "hub": "Antalya (AYT) / İzmir (ADB)",
        "type": "Turistik havayolu", "parent": "THY & Lufthansa"
    },
    "Türk Hava Yolları": {
        "iata": "TK", "icao": "THY", "callsign": "TURKISH",
        "name_tr": "Türk Hava Yolları", "hub": "İstanbul (IST)",
        "type": "Bayrak taşıyıcı", "parent": None
    },
    
    # Charter Havayolları
    "Corendon Airlines": {
        "iata": "XC", "icao": "CAI", "callsign": "CORENDON",
        "name_tr": "Corendon Airlines", "hub": "Antalya (AYT)",
        "type": "Charter havayolu", "parent": None
    },
    "Freebird Hava Yolları": {
        "iata": "FH", "icao": "FHY", "callsign": "FREEBIRD AIR",
        "name_tr": "Freebird Hava Yolları", "hub": "Antalya (AYT)",
        "type": "Charter havayolu", "parent": None
    },
    "Tailwind Airlines": {
        "iata": "TI", "icao": "TWI", "callsign": "TAILWIND",
        "name_tr": "Tailwind Airlines", "hub": "Sabiha Gökçen (SAW)",
        "type": "Charter havayolu", "parent": None
    },
    "Mavi Gök Airlines": {
        "iata": "4M", "icao": "MGH", "callsign": "MAVI GOK",
        "name_tr": "Mavi Gök Airlines", "hub": "Antalya (AYT)",
        "type": "Charter havayolu", "parent": None
    },
    "Southwind Airlines": {
        "iata": "2S", "icao": "SWD", "callsign": "SOUTHWIND",
        "name_tr": "Southwind Airlines", "hub": "Antalya (AYT)",
        "type": "Charter havayolu", "parent": None
    },
}

IATA_TO_AIRLINE = {
    "VF": "AJet", "PC": "Pegasus", "XQ": "SunExpress", "TK": "Türk Hava Yolları",
    "XC": "Corendon Airlines", "FH": "Freebird Hava Yolları",
    "TI": "Tailwind Airlines", "4M": "Mavi Gök Airlines", "2S": "Southwind Airlines",
}

def get_airline_info(airline_code: str) -> dict:
    """IATA veya ICAO kodundan havayolu bilgisi getir"""
    # Önce IATA kodundan ara
    if airline_code in IATA_TO_AIRLINE:
        airline_name = IATA_TO_AIRLINE[airline_code]
        return AIRLINES_DB.get(airline_name, {})
    
    # Doğrudan isimle ara
    for name, info in AIRLINES_DB.items():
        if name.lower() == airline_code.lower():
            return info
        if info.get("iata") == airline_code:
            return info
    
    return {}

def is_turkish_airline(airline_name: str) -> bool:
    """Havayolunun Türk havayolu olup olmadığını kontrol et"""
    turkish_list = ["AJet", "Pegasus", "Türk Hava Yolları", "SunExpress", 
                    "Corendon", "Freebird", "Tailwind", "Mavi Gök", "Southwind"]
    for item in turkish_list:
        if item.lower() in airline_name.lower():
            return True
    return False