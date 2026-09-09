from flask import Blueprint, jsonify
from requests import RequestException

from src.scraper.binance_fetcher import BinanceFetcher

bp_usdt = Blueprint("usdt", __name__)


@bp_usdt.route("/usdt", methods=["GET"])
def usdt():
    try:
        fetcher = BinanceFetcher()
        result = fetcher.get_rate()

        if result:
            return jsonify(result), 200
        return jsonify({"error": "No se encontraron anuncios en Binance"}), 404

    except RequestException as e:
        return jsonify({"error": f"Error al consultar Binance: {e}"}), 502
