# Importar la instancia de db desde database.py
from database import db

# Definición del modelo de la tabla "Votacion"
class Votacion(db.Model):
    __tablename__ = 'votaciones'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(200), nullable=False)
    opciones = db.Column(db.PickleType, nullable=False)
    resultados = db.Column(db.PickleType, default={})
    mensaje_id = db.Column(db.Integer, nullable=False)
    canal_id = db.Column(db.Integer, nullable=False)
    servidor_id = db.Column(db.Integer, nullable=False)

    def __init__(self, pregunta, opciones, mensaje_id, canal_id, servidor_id):
        self.pregunta = pregunta
        self.opciones = opciones
        self.mensaje_id = mensaje_id
        self.canal_id = canal_id
        self.servidor_id = servidor_id
