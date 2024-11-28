import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i


class VerVentas(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Ver Ventas\nRegistradas", titulo_ventana="Ver Ventas Registradas")

        self.datos = datos
        self.datos_ventas = self.datos["Inventario"]

        self.nombre_seleccionado = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_tabla(self):
        encabezados = ["ID Venta", "Fecha de Realización", "Precio Total"]

        self.tabla = comp.CustomTreeview(self)
        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(self.datos_ventas.simple_complete_query("Ventas"))

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_venta)

        self.tabla.pack(pady=10)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_ver_contenido = comp.Boton(panel, text="Ver Contenido\nde Venta", command=self.abrir_ver_contenido)
        self.b_ver_contenido.deshabilitar_boton()

        self.b_filtrar = comp.Boton(panel, text="Filtrar", command=None)
        self.b_volver = comp.Boton(panel, text="Volver", command=self.volver)


        self.b_ver_contenido.pack(expand=True, side="left")
        self.b_filtrar.pack(expand=True, side="left")
        self.b_volver.pack(expand=True, side="left")

    
    def seleccionar_venta(self, event=None):
        selection = self.tabla.selection()
        if selection:
            self.b_ver_contenido.habilitar_boton()


    def abrir_ver_contenido(self):
        VerContenido(self)


    def volver(self, e=None):
        self.destroy()
        i.Inicio(self.datos)


class VerContenido(ven.VentanaTopLevel):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent, titulo="Contenido\nde Venta", titulo_ventana="Contenido de Venta")

        self.parent = parent

        self.configurar_ventana()


    def configurar_ventana(self):
        pass
