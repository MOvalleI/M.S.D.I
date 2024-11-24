import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven

class MenuPerfil(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__( titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.datos = datos

        self.usuario_logueado = self.datos["Usuario_Logueado"]