import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msbox
import gui.Ventanas as ven
import gui.Inicio as i
import gui.Componentes as comp

class Agregar(ven.VentanaPrincipal):
    def __init__(self, datos: dict=None):
        super().__init__(titulo_ventana="Añadir Productos", titulo="Añadir\nProductos")

        self.datos = datos
        self.datos_productos = self.datos["Inventario"]

        self.resizable(False, False)

        self.configurar_ventana()
        self.protocol("WM_DELETE_WINDOW", self.volver)

        # Eventos de Teclado
        self.bind('<Escape>', lambda event: self.volver)

    def configurar_ventana(self):
        ancho = 460
        alto = 625

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.agregar_titulo()

        self.panel_data = tk.Frame(self, background=self.bgcolor)
        self.panel_data.pack(expand=True, fill="both")

        self.agregar_fila_1()
        self.agregar_fila_2()
        self.agregar_fila_3()
        self.agregar_fila_4()

        self.agregar_botones_opciones()

        self.centrar_ventana()


    def agregar_fila_1(self):
        # Nombre y Clase
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Nombre
        panel_nombre = tk.Frame(panel, background=self.bgcolor)
        panel_nombre.pack(expand=True, fill="both", side="left")

        label_nombre = tk.Label(panel_nombre, text="Nombre:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label_nombre.pack(expand=True)

        self.nombre_entry = tk.Entry(panel_nombre, width=25)
        self.nombre_entry.pack(expand=True)

        self.label_error_nombre = tk.Label(panel_nombre, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_nombre.pack(expand=True)

        # Clase
        panel_clase = tk.Frame(panel, background=self.bgcolor)
        panel_clase.pack(expand=True, fill="both", side="left")

        label_clase = tk.Label(panel_clase, text="Clase:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label_clase.pack(expand=True)

        values = [x[1] for x in self.datos_productos.simple_complete_query("Clases")]

        self.clase_list = ttk.Combobox(panel_clase, values=values)
        self.clase_list.config(state="readonly")
        self.clase_list.current(0)
        self.clase_list.pack(expand=True)

    
    def agregar_fila_2(self):
        # Lugar de Compra y Unidad
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Lugar de Compra
        panel_lugar = tk.Frame(panel, background=self.bgcolor)
        panel_lugar.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_lugar, text="Lugar de Compra:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = [x[1] for x in self.datos_productos.simple_complete_query("Lugares")]

        self.lugar_compra_list = ttk.Combobox(panel_lugar, values=values)
        self.lugar_compra_list.config(state="readonly")
        self.lugar_compra_list.current(0)
        self.lugar_compra_list.pack(expand=True)

        # Unidad
        panel_unidad = tk.Frame(panel, background=self.bgcolor)
        panel_unidad.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_unidad, text="Unidad:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = [x[1] for x in self.datos_productos.simple_complete_query("Unidades")]

        self.unidad_list = ttk.Combobox(panel_unidad, values=values)
        self.unidad_list.config(state="readonly")
        self.unidad_list.current(0)
        self.unidad_list.pack(expand=True)


    def agregar_fila_3(self):
        # Precio y Stock Minimo
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Precio
        panel_precio = tk.Frame(panel, background=self.bgcolor)
        panel_precio.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_precio, text="Precio Unitario:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.precio_entry = comp.CampoTexto(panel_precio, tipo="int")
        self.precio_entry.config(width=15)
        self.precio_entry.pack()

        self.label_error_precio = tk.Label(panel_precio, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_precio.pack(expand=True)

        # Stock Mínimo
        panel_stock_min = tk.Frame(panel, background=self.bgcolor)
        panel_stock_min.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_min, text="Stock Mínimo:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_min_entry = comp.CampoTexto(panel_stock_min, tipo="int")
        self.stock_min_entry.config(width=15)
        self.stock_min_entry.pack()

        self.label_error_min = tk.Label(panel_stock_min, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_min.pack(expand=True)

    
    def agregar_fila_4(self):
        # Stock Deseado y Disponible
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Stock Deseado
        panel_stock_deseado = tk.Frame(panel, background=self.bgcolor)
        panel_stock_deseado.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_deseado, text="Stock Deseado:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_max_entry = comp.CampoTexto(panel_stock_deseado, tipo="int")
        self.stock_max_entry.config(width=15)
        self.stock_max_entry.pack()

        self.label_error_max = tk.Label(panel_stock_deseado, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_max.pack(expand=True)

        # Stock Disponible
        panel_stock_disponible = tk.Frame(panel, background=self.bgcolor)
        panel_stock_disponible.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_disponible, text="Stock Actual:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_actual_entry = comp.CampoTexto(panel_stock_disponible, tipo="int")
        self.stock_actual_entry.config(width=15)
        self.stock_actual_entry.pack()

        self.label_error_stock = tk.Label(panel_stock_disponible, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_stock.pack(expand=True)


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=15, fill="both")

        self.b_agregar = comp.Boton(panel, text="Agregar\nProducto", command=self.agregar_producto)
        self.b_agregar.pack(expand=True, side="left")

        self.b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        self.b_volver.pack(expand=True, side="left")


    def agregar_producto(self):
        is_valid = 0

        if self.nombre_entry.get() == "":
            self.label_error_nombre.config(text="* Campo Obligatorio")
        else:
            self.label_error_nombre.config(text="")
            is_valid+=1

        if self.precio_entry.get() == "":
            self.label_error_precio.config(text="* Campo Obligatorio")
        else:
            self.label_error_precio.config(text="")
            is_valid+=1

        if self.stock_min_entry.get() == "":
            self.label_error_min.config(text="* Campo Obligatorio")
        else:
            self.label_error_min.config(text="")
            is_valid+=1

        if self.stock_max_entry.get() == "":
            self.label_error_max.config(text="* Campo Obligatorio")
        else:
            self.label_error_max.config(text="")
            is_valid+=1

        if self.stock_actual_entry.get() == "":
            self.label_error_stock.config(text="* Campo Obligatorio")
        else:
            self.label_error_stock.config(text="")
            is_valid+=1

        if is_valid == 5:
            if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Agregar\neste Produto?", titulo_ventana="Agregar Producto").obtener_respuesta():
                pk = self.datos_productos.obtener_pk("Productos", "id_producto")
                id_clase = self.datos_productos.obtener_id_por_nombre("Clases", "ID_clase", "nombre_clase", self.clase_list.get())
                id_lugar = self.datos_productos.obtener_id_por_nombre("Lugares", "id_lugar", "nombre_lugar", self.lugar_compra_list.get())
                id_unidad = self.datos_productos.obtener_id_por_nombre("Unidades", "id_unidad", "nombre_unidad", self.unidad_list.get())
                if self.datos_productos.agregar_producto(pk, self.nombre_entry.get(), id_clase, id_lugar, id_unidad, self.precio_entry.get(), self.stock_min_entry.get(), self.stock_max_entry.get()): 
                    if self.datos_productos.insertar_stock_local(pk, self.stock_actual_entry.get()):
                        ven.VentanaAvisoTL(self, texto="¡Producto agregado con Éxito!", titulo_ventana="Agregar Producto")
                        self.datos["Usuario_Logueado"]["Registro"].insertar("Agregar", "Productos")
                        self.volver()
                    else:
                        ven.VentanaAvisoTL(self, texto="No se pudo agregar el Producto.", titulo_ventana="Error")
                else:
                    ven.VentanaAvisoTL(self, texto="No se pudo agregar el Producto.", titulo_ventana="Error")

                        




    def volver(self, e=None):
        self.destroy()
        i.Inicio(datos=self.datos)

    


if __name__ == "__main__":
    root = Agregar()
    root.mainloop()
