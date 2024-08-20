"""
    Main module for collecting Google flights data.
"""

import logging

from typing import List

import pandas as pd

from google_flights_scraper.models import Flight
from google_flights_scraper.scraper import GoogleFlightsScraper


DEFAULT_OUTPUT_FILE = "flights.csv"


class GoogleFlightsDataCollector:
    """Data collector class for Google Flights"""

    def __init__(
        self,
        output_file: str | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._scraper = GoogleFlightsScraper()
        self._output_file = output_file if output_file else DEFAULT_OUTPUT_FILE
        self._logger = logger if logger else logging.getLogger(__name__)

    def _save_to_csv(self, flights: List[Flight]) -> None:
        """Saves given list of flights to a CSV file."""
        self._logger.info(f"Writing {len(flights)} flights to {self._output_file}..")
        flight_objects = [flight.model_dump() for flight in flights]
        df = pd.DataFrame(flight_objects)
        df.to_csv(self._output_file)

    def save_flight_data_for_url(self, url: str) -> None:
        """
        Scrapes data from Google flights for a given flight url and stores it into a CSV file.

        Args:
            url (str): The URL of the flight for which to get Google flights results.
        """
        self._logger.info(f"Getting Google flights data for flight url {url}..")
        try:
            flights = self._scraper.get_flights_for_url(url)
        except Exception:
            self._logger.exception(f"Error when scraping Google flights for url {url}.")
            return

        if not flights:
            self._logger.info("No flights found.")
            return

        self._save_to_csv(flights)
