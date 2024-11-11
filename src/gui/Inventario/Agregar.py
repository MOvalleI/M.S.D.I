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

        # Textos de error
        self.label_error_nombre = None
        self.label_error_precio = None
        self.label_error_min = None
        self.label_error_max = None
        self.label_error_stock = None

        self.resizable(False, False)

        self.configurar_ventana()
        self.protocol("WM_DELETE_WINDOW", self.volver)

        # Eventos de Teclado
        self.bind('<Escape>', lambda event: self.volver)

    def configurar_ventana(self):
        self.agregar_titulo()

        self.panel_data = tk.Frame(self, background=self.bgcolor)
        self.panel_data.pack(expand=True, fill="both")

        self.agregar_entry_nombre()
        self.agregar_lista_clase()
        self.agregar_lista_lugar_compra()
        self.agregar_lista_unidad()
        self.agregar_entry_precio()
        self.agregar_entry_stock_min()
        self.agregar_entry_stock_deseado()
        self.agregar_entry_stock_actual()
        self.agregar_botones_opciones()


    def agregar_entry_nombre(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=0, column=0, pady=35, padx=5)

        label = tk.Label(panel, text="Nombre:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.nombre_entry = tk.Entry(panel, width=25)
        self.nombre_entry.pack(expand=True)

    
    def agregar_lista_clase(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=0, column=1, pady=35, padx=5)

        label = tk.Label(panel, text="Clase:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = ["clase1","clase2","clase3"]

        self.clase_list = ttk.Combobox(panel, values=values)
        self.clase_list.pack(expand=True)

    
    def agregar_lista_lugar_compra(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=1, column=0, pady=35, padx=5)

        label = tk.Label(panel, text="Lugar de Compra:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = ["clase1","clase2","clase3"]

        self.lugar_compra_list = ttk.Combobox(panel, values=values)
        self.lugar_compra_list.pack(expand=True)


    def agregar_lista_unidad(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=1, column=1, pady=35, padx=5)

        label = tk.Label(panel, text="Unidad:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = ["clase1","clase2","clase3"]

        self.unidad_list = ttk.Combobox(panel, values=values)
        self.unidad_list.pack(expand=True)

    
    def agregar_entry_precio(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=2, column=0, pady=35, padx=5)

        label = tk.Label(panel, text="Precio:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.precio_entry = comp.CampoTexto(panel, tipo="int")
        self.precio_entry.config(width=15)
        self.precio_entry.pack()


    def agregar_entry_stock_min(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=2, column=1, pady=35, padx=5)

        label = tk.Label(panel, text="Stock Mínimo:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_min_entry = comp.CampoTexto(panel, tipo="int")
        self.stock_min_entry.config(width=15)
        self.stock_min_entry.pack()

    
    def agregar_entry_stock_deseado(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=3, column=0, pady=35, padx=5)

        label = tk.Label(panel, text="Stock Deseado:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_max_entry = comp.CampoTexto(panel, tipo="int")
        self.stock_max_entry.config(width=15)
        self.stock_max_entry.pack()


    def agregar_entry_stock_actual(self):
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.grid(row=3, column=1, pady=35, padx=5)

        label = tk.Label(panel, text="Stock Actual:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_actual_entry = comp.CampoTexto(panel, tipo="int")
        self.stock_actual_entry.config(width=15)
        self.stock_actual_entry.pack()


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=35, fill="both")

        self.b_agregar = comp.Boton(panel, text="Agregar\nProducto", command=None)
        self.b_agregar.pack(expand=True, side="left")

        self.b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        self.b_volver.pack(expand=True, side="left")


    def volver(self, e=None):
        self.destroy()
        i.Inicio(datos=self.datos)

    

    # def aplicar_cambios(self) -> None:
    #     # Va a parecer una tonteria, pero no voy a reescribir todo para ajustar esto
    #     # No me importa si hay mas de 50 lineas en este metodo
    #     if self.label_error_nombre:
    #         self.label_error_nombre.grid_forget()
    #         self.label_error_nombre = None

    #     if self.label_error_precio:
    #         self.label_error_precio.grid_forget()
    #         self.label_error_precio = None

    #     if self.label_error_max:
    #         self.label_error_max.grid_forget()
    #         self.label_error_max = None

    #     if self.label_error_min:
    #         self.label_error_min.grid_forget()
    #         self.label_error_min = None

    #     if self.label_error_stock:
    #         self.label_error_stock.grid_forget()
    #         self.label_error_stock = None

    #     if self.frame1.comprobar_vacio():
    #         self.label_error_nombre = tk.Label(self.frame1, text="Campo obligatorio*", fg="red")
    #         self.label_error_nombre.grid(row=2, column=0, pady=10)

    #     if self.frame5.comprobar_vacio():
    #         self.label_error_precio = tk.Label(self.frame5, text="Campo obligatorio*", fg="red")
    #         self.label_error_precio.grid(row=2, column=0, pady=10)

    #     if self.frame6.comprobar_vacio():
    #         self.label_error_max = tk.Label(self.frame6, text="Campo obligatorio*", fg="red")
    #         self.label_error_max.grid(row=2, column=0, pady=10)

    #     if self.frame7.comprobar_vacio():
    #         self.label_error_min = tk.Label(self.frame7, text="Campo obligatorio*", fg="red")
    #         self.label_error_min.grid(row=2, column=0, pady=10)

    #     if self.frame8.comprobar_vacio():
    #         self.label_error_stock = tk.Label(self.frame8, text="Campo obligatorio*", fg="red")
    #         self.label_error_stock.grid(row=2, column=0, pady=10)

    #     if not self.frame1.comprobar_vacio() and not self.frame5.comprobar_vacio() and not self.frame6.comprobar_vacio() and not self.frame7.comprobar_vacio() and not self.frame8.comprobar_vacio():
    #         exists = CONSULTAS.get_specific_data(table="Inventario", column='nombre', name=self.frame1.get_entry(), column_where='nombre')
    #         if exists is None and int(self.frame6.get_entry())<int(self.frame7.get_entry()):
    #             message = msbox.askquestion("¿Aplicar Cambios?", "¿Desea ingresar los datos?")
    #             if message=="yes":
    #                 self.insertar_datos()
    #                 msbox.showinfo("Datos Ingresados", "¡Se han ingresado los datos correctamente!")
    #                 self.cerrar_ventana()
    #         else:
    #             if exists is not None:
    #                 self.label_error_nombre = tk.Label(self.frame1, text="El producto ya existe.", fg="red")
    #                 self.label_error_nombre.grid(row=2, column=0, pady=10)
    #             if int(self.frame6.get_entry())>=int(self.frame7.get_entry()):
    #                 msbox.showerror(title="¡Error!", message="Stock Mínimo no puede ser mayor o igual a Stock Máximo.")
                    

    # def insertar_datos(self) -> None:
    #     nombre = self.frame1.get_entry()
    #     clase = CONSULTAS.get_id_from_column(name=self.frame2.get_selected_list(), table="clases", column="nombre_clase")
    #     lugar = CONSULTAS.get_id_from_column(name=self.frame3.get_selected_list(), table="lugares", column="nombre_lugar")
    #     unidad = CONSULTAS.get_id_from_column(name=self.frame4.get_selected_list(), table="unidades", column="nombre_unidad")
    #     precio = self.frame5.get_entry()
    #     stock_minimo = self.frame6.get_entry()
    #     stock_maximo = self.frame7.get_entry()
    #     stock = self.frame8.get_entry()

    #     data = [nombre, clase, lugar, unidad, precio, stock_minimo, stock_maximo, stock]
    #     columnas = ["nombre", "id_clase", "id_lugar", "id_unidad", "precio", "stock_minimo", "stock_maximo", "stock"]

    #     CONSULTAS.insert_data(record=data, column=columnas, table="Inventario")

    # def matriz_a_lista(self, lista: list):
    #     values = []

    #     for i in range(len(lista)):
    #         values.append(lista[i][0])
    #     return values


if __name__ == "__main__":
    root = Agregar()
    root.mainloop()
