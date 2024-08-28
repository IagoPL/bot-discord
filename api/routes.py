import pickle
from flask import Blueprint, request, jsonify
from models import db, Votacion

# Crear un Blueprint para la API
api_bp = Blueprint('api', __name__)

# Ruta para crear una nueva votación
@api_bp.route('/crear_votacion', methods=['POST'])
def crear_votacion():
    data = request.json
    
    # Serializar las opciones y resultados
    opciones_serializadas = pickle.dumps(data['opciones'])
    resultados_serializados = pickle.dumps({opcion: 0 for opcion in data['opciones']})
    
    # Crear una nueva instancia de la clase Votacion
    nueva_votacion = Votacion(
        pregunta=data['pregunta'],
        opciones=opciones_serializadas,
        canal_id=data['canal_id'],
        servidor_id=data['servidor_id']
    )
    nueva_votacion.resultados = resultados_serializados
    
    # Agregar la nueva votación a la base de datos
    db.session.add(nueva_votacion)
    db.session.commit()
    
    return jsonify({"message": "Votación creada", "id": nueva_votacion.id}), 200


# Ruta para añadir un voto a una votación y guardar los resultados
@api_bp.route('/añadir_voto', methods=['POST'])
def añadir_voto():
    try:
        data = request.json
        votacion_id = data.get('votacion_id')
        voto = data.get('voto')

        votacion = Votacion.query.get(votacion_id)

        if not votacion:
            return jsonify({"message": "Votación no encontrada"}), 404

        # Si votacion.resultados ya es un dict, no intentar deserializarlo
        if isinstance(votacion.resultados, dict):
            resultados = votacion.resultados
        else:
            resultados = pickle.loads(votacion.resultados)

        # Aumentar el conteo del voto correspondiente
        if voto in resultados:
            resultados[voto] += 1
        else:
            return jsonify({"message": "Opción no válida"}), 400

        # Convertir dict a blob y guardar de nuevo en la base de datos
        votacion.resultados = pickle.dumps(resultados)

        # Guardar los cambios en la base de datos
        db.session.commit()

        print(f"Voto añadido correctamente. Resultados actualizados: {resultados}")
        return jsonify({"message": "Voto añadido correctamente"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error interno del servidor"}), 500



# Ruta para mostrar los detalles de una votación
@api_bp.route('/mostrar_votacion/<int:votacion_id>', methods=['GET'])
def mostrar_votacion(votacion_id):
    # Busca la votación en la base de datos por su ID
    votacion = Votacion.query.get(votacion_id)

    # Si no se encuentra la votación, devuelve un error
    if not votacion:
        return jsonify({"error": "Votación no encontrada"}), 404

    # Deserializar opciones y resultados
    try:
        opciones = pickle.loads(votacion.opciones)
        resultados = pickle.loads(votacion.resultados)
    except (pickle.PickleError, TypeError) as e:
        return jsonify({"message": "Error en los datos almacenados", "tipo": str(e)}), 500

    # Construye la respuesta con los detalles de la votación y los resultados
    respuesta = {
        "pregunta": votacion.pregunta,
        "opciones": opciones,  # Asume que esto es una lista de opciones
        "resultados": resultados,  # Asume que esto es un diccionario de resultados
        "total_votos": sum(resultados.values())  # Suma el total de votos
    }

    # Devuelve la respuesta como JSON
    return jsonify(respuesta), 200
