from flask import Blueprint, Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import urllib3

bp_bancos = Blueprint("bancos", __name__)

CORS(bp_bancos)

url = "https://www.bcv.org.ve/"

# encabezado para simular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Desactivar advertencias de certificado inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(url, verify=False, headers=headers)

# ruta para obtener el listado de bancos
@bp_bancos.route("/bancos", methods=["GET"])
def bancos():
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # buscar la tabla
        tabla_bancos = soup.find("table", class_="views-table cols-3 table table-0 table-0 table-0 table-0")
        cuerpo_tabla = tabla_bancos.find("tbody")
        filas = cuerpo_tabla.find_all("tr")

        lista_bancos = []

        for fila in filas:
            celdas = fila.find_all("td")

            banco = celdas[0].text.strip()
            tasa = celdas[1].text.strip()
            lista_bancos.append({"banco": banco.upper(), "tasa": tasa})

        return jsonify({"bancos": lista_bancos}), 200
    else:
        return jsonify({"error": "No se pudo obtener el listado de bancos"}), response.status_code

# ruta para obtener la tasas de un banco especifico
@bp_bancos.route("/bancos/<banco_nombre>", methods=["GET"])
def banco(banco_nombre):
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # buscar la tabla
        tabla_bancos = soup.find("table", class_="views-table cols-3 table table-0 table-0 table-0 table-0")
        cuerpo_tabla = tabla_bancos.find("tbody")
        filas = cuerpo_tabla.find_all("tr")

        lista_bancos = []

        for fila in filas:
            celdas = fila.find_all("td")

            banco = celdas[0].text.strip()
            tasa = celdas[1].text.strip()
            lista_bancos.append({"banco": banco.upper(), "tasa": tasa})

        # for banco in lista_bancos:
        #     if banco_nombre in banco["banco"]:
        #         return jsonify({"banco": banco}), 200
        #     else:
        #         return jsonify({"error": "No se encontro el banco"}), 404

        buscador = next((banco for banco in lista_bancos if banco_nombre.upper() in banco["banco"]), None)

        if buscador:
            return jsonify({"banco": buscador}), 200
        else:
            return jsonify({"error": "No se encontro el banco"}), 404
    else:
        return jsonify({"error": "No se pudo obtener el listado de bancos"}), response.status_code