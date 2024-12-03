import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i

class VerInventario(ven.VentanaPrincipal):
    def __init__(self, datos: dict, tipo: str = "Ver"):
        super().__init__(titulo_ventana = "MSDI | Micro Sistema de Inventario | Ver Inventario", titulo = "Ver\nInventario")

        self.datos = datos
        self.inventario = self.datos["Inventario"]

        self.tipo = tipo

        if self.tipo == "Ver":
            self.datos["Usuario_Logueado"]["Registro"].insertar("Ver", "Productos")

        self.producto_seleccionado = None
        self.id_producto_seleccionado = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()


    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        label = tk.Label(panel, text="Buscar Producto por Nombre", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 14))
        label.pack(expand=True)

        self.producto_entry = comp.CampoTexto(panel)
        self.producto_entry.config(width=25)
        self.producto_entry.pack(pady=5)

        encabezados = ["ID producto", "Nombre", "Stock Mínimo", "Stock Deseado", "Stock Disponible"]

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(self.inventario.inner_join_productos())
        self.tabla.añadir_scrollbarv(1)
        self.tabla.pack(pady=5)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_producto)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        # Ver Detalles
        self.b_detalles = comp.Boton(panel, command=self.abrir_mas_detalles, text="Ver Detalles\ndel Producto")
        self.b_detalles.deshabilitar_boton()
        self.b_detalles.pack(expand=True)


        # Ver Otros Datos
        panel_otros = tk.Frame(self, background=self.bgcolor)
        panel_otros.pack(expand=True, fill="both", pady=20)

        b_clases = comp.Boton(panel_otros, text="Ver Clases\nDisponibles", command=self.ver_clases)
        b_clases.pack(expand=True, side="left")

        b_lugares = comp.Boton(panel_otros, text="Ver Lugares\nde Compra", command=self.ver_lugares)
        b_lugares.pack(expand=True, side="left")
        
        b_unidades = comp.Boton(panel_otros, text="Ver Unidades\nDisponibles", command=self.ver_unidades)
        b_unidades.pack(expand=True, side="left")

        # Opciones
        panel_opciones = tk.Frame(self, background=self.bgcolor)
        panel_opciones.pack(expand=True, fill="both", pady=20)

        self.b_accion = None

        if self.tipo == "Eliminar":
            self.b_accion = comp.Boton(panel_opciones, text="Eliminar\nProducto", command=None)
            self.b_accion.deshabilitar_boton()
            self.b_accion.pack(expand=True, side="left")
        elif self.tipo == "Modificar":                
            self.b_accion = comp.Boton(panel_opciones, text="Modificar\nProducto", command=self.modificar_producto)
            self.b_accion.deshabilitar_boton()
            self.b_accion.pack(expand=True, side="left")

        b_filtrar = comp.Boton(panel_opciones, text="Filtrar", command=self.abrir_filtrar)
        b_filtrar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel_opciones, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)


    def ver_lugares(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar lugares",
                             titulo = "Lugares",
                             encabezados = ["ID Lugares","Lugares", "Direccion"],
                             datos = self.inventario.simple_complete_query("Lugares"))

    def ver_unidades(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar unidades",
                             titulo = "Unidades",
                             encabezados = ["ID Unidades","Unidades"],
                             datos = self.inventario.simple_complete_query("Unidades"))


    def ver_clases(self):
        self.crear_sub_tabla(titulo_ventana = "Vizualizar clases",
                             titulo = "Clases",
                             encabezados = ["ID Clase","Clase"],
                             datos = self.inventario.simple_complete_query("Clases"))

    def crear_sub_tabla(self, titulo_ventana, titulo, encabezados, datos):
        sub_tabla = ven.VentanaTopLevel(parent = self,
                                      titulo = titulo,
                                      titulo_ventana = titulo_ventana)
        sub_tabla.agregar_titulo()
        sub_tabla.grab_set()

        tabla = comp.CustomTreeview(sub_tabla)
        tabla.create_table(encabezados)
        tabla.add_data(datos)
        tabla.añadir_scrollbarv(1)
        tabla.pack()

        b_volver = comp.Boton(sub_tabla, text="Cerrar", command=sub_tabla.destroy)
        b_volver.pack(expand=True, pady=10)


    def abrir_mas_detalles(self):
        ventana = ven.VentanaTopLevel(self, titulo=f"Detalles de\n{self.producto_seleccionado}", titulo_ventana="Mas Detalles")

        ventana.agregar_titulo()
        
        texto_clase = self.inventario.buscar_tabla_por_producto(self.id_producto_seleccionado, "Clases", "nombre_clase", "id_clase")
        label_clase = tk.Label(ventana, text=f"Clase: {texto_clase}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 20))
        label_clase.pack(expand=True)

        texto_lugar = self.inventario.buscar_tabla_por_producto(self.id_producto_seleccionado, "Lugares", "nombre_lugar", "id_lugar")
        label_lugar = tk.Label(ventana, text=f"Lugar de Compra: {texto_lugar}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 20))
        label_lugar.pack(expand=True)
        
        texto_unidad = self.inventario.buscar_tabla_por_producto(self.id_producto_seleccionado, "Unidades", "nombre_unidad", "id_unidad")
        label_unidad = tk.Label(ventana, text=f"Unidad de Almacenamiento: {texto_unidad}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 20))
        label_unidad.pack(expand=True)

        texto_precio = self.inventario.obtener_valor_producto(self.id_producto_seleccionado, "precio_unitario")
        label_precio = tk.Label(ventana, text=f"Precio Unitario: {texto_precio}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 20))
        label_precio.pack(expand=True)

        cerrar = comp.Boton(ventana, text="Cerrar", command=ventana.destroy)
        cerrar.pack(expand=True)
    

    def abrir_filtrar(self):
        Filtrar(self)


    def eliminar_producto(self):
        pass


    def modificar_producto(self):
        clase = self.inventario.buscar_tabla_por_producto(self.id_producto_seleccionado, "Clases", "nombre_clase", "id_clase")
        lugar = self.inventario.buscar_tabla_por_producto(self.id_producto_seleccionado, "Lugares", "nombre_lugar", "id_lugar")
        unidad = self.inventario.buscar_tabla_por_producto(self.id_producto_seleccionado, "Unidades", "nombre_unidad", "id_unidad")
        precio = self.inventario.obtener_valor_producto(self.id_producto_seleccionado, "precio_unitario")
        min = self.inventario.obtener_valor_producto(self.id_producto_seleccionado, "stock_minimo")
        max = self.inventario.obtener_valor_producto(self.id_producto_seleccionado, "stock_maximo")
        act = self.inventario.obtener_stock_actual(self.id_producto_seleccionado)

        Modificar(self, self.id_producto_seleccionado, self.producto_seleccionado, clase, lugar, unidad, precio, min, max, act)

    
    def actualizar_tabla(self, datos):
        data = self.inventario.filtrar_productos(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7])
        self.tabla.recharge_data(data)


    def seleccionar_producto(self, event):
        curItem = self.tabla.focus()
        valores = self.tabla.item(curItem)["values"]

        self.id_producto_seleccionado = valores[0]
        self.producto_seleccionado = valores[1]

        self.b_detalles.habilitar_boton()
        if self.b_accion is not None:
            self.b_accion.habilitar_boton()


class Filtrar(ven.VentanaTopLevel):
    def __init__(self, parent = None):
        super().__init__(parent,titulo_ventana = "Filtrar", titulo = "Filtrar")

        self.fecha = None
        self.parent = parent

        self.configurar_ventana()

    
    def configurar_ventana(self):
        ancho = 520
        alto = 625

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.agregar_titulo()

        self.panel_data = tk.Frame(self, background=self.bgcolor)
        self.panel_data.pack(expand=True, fill="both")

        self.agregar_fila_1()
        self.agregar_fila_2()
        self.agregar_fila_3()
        self.agregar_fila_4()

        self.agregar_botones_opciones()


    def agregar_fila_1(self):
        # Nombre y Clase
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Nombre
        panel_nombre = tk.Frame(panel, background=self.bgcolor)
        panel_nombre.pack(expand=True, fill="both", side="left")

        label_nombre = tk.Label(panel_nombre, text="Nombre:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label_nombre.pack(expand=True)

        self.nombre_entry = tk.Entry(panel_nombre, width=25)
        self.nombre_entry.pack(expand=True)

        # Clase
        panel_clase = tk.Frame(panel, background=self.bgcolor)
        panel_clase.pack(expand=True, fill="both", side="left")

        label_clase = tk.Label(panel_clase, text="Clase:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label_clase.pack(expand=True)

        values = ["(nada)"] + [x[1] for x in self.parent.inventario.simple_complete_query("Clases")]

        self.clase_list = ttk.Combobox(panel_clase, values=values)
        self.clase_list.config(state="readonly")
        self.clase_list.current(0)
        self.clase_list.pack(expand=True)

    
    def agregar_fila_2(self):
        # Lugar de Compra y Unidad
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Lugar de Compra
        panel_lugar = tk.Frame(panel, background=self.bgcolor)
        panel_lugar.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_lugar, text="Lugar de Compra:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = ["(nada)"] + [x[1] for x in self.parent.inventario.simple_complete_query("Lugares")]

        self.lugar_compra_list = ttk.Combobox(panel_lugar, values=values)
        self.lugar_compra_list.config(state="readonly")
        self.lugar_compra_list.current(0)
        self.lugar_compra_list.pack(expand=True)

        # Unidad
        panel_unidad = tk.Frame(panel, background=self.bgcolor)
        panel_unidad.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_unidad, text="Unidad:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = ["(nada)"] + [x[1] for x in self.parent.inventario.simple_complete_query("Unidades")]

        self.unidad_list = ttk.Combobox(panel_unidad, values=values)
        self.unidad_list.config(state="readonly")
        self.unidad_list.current(0)
        self.unidad_list.pack(expand=True)


    def agregar_fila_3(self):
        values = ["(nada)", "Mayor que", "Mayor Igual que", "Menor que", "Menor Igual que"]

        # Precio y Stock Minimo
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Precio
        panel_precio = tk.Frame(panel, background=self.bgcolor)
        panel_precio.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_precio, text="Precio Unitario:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        sub_panel2 = tk.Frame(panel_precio, background=self.bgcolor)
        sub_panel2.pack(expand=True, fill="both")

        self.cb_precio = ttk.Combobox(sub_panel2, values=values)
        self.cb_precio.config(state="readonly")
        self.cb_precio.current(0)
        self.cb_precio.pack(side="left", padx=3)

        self.precio_entry = comp.CampoTexto(sub_panel2, tipo="int")
        self.precio_entry.config(width=15)
        self.precio_entry.pack()

        # Stock Mínimo
        panel_stock_min = tk.Frame(panel, background=self.bgcolor)
        panel_stock_min.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_min, text="Stock Mínimo:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        sub_panel1 = tk.Frame(panel_stock_min, background=self.bgcolor)
        sub_panel1.pack(expand=True, fill="both")

        self.cb_stock_min = ttk.Combobox(sub_panel1, values=values)
        self.cb_stock_min.config(state="readonly")
        self.cb_stock_min.current(0)
        self.cb_stock_min.pack(side="left", padx=3)

        self.stock_min_entry = comp.CampoTexto(sub_panel1, tipo="int")
        self.stock_min_entry.config(width=15)
        self.stock_min_entry.pack(side="left")

    
    def agregar_fila_4(self):
        # Stock Deseado y Disponible
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Stock Deseado
        panel_stock_deseado = tk.Frame(panel, background=self.bgcolor)
        panel_stock_deseado.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_deseado, text="Stock Deseado:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        sub_panel1 = tk.Frame(panel_stock_deseado, background=self.bgcolor)
        sub_panel1.pack(expand=True, fill="both")

        values = ["(nada)", "Mayor que", "Mayor Igual que", "Menor que", "Menor Igual que"]

        self.cb_stock_max = ttk.Combobox(sub_panel1, values=values)
        self.cb_stock_max.config(state="readonly")
        self.cb_stock_max.current(0)
        self.cb_stock_max.pack(side="left", padx=3)

        self.stock_max_entry = comp.CampoTexto(sub_panel1, tipo="int")
        self.stock_max_entry.config(width=15)
        self.stock_max_entry.pack(side="left")


        # Stock Disponible
        panel_stock_disponible = tk.Frame(panel, background=self.bgcolor)
        panel_stock_disponible.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_disponible, text="Stock Actual:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        sub_panel2 = tk.Frame(panel_stock_disponible, background=self.bgcolor)
        sub_panel2.pack(expand=True, fill="both")

        self.cb_stock_actual = ttk.Combobox(sub_panel2, values=values)
        self.cb_stock_actual.config(state="readonly")
        self.cb_stock_actual.current(0)
        self.cb_stock_actual.pack(side="left", padx=3)

        self.stock_actual_entry = comp.CampoTexto(sub_panel2, tipo="int")
        self.stock_actual_entry.config(width=15)
        self.stock_actual_entry.pack(side="left")


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=15, fill="both")

        self.b_agregar = comp.Boton(panel, text="Filtrar", command=self.filtrar)
        self.b_agregar.pack(expand=True, side="left")

        self.b_volver = comp.Boton(panel, text="Cancelar", command=self.destroy)
        self.b_volver.pack(expand=True, side="left")

    def filtrar(self):
        datos = []

        if self.nombre_entry.get() == "":
            datos.append(None)
        else:
            datos.append(self.nombre_entry.get())

        if self.clase_list.get() != "(nada)":
            datos.append(self.parent.inventario.obtener_id_por_nombre("Clases", "ID_clase", "nombre_clase", self.clase_list.get()))
        else:
            datos.append(None)

        if self.lugar_compra_list.get() != "(nada)":
            datos.append(self.parent.inventario.obtener_id_por_nombre("Lugares", "ID_lugar", "nombre_lugar", self.lugar_compra_list.get()))
        else:
            datos.append(None)

        if self.unidad_list.get() != "(nada)":
            datos.append(self.parent.inventario.obtener_id_por_nombre("Unidades", "ID_unidad", "nombre_unidad", self.unidad_list.get()))
        else:
            datos.append(None)

        if self.precio_entry.get() != "" and self.cb_precio.get() != "(nada)":
            precio = []
            match self.cb_precio.get():
                case "Mayor que":
                    precio.append(">")
                case "Mayor igual que":
                    precio.append(">=")
                case "Menor que":
                    precio.append("<")
                case "Menor igual que":
                    precio.append("<=")
            precio.append(int(self.precio_entry.get()))
            datos.append(precio)
        else:
            datos.append(None)

        if self.stock_min_entry.get() != "" and self.cb_stock_min.get() != "(nada)":
            min = []
            match self.cb_stock_min.get():
                case "Mayor que":
                    min.append(">")
                case "Mayor igual que":
                    min.append(">=")
                case "Menor que":
                    min.append("<")
                case "Menor igual que":
                    min.append("<=")
            min.append(int(self.stock_min_entry.get()))
            datos.append(min)
        else:
            datos.append(None)

        if self.stock_max_entry.get() != "" and self.cb_stock_max.get() != "(nada)":
            max = []
            match self.cb_stock_max.get():
                case "Mayor que":
                    max.append(">")
                case "Mayor igual que":
                    max.append(">=")
                case "Menor que":
                    max.append("<")
                case "Menor igual que":
                    precio.append("<=")
            max.append(int(self.stock_max_entry.get()))
            datos.append(max)
        else:
            datos.append(None)

        if self.stock_actual_entry.get() != "" and self.cb_stock_actual.get() != "(nada)":
            act = []
            match self.cb_stock_actual.get():
                case "Mayor que":
                    act.append(">")
                case "Mayor igual que":
                    act.append(">=")
                case "Menor que":
                    act.append("<")
                case "Menor igual que":
                    act.append("<=")
            act.append(int(self.stock_actual_entry.get()))
            datos.append(act)
        else:
            datos.append(None)
        

        self.destroy()
        self.parent.actualizar_tabla(datos)


class Modificar(ven.VentanaTopLevel):
    def __init__(self, parent, id_producto, nombre, clase, lugar, unidad, precio, stock_min, stock_max, stock_act):
        super().__init__(parent,titulo_ventana = "Filtrar", titulo = "Filtrar")

        self.parent = parent

        self.id_producto = id_producto
        self.nombre = nombre
        self.clase = clase
        self.lugar = lugar
        self.unidad = unidad
        self.precio = precio
        self.stock_min = stock_min
        self.stock_max = stock_max
        self.stock_act = stock_act

        self.configurar_ventana()

    
    def configurar_ventana(self):
        ancho = 460
        alto = 625

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.agregar_titulo()

        self.panel_data = tk.Frame(self, background=self.bgcolor)
        self.panel_data.pack(expand=True, fill="both")

        self.agregar_fila_1()
        self.agregar_fila_2()
        self.agregar_fila_3()
        self.agregar_fila_4()

        self.agregar_botones_opciones()

        self.centrar_ventana()


    def agregar_fila_1(self):
        # Nombre y Clase
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Nombre
        panel_nombre = tk.Frame(panel, background=self.bgcolor)
        panel_nombre.pack(expand=True, fill="both", side="left")

        label_nombre = tk.Label(panel_nombre, text="Nombre:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label_nombre.pack(expand=True)

        self.nombre_entry = comp.CampoTexto(panel_nombre)
        self.nombre_entry.config(width=25)
        self.nombre_entry.set(self.nombre)
        self.nombre_entry.pack(expand=True)

        self.label_error_nombre = tk.Label(panel_nombre, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_nombre.pack(expand=True)

        # Clase
        panel_clase = tk.Frame(panel, background=self.bgcolor)
        panel_clase.pack(expand=True, fill="both", side="left")

        label_clase = tk.Label(panel_clase, text="Clase:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label_clase.pack(expand=True)

        values = [x[1] for x in self.parent.inventario.simple_complete_query("Clases")]

        self.clase_list = ttk.Combobox(panel_clase, values=values)
        self.clase_list.config(state="readonly")
        index = self.clase_list['values'].index(self.clase)
        self.clase_list.current(index)
        self.clase_list.pack(expand=True)

    
    def agregar_fila_2(self):
        # Lugar de Compra y Unidad
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Lugar de Compra
        panel_lugar = tk.Frame(panel, background=self.bgcolor)
        panel_lugar.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_lugar, text="Lugar de Compra:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = [x[1] for x in self.parent.inventario.simple_complete_query("Lugares")]

        self.lugar_compra_list = ttk.Combobox(panel_lugar, values=values)
        self.lugar_compra_list.config(state="readonly")
        index = self.lugar_compra_list['values'].index(self.lugar)
        self.lugar_compra_list.current(index)
        self.lugar_compra_list.pack(expand=True)

        # Unidad
        panel_unidad = tk.Frame(panel, background=self.bgcolor)
        panel_unidad.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_unidad, text="Unidad:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        values = [x[1] for x in self.parent.inventario.simple_complete_query("Unidades")]

        self.unidad_list = ttk.Combobox(panel_unidad, values=values)
        self.unidad_list.config(state="readonly")
        index = self.unidad_list['values'].index(self.unidad)
        self.unidad_list.current(index)
        self.unidad_list.pack(expand=True)


    def agregar_fila_3(self):
        # Precio y Stock Minimo
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Precio
        panel_precio = tk.Frame(panel, background=self.bgcolor)
        panel_precio.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_precio, text="Precio Unitario:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.precio_entry = comp.CampoTexto(panel_precio, tipo="int")
        self.precio_entry.config(width=15)
        self.precio_entry.set(self.precio)
        self.precio_entry.pack()

        self.label_error_precio = tk.Label(panel_precio, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_precio.pack(expand=True)

        # Stock Mínimo
        panel_stock_min = tk.Frame(panel, background=self.bgcolor)
        panel_stock_min.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_min, text="Stock Mínimo:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_min_entry = comp.CampoTexto(panel_stock_min, tipo="int")
        self.stock_min_entry.config(width=15)
        self.stock_min_entry.set(self.stock_min)
        self.stock_min_entry.pack()

        self.label_error_min = tk.Label(panel_stock_min, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_min.pack(expand=True)

    
    def agregar_fila_4(self):
        # Stock Deseado y Disponible
        panel = tk.Frame(self.panel_data, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=15)

        # Stock Deseado
        panel_stock_deseado = tk.Frame(panel, background=self.bgcolor)
        panel_stock_deseado.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_deseado, text="Stock Deseado:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_max_entry = comp.CampoTexto(panel_stock_deseado, tipo="int")
        self.stock_max_entry.config(width=15)
        self.stock_max_entry.set(self.stock_max)
        self.stock_max_entry.pack()

        self.label_error_max = tk.Label(panel_stock_deseado, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_max.pack(expand=True)

        # Stock Disponible
        panel_stock_disponible = tk.Frame(panel, background=self.bgcolor)
        panel_stock_disponible.pack(expand=True, fill="both", side="left")

        label = tk.Label(panel_stock_disponible, text="Stock Actual:", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True)

        self.stock_actual_entry = comp.CampoTexto(panel_stock_disponible, tipo="int")
        self.stock_actual_entry.config(width=15)
        self.stock_actual_entry.set(self.stock_act)
        self.stock_actual_entry.pack()

        self.label_error_stock = tk.Label(panel_stock_disponible, background=self.bgcolor, foreground="red", font=(self.font, 16), text="")
        self.label_error_stock.pack(expand=True)


    def agregar_botones_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, pady=15, fill="both")

        self.b_modificar = comp.Boton(panel, text="Aplicar\nCambios", command=self.modificar_producto)
        self.b_modificar.pack(expand=True, side="left")

        self.b_volver = comp.Boton(panel, text="Volver", command=self.destroy)
        self.b_volver.pack(expand=True, side="left")


    def modificar_producto(self):
        is_valid = 0

        if self.nombre_entry.get() == "":
            self.label_error_nombre.config(text="* Campo Obligatorio")
        else:
            self.label_error_nombre.config(text="")
            is_valid+=1

        if self.precio_entry.get() == "":
            self.label_error_precio.config(text="* Campo Obligatorio")
        else:
            self.label_error_precio.config(text="")
            is_valid+=1

        if self.stock_min_entry.get() == "":
            self.label_error_min.config(text="* Campo Obligatorio")
        else:
            self.label_error_min.config(text="")
            is_valid+=1

        if self.stock_max_entry.get() == "":
            self.label_error_max.config(text="* Campo Obligatorio")
        else:
            self.label_error_max.config(text="")
            is_valid+=1

        if self.stock_actual_entry.get() == "":
            self.label_error_stock.config(text="* Campo Obligatorio")
        else:
            self.label_error_stock.config(text="")
            is_valid+=1

        if is_valid == 5:
            if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Modificar\neste Produto?", titulo_ventana="Modificar Producto").obtener_respuesta():
                id_clase = self.parent.inventario.obtener_id_por_nombre("Clases", "ID_clase", "nombre_clase", self.clase_list.get())
                id_lugar = self.parent.inventario.obtener_id_por_nombre("Lugares", "id_lugar", "nombre_lugar", self.lugar_compra_list.get())
                id_unidad = self.parent.inventario.obtener_id_por_nombre("Unidades", "id_unidad", "nombre_unidad", self.unidad_list.get())

                datos = [self.nombre_entry.get(), id_clase, id_lugar, id_unidad, self.precio_entry.get(), self.stock_min_entry.get(), self.stock_max_entry.get(), self.stock_actual_entry.get()]

                if self.parent.inventario.modificar_producto(self.parent.id_producto_seleccionado, datos, self.parent.datos["Local"]): 
                    ven.VentanaAvisoTL(self, texto="¡Producto Modificado con Éxito!", titulo_ventana="Modificar Producto").wait_window()
                    self.parent.datos["Usuario_Logueado"]["Registro"].insertar("Modificar", "Productos")
                    self.destroy()
                    self.parent.actualizar_tabla([None,None,None,None,None,None,None,None])
                else:
                    ven.VentanaAvisoTL(self, texto="No se pudo modificar el Producto.", titulo_ventana="Error").wait_window()