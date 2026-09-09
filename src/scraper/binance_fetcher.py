import os
import time
import requests

class BinanceFetcher:
    _cache_data = None
    _cache_timestamp = 0

    def __init__(self):
        self._url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        self._timeout = int(os.getenv("BCV_TIMEOUT", "10"))
        # Usamos el mismo TTL del caché para simplificar
        self._cache_ttl = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
        self._headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            ),
            "Content-Type": "application/json"
        }

    def _fetch_api(self):
        now = time.time()

        if (
            BinanceFetcher._cache_data is not None
            and (now - BinanceFetcher._cache_timestamp) < self._cache_ttl
        ):
            return BinanceFetcher._cache_data

        payload = {
            "proMerchantAds": False,
            "page": 1,
            "rows": 10,
            "payTypes": [],
            "countries": [],
            "publisherType": None,
            "asset": "USDT",
            "fiat": "VES",
            "tradeType": "BUY"
        }

        response = requests.post(
            self._url,
            json=payload,
            headers=self._headers,
            timeout=self._timeout,
        )
        response.raise_for_status()

        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            prices = [float(item["adv"]["price"]) for item in data["data"]]
            avg_price = sum(prices) / len(prices)
            result = {
                "usdt": f"{avg_price:.2f}",
                "currency": "USDT"
            }
            BinanceFetcher._cache_data = result
            BinanceFetcher._cache_timestamp = now
            return result

        return None

    def get_rate(self):
        return self._fetch_api()
