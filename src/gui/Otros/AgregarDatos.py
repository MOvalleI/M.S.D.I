import tkinter as tk
import tkinter.ttk as ttk
import gui.Inicio as i
import gui.Componentes as comp
import gui.Ventanas as ven


class AgregarDatos(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar Otros\nDatos", titulo_ventana="Agregar Otros Datos")
            
        self.datos = datos

        self.tabla_seleccionada = ""

        self.configurar_ventana()

    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_lista()
        self.agregar_nombre_tabla()
        self.agregar_formularios()
        self.agregar_opciones()

        self.centrar_ventana()


    def agregar_lista(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12), text="Selecciona una Tabla:")
        label.pack()

        valores = ["Clase","Lugar de Compra","Unidad","Categoria","Tamaño"]

        self.lista = ttk.Combobox(panel, values=valores)
        self.lista.config(state="readonly")
        self.lista.current(0)
        self.tabla_seleccionada = self.lista.get()
        self.lista.pack()

        self.lista.bind("<<ComboboxSelected>>", lambda e: self.cambiar_nombre_label(self.lista.get(), event=e))


    def agregar_nombre_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.nombre_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 18), text=f"Agregar\n{self.tabla_seleccionada}")
        self.nombre_label.pack(expand=True)


    def cambiar_nombre_label(self, texto: str, event=None):
        self.tabla_seleccionada = texto
        self.nombre_label.config(text=f"Agregar\n{self.tabla_seleccionada}")

        if self.tabla_seleccionada == "Lugar de Compra":
            self.mostrar_direccion_panel()
        else:
            self.ocultar_direccion_panel()

    
    def agregar_formularios(self):
        panel_nombre = tk.Frame(self, background=self.bgcolor)
        panel_nombre.pack(expand=True, fill="both", pady=10)

        # Nombre
        label_nombre = tk.Label(panel_nombre, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Nombre:")
        label_nombre.pack()

        self.nombre_entry = comp.CampoTexto(panel_nombre)
        self.nombre_entry.config(width=25)
        self.nombre_entry.pack()

        # Direccion (Solo aparece cuando se selecciona "Lugares")
        self.panel_direccion = tk.Frame(self, background=self.bgcolor)
        self.panel_direccion.pack_forget()

        label_direccion = tk.Label(self.panel_direccion, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Dirección:")
        label_direccion.pack()

        self.direccion_entry = comp.CampoTexto(self.panel_direccion)
        self.direccion_entry.config(width=25)
        self.direccion_entry.pack()


    def agregar_opciones(self):
        self.panel_opciones = tk.Frame(self, background=self.bgcolor)
        self.panel_opciones.pack(expand=True, fill="both", pady=10)

        b_agregar = comp.Boton(self.panel_opciones, text="Agregar", command=None)
        b_agregar.pack(side="left", expand=True)

        b_volver = comp.Boton(self.panel_opciones, text="Volver", command=self.volver)
        b_volver.pack(side="left", expand=True)


    def mostrar_direccion_panel(self):
        self.panel_direccion.pack(expand=True, fill="both", before=self.panel_opciones, pady=10)


    def ocultar_direccion_panel(self):
        self.panel_direccion.pack_forget()


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)

