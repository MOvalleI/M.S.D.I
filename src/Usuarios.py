import sqlite3
import hashlib

USERDATABASE = "./db/NewUsers.db"
QUERYUSERS = "SELECT * FROM usuarios"
QUERYTYPES = "SELECT * FROM tipo"
QUERYIMAGES = "SELECT * FROM foto_perfil"

class Usuarios:
    def __init__(self):
        self._datos_usuarios = None
        self._datos_tipo_usuario = None
        self._datos_imagenes = None
        self._usuario_logueado = None

        conn = sqlite3.connect(USERDATABASE)
        self.cursor = conn.cursor()
        
        self._datos_usuarios = self.obtener_datos(consulta=QUERYUSERS)
        self._datos_tipo_usuario = self.obtener_datos(consulta=QUERYTYPES)
        self._datos_imagenes = self.obtener_datos(consulta=QUERYIMAGES)

        self.cursor.close()
        conn.close()
    

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
    

    def buscar_datos_usuario(self, nombre: str) -> int:
        """
        Devuelve el id correspondiente al usuario.
        Devuelve 0 en caso de no encontrar al usuario.
        """
        for id_usuario, valores in self._datos_usuarios.items():
            if nombre == valores[0]:
                return id_usuario
        return 0
    

    def buscar_id_tipo_por_nombre(self, nombre_tipo: str) -> int:
        for id_tipo, valores in self._datos_tipo_usuario.items():
            if nombre_tipo in valores:
                return id_tipo
           
            
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
            
    
    def agregar_nuevo_usuario(self, nombre: str, passwd: str, tipo: str) -> bool:
        id_usuario = int(list(self._datos_usuarios.keys())[-1]) + 1

        for valores in self._datos_usuarios.values():
            if nombre not in valores:
                hashed_passwd = self.convertir_passwd(passwd)
                id_tipo = self.buscar_id_tipo_por_nombre(tipo)
                self._datos_usuarios[id_usuario] = [nombre, hashed_passwd, id_tipo]
                return True
        return False
    
        
    def eliminar_usuario_existente(self, usuario: str) -> bool:
        for id_usuario, valores in self._datos_usuarios.items():
            if usuario == valores[0]:
                self._datos_usuarios.pop(id_usuario, None)
                return True
        return False
    

    def modificar_nombre_usuario(self, nombre_anterior: str, nuevo_nombre: str) -> bool:
        for id_usuario, valores in self._datos_usuarios.items():
            if nombre_anterior == valores[0] and nuevo_nombre != valores[0]:
                self._datos_usuarios[id_usuario][0] = nuevo_nombre
                return True
        return False
    

    def modificar_passwd_usuario(self, usuario: str, nuevo_passwd: str) -> bool:
        for id_usuario, valores in self._datos_usuarios.items():
            if usuario == valores[0]:
                self._datos_usuarios[id_usuario][1] = self.convertir_passwd(nuevo_passwd)
                return True
        return False
    

if __name__ == "__main__":
    a = Usuarios()
    print(a._datos_imagenes)