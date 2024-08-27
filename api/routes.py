import pickle
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
        canal_id=data['canal_id'],
        servidor_id=data['servidor_id']
    )
    
    # Agregar la nueva votación a la base de datos
    db.session.add(nueva_votacion)
    db.session.commit()
    
    return jsonify({"message": "Votación creada", "id": nueva_votacion.id}), 200

# Ruta para cerrar una votación y evitar modificaciones
@api_bp.route('/cerrar_votacion/<int:votacion_id>', methods=['POST'])
def cerrar_votacion(votacion_id):
    # Busca la votación en la base de datos por su ID
    votacion = Votacion.query.get(votacion_id)

    # Si no se encuentra la votación, devuelve un error
    if not votacion:
        return jsonify({"error": "Votación no encontrada"}), 404

    # Marcar la votación como cerrada
    votacion.cerrada = True

    # Guardar los cambios en la base de datos
    try:
        db.session.commit()
        return jsonify({"message": "Votación cerrada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al cerrar la votación", "detalles": str(e)}), 500


# Ruta para añadir un voto a una votación y guardar los resultados
@api_bp.route('/añadir_voto', methods=['POST'])
def añadir_voto():
    import pickle

    data = request.json
    votacion_id = data.get('votacion_id')
    voto = data.get('voto')

    votacion = Votacion.query.get(votacion_id)

    if not votacion:
        return jsonify({"message": "Votación no encontrada"}), 404

    if votacion.cerrada:
        return jsonify({"message": "La votación está cerrada"}), 400

    # Verificar y cargar los resultados de la votación
    if isinstance(votacion.resultados, bytes):
        resultados = pickle.loads(votacion.resultados)
    elif isinstance(votacion.resultados, dict):
        resultados = votacion.resultados
    else:
        return jsonify({"message": "Error en los datos almacenados", "tipo": str(type(votacion.resultados))}), 500

    # Verificar que el voto sea una opción válida
    if voto in resultados:
        resultados[voto] += 1
    else:
        return jsonify({"message": "Opción no válida"}), 400

    # Guardar los resultados actualizados
    votacion.resultados = pickle.dumps(resultados)
    db.session.commit()

    return jsonify({"message": "Voto añadido correctamente"}), 200



@api_bp.route('/mostrar_votacion/<int:votacion_id>', methods=['GET'])
def mostrar_votacion(votacion_id):
    # Busca la votación en la base de datos por su ID
    votacion = Votacion.query.get(votacion_id)

    # Si no se encuentra la votación, devuelve un error
    if not votacion:
        return jsonify({"error": "Votación no encontrada"}), 404

    # Convertir los resultados de blob a dict si es necesario
    if isinstance(votacion.resultados, bytes):
        resultados = pickle.loads(votacion.resultados)
    elif isinstance(votacion.resultados, dict):
        resultados = votacion.resultados
    else:
        return jsonify({"message": "Error en los datos almacenados", "tipo": str(type(votacion.resultados))}), 500

    # Construye la respuesta con los detalles de la votación y los resultados
    respuesta = {
        "pregunta": votacion.pregunta,
        "opciones": votacion.opciones,  # Asume que esto es una lista de opciones
        "resultados": resultados,  # Asume que esto es un diccionario de resultados
        "total_votos": sum(resultados.values())  # Suma el total de votos
    }

    # Devuelve la respuesta como JSON
    return jsonify(respuesta), 200
