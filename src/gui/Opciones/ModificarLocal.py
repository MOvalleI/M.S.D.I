import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import data.LocalInfo as li
import gui.Inicio as i

class ModificarLocal(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo_ventana = "Modificar Local", titulo = "Modificar\nLocal")

        self.datos = datos

        self.local_seleccionado = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        encabezados = ["ID Local", "Dirección"]

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(encabezados)
        
        datos = self.datos["Inventario"].simple_complete_query("Locales")
        self.tabla.add_data(datos)
        
        self.tabla.pack(expand=True)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_local)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_establecer = comp.Boton(panel, text="Establecer\ncomo Local", command=self.cambiar_local)
        self.b_establecer.deshabilitar_boton()
        self.b_establecer.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.volver)
        b_cancelar.pack(expand=True, side="left")


    def seleccionar_local(self, event):
        self.local_seleccionado = self.tabla.item(self.tabla.focus())["values"][0]
        self.b_establecer.habilitar_boton()
        print(self.local_seleccionado)

    
    def cambiar_local(self):
        if li.cambiar_info_local(self.local_seleccionado):
            texto = "¡Cambio Realizado con Exito!"
            ven.VentanaAvisoTL(self, texto=texto, titulo_ventana="Cambio Realizado")
            self.volver()
        else:
            texto = "¡No se pudo realizar el Cambio!"
            ven.VentanaAvisoTL(self, texto=texto, titulo_ventana="Error")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)