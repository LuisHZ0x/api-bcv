from flask import Blueprint, Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import urllib3

bp_euro = Blueprint("euro", __name__)

CORS(bp_euro)

url = "https://www.bcv.org.ve/"

# encabezado para simular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Desactivar advertencias de certificado inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(url, verify=False, headers=headers)

@bp_euro.route("/euro", methods=["GET"])
def euro():
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        euros = soup.find_all("div", id="euro")

        for euro in euros:

            tasa = euro.find("strong") 
            currency = euro.find("span")

            #respuesta en json
            return jsonify({
                "euro": tasa.text,
                "currency": currency.text
                }), 200
    else:
        return jsonify({f"error {response.status_code}": "No se pudo obtener la tasa del euro"}), response.status_code
