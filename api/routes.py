from flask import Blueprint, request, jsonify
from models import db, Votacion

# Crear un Blueprint para la API
api_bp = Blueprint('api', __name__)

# Ruta para crear una nueva votación
@api_bp.route('/crear_votacion', methods=['POST'])
def crear_votacion():
    data = request.json
    
    # Crear una nueva instancia de la clase Votacion
    nueva_votacion = Votacion(
        pregunta=data['pregunta'],
        opciones=data['opciones'],
        mensaje_id=data['mensaje_id'],
        canal_id=data['canal_id'],
        servidor_id=data['servidor_id']
    )
    
    # Agregar la nueva votación a la base de datos
    db.session.add(nueva_votacion)
    db.session.commit()
    
    return jsonify({"message": "Votación creada"}), 200

# Ruta para cerrar una votación y guardar los resultados
@api_bp.route('/cerrar_votacion', methods=['POST'])
def cerrar_votacion():
    data = request.json
    
    # Buscar la votación por mensaje_id
    votacion = Votacion.query.filter_by(mensaje_id=data['mensaje_id']).first()
    
    if votacion:
        # Actualizar los resultados de la votación
        votacion.resultados = data['resultados']
        db.session.commit()
        return jsonify({"message": "Resultados guardados"}), 200
    
    return jsonify({"error": "Votación no encontrada"}), 404
