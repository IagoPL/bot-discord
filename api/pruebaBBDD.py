from sqlalchemy import create_engine

DATABASE_URI = 'mysql+pymysql://root:root@localhost/votaciones_db'

try:
    engine = create_engine(DATABASE_URI)
    connection = engine.connect()
    print("Conexión exitosa a la base de datos")
    connection.close()
except Exception as e:
    print(f"Error al conectar: {e}")
