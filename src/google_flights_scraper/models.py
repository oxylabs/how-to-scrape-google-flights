"""
    Pydantic models for Google Flights scraper.
"""

from pydantic import BaseModel


class Flight(BaseModel):
    price: str
    departure_time: str
    arrival_time: str
    airline: str
    stops: str
    full_detail: str
