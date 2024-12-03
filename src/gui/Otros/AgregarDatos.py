import tkinter as tk
import tkinter.ttk as ttk
import gui.Inicio as i
import gui.Componentes as comp
import gui.Ventanas as ven


class AgregarDatos(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar Otros\nDatos", titulo_ventana="Agregar Otros Datos")
            
        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

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

        if self.tabla_seleccionada == "Lugares":
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

        self.label_nombre_error = tk.Label(panel_nombre, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_nombre_error.pack()

        # Direccion (Solo aparece cuando se selecciona "Lugares")
        self.panel_direccion = tk.Frame(self, background=self.bgcolor)
        self.panel_direccion.pack_forget()

        label_direccion = tk.Label(self.panel_direccion, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Dirección:")
        label_direccion.pack()

        self.direccion_entry = comp.CampoTexto(self.panel_direccion)
        self.direccion_entry.config(width=25)
        self.direccion_entry.pack()

        self.label_direccion_error = tk.Label(self.panel_direccion, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_direccion_error.pack()


    def agregar_opciones(self):
        self.panel_opciones = tk.Frame(self, background=self.bgcolor)
        self.panel_opciones.pack(expand=True, fill="both", pady=10)

        b_agregar = comp.Boton(self.panel_opciones, text="Agregar", command=self.agregar_otros_datos)
        b_agregar.pack(side="left", expand=True)

        b_volver = comp.Boton(self.panel_opciones, text="Volver", command=self.volver)
        b_volver.pack(side="left", expand=True)


    def mostrar_direccion_panel(self):
        self.panel_direccion.pack(expand=True, fill="both", before=self.panel_opciones, pady=10)


    def ocultar_direccion_panel(self):
        self.panel_direccion.pack_forget()
        self.label_direccion_error.config(text="")

    
    def agregar_otros_datos(self):
        if self.nombre_entry.get() == "":
            self.label_nombre_error.config(text="* Campo Obligatorio")
        else:
            self.label_nombre_error.config(text="")

        direccion = None
        if self.tabla_seleccionada == "Lugares":
            direccion == self.direccion_entry.get()

        if self.tabla_seleccionada == "Lugares" and self.direccion_entry.get() == "":
            self.label_direccion_error.config(text="* Campo Obligatorio")
        elif self.tabla_seleccionada == "Lugares" and self.direccion_entry.get() != "":
            self.label_direccion_error.config(text="")

        if self.nombre_entry.get() != "":
            if self.datos_inventario.existe_otro_dato(self.lista.get(), self.valores[self.lista.get()][1], self.nombre_entry.get()) == 0:
                if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Agregar\nEstos Datos?", titulo_ventana="Agregar Datos").obtener_respuesta():
                    pk = self.datos_inventario.obtener_pk(self.lista.get(), self.valores[self.lista.get()][0])
                    self.datos_inventario.insertar_otros_datos(self.lista.get(), pk, self.nombre_entry.get(),direccion)
                    self.datos["Usuario_Logueado"]["Registro"].insertar("Agregar", self.tabla_seleccionada)
                    self.volver()
            else:
                self.label_nombre_error.config(text="* Ya existe un valor con este nombre")




    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)

