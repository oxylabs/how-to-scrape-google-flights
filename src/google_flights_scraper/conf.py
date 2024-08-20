"""
    Config module for google_flights_scraper.
"""

from pydantic_settings import BaseSettings


class GoogleFlightsScraperSettings(BaseSettings):
    """Settings class for Google Flights Scraper"""

    flights_url: str = "https://www.google.com/travel/flights"


google_flights_scraper_settings = GoogleFlightsScraperSettings()
