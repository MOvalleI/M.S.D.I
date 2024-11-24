import tkinter as tk
import tkinter.ttk as ttk
import gui.Ventanas as ven
import gui.Inicio as i
import gui.Componentes as comp


class AgregarMenu(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar\nMenu",titulo_ventana="Agregar Menu")

        self.datos = datos

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_nombre()
        self.agregar_categoria()
        self.agregar_tamaño()
        self.agregar_precio()
        self.agregar_opciones()

        self.centrar_ventana()


    def agregar_nombre(self) -> tk.Frame:
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Nombre:")
        label.pack()

        self.nombre_entry =  comp.CampoTexto(panel)
        self.nombre_entry.config(width=25)
        self.nombre_entry.pack()


    def agregar_categoria(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Categoría:")
        label.pack()

        valores = ["Valor1", "Valor1", "Valor1", "Valor1", "Valor1"]

        self.lista_categoria = ttk.Combobox(panel, values=valores)
        self.lista_categoria.config(state="readonly")
        self.lista_categoria.current(0)
        self.lista_categoria.pack()


    def agregar_tamaño(self) :
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Tamaño:")
        label.pack()

        valores = ["Valor1", "Valor1", "Valor1", "Valor1", "Valor1"]

        self.lista_tamaño = ttk.Combobox(panel, values=valores)
        self.lista_tamaño.config(state="readonly")
        self.lista_tamaño.current(0)
        self.lista_tamaño.pack()


    def agregar_precio(self) -> tk.Frame:
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Precio:")
        label.pack()

        self.precio_entry =  comp.CampoTexto(panel, tipo="int")
        self.precio_entry.config(width=25)
        self.precio_entry.pack()


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        b_agregar = comp.Boton(panel, command=None, text="Agregar")
        b_agregar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel, command=self.volver, text="Volver")
        b_volver.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)
