"""
    Module for scraping Google flights.
"""

import logging
import time

from typing import List

from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from google_flights_scraper.conf import google_flights_scraper_settings
from google_flights_scraper.models import Flight


logging.getLogger("WDM").setLevel(logging.ERROR)


class ConsentFormAcceptError(BaseException):
    message = "Unable to accept Google consent form."


class DriverInitializationError(BaseException):
    message = "Unable to initialize Chrome webdriver for scraping."


class DriverGetFlightDataError(BaseException):
    message = "Unable to get Google flight data with Chrome webdriver."


class GoogleFlightsScraper:
    """Class for scraping Google flights"""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger if logger else logging.getLogger(__name__)
        self._consent_button_xpath = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span"

    def _init_chrome_driver(self) -> webdriver.Chrome:
        """Initializes Chrome webdriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _click_consent_button(self, driver: webdriver.Chrome) -> None:
        """Clicks google consent form with selenium Chrome webdriver"""
        self._logger.info("Accepting consent form..")
        try:
            driver.get(google_flights_scraper_settings.flights_url)
            consent_button = driver.find_element(
                By.XPATH,
                self._consent_button_xpath,
            )
            consent_button.click()
        except Exception as e:
            raise ConsentFormAcceptError from e

        time.sleep(2)

    def _get_data_from_flight_div(self, div: webdriver.Chrome) -> Flight:
        """Retrieves flight data from a div element and returns it as a Flight object."""
        price = (
            div.find_element(
                By.CLASS_NAME,
                "BVAVmf",
            )
            .find_element(By.CLASS_NAME, "YMlIz")
            .find_element(By.TAG_NAME, "span")
            .get_attribute("aria-label")
        )
        detail = div.find_element(By.CLASS_NAME, "JMc5Xc").get_attribute("aria-label")
        departure_time = div.find_element(By.CLASS_NAME, "wtdjmc").get_attribute(
            "aria-label"
        )

        arrival_time = div.find_element(By.CLASS_NAME, "XWcVob").get_attribute(
            "aria-label"
        )
        info_div = div.find_element(By.CLASS_NAME, "gKm0ye")
        airline = (
            info_div.find_element(By.CLASS_NAME, "h1fkLb")
            .find_element(By.TAG_NAME, "span")
            .text
        )

        stops = info_div.find_element(By.CLASS_NAME, "VG3hNb").text

        return Flight(
            price=price,
            departure_time=(
                departure_time.split("Departure time: ")[1] if departure_time else None
            ),
            arrival_time=(
                arrival_time.split("Arrival time: ")[1] if arrival_time else None
            ),
            airline=airline,
            stops=stops,
            full_detail=detail,
        )

    def _get_flights_from_page(
        self, url: str, driver: webdriver.Chrome
    ) -> List[Flight]:
        """Retrieves Flight data from a Google flights search page."""
        self._logger.info("Scraping Google flights page..")
        driver.get(url)
        time.sleep(5)
        flights = driver.find_elements(By.CLASS_NAME, "pIav2d")

        flight_data = []

        for div in flights:
            try:
                flight_entry = self._get_data_from_flight_div(div)
            except ValidationError:
                self._logger.error(
                    f"Data missing from flight div: {div.get_attribute('outerHTML')}"
                )
                continue

            flight_data.append(flight_entry)

        return flight_data

    def get_flights_for_url(self, url: str) -> List[Flight]:
        """
        Retrieves a list of flights queried in Google flights for a given Flight URL.

        Returns:
            List[Flight]: A list of Flight objects.
        Raises:
            ConsentFormAcceptError: If the Google consent form cannot be accepted.
            DriverInitializationError: If the Chrome webdriver cannot be initialized.
            DriverGetFlightDataError: If the Flight data cannot be scraped from the Google flights site.
        """
        self._logger.info(f"Retrieving flights for {url}..")

        try:
            driver = self._init_chrome_driver()
        except Exception as e:
            raise DriverInitializationError from e

        try:
            self._click_consent_button(driver)
        except Exception as e:
            driver.close()
            raise e

        try:
            return self._get_flights_from_page(url, driver)
        except Exception as e:
            raise DriverGetFlightDataError from e
        finally:
            driver.close()
