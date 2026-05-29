from flask import Blueprint, jsonify
from requests import RequestException

from src.scraper import BCVScraper

bp_bancos = Blueprint("bancos", __name__)


@bp_bancos.route("/bancos", methods=["GET"])
def bancos():
    try:
        scraper = BCVScraper()
        banks = scraper.get_banks()

        if banks is not None:
            return jsonify({"bancos": banks}), 200
        return jsonify({"error": "No se encontró la tabla de bancos"}), 404

    except RequestException as e:
        return jsonify({"error": f"Error al consultar el BCV: {e}"}), 502


@bp_bancos.route("/bancos/<banco_nombre>", methods=["GET"])
def banco(banco_nombre):
    try:
        scraper = BCVScraper()
        banks = scraper.get_banks()

        if banks is None:
            return jsonify({"error": "No se encontró la tabla de bancos"}), 404

        match = next(
            (b for b in banks if banco_nombre.upper() in b["banco"]),
            None,
        )

        if match:
            return jsonify({"banco": match}), 200
        return jsonify({"error": "No se encontró el banco"}), 404

    except RequestException as e:
        return jsonify({"error": f"Error al consultar el BCV: {e}"}), 502