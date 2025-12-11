from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import urllib3

bp_bancos = Blueprint("bancos", __name__)

CORS(bp_bancos)

def fetch_bcv_data():
    url = "https://www.bcv.org.ve/"
    
    # encabezado para simular un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Desactivar advertencias de certificado inseguro
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.get(url, verify=False, headers=headers, timeout=10)
        return response
    except Exception as e:
        print(f"Error fetching BCV data: {e}")
        return None

# ruta para obtener el listado de bancos
@bp_bancos.route("/bancos", methods=["GET"])
def bancos():
    response = fetch_bcv_data()
    
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # buscar la tabla
        tabla_bancos = soup.find("table", class_="views-table cols-3 table table-0 table-0 table-0 table-0")
        if not tabla_bancos:
             return jsonify({"error": "No se encontró la tabla de bancos"}), 404
             
        cuerpo_tabla = tabla_bancos.find("tbody")
        filas = cuerpo_tabla.find_all("tr")

        lista_bancos = []

        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) >= 2:
                banco = celdas[0].text.strip()
                tasa = celdas[1].text.strip()
                lista_bancos.append({"banco": banco.upper(), "tasa": tasa})

        return jsonify({"bancos": lista_bancos}), 200
    else:
        status = response.status_code if response else 500
        return jsonify({"error": "No se pudo obtener el listado de bancos"}), status

# ruta para obtener la tasas de un banco especifico
@bp_bancos.route("/bancos/<banco_nombre>", methods=["GET"])
def banco(banco_nombre):
    response = fetch_bcv_data()

    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # buscar la tabla
        tabla_bancos = soup.find("table", class_="views-table cols-3 table table-0 table-0 table-0 table-0")
        if not tabla_bancos:
             return jsonify({"error": "No se encontró la tabla de bancos"}), 404

        cuerpo_tabla = tabla_bancos.find("tbody")
        filas = cuerpo_tabla.find_all("tr")

        lista_bancos = []

        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) >= 2:
                banco = celdas[0].text.strip()
                tasa = celdas[1].text.strip()
                lista_bancos.append({"banco": banco.upper(), "tasa": tasa})

        buscador = next((banco for banco in lista_bancos if banco_nombre.upper() in banco["banco"]), None)

        if buscador:
            return jsonify({"banco": buscador}), 200
        else:
            return jsonify({"error": "No se encontro el banco"}), 404
    else:
        status = response.status_code if response else 500
        return jsonify({"error": "No se pudo obtener el listado de bancos"}), status