from flask import Flask, jsonify
import requests
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Configura Sentry (reemplaza TU_DSN_DE_SENTRY)
sentry_sdk.init(
    dsn="https://4b88e5ab59fb983efb92b16acba2e18a@o4509543868727296.ingest.us.sentry.io/4509544645787648",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

# La URL para Proyecto A. Usamos el nombre del servicio Docker Compose: 'proyecto_a'
PROYECTO_A_URL = "http://proyecto_a:5000"

@app.route("/saludo")
def hello_world_b():
    return "Hola desde Proyecto B"

@app.route("/enviar_get_a_proyecto_a")
def enviar_get():
    try:
        response = requests.get(f"{PROYECTO_A_URL}/recibir_get?mensaje=Hola_desde_Proyecto_B_via_GET")
        response.raise_for_status() # Lanza un error para códigos de estado HTTP erróneos
        return jsonify({"status": "GET enviado", "respuesta_de_A": response.json()})
    except requests.exceptions.RequestException as e:
        sentry_sdk.capture_exception(e) # Captura errores de red en Sentry
        return jsonify({"status": "Error al enviar GET", "error": str(e)}), 500

@app.route("/enviar_post_a_proyecto_a")
def enviar_post():
    payload = {"mensaje": "Hola desde Proyecto B via POST"}
    try:
        response = requests.post(f"{PROYECTO_A_URL}/recibir_post", json=payload)
        response.raise_for_status() # Lanza un error para códigos de estado HTTP erróneos
        return jsonify({"status": "POST enviado", "respuesta_de_A": response.json()})
    except requests.exceptions.RequestException as e:
        sentry_sdk.capture_exception(e) # Captura errores de red en Sentry
        return jsonify({"status": "Error al enviar POST", "error": str(e)}), 500

@app.route("/error_b")
def trigger_error_b():
    # Error para probar Sentry en Proyecto B
    division_by_zero = 1 / 0
    return "Este código no se ejecutará"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # Puerto interno del contenedor para Proyecto B