import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from requests import RequestException

from src.routes import bp_bancos, bp_dolar, bp_euro
from src.scraper import BCVScraper

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # registrar blueprints
    app.register_blueprint(bp_dolar, url_prefix="/v1")
    app.register_blueprint(bp_euro, url_prefix="/v1")
    app.register_blueprint(bp_bancos, url_prefix="/v1")

    @app.route("/v1", methods=["GET"])
    def index():
        date_text = "Fecha no disponible"
        try:
            scraper = BCVScraper()
            date_text = scraper.get_date()
        except RequestException as e:
            print(f"Error fetching date: {e}")

        return jsonify({
            "endpoints": [
                {
                    "tasa del dolar": "/dolar",
                    "tasa del euro": "/euro",
                    "bancos": "/bancos",
                    "buscar banco": "/bancos/<banco_nombre>",
                }
            ],
            "date": date_text,
        }), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)