import tkinter as tk
import tkinter.ttk as ttk
import gui.Ventanas as ven
import gui.Inicio as i
import data.BuscadorDB as bi

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

        self.agregar_titulo()
        self.agregar_lista_productos()
        self.agregar_datos_productos()
        self.agregar_botones_opciones()

        
    def agregar_lista_productos(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        label = tk.Label(panel, text="Selecciona un Producto:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label.pack(expand=True)

        values = []

        for id_menu in self.datos_inventario.Menu.keys():
                nombre = self.datos_inventario.Menu[id_menu][0]
                values.append(nombre)

        self.prod_list = ttk.Combobox(panel, values=values)
        self.prod_list.pack(expand=True)
        

    def agregar_datos_productos(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        # Titulos

        titulo_nombre = tk.Label(panel, text="Nombre: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_clase = tk.Label(panel, text="Clase: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_lugar = tk.Label(panel, text="Lugar de Compra: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_unidad = tk.Label(panel, text="Unidad: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_precio = tk.Label(panel, text="Precio: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_stock_min = tk.Label(panel, text="Stock Minimo: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_stock_max = tk.Label(panel, text="Stock Deseado: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        titulo_stock = tk.Label(panel, text="Stock Disponible: ", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))

        titulo_nombre.grid(row=0, column=0, sticky='w')
        titulo_clase.grid(row=1, column=0, sticky='w')
        titulo_lugar.grid(row=2, column=0, sticky='w')
        titulo_unidad.grid(row=3, column=0, sticky='w')
        titulo_precio.grid(row=4, column=0, sticky='w')
        titulo_stock_min.grid(row=5, column=0, sticky='w')
        titulo_stock_max.grid(row=6, column=0, sticky='w')
        titulo_stock.grid(row=7, column=0, sticky='w')
    
        # Datos
        
        self.dato_nombre = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_clase = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_lugar = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_unidad = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_precio = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_stock_min = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_stock_max = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.dato_stock = tk.Label(panel, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))

        self.dato_nombre.grid(row=0, column=1, sticky='e')
        self.dato_clase.grid(row=1, column=1, sticky='e')
        self.dato_lugar.grid(row=2, column=1, sticky='e')
        self.dato_unidad.grid(row=3, column=1, sticky='e')
        self.dato_precio.grid(row=4, column=1, sticky='e')
        self.dato_stock_min.grid(row=5, column=1, sticky='e')
        self.dato_stock_max.grid(row=6, column=1, sticky='e')
        self.dato_stock.grid(row=7, column=1, sticky='e')


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        self.b_eliminar = tk.Button(panel, text="Eliminar", anchor="center", state="disabled", command=None)
        self.b_eliminar.pack(expand=True, side="left")

        self.b_volver = tk.Button(panel, text="Volver", anchor="center", command=self.volver)
        self.b_volver.pack(expand=True, side="left")




    def volver(self, e=None):
        self.destroy()
        i.Inicio(datos=self.datos)