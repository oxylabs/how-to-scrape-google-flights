"""
    Main module for google_flights_scraper.
"""

import logging

import click

from google_flights_scraper.collector import GoogleFlightsDataCollector


logging.basicConfig(level=logging.INFO)


@click.command()
@click.option(
    "--url",
    help="The url for which to return Google Flights results for.",
    required=True,
)
def scrape_google_flights(url: str) -> None:
    collector = GoogleFlightsDataCollector()
    collector.save_flight_data_for_url(url)


if __name__ == "__main__":
    scrape_google_flights()
