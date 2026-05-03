from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FlightOffer(BaseModel):
    id: str
    airlines: List[str]
    price: float
    currency: str
    outbound: dict
    inbound: Optional[dict] = None
    booking_url: Optional[str] = None
    source: Optional[str] = None
    
    @property
    def main_airline(self) -> str:
        return self.airlines[0] if self.airlines else "?"
    
    @property
    def main_airline_code(self) -> str:
        return self.airlines[0] if self.airlines else "?"
    
    @property
    def formatted_price(self) -> str:
        return f"{self.currency} {self.price:,.2f}"
    
    @property
    def departure_time(self) -> str:
        segments = self.outbound.get('segments', [])
        if segments:
            dep = segments[0].get('departure', '')
            return dep.split('T')[1][:5] if 'T' in dep else '??:??'
        return '??:??'
    
    @property
    def arrival_time(self) -> str:
        segments = self.outbound.get('segments', [])
        if segments:
            arr = segments[-1].get('arrival', '')
            return arr.split('T')[1][:5] if 'T' in arr else '??:??'
        return '??:??'
    
    @property
    def stops(self) -> int:
        # Önce API'den gelen stopovers değerini dene
        stopovers = self.outbound.get('stopovers')
        if stopovers is not None:
            return int(stopovers)
        # Yoksa segment sayısından hesapla
        segments = self.outbound.get('segments', [])
        if segments:
            return max(0, len(segments) - 1)
        return 0
    
    @property
    def stop_text(self) -> str:
        if self.stops == 0:
            return "✈️ Direkt uçuş"
        return f"🔄 {self.stops} aktarmalı"
    
    @property
    def segments(self) -> List[dict]:
        return self.outbound.get('segments', [])
    
    @property
    def total_duration_minutes(self) -> int:
        return self.outbound.get('total_duration_seconds', 0) // 60
    
    @property
    def total_duration_str(self) -> str:
        minutes = self.total_duration_minutes
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours} saat {mins} dakika" if hours > 0 else f"{mins} dakika"
    
    @property
    def route_summary(self) -> str:
        segments = self.segments
        if not segments:
            return "Rota bilgisi yok"
        if self.stops == 0:
            seg = segments[0]
            return f"✈️ {seg.get('origin', '?')} → {seg.get('destination', '?')}"
        route_parts = []
        for i, seg in enumerate(segments):
            origin = seg.get('origin', '?')
            dest = seg.get('destination', '?')
            code = seg.get('airline', '?')
            if i == 0:
                route_parts.append(f"{origin} → {dest} ({code})")
            else:
                route_parts.append(f"→ {dest} ({code})")
        return " 🔄 ".join(route_parts)
    
    @property
    def segment_details(self) -> List[dict]:
        details = []
        for i, seg in enumerate(self.segments, 1):
            dep_raw = seg.get('departure', '')
            arr_raw = seg.get('arrival', '')
            dep_time = dep_raw.split('T')[1][:5] if 'T' in dep_raw else '??:??'
            arr_time = arr_raw.split('T')[1][:5] if 'T' in arr_raw else '??:??'
            details.append({
                "no": i,
                "airline_code": seg.get('airline', '?'),
                "airline_name": seg.get('airline_name', ''),
                "flight_no": seg.get('flight_no', ''),
                "origin": seg.get('origin', '?'),
                "destination": seg.get('destination', '?'),
                "origin_city": seg.get('origin_city', ''),
                "destination_city": seg.get('destination_city', ''),
                "departure_time": dep_time,
                "arrival_time": arr_time,
                "duration_minutes": seg.get('duration_seconds', 0) // 60
            })
        return details
    
    @property
    def layover_details(self) -> List[dict]:
        segments = self.segments
        if len(segments) <= 1:
            return []
        layovers = []
        for i in range(len(segments) - 1):
            current = segments[i]
            next_seg = segments[i + 1]
            arrival_str = current.get('arrival', '')
            departure_str = next_seg.get('departure', '')
            layover_minutes = 0
            layover_str = "Bilinmiyor"
            if arrival_str and departure_str:
                try:
                    arr_dt = datetime.fromisoformat(arrival_str.replace('Z', '+00:00'))
                    dep_dt = datetime.fromisoformat(departure_str.replace('Z', '+00:00'))
                    layover_minutes = int((dep_dt - arr_dt).total_seconds() / 60)
                    if layover_minutes > 0:
                        h = layover_minutes // 60
                        m = layover_minutes % 60
                        layover_str = f"{h} saat {m} dakika" if h > 0 else f"{m} dakika"
                    elif layover_minutes < 0:
                        layover_str = "Ertesi gün"
                except:
                    pass
            layovers.append({
                "city": current.get('destination_city') or current.get('destination', '?'),
                "airport": current.get('destination', '?'),
                "duration_minutes": layover_minutes,
                "duration_str": layover_str,
                "next_airline": next_seg.get('airline', '?')
            })
        return layovers