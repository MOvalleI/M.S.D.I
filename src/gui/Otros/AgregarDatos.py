import tkinter as tk
import tkinter.ttk as ttk
import gui.Inicio as i
import gui.Componentes as comp
import gui.Ventanas as ven


class AgregarDatos(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar Otros\nDatos", titulo_ventana="Agregar Otros Datos")
            
        self.datos = datos

        self.configurar_ventana()

    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_lista()


    def agregar_lista(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        label = tk.Label(panel, self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label.pack()

        valores = ["Clase","Lugar de Compra","Unidad","Categoria","Tamaño"]

        self.lista = ttk.Combobox(panel, values=valores)
        self.lista.current(0)
        self.lista.pack()


    def agregar_nombre_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        self.nombre_label = tk.Label(panel, self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        self.nombre_label.pack(expand=True)


    def cambiar_nombre_label(self, texto: str):
        self.nombre_label.config(text=f"Agregar\n{texto}")

    
    def agregar_formularios(self):
        panel_nombre = tk.Frame(self, background=self.bgcolor)
        panel_nombre.pack(expand=True, fill="both")

        # Nombre
        label_nombre = tk.Label(panel_nombre, self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label_nombre.pack()

        self.nombre_entry = comp.CampoTexto(panel_nombre)
        self.nombre_entry.pack()

        # Direccion (Solo aparece cuando se selecciona "Lugares")
        self.panel_direccion = tk.Frame(self, background=self.bgcolor)
        self.panel_direccion.pack_forget()

        label_direccion = tk.Label(self.panel_direccion, self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label_direccion.pack()

        self.direccion_entry = comp.CampoTexto(self.panel_direccion)
        self.direccion_entry.pack()


    def mostrar_direccion_panel(self):
        self.panel_direccion.pack(expand=True, fill="both")

    def ocultar_direccion_panel(self):
        self.panel_direccion.pack_forget()

