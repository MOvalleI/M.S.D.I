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

        self.boton_tamaños = comp.Boton(panel, text="Ver tamaños")
        self.boton_tamaños.config(command=self.ver_tamaños)
        self.boton_tamaños.pack(expand=True, side="left")


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, bg=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        self.boton_eliminar = comp.Boton(panel, text="Eliminar", command=self.eliminar_menu)
        self.boton_eliminar.deshabilitar_boton()
        self.boton_eliminar.pack(expand=True, side="left")

        self.boton_filtrar = comp.Boton(panel, text="Filtrar")
        self.boton_filtrar.config(command=self.ventana_filtro)
        self.boton_filtrar.pack(expand=True, side="left")

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
            self.boton_eliminar.habilitar_boton()
            item = self.tabla_menu.item(selection[0], "values")
            self.label_nombre.config(text=item[1])
            self.id_seleccionado = int(item[0])
        
        
    def buscar_nombre(self):
        self.like = self.entry_busqueda.get().strip().lower()
        self.actualizar_tabla()
        self.boton_eliminar.deshabilitar_boton()
        

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
            self.boton_eliminar.deshabilitar_boton()
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