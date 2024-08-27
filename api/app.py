import logging
from flask import Flask
from routes import api_bp
from database import init_db
from dotenv import load_dotenv
import os

# Configuración de logging para registrar información adicional
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración para conectar a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos usando la función init_db del archivo database.py
init_db(app)

# Registrar el Blueprint para las rutas de la API
app.register_blueprint(api_bp)

# Ruta de prueba para verificar el manejo de JSON
@app.route('/prueba_json', methods=['POST'])
def prueba_json():
    from flask import request, jsonify
    data = request.json
    if not data:
        return jsonify({"error": "No se enviaron datos JSON"}), 415
    return jsonify({"message": "JSON recibido correctamente", "data": data}), 200

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
