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


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        label = tk.Label(panel, text="Buscar Producto por Nombre", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 14))
        label.pack(expand=True)

        self.producto_entry = comp.CampoTexto(panel)
        self.producto_entry.config(width=25)
        self.producto_entry.pack(pady=5)

        encabezados = ["Nombre", "Stock Mínimo", "Stock Deseado", "Stock Disponible"]

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=encabezados)
        self.tabla.pack(pady=5)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        # Ver Detalles
        b_detalles = comp.Boton(panel, command=None, text="Ver Detalles\ndel Producto")
        b_detalles.deshabilitar_boton()
        b_detalles.pack(expand=True)


        # Ver Otros Datos
        panel_otros = tk.Frame(self, background=self.bgcolor)
        panel_otros.pack(expand=True, fill="both", pady=20)

        b_clases = comp.Boton(panel_otros, text="Ver Clases\nDisponibles")
        b_clases.pack(expand=True, side="left")

        b_lugares = comp.Boton(panel_otros, text="Ver Lugares\nde Compra")
        b_lugares.pack(expand=True, side="left")
        
        b_unidades = comp.Boton(panel_otros, text="Ver Unidades\nDisponibles")
        b_unidades.pack(expand=True, side="left")

        # Opciones
        panel_opciones = tk.Frame(self, background=self.bgcolor)
        panel_opciones.pack(expand=True, fill="both", pady=20)

        b_filtrar = comp.Boton(panel_opciones, text="Filtrar", command=None)
        b_filtrar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel_opciones, text="Volver", command=None)
        b_volver.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)