# Havayolu puanları ve yorumları (1-5 yıldız)
AIRLINE_RATINGS = {
    "TK": {"rating": 4.5, "stars": "★★★★½", "review": "Avrupa'nın en iyi havayollarından, yemekler harika"},
    "PC": {"rating": 3.8, "stars": "★★★½", "review": "Düşük bütçeli, zamanında kalkış, fiyatlar uygun"},
    "VF": {"rating": 3.5, "stars": "★★★½", "review": "THY alt kuruluşu, uygun fiyatlı"},
    "XQ": {"rating": 4.0, "stars": "★★★★", "review": "Turistik rotalarda iyi, güzel hizmet"},
    "BA": {"rating": 4.2, "stars": "★★★★", "review": "Profesyonel hizmet, konforlu uçuş"},
    "LH": {"rating": 4.3, "stars": "★★★★", "review": "Alman punctuality, iyi hizmet"},
    "EK": {"rating": 4.7, "stars": "★★★★½", "review": "Lüks deneyim, mükemmel eğlence sistemi"},
    "QR": {"rating": 4.6, "stars": "★★★★½", "review": "5 yıldızlı havayolu, üstün hizmet"},
}

def get_airline_rating(airline_code):
    """Havayolu puanını getir"""
    if airline_code in AIRLINE_RATINGS:
        return AIRLINE_RATINGS[airline_code]
    return {"rating": 3.5, "stars": "★★★½", "review": "Standart hizmet kalitesi"}

def display_rating_stars(rating):
    """Yıldız gösterimi"""
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    
    stars = "★" * full + "½" * half + "☆" * empty
    return stars