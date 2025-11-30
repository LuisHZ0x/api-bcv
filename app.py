from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import urllib3

app = Flask(__name__)

url = "https://www.bcv.org.ve/"

# encabezado para simular un navegador real
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

# Desactivar advertencias de certificado inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(url, verify=False, headers=headers)

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
                "tasa del euro": "/euro"
            }
        ],
        "date": date.text
    }), 200

# ruta para obtener la tasa del dolar
@app.route('/dolar', methods=['GET'])
def dolar():
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        dollars = soup.find_all("div", id="dolar")

        for dollar in dollars:

            tasa = dollar.find("strong") 
            currency = dollar.find("span")

            #respuesta en json
            return jsonify({
                "dolar": tasa.text,
                "currency": currency.text
                }), 200
    else:
        return jsonify({f"error {response.status_code}": "No se pudo obtener la tasa del dolar"}), response.status_code

# ruta para obtener la tasa del euro
@app.route('/euro', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)