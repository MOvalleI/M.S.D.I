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
