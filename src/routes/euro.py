from flask import Blueprint, jsonify
from requests import RequestException

from src.scraper import BCVScraper

bp_euro = Blueprint("euro", __name__)


@bp_euro.route("/euro", methods=["GET"])
def euro():
    try:
        scraper = BCVScraper()
        result = scraper.get_rate("euro")

        if result:
            return jsonify(result), 200
        return jsonify({"error": "No se encontró la tasa del euro"}), 404

    except RequestException as e:
        return jsonify({"error": f"Error al consultar el BCV: {e}"}), 502
