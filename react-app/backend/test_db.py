from app.database import engine

try:
    connection = engine.connect()
    print("✅ Conexión exitosa a la base de datos")
    connection.close()
except Exception as e:
    print("❌ Error de conexión:", e)