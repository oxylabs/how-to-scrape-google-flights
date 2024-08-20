# How to Scrape Google Flights with Python

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

[![](https://dcbadge.vercel.app/api/server/eWsVUJrnG5)](https://discord.gg/GbxmdGhZjq)

In this quick guide, we’re going to demonstrate how to scrape public data from **flight pages** and generate **search results** with Python and [Oxylabs Google Flights API](https://oxylabs.io/products/scraper-api/serp/google/flights). To use the Oxylabs API, you'll need an **active subscription** – you can get a **free trial** by signing up [via the self-service dashboard](https://dashboard.oxylabs.io/).

We’ll gather all sorts of data, including **price**, **flight time**, and **airline name**.

Head to our blog to see the [complete article](https://oxylabs.io/blog/how-to-scrape-google-flights) with in-depth explanations and images for a visual reference.

- [1. Installing prerequisite libraries](#1-installing-prerequisite-libraries)
- [2. Creating core structure](#2-creating-core-structure)
- [3. Getting the price](#3-getting-the-price)
- [4. Getting the flight time](#4-getting-the-flight-time)
- [5. Getting the airline name](#5-getting-the-airline-name)
- [6. Final result](#6-final-result)

## 1. Installing prerequisite libraries

```bash
pip install bs4
```

## 2. Creating core structure

To start off, let’s create a function that will take a URL as a parameter, scrape that URL with [Google Flights API](https://oxylabs.io/products/scraper-api/serp/google/flights) (you can get **a free 7-day trial** for it) and return the scraped HTML:

```python
def get_flights_html(url):
    payload = {
        'source': 'google',
        'render': 'html',
        'url': url,
    }

    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('username', 'password'),
        json=payload,
    )

    response_json = response.json()

    html = response_json['results'][0]['content']

    return html
```

Make sure to change up `USERNAME` and `PASSWORD` with your actual Oxylabs credentials.

Next up, we’ll create a function that accepts a `BeautifulSoup` object created from the HTML of the whole page. This function will create and return an array of objects containing information from individual flight listings. Let’s try to form the function in such a way that makes it easily extendible if required:

```python
def extract_flight_information_from_soup(soup_of_the_whole_page):
    flight_listings = soup_of_the_whole_page.find_all('li','pIav2d')

    flights = []

    for listing in flight_listings:
        if listing is not None:
            # Add some specific data extraction here

            flight = {}

            flights.append(flight)

    return flights
```

Now that we can get the HTML and have a function to hold our information extraction, we can organize both of those into one:

```python
def extract_flights_data_from_urls(urls):
    constructed_flight_results = []

    for url in urls:
        html = get_flights_html(url)

        soup = BeautifulSoup(html,'html.parser')

        flights = extract_flight_information_from_soup(soup)

        constructed_flight_results.append({
            'url': url,
            'flight_data': flights
        })

    return constructed_flight_results
```

This function will take an array of URLs as a parameter and return an object of extracted flight data.

One thing left for our core is a function that takes this data and saves it as a file:

```python
def save_results(results, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    return
```

We can finish by creating a simple `main` function to invoke all that we’ve created so far:
```python
def main():
    results_file = 'data.json'

    urls = [
        'https://www.google.com/travel/flights?tfs=CBsQAhooEgoyMDI0LTA3LTI4agwIAxIIL20vMDE1NnFyDAgCEggvbS8wNGpwbBooEgoyMDI0LTA4LTAxagwIAhIIL20vMDRqcGxyDAgDEggvbS8wMTU2cUABSAFSA0VVUnABemxDalJJTkRCNVRGbDBOMU5UVEdOQlJ6aG5lRUZDUnkwdExTMHRMUzB0TFMxM1pXc3lOMEZCUVVGQlIxZ3dhRWxSUVRoaWFtTkJFZ1pWTWpnMk1qSWFDZ2lRYnhBQ0dnTkZWVkk0SEhEN2VBPT2YAQGyARIYASABKgwIAxIIL20vMDRqcGw&hl=en-US&curr=EUR&sa=X&ved=0CAoQtY0DahgKEwiAz9bF5PaEAxUAAAAAHQAAAAAQngM',
        'https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI0LTA3LTI4agwIAxIIL20vMDE1NnFyDAgDEggvbS8wN19rcRooEgoyMDI0LTA4LTAxagwIAxIIL20vMDdfa3FyDAgDEggvbS8wMTU2cUABSAFwAYIBCwj___________8BmAEB&hl=en-US&curr=EUR'
    ]

    constructed_flight_results = extract_flights_data_from_urls(urls)

    save_results(constructed_flight_results, results_file)
```

## 3. Getting the price

```python
def get_price(soup_element):
    price = soup_element.find('div','BVAVmf').find('div','YMlIz').get_text()

    return price
```

## 4. Getting the flight time

```python
def get_time(soup_element):
    spans = soup_element.find('div','Ir0Voe').find('div','zxVSec', recursive=False).find_all('span', 'eoY5cb')

    time = ""

    for span in spans:
        time = time + span.get_text() + "; "

    return time
```

## 5. Getting the airline name

```python
def get_airline(soup_element):
    airline = soup_element.find('div','Ir0Voe').find('div','sSHqwe')

    spans = airline.find_all('span', attrs={"class": None}, recursive=False)

    result = ""

    for span in spans:
        result = result + span.get_text() + "; "

    return result
```

Having all of these functions for data extraction, we just need to add them to the place we designated earlier to finish up our code.


```python
def extract_flight_information_from_soup(soup_of_the_whole_page):
    flight_listings = soup_of_the_whole_page.find_all('li','pIav2d')

    flights = []

    for listing in flight_listings:
        if listing is not None:
            price = get_price(listing)
            time = get_time(listing)
            airline = get_airline(listing)

            flight = {
                "airline": airline,
                "time": time,
                "price": price
            }

            flights.append(flight)

    return flights
```
## 6. Final result
If we add all of it together, the final product should look something like this.


```python
from bs4 import BeautifulSoup
import requests
import json

def get_price(soup_element):
    price = soup_element.find('div','BVAVmf').find('div','YMlIz').get_text()

    return price


def get_time(soup_element):
    spans = soup_element.find('div','Ir0Voe').find('div','zxVSec', recursive=False).find_all('span', 'eoY5cb')

    time = ""

    for span in spans:
        time = time + span.get_text() + "; "

    return time


def get_airline(soup_element):
    airline = soup_element.find('div','Ir0Voe').find('div','sSHqwe')

    spans = airline.find_all('span', attrs={"class": None}, recursive=False)

    result = ""

    for span in spans:
        result = result + span.get_text() + "; "

    return result


def save_results(results, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    return


def get_flights_html(url):
    payload = {
        'source': 'google',
        'render': 'html',
        'url': url,
    }

    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('username', 'password'),
        json=payload,
    )

    response_json = response.json()

    html = response_json['results'][0]['content']

    return html


def extract_flight_information_from_soup(soup_of_the_whole_page):
    flight_listings = soup_of_the_whole_page.find_all('li','pIav2d')

    flights = []

    for listing in flight_listings:
        if listing is not None:
            price = get_price(listing)
            time = get_time(listing)
            airline = get_airline(listing)

            flight = {
                "airline": airline,
                "time": time,
                "price": price
            }

            flights.append(flight)

    return flights


def extract_flights_data_from_urls(urls):
    constructed_flight_results = []

    for url in urls:
        html = get_flights_html(url)

        soup = BeautifulSoup(html,'html.parser')

        flights = extract_flight_information_from_soup(soup)

        constructed_flight_results.append({
            'url': url,
            'flight_data': flights
        })

    return constructed_flight_results


def main():
    results_file = 'data.json'

    urls = [
        'https://www.google.com/travel/flights?tfs=CBsQAhooEgoyMDI0LTA3LTI4agwIAxIIL20vMDE1NnFyDAgCEggvbS8wNGpwbBooEgoyMDI0LTA4LTAxagwIAhIIL20vMDRqcGxyDAgDEggvbS8wMTU2cUABSAFSA0VVUnABemxDalJJTkRCNVRGbDBOMU5UVEdOQlJ6aG5lRUZDUnkwdExTMHRMUzB0TFMxM1pXc3lOMEZCUVVGQlIxZ3dhRWxSUVRoaWFtTkJFZ1pWTWpnMk1qSWFDZ2lRYnhBQ0dnTkZWVkk0SEhEN2VBPT2YAQGyARIYASABKgwIAxIIL20vMDRqcGw&hl=en-US&curr=EUR&sa=X&ved=0CAoQtY0DahgKEwiAz9bF5PaEAxUAAAAAHQAAAAAQngM',
        'https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI0LTA3LTI4agwIAxIIL20vMDE1NnFyDAgDEggvbS8wN19rcRooEgoyMDI0LTA4LTAxagwIAxIIL20vMDdfa3FyDAgDEggvbS8wMTU2cUABSAFwAYIBCwj___________8BmAEB&hl=en-US&curr=EUR'
    ]

    constructed_flight_results = extract_flights_data_from_urls(urls)

    save_results(constructed_flight_results, results_file)


if __name__ == "__main__":
    main()
```

By employing Python and Oxylabs SERP Scraper API, you can easily deal with the dynamic nature of Google Flights and gather public data successfully.
