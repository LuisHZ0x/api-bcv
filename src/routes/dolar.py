from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import urllib3

bp_dolar = Blueprint("dolar", __name__)

CORS(bp_dolar)

@bp_dolar.route("/dolar", methods=["GET"])
def dolar():
    url = "https://www.bcv.org.ve/"
    
    # encabezado para simular un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Desactivar advertencias de certificado inseguro
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.get(url, verify=False, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            dollars = soup.find_all("div", id="dolar")
            
            result = {}
            for dollar in dollars:
                tasa = dollar.find("strong") 
                currency = dollar.find("span")
                if tasa and currency:
                    result = {
                        "dolar": tasa.text.strip(),
                        "currency": currency.text.strip()
                    }
                    # Assuming we only want the first one or there is only one
                    break
            
            if result:
                return jsonify(result), 200
            else:
                 return jsonify({"error": "No se encontró la tasa del dolar"}), 404

        else:
            return jsonify({f"error {response.status_code}": "No se pudo obtener la tasa del dolar"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
