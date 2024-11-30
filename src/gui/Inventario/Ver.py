import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i

class VerInventario(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.datos = datos
        self.inventario = self.datos["Inventario"]

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        label = tk.Label(panel, text="Buscar Producto por Nombre", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 14))
        label.pack(expand=True)

        self.producto_entry = comp.CampoTexto(panel)
        self.producto_entry.config(width=25)
        self.producto_entry.pack(pady=5)

        encabezados = ["ID producto", "Nombre", "Stock Mínimo", "Stock Deseado", "Stock Disponible"]

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(self.inventario.inner_join_productos())
        self.tabla.añadir_scrollbarv(1)
        self.tabla.pack(pady=5)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_producto)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        # Ver Detalles
        self.b_detalles = comp.Boton(panel, command=None, text="Ver Detalles\ndel Producto")
        self.b_detalles.deshabilitar_boton()
        self.b_detalles.pack(expand=True)


        # Ver Otros Datos
        panel_otros = tk.Frame(self, background=self.bgcolor)
        panel_otros.pack(expand=True, fill="both", pady=20)

        b_clases = comp.Boton(panel_otros, text="Ver Clases\nDisponibles", command=self.ver_clases)
        b_clases.pack(expand=True, side="left")

        b_lugares = comp.Boton(panel_otros, text="Ver Lugares\nde Compra", command=self.ver_lugares)
        b_lugares.pack(expand=True, side="left")
        
        b_unidades = comp.Boton(panel_otros, text="Ver Unidades\nDisponibles", command=self.ver_unidades)
        b_unidades.pack(expand=True, side="left")

        # Opciones
        panel_opciones = tk.Frame(self, background=self.bgcolor)
        panel_opciones.pack(expand=True, fill="both", pady=20)

        b_filtrar = comp.Boton(panel_opciones, text="Filtrar")
        b_filtrar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel_opciones, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)

    def ver_lugares(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar lugares",
                             titulo = "Lugares",
                             encabezados = ["ID Lugares","Lugares", "Direccion"],
                             datos = self.inventario.simple_complete_query("Lugares"))

    def ver_unidades(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar unidades",
                             titulo = "Unidades",
                             encabezados = ["ID Unidades","Unidades"],
                             datos = self.inventario.simple_complete_query("Unidades"))


    def ver_clases(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar clases",
                             titulo = "Clases",
                             encabezados = ["ID Clase","Clase"],
                             datos = self.inventario.simple_complete_query("Clases"))

    def crear_sub_tabla(self, titulo_ventana, titulo, encabezados, datos):
        sub_tabla = ven.VentanaTopLevel(parent = self,
                                      titulo = titulo,
                                      titulo_ventana = titulo_ventana)
        sub_tabla.agregar_titulo()
        sub_tabla.grab_set()

        tabla = comp.CustomTreeview(sub_tabla)
        tabla.create_table(encabezados)
        tabla.add_data(datos)
        tabla.añadir_scrollbarv(1)
        tabla.pack()

        b_volver = comp.Boton(sub_tabla, text="Cerrar", command=sub_tabla.destroy)
        b_volver.pack(expand=True, pady=10)

    def seleccionar_producto(self, event):
        selection = self.tabla.selection()
        if selection:
            self.b_detalles.habilitar_boton()
