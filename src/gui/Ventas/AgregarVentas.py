import tkinter as tk
import tkinter.messagebox as msg
import gui.Inicio as i
import gui.Ventas.ModificarPedido as mp
import gui.Ventanas as ven
import gui.Ventas.AgregarPedido as p
import gui.Componentes as comp


class AgregarVentas(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Registrar\nVenta", titulo_ventana="Registrar Venta")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.precio_total = 0

        self.menu_seleccionado = None
        self.cantidad_seleccionada = None
        self.precio_seleccionado = None
        self.id_seleccionado = None

        self.precio_modificado = False

        self.datos_venta = []

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()

        self.label_precio = tk.Label(self, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Precio Total: ${self.precio_total}")
        self.label_precio.pack(expand=True)

        self.botones_modificar_tabla()
        self.botones_confirmacion()

        self.centrar_ventana()


    def agregar_tabla(self):
        panel_tabla = tk.Frame(self, background=self.bgcolor)
        panel_tabla.pack(expand=True, fill="both", pady=10)

        panel_tabla.grid_rowconfigure(0, weight=1)
        panel_tabla.grid_columnconfigure(0, weight=1)

        encabezados = ("Nombre", "Precio", "Cantidad")

        self.tabla = comp.CustomTreeview(panel_tabla)
        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(self.datos_venta)

        self.tabla.grid(row=0, column=0, sticky="nsew")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_menu)


    def botones_modificar_tabla(self):
        button_panel = tk.Frame(self, background=self.bgcolor)
        button_panel.pack(expand=True, fill="x", pady=10)

        b_agregar = comp.Boton(button_panel, text="Agregar\nPedido")
        b_agregar.config(command=self.abrir_agregar_pedido)

        b_agregar.pack(expand=True, side="left")

        self.b_modificar = comp.Boton(button_panel, text="Modificar Pedido\nSeleccionado", command=self.abrir_modificar_pedido)
        self.b_modificar.deshabilitar_boton()
        self.b_modificar.pack(expand=True, side="left")

        self.b_eliminar = comp.Boton(button_panel, text="Eliminar Pedido\nSeleccionado", command=self.eliminar_menu)
        self.b_eliminar.deshabilitar_boton()
        self.b_eliminar.pack(expand=True, side="left")

    
    def botones_confirmacion(self):
        button_panel = tk.Frame(self, background=self.bgcolor)
        button_panel.pack(expand=True, fill="x", pady=10)

        b_confirmar = comp.Boton(button_panel, text="Registrar Venta")
        b_confirmar.config(command=self.registrar_venta)
        b_confirmar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(button_panel, text="Cancelar")
        b_cancelar.config(command=self.volver)
        b_cancelar.pack(expand=True, side="left")

    
    def abrir_agregar_pedido(self):
        p.Pedido(parent=self, datos_inventario=self.datos_inventario)


    def abrir_modificar_pedido(self):
        self.precio_total -= self.precio_seleccionado
        mp.ModificarPedido(parent=self, id=self.id_seleccionado, values=(self.menu_seleccionado, self.precio_seleccionado, self.cantidad_seleccionada))
        

    def registrar_venta(self):
        if ven.VentanaConfirmacion(self, texto="¿Está seguro de registrar esta venta?", titulo_ventana="Registrar Venta").obtener_respuesta():
            self.agregar_venta()
            ven.VentanaAvisoTL(self, texto="¡Venta Registrada con Exito!", titulo_ventana="Venta Registrada")
            self.datos["Usuario_Logueado"]["Registro"].insertar("Agregar", "Ventas")
            self.volver()

        
    def agregar_venta(self):
        pk = self.datos_inventario.obtener_pk("Ventas", "ID_venta")

        self.datos_inventario.insertar_venta(pk, self.datos["Local"])

        contenido = []

        for iid in self.tabla.get_children():
            # Obtener los valores de la fila (iid es el identificador de la fila)
            valores_fila = self.tabla.item(iid)['values']
            
            # Tomar el valor del iid y el valor de la segunda columna
            iid_valor = iid
            segunda_columna_valor = valores_fila[2]  # Suponiendo que la segunda columna está en el índice 1
            
            # Almacenar el iid y el valor de la segunda columna en la lista
            contenido.append((iid_valor, segunda_columna_valor))
    
        self.datos_inventario.insertar_contenido_venta(pk, contenido)
        


    def agregar_pedido_a_tabla(self, id: int, values: tuple):
        self.tabla.insert("", tk.END, values=values, iid=id)
        self.precio_total += values[1]
        self.label_precio.config(text=f"Precio Total: ${self.precio_total}")


    def actualizar_pedido(self, id: int, values: tuple):
        if self.precio_modificado:
            self.tabla.item(id, values=values)

            self.precio_total += values[1]

            self.id_seleccionado = None
            self.menu_seleccionado = None
            self.precio_seleccionado = None
            self.cantidad_seleccionada = None
            self.tamaño_seleccionado = None
        
            self.label_precio.config(text=f"Precio Total: ${self.precio_total}")
        else:
            self.precio_total += self.precio_seleccionado

        self.tabla.selection_remove(self.tabla.focus())
    

    def seleccionar_menu(self, event):
        if len(self.tabla.selection()) > 0:
            self.id_seleccionado = self.tabla.selection()[0]

            item = self.tabla.item(self.id_seleccionado)
            valores = item['values']

            self.menu_seleccionado = valores[0]
            self.precio_seleccionado = valores[1]
            self.cantidad_seleccionada = valores[2]
        else:
            self.id_seleccionado = None
            self.menu_seleccionado = None
            self.precio_seleccionado = None
            self.cantidad_seleccionada = None

        self.activar_botones()


    def eliminar_menu(self):
        self.tabla.delete(self.id_seleccionado)
        self.precio_total -= self.precio_seleccionado
        self.label_precio.config(text=f"Precio Total: {self.precio_total}")

        self.menu_seleccionado = None
        self.cantidad_seleccionada = None
        self.precio_seleccionado = None
        self.id_seleccionado = None

        self.activar_botones()

    
    def activar_botones(self):
        if self.menu_seleccionado:
            self.b_modificar.habilitar_boton()
            self.b_eliminar.habilitar_boton()
        else:
            self.b_modificar.deshabilitar_boton()
            self.b_eliminar.deshabilitar_boton()


    def quitar_focus(self):
        self.tabla.selection_remove(self.tabla.focus())


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)
    
