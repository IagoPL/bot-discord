from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa la base de datos con la aplicación Flask.
    Esta función se llama desde el archivo app.py.
    """
    db.init_app(app)

    # Crear todas las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()
