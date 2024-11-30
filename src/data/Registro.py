"Clase que almacena tanto el inicio como el cierre de sesión de un usuario"
class Sesion:
    def __init__(self):
        self.fecha1 = None
        self.hora1 = None
        self.fecha2 = None
        self.hora2 = None

    def registrar_inicio_sesion(self, fecha, hora):
        self.fecha1 = fecha
        self.hora1 = hora

    def registrar_cierre_sesion(self, fecha, hora):
        self.fecha2 = fecha
        self.hora2 = hora

    def obtener_datos(self):
        # Devuelve los datos en una tupla o lista
        return [self.fecha1, self.hora1, self.fecha2, self.hora2]
    

"Almacena la acción realizada por el usuario dentro del programa"
class Accion:
    def __init__(self, accion, fecha, hora, objeto):
        self.accion = accion
        self.fecha = fecha
        self.hora = hora
        self.objeto = objeto
        self.izquierda = None
        self.derecha = None


class ArbolAcciones:
    def __init__(self):
        self.raiz = None

    def insertar(self, accion, fecha, hora, objeto):
        nuevo_nodo = Accion(accion, fecha, hora, objeto)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, actual, nuevo_nodo):
        # Aquí puedes personalizar la lógica de inserción
        # Por ejemplo, usar la fecha como criterio de ordenamiento
        if nuevo_nodo.fecha < actual.fecha:
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
            else:
                self._insertar_recursivo(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo_nodo
            else:
                self._insertar_recursivo(actual.derecha, nuevo_nodo)

    def recorrer_inorden(self):
        # Devuelve los datos almacenados en orden (lista de tuplas)
        resultado = []
        self._recorrer_inorden_recursivo(self.raiz, resultado)
        return resultado

    def _recorrer_inorden_recursivo(self, actual, resultado):
        if actual is not None:
            self._recorrer_inorden_recursivo(actual.izquierda, resultado)
            resultado.append((actual.accion, actual.fecha, actual.hora, actual.objeto))
            self._recorrer_inorden_recursivo(actual.derecha, resultado)
