import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
import tkcalendar


class VerVentas(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Ver Ventas\nRegistradas", titulo_ventana="Ver Ventas Registradas")

        self.datos = datos
        self.datos_ventas = self.datos["Inventario"]

        self.nombre_seleccionado = None

        self.venta_seleccionada = None
        self.precio_total_venta = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_tabla(self):
        encabezados = ["ID Venta", "Fecha de Realización", "Precio Total"]

        self.tabla = comp.CustomTreeview(self)
        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(self.datos_ventas.obtener_ventas(1))
        self.tabla.añadir_scrollbarv(1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_venta)

        self.tabla.pack(pady=10)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_ver_contenido = comp.Boton(panel, text="Ver Contenido\nde Venta", command=self.abrir_ver_contenido)
        self.b_ver_contenido.deshabilitar_boton()

        self.b_filtrar = comp.Boton(panel, text="Filtrar", command=self.abrir_filtrar)
        self.b_volver = comp.Boton(panel, text="Volver", command=self.volver)


        self.b_ver_contenido.pack(expand=True, side="left")
        self.b_filtrar.pack(expand=True, side="left")
        self.b_volver.pack(expand=True, side="left")

    
    def seleccionar_venta(self, event=None):
        curItem = self.tabla.focus()
        valores = self.tabla.item(curItem)["values"]

        if valores is not None:
            self.b_ver_contenido.habilitar_boton()
            self.venta_seleccionada = valores[0]
            self.precio_total_venta = valores[2]


    def abrir_ver_contenido(self):
        VerContenido(self, self.venta_seleccionada, 1, self.precio_total_venta)


    def abrir_filtrar(self):
        Filtrar(self)

    
    def actualizar_tabla(self, datos: list):
        data = self.datos_ventas.generar_query_con_filtros(datos[0],datos[1],datos[2],datos[3])
        self.tabla.recharge_data(data)


    def volver(self, e=None):
        self.destroy()
        i.Inicio(self.datos)


class VerContenido(ven.VentanaTopLevel):
    def __init__(self, parent: tk.Widget, id_venta, id_local, precio_total: int):
        super().__init__(parent, titulo="Contenido\nde Venta", titulo_ventana="Contenido de Venta")

        self.parent = parent
        self.venta = id_venta
        self.local = id_local
        self.precio = precio_total

        self.configurar_ventana()


    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_tabla()

        label = tk.Label(self, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 18), text=f"Precio Total: ${self.precio}")
        label.pack(expand=True, pady=10)

        b_volver = comp.Boton(self, text="Cerrar", command=self.destroy)
        b_volver.pack(expand=True, pady=10)

    
    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=("Menu", "Cantidad", "Precio x Cantidad"))
        self.tabla.add_data(self.parent.datos_ventas.obtener_contenido_venta(self.venta, self.local))
        self.tabla.añadir_scrollbarv(1)
        self.tabla.pack(expand=True, pady=10)


class Filtrar(ven.VentanaTopLevel):
    def __init__(self, parent = None):
        super().__init__(parent,titulo_ventana = "Filtrar", titulo = "Filtrar")

        self.fecha = None
        self.parent = parent

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_filtro_fecha()
        self.agregar_filtro_precio()

        b_vaciar = comp.Boton(self, text="Vaciar", command=self.vaciar)
        b_vaciar.pack(expand=True, pady=10)

        self.agregar_opciones()


    def agregar_filtro_fecha(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.label_fecha = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Buscar a Partir de: ")
        self.label_fecha.pack(expand=True)

        self.calendario = tkcalendar.Calendar(self, date_pattern="yyyy-mm-dd")
        self.calendario.pack(expand=True)
        self.calendario.bind("<<CalendarSelected>>", self.obtener_fecha)


    def obtener_fecha(self, event):
        # Obtener la fecha seleccionada
        fecha_seleccionada = self.calendario.get_date()
        # Actualizar la entrada principal con la fecha seleccionada
        self.fecha = fecha_seleccionada
        self.label_fecha.config(text=f"Buscar a Partir de: {self.fecha}")


    def agregar_filtro_precio(self):
        label = tk.Label(self, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Buscar por Precio:")
        label.pack(expand=True)

        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        valores = ["(nada)", "Mayor que","Mayor igual que","Menor que","Menor igual que"]

        self.cb = ttk.Combobox(panel, values=valores)
        self.cb.config(state="readonly")
        self.cb.current(0)
        self.cb.pack(side="left", padx=5)

        self.precio_entry = comp.CampoTexto(panel, tipo="int")
        self.precio_entry.config(width=25)
        self.precio_entry.pack(side="left", padx=5)
        
    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_aplicar = comp.Boton(panel, text="Aplicar\nFiltro", command=self.filtrar)
        b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")

    
    def vaciar(self):
        self.fecha = None
        self.label_fecha.config(text="Buscar a Partir de: ")
        self.cb.current(0)
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, "")

    def filtrar(self):
        datos = []

        if self.precio_entry.get() != "" and self.cb.get() != "(nada)":
            match self.cb.get():
                case "Mayor que":
                    datos.append(">")
                case "Mayor igual que":
                    datos.append(">=")
                case "Menor que":
                    datos.append("<")
                case "Menor igual que":
                    datos.append("<=")
            datos.append(int(self.precio_entry.get()))
        else:
            datos.append(None)
            datos.append(None)

        datos.append(self.fecha)
        datos.append(int(self.parent.datos["Local"]))

        self.destroy()
        self.parent.actualizar_tabla(datos)
