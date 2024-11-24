import tkinter as tk
import tkinter.ttk as ttk
import gui.Ventanas as ven
import gui.Inicio as i
import data.BuscadorDB as bi
import gui.Componentes as comp

class Eliminar(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo_ventana="Eliminar Producto", titulo="Eliminar\nProducto")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.producto_seleccionado = None

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.protocol("WM_DELETE_WINDOW", self.volver)
        self.bind('<Escape>', lambda event: self.volver)

        self.resizable(False, False)

        self.agregar_titulo()
        self.agregar_tabla_productos()
        self.agregar_botones_opciones()

        self.centrar_ventana()

        
    def agregar_lista_productos(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Selecciona un Producto:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label.pack(expand=True)

        values = ["(no seleccionado)"]

        for id_prod in self.datos_inventario.Productos.keys():
                nombre = self.datos_inventario.Productos[id_prod][0]
                values.append(nombre)

        self.prod_list = ttk.Combobox(panel, values=values)
        self.prod_list.current(0)
        self.prod_list.pack(expand=True)
        

    def agregar_tabla_productos(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=10)

        label = tk.Label(panel, text="Busca un Producto por Nombre:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label.pack(side="left")

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.pack(side="left")

        encabezados = ["Nombre", "Clase", "Lugar de Compra", "Unidad", "Precio", "Stock Mínimo", "Stock Deseado", "Stock Disponible"]

        self.tabla = comp.CustomTreeview(self)
        self.tabla.create_table(head=encabezados, width=100)

        self.tabla.pack(expand=True)


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_eliminar = comp.Boton(panel, text="Eliminar", command=self.confirmar_eliminar)
        #self.b_eliminar.deshabilitar_boton()
        self.b_eliminar.pack(expand=True, side="left")

        self.b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        self.b_volver.pack(expand=True, side="left")


    def confirmar_eliminar(self):
        op = ven.VentanaConfirmacion(self, texto="¿Está seguro de eliminar\n este producto?")
        if op.obtener_respuesta():
            print("Objeto Eliminado")
        else:
            print("El objeto no se elimino")


    def volver(self, e=None):
        self.destroy()
        i.Inicio(datos=self.datos)
