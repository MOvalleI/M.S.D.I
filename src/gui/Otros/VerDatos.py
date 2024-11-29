import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
import tkinter as tk
import tkinter.ttk as ttk


class VerDatos(ven.VentanaPrincipal):
    def __init__(self, datos: dict, accion: str = "Ver"):
        super().__init__(titulo_ventana = "Ver Otros Datos", titulo = "Ver Otros\nDatos")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.accion = accion

        self.selected_table = None
        self.selected_value = None

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

        valores = ["Clases","Lugares","Unidades","Categorias","Tamaños"]
        self.lista = ttk.Combobox(panel, values=valores)
        self.lista.config(state="readonly")
        self.lista.current(0)
        self.lista.pack()

        self.selected_table = valores[0]

        self.lista.bind("<<ComboboxSelected>>", self.cambiar_tabla)


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=["ID", "Nombre"])

        self.tabla.pack(expand=True)

        self.cambiar_tabla()

        self.tabla.bind("<<TreeviewSelect>>", self.on_selected)


    def agregar_opciones(self):
        self.panel_botones = tk.Frame(self, background=self.bgcolor)
        self.panel_botones.pack(expand=True, fill="both", pady=10)

        self.b_volver = comp.Boton(self, text="Volver", command=self.volver)

        if self.accion != "Ver":
            self.b_accion = comp.Boton(self, text=self.accion)
            if self.accion == "Eliminar":
                self.b_accion.configurar(command = self.eliminar)
            else:
                self.b_accion.configurar(command = self.modificar_dato)
            self.b_accion.deshabilitar_boton()

            self.b_volver.pack(expand=True, fill="both", side="left")
            self.b_accion.pack(expand=True, fill="both", before=self.b_volver, side="left")
        else:
            self.b_volver.pack(expand=True, fill="both")


    def cambiar_tabla(self, event=None):
        self.selected_table = self.lista.get()

        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        self.tabla["columns"] = ()

        encabezados = ["ID", "Nombre"]

        if self.selected_table == "Lugares":
            encabezados.append("Dirección")

        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(self.datos_inventario.simple_complete_query(self.selected_table))

    
    def on_selected(self, event):
        if self.accion != "Ver": 
            self.b_accion.habilitar_boton()

            curItem = self.tabla.focus()
            self.selected_value = self.tabla.item(curItem)["values"]


    def modificar_dato(self):
        Modificar(self, self.selected_table, self.selected_value)


    def eliminar(self):
        if ven.VentanaConfirmacion(self, texto="¿Está seguro que desea\nELIMINAR este dato?\n¡Este cambio no se puede deshacer!", titulo_ventana=f"Eliminar de {self.selected_table}", opcion1="Eliminar").obtener_respuesta():
            self.cambiar_tabla()


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)


class Modificar(ven.VentanaTopLevel):
    def __init__(self, parent, tabla, datos):
        super().__init__(parent, titulo_ventana = "Modificar Dato", titulo = f"Modificar {tabla}")

        self.tabla = tabla
        self.datos = datos

        self.configurar_ventana()

    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_entry_nombre()
        if self.tabla == "Lugares":
            self.agregar_entry_direccion()
        self.agregar_opciones()


    def agregar_entry_nombre(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Nombre:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        label.pack(pady=5)

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.config(width=50)
        self.nombre_entry.set(self.datos[1])
        self.nombre_entry.pack(pady=5)
    
    
    def agregar_entry_direccion(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Dirección:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        label.pack(pady=5)

        self.direccion_entry = comp.CampoTexto(panel)
        self.direccion_entry.config(width=50)
        self.direccion_entry.set(self.datos[2])
        self.direccion_entry.pack(pady=5)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_aplicar = comp.Boton(panel, text="Aplicar\nCambios", command=self.modificar)
        b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")

    
    def modificar(self):
        if ven.VentanaConfirmacion(self, texto="¿Está seguro de\nmodificar estos datos?", titulo_ventana=f"Modificar {self.tabla}", opcion1="Aceptar").obtener_respuesta():
            self.destroy()
            self.parent.cambiar_tabla()

    