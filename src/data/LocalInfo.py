import sqlite3

"Modulo con funciones para configurar la base de datos PREFERENCES"

def conectar() -> sqlite3:
    conn = sqlite3.connect("./db/Preferences.db")
    cursor = conn.cursor()
    return conn, cursor

def desconectar(conn, cursor):
    cursor.close()
    conn.close()

def obtener_info_local():
    conn, cursor = conectar()
    cursor.execute("SELECT numero_local FROM local")
    res = cursor.fetchone()
    desconectar(conn=conn, cursor=cursor)
    return res[0]

def cambiar_info_local(nuevo_local):
    cambio_exitoso = False
    conn, cursor = None, None  # Inicializamos las variables
    try:
        conn, cursor = conectar()
        cursor.execute("UPDATE local SET numero_local = ?", (nuevo_local,))
        conn.commit()
        cambio_exitoso = True
    except Exception as e:
        print(f"Error al cambiar la información del local: {e}")
    finally:
        if conn and cursor:  # Verificamos que estén inicializados
            desconectar(conn=conn, cursor=cursor)
    return cambio_exitoso

