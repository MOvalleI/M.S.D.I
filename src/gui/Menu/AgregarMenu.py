import tkinter as tk
import tkinter.ttk as ttk
import gui.Ventanas as ven
import gui.Inicio as i
import gui.Componentes as comp


class AgregarMenu(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar\nMenu",titulo_ventana="Agregar Menu")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.nombre = None
        self.precio = None
        self.categoria = None
        self.tamaño = None
        self.ingredientes = []

        self.ingrediente_seleccionado = ""

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_pagina_1()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_pagina_1(self):
        "Pagina dedicada a los datos principales del menu"
        self.pagina1 = tk.Frame(self, background=self.bgcolor)
        self.pagina1.pack(expand=True, fill="both", pady=10)

        self.agregar_nombre()
        self.agregar_categoria()
        self.agregar_tamaño()
        self.agregar_precio()


    def agregar_nombre(self) -> tk.Frame:
        panel = tk.Frame(self.pagina1, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Nombre:")
        label.pack()

        self.nombre_entry =  comp.CampoTexto(panel)
        self.nombre_entry.config(width=25)
        self.nombre_entry.pack()

        self.label_nombre_error = tk.Label(panel, background=self.bgcolor, foreground="red", font=(self.font, 14), text="")
        self.label_nombre_error.pack()


    def agregar_categoria(self):
        panel = tk.Frame(self.pagina1, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Categoría:")
        label.pack()

        valores = []

        for valor in self.datos_inventario.obtener_columna_tablas("categorias", "nombre_categoria"):
            valores.append(valor[0])

        self.lista_categoria = ttk.Combobox(panel, values=valores)
        self.lista_categoria.config(state="readonly")
        self.lista_categoria.current(0)
        self.lista_categoria.pack()


    def agregar_tamaño(self) :
        panel = tk.Frame(self.pagina1, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Tamaño:")
        label.pack()

        valores = []

        for valor in self.datos_inventario.obtener_columna_tablas("tamaños", "nombre_tamaño"):
            valores.append(valor[0])

        self.lista_tamaño = ttk.Combobox(panel, values=valores)
        self.lista_tamaño.config(state="readonly")
        self.lista_tamaño.current(0)
        self.lista_tamaño.pack()


    def agregar_precio(self) -> tk.Frame:
        panel = tk.Frame(self.pagina1, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14), text="Precio:")
        label.pack()

        self.precio_entry =  comp.CampoTexto(panel, tipo="int")
        self.precio_entry.config(width=25)
        self.precio_entry.pack()

        self.label_precio_error = tk.Label(panel, background=self.bgcolor, foreground="red", font=(self.font, 14), text="")
        self.label_precio_error.pack()


    def agregar_opciones(self):
        self.panel_opciones = tk.Frame(self, background=self.bgcolor)
        self.panel_opciones.pack(expand=True, fill="both", pady=10)

        self.b_agregar = comp.Boton(self.panel_opciones, text="Siguiente", command=self.cambiar_pagina)
        self.b_agregar.pack(expand=True, side="left")

        b_volver = comp.Boton(self.panel_opciones, command=self.volver, text="Cancelar")
        b_volver.pack(expand=True, side="left")

    
    def agregar_pagina_2(self):
        "Pagina dedicada a los datos principales del menu"
        self.pagina1.pack_forget()

        self.b_agregar.configurar(command=self.agregar_menu)
        self.b_agregar.deshabilitar_boton()
        self.b_agregar.config(text="Agregar\nMenu")

        self.pagina2 = tk.Frame(self, background=self.bgcolor)
        self.pagina2.pack(expand=True, fill="both", pady=10, before=self.panel_opciones)

        self.agregar_tabla_ingredientes()

        self.centrar_ventana()

    
    def agregar_tabla_ingredientes(self):
        panel = tk.Frame(self.pagina2, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 20), text="Ingredientes")
        label.pack(expand=True, pady=10)

        # Tabla
        encabezados = ["Nombre Ingrediente"]

        self.tabla_ingredientes = comp.CustomTreeview(panel)
        self.tabla_ingredientes.create_table(head=encabezados, width=200)
        self.tabla_ingredientes.añadir_scrollbarv(1)
        self.tabla_ingredientes.pack(expand=True, pady=10)
        self.tabla_ingredientes.bind("<<TreeviewSelect>>", self.seleccionar_ingrediente)

        # Opciones de Ingredientes
        panel_botones = tk.Frame(panel, background=self.bgcolor)
        panel_botones.pack(expand=True, fill="both", pady=10)

        self.b_agregar_ingrediente = comp.Boton(panel_botones, text="Agregar\nIngrediente", command=self.abrir_ingredientes)
        self.b_agregar_ingrediente.pack(expand=True, side="left")

        self.b_eliminar_ingrediente = comp.Boton(panel_botones, text="Eliminar\nIngrediente", command=self.eliminar_ingrediente)
        self.b_eliminar_ingrediente.deshabilitar_boton()
        self.b_eliminar_ingrediente.pack(expand=True, side="left")


    def cambiar_pagina(self):
        if self.nombre_entry.get() == "":
            self.label_nombre_error.config(text="* Campo Obligatorio")
        else:
            self.label_nombre_error.config(text="")

        if self.precio_entry.get() == "":
            self.label_precio_error.config(text="* Campo Obligatorio")
        else:
            self.label_precio_error.config(text="")

        if self.nombre_entry.get() != "" and self.precio_entry.get() != "":
            existe = self.datos_inventario.existe_menu(self.nombre_entry.get())
            if existe == 0:
                self.nombre = self.nombre_entry.get()
                self.precio = self.precio_entry.get()
                self.categoria = self.datos_inventario.obtener_id_por_nombre("Categorias", "id_categoria", "nombre_categoria", self.lista_categoria.get())
                self.tamaño = self.datos_inventario.obtener_id_por_nombre("Tamaños", "id_tamaño", "nombre_tamaño", self.lista_tamaño.get())
                self.agregar_pagina_2()
            else:
                self.label_nombre_error.config(text="* El Menu ya existe")


    def actualizar_tabla(self):
        lista_transformada = [(item,) for item in self.ingredientes]
        self.tabla_ingredientes.recharge_data(lista_transformada)
        self.b_eliminar_ingrediente.deshabilitar_boton()
        if len(self.ingredientes) == 0:
            self.b_agregar.deshabilitar_boton()
        else:
            self.b_agregar.habilitar_boton()



    def seleccionar_ingrediente(self, event):
        curItem = self.tabla_ingredientes.focus()
        valores = self.tabla_ingredientes.item(curItem)["values"]

        self.ingrediente_seleccionado = valores[0]
        self.b_eliminar_ingrediente.habilitar_boton()


    def eliminar_ingrediente(self):
        index = self.ingredientes.index(self.ingrediente_seleccionado)
        self.ingredientes.pop(index)
        self.actualizar_tabla()


    def abrir_ingredientes(self):
        Ingredientes(self)


    def agregar_menu(self):
        if ven.VentanaConfirmacion(self, texto="¿Seguro que desea\nAgregar este Menu?", titulo_ventana="Agregar Menu").obtener_respuesta():
            for i in range(len(self.ingredientes)):
                self.ingredientes[i] = self.datos_inventario.obtener_id_ingredientes_por_nombre(self.ingredientes[i])[0]
            pk = self.datos_inventario.obtener_pk("Menu", "ID_menu")
            self.datos_inventario.agregar_menu(pk, self.nombre, self.precio, self.categoria, self.tamaño, self.ingredientes)
            self.destroy()


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)


class Ingredientes(ven.VentanaTopLevel):
    def __init__(self, parent = None):
        super().__init__(parent, titulo_ventana = "Agregar Ingrediente", titulo = "Agregar\nIngrediente")

        self.parent = parent

        self.ingrediente_seleccionado = None

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_buscador()
        self.agregar_tabla()
        self.agregar_opciones()

    
    def agregar_buscador(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Buscar Ingrediente:")
        label.pack(expand=True, pady=3)

        self.ingrediente_entry = comp.CampoTexto(panel)
        self.ingrediente_entry.config(width=50)
        self.ingrediente_entry.pack(pady=3)

        self.ingrediente_entry.bind("<KeyRelease>",self.actualizar_tabla)

    
    def agregar_tabla(self):
        encabezados = ["Nombre Ingrediente", "Clase Ingrediente"]

        self.tabla = comp.CustomTreeview(self)
        self.tabla.create_table(head=encabezados, width=200)
        self.tabla.add_data(self.parent.datos_inventario.obtener_ingredientes(None))
        self.tabla.añadir_scrollbarv(1)
        self.tabla.pack(expand=True, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_ingrediente)
        

    def actualizar_tabla(self, event):
        self.b_agregar.deshabilitar_boton()
        self.ingrediente_seleccionado = None
        self.tabla.recharge_data(self.parent.datos_inventario.obtener_ingredientes(self.ingrediente_entry.get()))
    

    def seleccionar_ingrediente(self, event):
        curItem = self.tabla.focus()
        valores = self.tabla.item(curItem)["values"]

        self.ingrediente_seleccionado = valores[0]
        self.b_agregar.habilitar_boton()


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_agregar = comp.Boton(panel, text="Agregar", command=self.agregar_ingrediente)
        self.b_agregar.deshabilitar_boton()
        self.b_agregar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")

    
    def agregar_ingrediente(self):
        self.parent.ingredientes.append(self.ingrediente_seleccionado)
        self.destroy()
        self.parent.actualizar_tabla()



