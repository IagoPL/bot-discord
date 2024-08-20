from flask import Flask
from routes import api_bp
from database import init_db
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración para conectar a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos usando la función init_db del archivo database.py
init_db(app)

# Registrar el Blueprint para las rutas de la API
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
