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
        query = """SELECT M.ID_menu, M.nombre_menu, M.precio, C.nombre_categoria, t.nombre_tamaño FROM Menu M 
                    INNER JOIN Categorias C ON M.ID_categoria = C.ID_categoria 
                    INNER JOIN Tamaños T ON M.ID_tamaño = T.ID_tamaño
                    INNER JOIN MenuLocales ML ON ML.id_menu = M.id_menu """

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
    

    def obtener_ventas(self, local: int):
        query = f"EXEC ventas_local {local}"
        return self.query_execute(query)
    

    def obtener_contenido_venta(self, id_venta, local: int):
        query = f"EXEC contenido_venta_local {id_venta}, {local}"
        return self.query_execute(query)
    

    def generar_query_con_filtros(self, operador_precio: str, precio: int, 
                               fecha: str, id_local: int):
        # Lista para guardar las condiciones de filtro WHERE
        condiciones = []

        condiciones.append(f"WHERE ven.ID_local = {id_local}")
        
        # Comprobar si el segundo operador de fecha es válido
        if fecha is not None:
            condiciones.append(f"ven.fecha >= '{fecha}'")
        
        # Generar la parte de WHERE
        where_clause = " AND ".join(condiciones)

        print(where_clause)
        
        # Generar el query
        query = f"""
            SELECT ven.ID_venta, ven.fecha, SUM(men.precio * cv.cantidad) as precio
            FROM Ventas AS ven
            INNER JOIN ContenidoVenta AS cv ON cv.ID_venta = ven.ID_venta
            INNER JOIN Menu AS men ON men.ID_menu = cv.ID_menu
            {where_clause}
            GROUP BY ven.ID_venta, ven.fecha
        """
        
        # Añadir la cláusula HAVING si se está filtrando por precio
        if operador_precio and precio is not None:
            query += f" HAVING SUM(men.precio * cv.cantidad) {operador_precio} {precio};"

        # Ejecutar el query
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def query_execute(self, query):
        self.cursor.execute(query)

        return self.cursor.fetchall()
    

    def obtener_pk(self, tabla, columna) -> int:
        query = f"""SELECT TOP 1 {columna} FROM {tabla}
                    ORDER BY {columna} DESC"""
        
        self.cursor.execute(query)
        datos = self.cursor.fetchone()
        return (int(datos[0])+1)
    
    def insertar_venta(self, id_venta, id_local):
        query = "INSERT INTO Ventas(ID_venta, ID_local) VALUES (?, ?)"
        self.cursor.execute(query, (id_venta, id_local))
        self.conn.commit()


    def insertar_contenido_venta(self, id_venta, menu: list):
        query = "INSERT INTO ContenidoVenta VALUES (?, ?, ?)"

        datos_para_insertar = [(id_venta, datos_menu[0], datos_menu[1]) for datos_menu in menu]
        self.cursor.executemany(query, datos_para_insertar)
        self.conn.commit()

    
    def obtener_ventas_dia(self, local: int):
        query = f"EXEC SP_Ventas_hoy_por_local {local}"
        return self.query_execute(query)
    

    def obtener_total_vendido_dia(self, local: int):
        query = f"SELECT dbo.SF_total_vendido_hoy_por_local({local})"
        return self.query_execute(query)
    

    def obtener_columna_tablas(self, tabla, columna):
        query = f"SELECT {columna} FROM {tabla}"
        return self.query_execute(query)
    

    def obtener_id_por_nombre(self, tabla, columna1, columna2, nombre):
        query = f"SELECT {columna1} FROM {tabla} WHERE {columna2} = ?"
        self.cursor.execute(query, (nombre,))
        res = self.cursor.fetchone()

        return int(res[0])
    

    def existe_menu(self, nombre_menu):
        query = f"SELECT dbo.existe_menu(?)"
        self.cursor.execute(query, (nombre_menu,))
        res = self.cursor.fetchone()

        return int(res[0])
    

    def obtener_ingredientes(self, nombre: str):
        query = f"EXEC obtener_ingredientes ?"
        self.cursor.execute(query, (nombre,))
        return self.cursor.fetchall()
    
    def obtener_id_ingredientes_por_nombre(self, nombre: str):
        query = f"SELECT ID_producto FROM Productos WHERE nombre_producto = ?"
        self.cursor.execute(query, (nombre,))
        return self.cursor.fetchone()
    

    def agregar_menu(self, id, nombre, precio, id_categoria, id_tamaño, ingredientes: list):
        query_menu = "INSERT INTO Menu VALUES (?,?,?,?,?)"
        self.cursor.execute(query_menu, (id,nombre,precio,id_categoria,id_tamaño))

        lista_transformada = [(int(id), int(item)) for item in ingredientes]
        query_ingredientes = "INSERT INTO Ingredientes VALUES (?,?)"
        self.cursor.executemany(query_ingredientes, lista_transformada)

        self.conn.commit()

    
    def eliminar_menu(self, id_menu):
        query = "DELETE FROM Menu WHERE id_menu = ?"
        self.cursor.execute(query, (id_menu,))
        self.conn.commit()


    def actualizar_menu(self, id, nombre, precio, id_categoria, id_tamaño):
        query = """UPDATE Menu 
                SET nombre_menu = ?,
                    precio = ?,
                    id_categoria = ?,
                    id_tamaño = ?
                WHERE id_menu = ?"""
        
        self.cursor.execute(query, (nombre, precio, id_categoria, id_tamaño, id))
        self.conn.commit()


        
    def query_insert(self, query):
        self.cursor.execute(query)
        self.conn.commit()