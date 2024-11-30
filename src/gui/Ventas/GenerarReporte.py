import gui.Componentes as comp
import tkinter as tk
import gui.Ventanas as ven
import gui.Inicio as i
import data.PDF as pdf

class Generar(ven.VentanaPrincipal):
    def __init__(self, datos: dict, tipo: str):
        super().__init__(titulo_ventana = "Generar Reporte", titulo = "Generar\nReporte")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.tipo = tipo

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_firma()
        self.agregar_opciones()


    def agregar_firma(self):
        label = tk.Label(self, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16))
        label.config(text="Ingrese su firma para generar el reporte:")
        label.pack(expand=True)

        self.firma = pdf.DibujarFirma(self, datosDB=self.datos_inventario)
        self.firma.pack(expand=True)

        b_borrar = comp.Boton(self, text="Borrar", command=self.firma.draw_delete)
        b_borrar.pack(expand=True)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        b_generar = comp.Boton(panel, text="Generar\nReporte", command=self.volver)
        b_generar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.volver)
        b_cancelar.pack(expand=True, side="left")
    
    
    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)