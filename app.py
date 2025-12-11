from flask import Flask, jsonify, request
from src.routes import bp_dolar, bp_euro, bp_bancos
import requests
from bs4 import BeautifulSoup
import urllib3
from flask_cors import CORS

def app():
    app = Flask(__name__)

    CORS(app)

    url = "https://www.bcv.org.ve/"

    # encabezado para simular un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Desactivar advertencias de certificado inseguro
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(url, verify=False, headers=headers)

    # registrar blueprints
    app.register_blueprint(bp_dolar)
    app.register_blueprint(bp_euro)
    app.register_blueprint(bp_bancos)

    # ruta de bienvenida
    @app.route('/', methods=['GET'])
    def index():

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            date = soup.find("span", class_="date-display-single")

        return jsonify({
            "message": "API BCV for private company use 16 systems",
            "endpoints": [
            {
                "tasa del dolar": "/dolar",
                "tasa del euro": "/euro",
                "bancos": "/bancos"
            }
        ],
        "date": date.text
    }), 200

    return app

if __name__ == '__main__':
    app = app()
    app.run(debug=True, port=5001)