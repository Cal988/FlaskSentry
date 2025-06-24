from flask import Flask, request, jsonify
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

@app.route("/saludo")
def hello_world():
    return "Hola desde Proyecto A"

@app.route("/recibir_get", methods=['GET'])
def recibir_get():
    mensaje = request.args.get('mensaje', 'No se recibió mensaje GET')
    print(f"Proyecto A recibió GET: {mensaje}") # Para ver en la consola de Docker
    return jsonify({"status": "recibido", "mensaje": f"GET: {mensaje} de Proyecto B"})

@app.route("/recibir_post", methods=['POST'])
def recibir_post():
    if request.is_json:
        data = request.get_json()
        mensaje = data.get('mensaje', 'No se recibió mensaje POST JSON')
        print(f"Proyecto A recibió POST: {mensaje}") # Para ver en la consola de Docker
        return jsonify({"status": "recibido", "mensaje": f"POST: {mensaje} de Proyecto B"})
    else:
        mensaje = request.data.decode('utf-8')
        print(f"Proyecto A recibió POST (texto/form): {mensaje}") # Para ver en la consola de Docker
        return jsonify({"status": "recibido", "mensaje": f"POST (texto/form): {mensaje} de Proyecto B"})

@app.route("/error_a")
def trigger_error_a():
    # Error para probar Sentry en Proyecto A
    division_by_zero = 1 / 0
    return "Este código no se ejecutará"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Puerto interno del contenedor para Proyecto A