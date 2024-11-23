import json

def obtener_info_db(file: str = "./db/db_info.json") -> str:
    with open(file, 'r') as archivo:
        datos = json.load(archivo)

        datos_usuarios = datos["usuarios"]

        info = ""

        for clave, valor in datos_usuarios.items():
            info += f"{clave}={valor}"
            info += " "

        return info


print(obtener_info_db())