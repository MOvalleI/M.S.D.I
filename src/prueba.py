from datetime import datetime

class NodoAccion:
    def __init__(self, fecha_hora, accion):
        self.fecha_hora = fecha_hora  # Timestamp de la acción
        self.accion = accion          # Acción realizada
        self.izquierda = None         # Nodo a la izquierda (acciones más antiguas)
        self.derecha = None           # Nodo a la derecha (acciones más recientes)

class ArbolAcciones:
    def __init__(self):
        self.raiz = None

    def agregar_accion(self, fecha_hora, accion):
        nuevo_nodo = NodoAccion(fecha_hora, accion)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._agregar_recursivo(self.raiz, nuevo_nodo)

    def _agregar_recursivo(self, nodo_actual, nuevo_nodo):
        if nuevo_nodo.fecha_hora < nodo_actual.fecha_hora:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nuevo_nodo
            else:
                self._agregar_recursivo(nodo_actual.izquierda, nuevo_nodo)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nuevo_nodo
            else:
                self._agregar_recursivo(nodo_actual.derecha, nuevo_nodo)

    def recorrer_inorden(self):
        acciones = []
        self._recorrer_inorden_recursivo(self.raiz, acciones)
        return acciones

    def _recorrer_inorden_recursivo(self, nodo, acciones):
        if nodo:
            self._recorrer_inorden_recursivo(nodo.izquierda, acciones)
            acciones.append((nodo.fecha_hora, nodo.accion))
            self._recorrer_inorden_recursivo(nodo.derecha, acciones)

# Crear el árbol
historial = ArbolAcciones()

# Agregar acciones
historial.agregar_accion(datetime(2024, 11, 29, 10, 30), "Ver Datos")
historial.agregar_accion(datetime(2024, 11, 29, 10, 45), "Modificar Datos")
historial.agregar_accion(datetime(2024, 11, 29, 11, 00), "Añadir Datos")
historial.agregar_accion(datetime(2024, 11, 29, 11, 15), "Eliminar Datos")

# Mostrar el historial ordenado
acciones_ordenadas = historial.recorrer_inorden()
for fecha_hora, accion in acciones_ordenadas:
    print(f"{fecha_hora}: {accion}")
