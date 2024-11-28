import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i

class Modificar(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.protocol("WM_DELETE_WINDOW", self.volver)
        self.resizable(True, True)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_botones_modificar()
        self.agregar_opciones()


    def agregar_tabla(self):
        panel= tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.busqueda_entry = comp.CampoTexto(panel)
        self.busqueda_entry.pack(pady=5)

        encabezados = ["ID Menu", "Nombre", "Precio", "Categoría", "Tamaño"]

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=encabezados)
        self.tabla.pack(pady=5)

    
    def agregar_botones_modificar(self):
        panel= tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_modificar_menu = comp.Boton(panel, text="Modificar Menu\nSeleccionado")
        self.b_modificar_menu.deshabilitar_boton()
        self.b_modificar_menu.pack(expand=True, side="left")
        
        self.b_modificar_ingredientes = comp.Boton(panel, text="Modificar\nIngredientes")
        self.b_modificar_ingredientes.deshabilitar_boton()
        self.b_modificar_ingredientes.pack(expand=True, side="left")


    def agregar_opciones(self):
        panel= tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_filtrar = comp.Boton(panel, text="Filtrar")
        b_filtrar.pack(expand=True, side="left")
        
        b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)