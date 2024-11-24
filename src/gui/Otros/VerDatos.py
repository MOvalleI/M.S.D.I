import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
import tkinter as tk
import tkinter.ttk as ttk


class VerDatos(ven.VentanaPrincipal):
    def __init__(self, datos: dict, accion: str = "Ver"):
        super().__init__(titulo_ventana = "Ver Otros Datos", titulo = "Ver Otros\nDatos")

        self.datos = datos
        self.accion = accion

        self.configurar_ventana()
    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)
        
        self.agregar_titulo()
        self.agregar_lista()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()


    def agregar_lista(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Selecciona una tabla:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label.pack()

        valores = ["Clase","Lugares","Unidad","Categoria","Tamaño"]
        self.lista.config(state="readonly")
        self.lista.current(0)
        self.lista = ttk.Combobox(panel, values=valores)
        self.lista.pack()


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=["Nombre"])

        self.tabla.pack(expand=True)


    def agregar_opciones(self):
        self.panel_botones = tk.Frame(self, background=self.bgcolor)
        self.panel_botones.pack(expand=True, fill="both", pady=10)

        self.b_volver = comp.Boton(self, text="Volver", command=self.volver)

        if self.accion != "Ver":
            self.b_accion = comp.Boton(self, text=self.accion)
            if self.accion == "Eliminar":
                self.b_accion.configurar(command = self.volver)
            else:
                self.b_accion.configurar(command = self.volver)

            self.b_volver.pack(expand=True, fill="both", side="left")
            self.b_accion.pack(expand=True, fill="both", before=self.b_volver, side="left")
        else:
            self.b_volver.pack(expand=True, fill="both")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)

