import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i


class Eliminar(ven.VentanaPrincipal): 
    def __init__(self, datos: dict):
        super().__init__(titulo_ventana = "Eliminar Menu", titulo = "Eliminar\nMenu")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()


    def agregar_tabla(self):
        panel= tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.busqueda_entry = comp.CampoTexto(panel)
        self.busqueda_entry.pack(pady=5)

        encabezados = ["ID Menu", "Nombre", "Precio", "Categoría", "Tamaño"]

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=encabezados)
        self.tabla.pack(pady=5)


    def agregar_opciones(self):
        panel= tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_eliminar = comp.Boton(panel, text="Eliminar")
        self.b_eliminar.deshabilitar_boton()
        self.b_eliminar.pack(expand=True, side="left")

        b_filtrar = comp.Boton(panel, text="Filtrar")
        b_filtrar.pack(expand=True, side="left")
        
        b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)