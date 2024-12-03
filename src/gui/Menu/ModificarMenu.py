import gui.Ventanas as v
import gui.Componentes as comp
import tkinter as tk
import tkinter.ttk as ttk
import gui.Inicio as i

class Modificar(v.VentanaPrincipal):
    def __init__(self, datos: dict,**kwargs):
        super().__init__(titulo_ventana="Eliminar Menu",
                         titulo="Eliminar\nMenu",
                         **kwargs)
        self.agregar_titulo()

        self.resizable(False, False)

        self.datos = datos
        self.datos_menu = datos["Inventario"]
        self.like = None
        self.orden = "ID Menu"
        self.id_seleccionado = None
        self.datos_seleccionados = []
        self.where = [f"id_local = {self.datos["Local"]}", "ML.menu_disponible = 1"]

        self.where_principal = [f"id_local = {self.datos["Local"]}", "ML.menu_disponible = 1"]

        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.entry_busqueda = ttk.Entry(self)
        self.entry_busqueda.pack(pady=5)
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.buscar_nombre())

        self.inicializar_tabla()
        self.tabla_menu.bind("<<TreeviewSelect>>", self.seleccionar_menu)

        self.label_nombre = tk.Label(self, text="", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 14))
        self.label_nombre.pack(pady=10)

        self.boton_ingredientes = comp.Boton(self, text="Ver ingredientes", command=self.ver_ingredientes)
        self.boton_ingredientes.deshabilitar_boton()
        self.boton_ingredientes.pack(pady=10)

        self.agregar_botones_otros_datos()
        self.agregar_botones_opciones()

        self.centrar_ventana()


    def agregar_botones_otros_datos(self):
        panel = tk.Frame(self, bg=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.boton_categorias = comp.Boton(panel, text="Ver categorias")
        self.boton_categorias.config(command=self.ver_categorias)
        self.boton_categorias.pack(expand=True, side="left")

        self.boton_filtrar = comp.Boton(panel, text="Filtrar")
        self.boton_filtrar.config(command=self.ventana_filtro)
        self.boton_filtrar.pack(expand=True, side="left")

        self.boton_tamaños = comp.Boton(panel, text="Ver tamaños")
        self.boton_tamaños.config(command=self.ver_tamaños)
        self.boton_tamaños.pack(expand=True, side="left")


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, bg=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        self.boton_modificar_detalles = comp.Boton(panel, text="Modificar\nDetalles", command=self.abrir_modificar_detalles)
        self.boton_modificar_detalles.deshabilitar_boton()
        self.boton_modificar_detalles.pack(expand=True, side="left")

        self.boton_modificar_ingredientes = comp.Boton(panel, text="Modificar\nIngredientes", command=None)
        self.boton_modificar_ingredientes.deshabilitar_boton()
        self.boton_modificar_ingredientes.pack(expand=True, side="left")


        self.boton_volver = comp.Boton(panel, text="Volver") 
        self.boton_volver.config(command=self.volver)
        self.boton_volver.pack(expand=True, side="left")


    def volver(self, e=None):
        self.destroy()
        i.Inicio(datos=self.datos)


    def seleccionar_menu(self, event):
        selection = self.tabla_menu.selection()
        if selection:
            self.boton_ingredientes.habilitar_boton()
            self.boton_modificar_ingredientes.habilitar_boton()
            self.boton_modificar_detalles.habilitar_boton()
            item = self.tabla_menu.item(selection[0], "values")
            print(item)
            self.label_nombre.config(text=item[1])
            self.id_seleccionado = int(item[0])
            self.datos_seleccionados.clear()
            self.datos_seleccionados.append(item[1])
            self.datos_seleccionados.append(item[2])
            self.datos_seleccionados.append(item[3])
            self.datos_seleccionados.append(item[4])
            print(self.datos_seleccionados)
        
        
    def buscar_nombre(self):
        self.like = self.entry_busqueda.get().strip().lower()
        self.actualizar_tabla()
        self.boton_modificar_ingredientes.deshabilitar_boton()
        self.boton_modificar_detalles.deshabilitar_boton()
        

    def inicializar_tabla(self):
        self.encabezados = {"ID Menu": "ID_menu", "Nombre del Menu": "nombre_menu", "Precio":"precio", "Categoria":"ID_categoria", "Tamaño":"ID_tamaño"}
        self.tabla_menu = comp.CustomTreeview(self)
        self.tabla_menu.create_table(list(self.encabezados.keys()))
        self.tabla_menu.add_data(self.datos_menu.inner_join_menu(where=self.where_principal))
        self.tabla_menu.añadir_scrollbarv(1)
        self.tabla_menu.pack()

        for columna in self.encabezados:
            self.tabla_menu.heading(columna, command=lambda col=columna: self.ordenar_tabla(col))

    def ordenar_tabla(self, columna):
        self.orden = columna
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tabla_menu.recharge_data(self.datos_menu.inner_join_menu(like = self.like, order = self.encabezados[self.orden], where = self.where))
        
    def ver_ingredientes(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar ingredientes",
                             titulo = self.label_nombre.cget("text"),
                             encabezados = ["ID producto","producto"],
                             datos = self.datos_menu.inner_join_menu_to_ingredient(self.id_seleccionado))
        

        
    def ver_categorias(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar categorias",
                             titulo = "Categorias",
                             encabezados = ["ID Categoria","Categoria"],
                             datos = self.datos_menu.simple_complete_query("Categorias"))

    def ver_tamaños(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar tamaños",
                             titulo = "Tamaños",
                             encabezados = ["ID Tamaños","Tamaños"],
                             datos = self.datos_menu.simple_complete_query("Tamaños"))

    def crear_sub_tabla(self, titulo_ventana, titulo, encabezados, datos):
        sub_tabla = v.VentanaTopLevel(parent = self,
                                      titulo = titulo,
                                      titulo_ventana = titulo_ventana)
        sub_tabla.agregar_titulo()
        sub_tabla.grab_set()

        tabla_menu = comp.CustomTreeview(sub_tabla)
        tabla_menu.create_table(encabezados)
        tabla_menu.add_data(datos)
        tabla_menu.añadir_scrollbarv(1)
        tabla_menu.pack()

        b_volver = comp.Boton(sub_tabla, text="Cerrar", command=sub_tabla.destroy)
        b_volver.pack(expand=True, pady=10)

    def ventana_filtro(self):
        ventana = v.VentanaTopLevel(parent = self,
                                    titulo = "Filtros",
                                    titulo_ventana = "Ventana filtros",
                                    logo=self.logo)
        ventana.agregar_titulo()
        ventana.grab_set()

        def aplicar_filtros():
            filtros = []
            if comobobox_categoria.get() != por_defecto:
                filtros.append(f"C.nombre_categoria = '{comobobox_categoria.get()}'")
            if comobobox_tamaño.get() != por_defecto:
                filtros.append(f"T.nombre_tamaño = '{comobobox_tamaño.get()}'")
            if comobobox_precio.get() != por_defecto:
                simbolo = {"Mayor que": ">", "Mayor o igual que": ">=", "Igual que": "=", "Menor o igual que": "<=", "Menor que": "<"}
                filtros.append(f"M.precio {simbolo[comobobox_precio.get()]} {int(precio_entry.get())}")
            if filtros:
                filtros.append(self.where_principal[0])
                filtros.append(self.where_principal[1])
            self.where = filtros if filtros else self.where_principal
            ventana.destroy()
            self.boton_modificar_ingredientes.deshabilitar_boton()
            self.boton_modificar_detalles.deshabilitar_boton()
            self.actualizar_tabla()

        def command_vaciar():
            comobobox_categoria.set(por_defecto)
            comobobox_precio.set(por_defecto)
            comobobox_tamaño.set(por_defecto)
            precio_entry.delete(0, tk.END)
            

        por_defecto = "(nada)"

        self.label_categoria = tk.Label(ventana, text="Categoría", bg=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        self.label_categoria.pack(pady=(10, 5))

        comobobox_categoria = ttk.Combobox(ventana,
                                           values=[por_defecto] + [x[1] for x in self.datos_menu.simple_complete_query("Categorias")],
                                           state='readonly')
        comobobox_categoria.set(por_defecto)
        comobobox_categoria.pack(pady=(0, 10))

        label_tamaño = tk.Label(ventana, text="Tamaño", bg=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label_tamaño.pack(pady=(10, 5))

        comobobox_tamaño = ttk.Combobox(ventana,
                                        values=[por_defecto] + [x[1] for x in self.datos_menu.simple_complete_query("Tamaños")],
                                        state='readonly')
        comobobox_tamaño.set(por_defecto)
        comobobox_tamaño.pack(pady=(0, 10))

        label_precio = tk.Label(ventana, text="Precio", bg=self.bgcolor, foreground=self.fgcolor, font=(self.font, 12))
        label_precio.pack(pady=(10, 5))


        panel_precio = tk.Frame(ventana, background=self.bgcolor)
        panel_precio.pack(pady=10, expand=True)

        comobobox_precio = ttk.Combobox(panel_precio,
                                        values=[por_defecto, "Mayor que", "Mayor o igual que", "Igual que", "Menor o igual que", "Menor que"],
                                        state='readonly')
        comobobox_precio.set(por_defecto)
        comobobox_precio.config(width=20)
        comobobox_precio.pack(padx=5, side="left")

        def solo_numeros(P):
            if P == "" or P.isdigit():
                return True
            return False
        vcmd = ventana.register(solo_numeros)

        precio_entry = tk.Entry(panel_precio, validate="key", validatecommand=(vcmd, "%P"))
        precio_entry.config(width=10)
        precio_entry.pack(padx=5, side="left")

        boton_vaciar = comp.Boton(ventana, text="Vaciar", command=command_vaciar)
        boton_vaciar.pack(pady=10)

        panel = tk.Frame(ventana, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        boton_aplicar = comp.Boton(panel, text="Filtrar", command=aplicar_filtros)
        boton_aplicar.pack(expand=True, side="left")

        boton_cancelar = comp.Boton(panel, text="Cancelar", command=ventana.destroy)
        boton_cancelar.pack(expand=True, side="left")


    def eliminar_menu(self):
        if v.VentanaConfirmacion(self, texto="¿Esta seguro que desea\nEliminarlo este Menu?\nDespues se no puede\ndeshacer el cambio", titulo_ventana="Eliminar del Menu").obtener_respuesta():
            self.datos_menu.eliminar_menu(self.id_seleccionado)
            self.actualizar_tabla()

    
    def abrir_modificar_detalles(self):
        Detalles(self)


class Detalles(v.VentanaTopLevel):
    def __init__(self, parent = None):
        super().__init__(parent, titulo_ventana = "Modificar Detalles", titulo = "Modificar\nDetalles")

        self.parent = parent

        print(self.parent.datos_seleccionados[0])
        print(self.parent.datos_seleccionados[1])
        print(self.parent.datos_seleccionados[2])
        print(self.parent.datos_seleccionados[3])

        self.configurar_ventana()


    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_nombre()
        self.agregar_precio()
        self.agregar_categoria()
        self.agregar_tamaño()
        self.agregar_opciones()


    def agregar_nombre(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Nombre:")
        label.pack(pady=5)

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.config(width=50)
        self.nombre_entry.pack(pady=5)

        self.label_nombre_error = tk.Label(panel, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_nombre_error.pack(pady=5)

        self.nombre_entry.insert(0, self.parent.datos_seleccionados[0]) # Nombre del Menu


    def agregar_precio(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Precio")
        label.pack(pady=5)

        self.precio_entry = comp.CampoTexto(panel, tipo="int")
        self.precio_entry.config(width=50)
        self.precio_entry.pack(pady=5)

        self.label_precio_error = tk.Label(panel, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_precio_error.pack(pady=5)
    
        self.precio_entry.insert(0, self.parent.datos_seleccionados[1]) # Precio del Menu
    

    def agregar_categoria(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Categoría:")
        label.pack(pady=5)

        por_defecto = "(nada)"
    
        self.categorias_cb = ttk.Combobox(panel, values=[por_defecto] + [x[1] for x in self.parent.datos_menu.simple_complete_query("Categorias")])
        self.categorias_cb.config(state="readonly")
        self.categorias_cb.pack(pady=5)

        # Obtener la lista de valores del Combobox
        valores = self.categorias_cb['values']

        # Buscar el índice del texto deseado
        if self.parent.datos_seleccionados[2] in valores:
            indice = valores.index(self.parent.datos_seleccionados[2])
            self.categorias_cb.current(indice) 
    

    def agregar_tamaño(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Tamaño:")
        label.pack(pady=5)

        por_defecto = "(nada)"

        self.tamaños_cb = ttk.Combobox(panel, values=[por_defecto] + [x[1] for x in self.parent.datos_menu.simple_complete_query("Tamaños")])
        self.tamaños_cb.config(state="readonly")
        self.tamaños_cb.pack(pady=5)

        # Obtener la lista de valores del Combobox
        valores = self.tamaños_cb['values']

        # Buscar el índice del texto deseado
        if self.parent.datos_seleccionados[3] in valores:
            indice = valores.index(self.parent.datos_seleccionados[3])
            self.tamaños_cb.current(indice) 
    
    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=10)

        b_aplicar = comp.Boton(panel, text="Aplicar\nCambios", command=self.modificar)
        b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")


    def modificar(self):
        if self.nombre_entry.get() == "":
            self.label_nombre_error.config("* Campo Obligatorio")

        if self.precio_entry.get() == "":
            self.label_precio_error.config("* Campo Obligatorio")

        if self.nombre_entry.get() != "" and self.precio_entry.get() != "":
            existe = self.parent.datos_menu.existe_menu(self.nombre_entry.get())
            if existe == 0:
                if v.VentanaConfirmacion(self, texto="¿Seguro que desea\nModificar estos Detalles?", titulo_ventana="Modificar Detalles").obtener_respuesta():
                    id_categoria = self.parent.datos_menu.obtener_id_por_nombre("Categorias", "ID_categoria", "nombre_categoria", self.categorias_cb.get())
                    id_tamaño = self.parent.datos_menu.obtener_id_por_nombre("Tamaños", "ID_tamaño", "nombre_tamaño", self.tamaños_cb.get())

                    self.parent.datos_menu.actualizar_menu(self.parent.id_seleccionado, self.nombre_entry.get(), self.precio_entry.get(), id_categoria, id_tamaño)
                    self.parent.datos["Usuario_Logueado"]["Registro"].insertar("Modificar", "Menu")
                    self.destroy()
                    self.parent.actualizar_tabla()
            else:
                self.label_nombre_error.config("* Ya Existe Menu con ese Nombre")


class Ingredientes(v.VentanaTopLevel):
    def __init__(self, parent = None):
        super().__init__(parent, titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.parent = parent

        self.configurar_ventana()


    def configurar_ventana(self):
        self.agregar_titulo()

    

