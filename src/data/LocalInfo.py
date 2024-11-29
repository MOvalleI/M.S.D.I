import sqlite3

"Modulo con funciones para configurar la base de datos PREFERENCES"

def conectar() -> sqlite3:
    conn = sqlite3.connect("./src/db/Preferences.db")
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




    

