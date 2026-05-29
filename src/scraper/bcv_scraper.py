import os
import time

import requests
import urllib3
from bs4 import BeautifulSoup

class BCVScraper:
    _cache_soup = None
    _cache_timestamp = 0

    def __init__(self):
        self._url = os.getenv("URL_BASE", "https://www.bcv.org.ve/")
        self._timeout = int(os.getenv("BCV_TIMEOUT", "10"))
        self._cache_ttl = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _fetch_page(self):

        now = time.time()

        if (
            BCVScraper._cache_soup is not None
            and (now - BCVScraper._cache_timestamp) < self._cache_ttl
        ):
            return BCVScraper._cache_soup

        response = requests.get(
            self._url,
            verify=False,
            headers=self._headers,
            timeout=self._timeout,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        BCVScraper._cache_soup = soup
        BCVScraper._cache_timestamp = now

        return soup

    def get_rate(self, currency_id):

        soup = self._fetch_page()
        elements = soup.find_all("div", id=currency_id)

        for element in elements:
            tasa = element.find("strong")
            currency = element.find("span")
            if tasa and currency:
                raw = tasa.text.strip().replace(".", "").replace(",", ".")
                tasa_format = f"{float(raw):,.2f}"
                return {
                    currency_id: tasa_format,
                    "currency": currency.text.strip(),
                }
        return None

    def get_banks(self):

        soup = self._fetch_page()
        table = soup.find(
            "table",
            class_="views-table cols-3 table table-0 table-0 table-0 table-0",
        )
        if not table:
            return None

        body = table.find("tbody")
        rows = body.find_all("tr")

        banks = []
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                banks.append({
                    "banco": cells[0].text.strip().upper(),
                    "tasa": cells[1].text.strip(),
                })
        return banks

    def get_date(self):

        soup = self._fetch_page()
        date_element = soup.find("span", class_="date-display-single")
        if date_element:
            return date_element.text.strip()
        return "Fecha no disponible"
