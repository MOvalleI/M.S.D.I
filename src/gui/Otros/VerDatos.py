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

        self.valores = {"Clases":["ID_Clase", "nombre_clase"] ,
                        "Lugares": ["ID_Lugar", "nombre_lugar", "direccion"],
                        "Unidades": ["ID_Unidad", "nombre_unidad"],
                        "Categorias":["ID_categoria", "nombre_categoria"],
                        "Tamaños":["ID_tamaño", "nombre_tamaño"]}

        val = []

        for key in self.valores.keys():
            val.append(key)

        self.lista = ttk.Combobox(panel, values=val)
        self.lista.config(state="readonly")
        self.lista.current(0)
        self.lista.pack()

        self.selected_table = val[0]

        self.lista.bind("<<ComboboxSelected>>", self.cambiar_tabla)


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=["ID", "Nombre"])

        self.tabla.pack(expand=True)

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

        # Esto esta aqui para evitar errores de que no se hayan creado los botones
        self.cambiar_tabla()


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

        if self.accion != "Ver": 
            self.b_accion.deshabilitar_boton()

    
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

        self.parent = parent

        self.tabla = tabla
        self.datos = datos

        self.direccion_entry = None
        self.nombre_entry = None

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

        print(self.nombre_entry.get())
    
        self.label_nombre_error = tk.Label(panel, text="", background=self.bgcolor, foreground="red", font=(self.font, 14))
        self.label_nombre_error.pack(pady=5)

    
    def agregar_entry_direccion(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Dirección:", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        label.pack(pady=5)

        self.direccion_entry = comp.CampoTexto(panel)
        self.direccion_entry.config(width=50)
        self.direccion_entry.set(self.datos[2])
        self.direccion_entry.pack(pady=5)

        self.label_direccion_error = tk.Label(panel, text="", background=self.bgcolor, foreground="red", font=(self.font, 14))
        self.label_direccion_error.pack(pady=5)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_aplicar = comp.Boton(panel, text="Aplicar\nCambios", command=self.modificar)
        b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")

    
    def modificar(self):
        if self.nombre_entry.get() == "":
            self.label_nombre_error.config(text="* Campo Obligatorio")
        else:
            self.label_nombre_error.config(text="")

        direccion = None
        columna_direccion = None
        if self.parent.selected_table == "Lugares":
            direccion = self.direccion_entry.get()
            columna_direccion = self.parent.valores[self.parent.selected_table][2]

        if self.parent.selected_table == "Lugares" and self.direccion_entry.get() == "":
            self.label_direccion_error.config(text="* Campo Obligatorio")
        elif self.parent.selected_table == "Lugares" and self.direccion_entry.get() != "":
            self.label_direccion_error.config(text="")

        if self.nombre_entry.get() != "":
            if self.parent.selected_table != "Lugares" and self.parent.datos_inventario.existe_otro_dato(self.parent.selected_table, self.parent.valores[self.parent.selected_table][1], self.nombre_entry.get()) == 0:
                if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Modificar\nEstos Datos?", titulo_ventana="Modificar Datos").obtener_respuesta():
                    pk = self.parent.selected_value[0]
                    self.parent.datos_inventario.modificar_otros_datos(self.parent.selected_table, self.parent.valores[self.parent.selected_table][0], self.parent.valores[self.parent.selected_table][1], pk, self.nombre_entry.get(), direccion=direccion, columna_direccion=columna_direccion)
                    self.destroy()
                    self.parent.cambiar_tabla()
            elif self.parent.selected_table == "Lugares":
                if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Modificar\nEstos Datos?", titulo_ventana="Modificar Datos").obtener_respuesta():
                    pk = self.parent.selected_value[0]
                    self.parent.datos_inventario.modificar_otros_datos(self.parent.selected_table, self.parent.valores[self.parent.selected_table][0], self.parent.valores[self.parent.selected_table][1], pk, self.nombre_entry.get(), direccion=direccion, columna_direccion=columna_direccion)
                    self.destroy()
                    self.parent.cambiar_tabla()
            else:
                self.label_nombre_error.config(text="* Ya existe un valor con este nombre")

    