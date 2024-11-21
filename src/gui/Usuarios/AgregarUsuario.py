import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i


class AgregarUsuario(comp.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar Nuevo\nUsuario", titulo_ventana="Agregar Nuevo Usuario")

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]

        self.configurar_ventana()


    def configurar_ventana(self):
        self.agregar_titulo()
        

    def agregar_nombre_entry(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill"both")

        label = tk.Frame(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label.pack(expand=True)

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.config(widht=25)


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)