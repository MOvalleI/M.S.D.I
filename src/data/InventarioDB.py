import pyodbc
import json

def obtener_info_db(file: str = "./db/db_info.json") -> str:
    with open(file, 'r') as archivo:
        datos = json.load(archivo)

        datos_usuarios = datos["inventario"]

        info = []

        for clave, valor in datos_usuarios.items():
            info.append(valor)

        return f"DRIVER={{{info[0]}}}; SERVER={info[1]}; DATABASE={info[4]}; UID={info[2]}; PWD={info[3]}"



class InventarioDB:
    def __init__(self):
        self.conn = pyodbc.connect(obtener_info_db())
        self.cursor = self.conn.cursor()   

    def cerrar(self):
        self.conn.close()

    def inner_join_menu(self, like = None, order = "ID_Menu", where = None):
        query = "SELECT M.ID_menu, M.nombre_menu, M.precio, C.nombre_categoria, t.nombre_tamaño FROM Menu M INNER JOIN Categorias C ON M.ID_categoria = C.ID_categoria INNER JOIN Tamaños T ON M.ID_tamaño = T.ID_tamaño "

        query_list = []

        if like:
            query_list.append("M.nombre_menu LIKE ?")

        if where:
            query_list += where

        if like or where:
            query += " WHERE " + " AND ".join(query_list)
        
        ordering_options = {"ID_categoria": "C.nombre_categoria","ID_tamaño": "T.nombre_tamaño"}
        tabla = ordering_options.get(order, (f"M.{order}"))
        query += f" ORDER BY {tabla};"

        if like:
            self.cursor.execute(query, (f"%{like}%",))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def simple_complete_query(self, table):
        query = f"SELECT * FROM {table}"
        
        return self.query_execute(query)

    def inner_join_menu_to_ingredient(self, ID_menu):
        query = f"SELECT p.ID_producto, p.nombre_producto FROM Productos as p INNER JOIN Ingredientes as i ON p.ID_producto = i.ID_producto WHERE ID_menu = {ID_menu}"

        return self.query_execute(query)

    def inner_join_productos(self):
        query = f"""SELECT p.ID_producto, p.nombre_producto, p.stock_minimo, p.stock_maximo, pl.stock_disponible
        FROM Productos as p INNER JOIN ProductosLocales as pl
        ON p.ID_producto = pl.ID_producto"""

        return self.query_execute(query)
    
    def inner_join_menu_venta(self, like = None, order = "ID_Menu", where = None):
        query = "SELECT M.ID_menu, M.nombre_menu, M.precio FROM Menu AS M"

        query_list = []

        if like:
            query_list.append("M.nombre_menu LIKE ?")

        if where:
            query_list += where

        if like or where:
            query += " WHERE " + " AND ".join(query_list)

        if like:
            self.cursor.execute(query, (f"%{like}%",))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def query_execute(self, query):
        self.cursor.execute(query)

        return self.cursor.fetchall()

        
            