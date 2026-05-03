import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
    CACHE_DURATION = int(os.getenv("CACHE_DURATION", 300))
    APP_NAME = "Uçuş Motoru Pro"
    APP_VERSION = "2.0.0"

settings = Settings()