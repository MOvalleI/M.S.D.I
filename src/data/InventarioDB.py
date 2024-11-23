import sqlite3
import psycopg

DATABASE = "./db/inventario.db"

DB_INFO = """
    host = localhost
    user = postgres
    password = admin
    dbname = r4d
"""

class Node:
    def __init__(self, clave, dato):
        self.id = clave
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

    def __str__(self):
        izquierdo_id = self.izquierdo.id if self.izquierdo else "None"
        derecho_id = self.derecho.id if self.derecho else "None"
        return f"""        Clave: {self.id}
        Datos: {self.dato}
        Izquierdo: {izquierdo_id}
        Derecho: {derecho_id}"""

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar_nodo(self, clave, dato):
        if self.raiz is None:
            self.raiz = Node(clave, dato)
        else:
            self._insertar_recursivo(self.raiz, clave, dato)

    def items(self):
        return self._items_recursivo(self.raiz)        

    def _insertar_recursivo(self, node, clave, dato):
        if clave < node.id:
            if node.izquierdo is None:
                node.izquierdo = Node(clave, dato)
            else:
                self._insertar_recursivo(node.izquierdo, clave, dato)
        else:
            if node.derecho is None:
                node.derecho = Node(clave, dato)
            else:
                self._insertar_recursivo(node.derecho, clave, dato)

    def buscar_ultimo_id(self):
        return self._buscar_ultimo_id_recursivo(self.raiz)

    def _buscar_ultimo_id_recursivo(self, node):
        if node.derecho is None:
            return node
        return self._buscar_ultimo_id_recursivo(node.derecho)

    def buscar_por_id(self, clave):
        return self._buscar_por_id_recursivo(self.raiz, clave)
        
    def _buscar_por_id_recursivo(self, node, clave):
        if node is None or node.id == clave:
            return node
        if clave < node.id:
            return self._buscar_por_id_recursivo(node.izquierdo, clave)
        return self._buscar_por_id_recursivo(node.derecho, clave)

    def _calcular_cantidad(self, node):
        if node is None:
            return 0
        return 1 + self._calcular_cantidad(node.izquierdo) + self._calcular_cantidad(node.derecho)

    def _items_recursivo(self, node):
        if node is None:
            return []
        return self._items_recursivo(node.izquierdo) + [(node.id,) + tuple(node.dato)] + self._items_recursivo(node.derecho)
 
    def __len__(self):
        return self._calcular_cantidad(self.raiz)

    def __str__(self):
        return str(self.raiz)

class InventarioDB:
    def __init__(self):
        self.conn = psycopg.connect(DB_INFO)
        self.cursor = self.conn.cursor()
        self.inicializar_estructuras()

    def inicializar_estructuras(self):
        self.Lugares = self._crear_arbol("Lugares","ID_lugar") #arbol
        self.Unidades = self._crear_arbol("Unidades","ID_unidad") #arbol
        self.Clases = self._crear_arbol("Clases","ID_clase") #arbol
        self.Categoria = self._crear_arbol("Categorias","ID_categoria") #arbol
        self.Tamaños = self._crear_arbol("Tamaños","ID_tamaño") #arbol
        self.Ingredientes = self._cargar_muchos_a_muchos("Ingredientes") #lista de diccionarios
        self.ContenidoVenta = self._cargar_muchos_a_muchos("ContenidoVenta") #lista de diccionarios
        self.Productos = self._cargar_tabla("Productos") #diccionario
        self.Menu = self._cargar_tabla("Menu") #diccionario
        self.Ventas = self._cargar_tabla("Ventas") #diccionario

   

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

    def _cargar_tabla(self, nombre_tabla):
        self.cursor.execute(f'SELECT * FROM {nombre_tabla};')
        registros = self.cursor.fetchall()
        diccionario = {}
        for registro in registros:
            id_valor = registro[0]
            valores = list(registro[1:])
            diccionario[id_valor] = valores
        return diccionario
        
    def _cargar_muchos_a_muchos(self, nombre_tabla):
        self.cursor.execute(f'SELECT * FROM {nombre_tabla};')
        registros = self.cursor.fetchall()
        relacion_izquierda = {}
        relacion_derecha = {}
        for registro in registros:
            relacion_izquierda.setdefault(registro[0], []).append(registro[1:])
            relacion_derecha.setdefault(registro[1], []).append(registro[0])
        return [relacion_izquierda, relacion_derecha]
            

    def _balancear_lista(self, lista_ordenada):
        if not lista_ordenada:
            return []
        
        medio = len(lista_ordenada) // 2
        nodo_central = [lista_ordenada[medio]]
        
        return nodo_central + self._balancear_lista(lista_ordenada[:medio]) + self._balancear_lista(lista_ordenada[medio + 1:])

    def _crear_arbol(self, nombre_tabla, columna_orden):
        self.cursor.execute(f'SELECT * FROM {nombre_tabla} ORDER BY {columna_orden};')
        registros = self.cursor.fetchall()
        lista_balanceada = self._balancear_lista(registros)
        arbol = ArbolBinarioBusqueda()
        for registro in lista_balanceada:
            id_valor = registro[0]
            valores = list(registro[1:])
            arbol.insertar_nodo(id_valor, valores)
        return arbol

    def __str__(self):
        return f"""        Lugares(arbol): {len(self.Lugares)}
        Unidades(arbol): {len(self.Unidades)}
        Clases(arbol): {len(self.Clases)}
        Categoria(arbol): {len(self.Categoria)}
        Tamaños(arbol): {len(self.Tamaños)}
        Ingredientes(lista de diccionarios): {len(self.Ingredientes[0])} & {len(self.Ingredientes[1])}
        ContenidoVenta(lista de diccionarios): {len(self.ContenidoVenta[0])} & {len(self.ContenidoVenta[1])}
        Productos(diccionario): {len(self.Productos)}
        Menu(diccionario): {len(self.Menu)}
        Ventas(diccionario): {len(self.Ventas)}"""
        


            
if __name__ == "__main__":
    a = InventarioDB()
    print(a.inner_join_menu(where = ["C.nombre_categoria = 'bebidas'", 'M.precio > 700']))
    
