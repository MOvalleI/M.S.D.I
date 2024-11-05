class BuscadorDB:
    @staticmethod
    def buscar_categoria_por_id(arbol_categoria, id_categoria: int) -> str:
        categoria = arbol_categoria.buscar_por_id(id_categoria)
        if categoria is not None:
            return categoria.dato[0]
        return None  
    
    @staticmethod
    def buscar_tamano_por_id(arbol_tamano, id_tamano: int) -> str:
        tamaño = arbol_tamano.buscar_por_id(id_tamano)
        if tamaño is not None:
            return tamaño.dato[0]
        return None    
    
    @staticmethod
    def buscar_unidad_por_id(arbol_unidades, id_unidad: int) -> str:
        unidad = arbol_unidades.buscar_por_id(id_unidad)
        if unidad is not None:
            return unidad.dato[0]
        return None  

    