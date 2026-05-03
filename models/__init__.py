import hashlib
import time

class CacheService:
    def __init__(self, duration: int = 300):
        self._cache = {}
        self.duration = duration
    
    def _get_key(self, origin: str, dest: str, date: str) -> str:
        data = f"{origin}{dest}{date}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, origin: str, dest: str, date: str):
        key = self._get_key(origin, dest, date)
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self.duration:
                return data
            else:
                del self._cache[key]
        return None
    
    def set(self, data, origin: str, dest: str, date: str):
        key = self._get_key(origin, dest, date)
        self._cache[key] = (data, time.time())

cache = CacheService()