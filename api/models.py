from database import db

class Votacion(db.Model):
    __tablename__ = 'votaciones'

    id = db.Column(db.Integer, primary_key=True)  # Este es el identificador principal
    pregunta = db.Column(db.String(200), nullable=False)
    opciones = db.Column(db.PickleType, nullable=False)  # Almacena una lista o un diccionario
    resultados = db.Column(db.PickleType, nullable=False, default=lambda: {})  # Almacena un diccionario con los resultados
    canal_id = db.Column(db.Integer, nullable=False)
    servidor_id = db.Column(db.Integer, nullable=False)
    cerrada = db.Column(db.Boolean, default=False)  # Campo para indicar si la votación está cerrada

    def __init__(self, pregunta, opciones, canal_id, servidor_id):
        self.pregunta = pregunta
        self.opciones = opciones
        self.canal_id = canal_id
        self.servidor_id = servidor_id
        self.resultados = {opcion: 0 for opcion in opciones}  # Inicializar resultados con 0 votos
