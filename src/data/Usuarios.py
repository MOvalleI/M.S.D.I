import hashlib
import pyodbc
import json
import sys
from pathlib import Path

def fetch_resource(rsrc_path):
        try:
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            return rsrc_path  # No es un exe, devuelve la ruta sin modificar
        else:
            return base_path / rsrc_path  # Retorna la ruta completa usando '/'

DB_INFO = fetch_resource("./db/db_info.json")

def obtener_info_db(file: str = DB_INFO) -> str:
    with open(file, 'r') as archivo:
        datos = json.load(archivo)

        datos_usuarios = datos["usuarios"]

        info = []

        for clave, valor in datos_usuarios.items():
            info.append(valor)

        return f"DRIVER={{{info[0]}}}; SERVER={info[1]}; DATABASE={info[4]}; UID={info[2]}; PWD={info[3]}"
    

QUERYUSERS = "EXEC obtener_usuarios"
QUERYROL = "EXEC obtener_roles"
QUERYIMAGES = "EXEC obtener_fotos"
QUERYTABLES = "EXEC obtener_tablas"
QUERYACTIONS = "EXEC obtener_acciones"


class UsuariosDB:
    def __init__(self):
        self._datos_usuarios = None
        self._datos_tipo_usuario = None
        self._datos_imagenes = None
        self._datos_tablas = None
        self._usuario_logueado = None

        self.conn = pyodbc.connect(obtener_info_db())
        
        self.cursor = self.conn.cursor()
        
        self._datos_usuarios = self.obtener_datos(consulta=QUERYUSERS)
        self._datos_tipo_usuario = self.obtener_datos(consulta=QUERYROL)
        self._datos_imagenes = self.obtener_datos(consulta=QUERYIMAGES)
        self._datos_tablas = self.obtener_datos(consulta=QUERYTABLES)
        self._datos_acciones = self.obtener_datos(consulta=QUERYACTIONS)
    

    def obtener_datos(self, consulta: str) -> dict:
        self.cursor.execute(consulta)

        datos = self.cursor.fetchall()
        diccionario = {}

        for dato in datos:
            id = dato[0]
            valores = list(dato[1:])
            diccionario[id] = valores

        return diccionario
    

    def convertir_passwd(self, passwd: str) -> str:
        h = hashlib.new("SHA256")
        h.update(passwd.encode())

        return h.hexdigest()
    

    def convertir_patron(self, patron: str) -> str:
        h = hashlib.new("SHA256")
        h.update(patron.encode())

        return h.hexdigest()


    def buscar_datos_usuario(self, regex: str) -> dict:
        """
        Devuelve un diccionario con los usuarios cuyo nombre contiene regex.
        """

        diccionario = {}

        for id_usuario, valores in self._datos_usuarios.items():
            if regex.lower() in valores[0].lower():
                diccionario[id_usuario] = valores

        return diccionario

    def buscar_datos_usuario_exacto(self, nombre: str) -> int:
        """
        Devuelve el id correspondiente al usuario exacto.
        Devuelve 0 en caso de no encontrar al usuario.
        """
        for id_usuario, valores in self._datos_usuarios.items():
            if nombre == valores[0]:
                return id_usuario
        return 0
    

    def buscar_id_tipo_por_nombre(self, nombre_tipo: str) -> int:
        for id_tipo, valores in self._datos_tipo_usuario.items():
            if valores[0] == nombre_tipo:  # Compara directamente con el nombre
                return id_tipo
        return 0  # Devuelve un valor por defecto si no se encuentra

           
            
    def buscar_nombre_tipo_por_id(self, id_tipo: int) -> str:
        for ids in self._datos_tipo_usuario.keys():
            if ids==id_tipo:
                return self._datos_tipo_usuario[ids][0]


    def verificar_passwd(self, id_usuario: int, passwd: str) -> bool:
        h = hashlib.new("SHA256")
        h.update(passwd.encode())

        passwd_hash = h.hexdigest()

        if passwd_hash==self._datos_usuarios[id_usuario][1]:
            return True
        return False
    

    def verificar_patron(self, id_usuario: int, patron: str) -> bool:
        h = hashlib.new("SHA256")
        h.update(patron.encode())

        patron_hash = h.hexdigest()

        if patron_hash==self._datos_usuarios[id_usuario][4]:
            return True
        return False
    

    def buscar_id_por_nombre(self, nombre_usuario: str) -> int:
        "Devuelve el id dado un nombre. Devuelve 0 si no encuentra el id"
        for ids in self._datos_tipo_usuario.keys():
            if self._datos_usuarios[ids][0] == nombre_usuario:
                return ids
        return 0 
    

    def modificar_nombre_usuario(self, nombre_anterior: str, nuevo_nombre: str) -> bool:
        for id_usuario, valores in self._datos_usuarios.items():
            if nombre_anterior == valores[0] and nuevo_nombre != valores[0]:
                self._datos_usuarios[id_usuario][0] = nuevo_nombre
                return True
        return False
    

    def modificar_passwd_usuario(self, id_usuario: str, nuevo_passwd: str) -> bool:
        try:    
            hashed_passwd = self.convertir_patron(patron=nuevo_passwd)

            query = """UPDATE Usuarios
                    SET contraseña = ?
                    WHERE id_usuario = ?"""
            
            self.cursor.execute(query, (hashed_passwd, id_usuario))
            self.conn.commit()
            return True
        except:
            return False
    
    
    def modificar_nombre_usuario(self, id_usuario: str, nuevo_nombre: str) -> bool:
        try:    
            query = """UPDATE Usuarios
                    SET nombre_usuario = ?
                    WHERE id_usuario = ?"""
            
            self.cursor.execute(query, (nuevo_nombre, id_usuario))
            self.conn.commit()
            return True
        except:
            return False
    
    
    

    def modificar_patron_usuario(self, id_usuario: int, nuevo_patron: str) -> bool:
        try:    
            hashed_patron = self.convertir_patron(patron=nuevo_patron)

            query = """UPDATE Usuarios
                    SET patron_desbloqueo = ?
                    WHERE id_usuario = ?"""
            
            self.cursor.execute(query, (hashed_patron, id_usuario))
            self.conn.commit()
            return True
        except:
            return False
        
    
    def modificar_patron_usuario(self, id_usuario: int, nuevo_patron: str) -> bool:
        try:    
            hashed_patron = self.convertir_patron(patron=nuevo_patron)

            query = """UPDATE Usuarios
                    SET patron_desbloqueo = ?
                    WHERE id_usuario = ?"""
            
            self.cursor.execute(query, (hashed_patron, id_usuario))
            self.conn.commit()
            return True
        except:
            return False
        
    
    def modificar_pfp_usuario(self, id_usuario: int, id_nueva_foto: int) -> bool:
        try:    
            query = """UPDATE Usuarios
                    SET id_foto_perfil = ?
                    WHERE id_usuario = ?"""
            
            self.cursor.execute(query, (id_nueva_foto, id_usuario))
            self.conn.commit()
            return True
        except:
            return False


    def buscar_imagen_por_id(self, id: int):
        for id_pfp in self._datos_imagenes.keys():
            if id == id_pfp:
                return self._datos_imagenes[id_pfp][0]
    

    def obtener_datos_usuarios(self) -> dict:
        return self._datos_usuarios
    

    def obtener_datos_tipo(self) -> dict:
        return self._datos_tipo_usuario
    

    def obtener_datos_fotos(self) -> dict:
        return self._datos_imagenes
    
    def obtener_datos_tablas(self) -> dict:
        return self._datos_tablas
    

    def recargar_datos(self):
        self._datos_usuarios = self.obtener_datos(consulta=QUERYUSERS)
        self._datos_tipo_usuario = self.obtener_datos(consulta=QUERYROL)
        self._datos_imagenes = self.obtener_datos(consulta=QUERYIMAGES)
        self._datos_tablas = self.obtener_datos(consulta=QUERYTABLES)
        self._datos_acciones = self.obtener_datos(consulta=QUERYACTIONS)

    
    def agregar_nuevo_usuario(self, nombre: str, passwd: str, patron: str, tipo: str, foto: int) -> bool:
        try:
            query = "INSERT INTO Usuarios Values (?, ?, ?, ?, ?, ?)"

            hashed_passwd = self.convertir_passwd(passwd)
            hashed_patron = self.convertir_patron(patron)
            id_tipo = self.buscar_id_tipo_por_nombre(tipo)

            self.cursor.execute(query, (nombre, hashed_passwd, hashed_patron, id_tipo, foto, 1))
            self.conn.commit()
            return True
        except:
            return False
    

    def eliminar_usuario_existente(self, usuario: str) -> bool:
        try:
            query = "EXEC eliminar_usuario ?"

            self.cursor.execute(query, (usuario,))
            self.conn.commit()
            return True
        except:
            return False
        
    
    def obtener_usuarios_filtro(self, nombre=None, id_rol=None):
        query = "EXEC obtener_usuarios_filtro ?, ?"

        self.cursor.execute(query, (nombre, id_rol))
        return self.cursor.fetchall()
    

    def registrar_auditoria(self, id_usuario: int, lista_acciones: list):
        for i in range(len(lista_acciones)):
            acciones = lista_acciones[i]

            id_accion = self.obtener_id_accion_por_nombre(acciones[0])
            id_tabla = self.obtener_id_tabla_por_nombre(acciones[3])

            query = "INSERT INTO Ejecuta VALUES (?, ?, ?, ?, ?)"

            self.cursor.execute(query, (id_usuario, id_accion, id_tabla, acciones[1], acciones[2]))
            self.conn.commit()


    def registrar_sesion(self, id_usuario: int, fechas: list):
        try:
            query = "INSERT INTO Sesion VALUES (?, ?, ?, ?, ?)"

            self.cursor.execute(query, (id_usuario, fechas[0],fechas[1],fechas[2],fechas[3]))
            self.conn.commit()
        except:
            pass
    

    def obtener_id_tabla_por_nombre(self, tabla: str) -> int:
        query = "SELECT id_tabla FROM Tabla WHERE nombre_tabla = ?"

        self.cursor.execute(query, (tabla,))
        return self.cursor.fetchone()[0] if not None else 0
    

    def obtener_id_accion_por_nombre(self, accion: str) -> int:
        query = "SELECT id_accion FROM Accion WHERE nombre_accion = ?"

        self.cursor.execute(query, (accion,))
        resultado = self.cursor.fetchone()

        # Verificar si no hay resultado
        if resultado is None:
            return 0  # Si no se encuentra la acción, devolver 0 o un valor que indique que no se encontró
        else:
            return resultado[0]  # Devolver el id_accion si se encuentra

    

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()
    
