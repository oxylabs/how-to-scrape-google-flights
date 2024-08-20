# Makefile for running the Google Flights scraper


.PHONY: install
install:
	pip install poetry==1.8.2
	poetry install


.PHONY: scrape
scrape:
	@if [ -z "$(URL)" ]; then \
		echo 'Error: A URL of a Google Flights page is required. Use make scrape URL="<url>"'; \
		exit 1; \
	else \
		poetry run python -m google_flights_scraper --url="$(URL)"; \
	fi
