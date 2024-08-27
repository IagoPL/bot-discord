# Documentación de la API de Votaciones

## Introducción

Esta API permite la gestión de votaciones, incluyendo la creación de nuevas votaciones, la visualización de votaciones existentes, la adición de votos y la obtención de resultados.

## Estructura de la Base de Datos

La base de datos contiene una única tabla `votaciones` con los siguientes campos:

- **id**: Entero, auto-incremental, clave primaria.
- **pregunta**: Cadena de caracteres, contiene la pregunta de la votación.
- **opciones**: BLOB, almacena las opciones de la votación en formato serializado.
- **resultados**: BLOB, almacena los resultados de la votación en formato serializado.
- **canal_id**: Entero, identifica el canal donde se realiza la votación.
- **servidor_id**: Entero, identifica el servidor donde se realiza la votación.
- **cerrada**: Booleano, indica si la votación está cerrada (valor por defecto `0`).

## Endpoints de la API

### 1. Crear una Votación

**Descripción**: Este endpoint permite crear una nueva votación.

- **URL**: `/api/crear_votacion`
- **Método**: `POST`
- **Datos de Entrada (JSON)**:
  
  ```json
  {
    "pregunta": "¿Cuál es tu lenguaje de programación favorito?",
    "opciones": ["Python", "JavaScript", "C#", "Java"],
    "canal_id": 123,
    "servidor_id": 456
  }
  ```
  
  ```json
  {
    "message": "Votación creada",
    "votacion_id": 1
  }
  ```

### 2. Añadir un Voto

**Descripción**: Permite añadir un voto a una opción específica de una votación.

- **URL**: `/api/añadir_voto`
- **Método**: `POST`
- **Datos de Entrada (JSON)**:
  ```json
  {
    "votacion_id": 1,
    "voto": "Python"
  }
  ```
- **Respuesta (JSON)**:
  ```json
  {
    "message": "Voto registrado correctamente"
  }
  ```

### 3. Mostrar una Votación

**Descripción**: Muestra los detalles y resultados de una votación específica.

- **URL**: `/api/mostrar_votacion/<int:votacion_id>`
- **Método**: `GET`
- **Respuesta (JSON)**:
  ```json
  {
    "pregunta": "¿Cuál es tu lenguaje de programación favorito?",
    "opciones": ["Python", "JavaScript", "C#", "Java"],
    "resultados": {
      "Python": 5,
      "JavaScript": 2,
      "C#": 3,
      "Java": 1
    },
    "total_votos": 11
  }
  ```

## Ejemplos de Uso con Postman

### 1. Crear una Votación

- **Método**: `POST`
- **URL**: `http://localhost:5000/api/crear_votacion`
- **Cuerpo (JSON)**:
  ```json
  {
    "pregunta": "¿Cuál es tu framework de frontend favorito?",
    "opciones": ["React", "Vue", "Angular"],
    "canal_id": 789,
    "servidor_id": 101112
  }
  ```

### 2. Añadir un Voto

- **Método**: `POST`
- **URL**: `http://localhost:5000/api/añadir_voto`
- **Cuerpo (JSON)**:
  ```json
  {
    "votacion_id": 1,
    "voto": "React"
  }
  ```

### 3. Mostrar los Resultados de una Votación

- **Método**: `GET`
- **URL**: `http://localhost:5000/api/mostrar_votacion/1`

## Instalación y Ejecución

1. **Instalar Dependencias**: Asegúrate de tener un entorno virtual configurado e instala las dependencias usando:
   
   ```bash
   pip install -r requirements.txt
   ```
2. **Ejecutar la Aplicación**: Inicia el servidor Flask:
   
   ```bash
   flask run
   ```
   
   El servidor estará corriendo en `http://localhost:5000`.

## Notas Adicionales

- **Formato de Resultados**: Los campos `opciones` y `resultados` están serializados usando `pickle`. Es importante manejar correctamente la serialización y deserialización de estos campos al interactuar con la base de datos.
- **Manejo de Errores**: La API devuelve mensajes de error en formato JSON en caso de fallos, por ejemplo, si se intenta votar en una opción que no existe.


