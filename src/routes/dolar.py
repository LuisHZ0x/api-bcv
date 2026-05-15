from flask import Blueprint, jsonify
from requests import RequestException

from src.scraper import BCVScraper

bp_dolar = Blueprint("dolar", __name__)


@bp_dolar.route("/dolar", methods=["GET"])
def dolar():
    try:
        scraper = BCVScraper()
        result = scraper.get_rate("dolar")

        if result:
            return jsonify(result), 200
        return jsonify({"error": "No se encontró la tasa del dolar"}), 404

    except RequestException as e:
        return jsonify({"error": f"Error al consultar el BCV: {e}"}), 502
