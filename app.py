from flask import Flask, jsonify
from src.routes import bp_dolar, bp_euro, bp_bancos
import requests
from bs4 import BeautifulSoup
import urllib3
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    # registrar blueprints
    app.register_blueprint(bp_dolar)
    app.register_blueprint(bp_euro)
    app.register_blueprint(bp_bancos)

    # ruta de bienvenida
    @app.route('/', methods=['GET'])
    def index():
        url = "https://www.bcv.org.ve/"
        
        # encabezado para simular un navegador real
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Desactivar advertencias de certificado inseguro
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        date_text = "Fecha no disponible"
        try:
            response = requests.get(url, verify=False, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                date_element = soup.find("span", class_="date-display-single")
                if date_element:
                    date_text = date_element.text.strip()
        except Exception as e:
            print(f"Error fetching date: {e}")

        return jsonify({
            "endpoints": [
            {
                "tasa del dolar": "/dolar",
                "tasa del euro": "/euro",
                "bancos": "/bancos"
            }
        ],
        "date": date_text
    }), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)