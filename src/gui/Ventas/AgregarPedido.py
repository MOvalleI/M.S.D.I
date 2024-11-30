import tkinter as tk
import tkinter.ttk as ttk
import data.BuscadorDB as bi
import gui.Ventanas as ven
import gui.Componentes as comp



class Pedido(ven.VentanaTopLevel):
    def __init__(self, parent: tk.Tk, datos_inventario: dict):
        super().__init__(parent=parent, titulo_ventana="Agregar Pedido", titulo="Agregar\nPedido")

        self.parent = parent

        self.datos_inventario = datos_inventario

        self.cantidad = 1
        self.precio_individual = 0
        self.precio = 0
        self.id_menu_seleccionado = None
        self.menu_seleccionado = ""

        self.is_selected = False

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_buscador()
        self.agregar_tabla()
        self.agregar_menu_seleccionado()
        self.agregar_cantidad()
        self.agregar_precio()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_buscador(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Buscar Menu por Nombre", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16))
        label.pack()

        self.buscador_entry = comp.CampoTexto(panel)
        self.buscador_entry.bind("<KeyRelease>", self.actualizar_tabla)
        self.buscador_entry.pack(expand=True)

    
    def agregar_tabla(self):
        panel_tabla = tk.Frame(self, background=self.bgcolor)
        panel_tabla.pack(expand=True, fill="both", pady=10)

        panel_tabla.grid_rowconfigure(0, weight=1)
        panel_tabla.grid_columnconfigure(0, weight=1)

        encabezados = ("ID Menu", "Nombre", "Precio")

        self.tabla = comp.CustomTreeview(panel_tabla)
        self.tabla.create_table(head=encabezados)
        self.tabla.add_data(data=self.datos_inventario.inner_join_menu_venta())
        self.tabla.añadir_scrollbarv(1)

        self.tabla.grid(row=0, column=0, sticky="nsew")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_elemento)

    
    def agregar_menu_seleccionado(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.menu_seleccionado_label = tk.Label(panel, text=f"Menu Seleccionado: {self.menu_seleccionado}", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16))
        self.menu_seleccionado_label.pack(expand=True)


    def agregar_cantidad(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.cantidad_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Cantidad: {self.cantidad}")
        self.cantidad_label.pack(side="left", expand=True, padx=5)

        self.b_aumentar = comp.Boton(panel, text="/\\", command=self.aumentar_cantidad)
        self.b_aumentar.deshabilitar_boton()
        self.b_aumentar.pack(side="left", expand=True, padx=5)

        self.b_disminuir = comp.Boton(panel, text="\\/", command=self.dismiunir_cantidad)
        self.b_disminuir.deshabilitar_boton()
        self.b_disminuir.pack(side="left", expand=True, padx=5)

    
    def agregar_precio(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.precio_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Precio: ${self.precio}")
        self.precio_label.pack(side="left", expand=True)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_agregar = comp.Boton(panel, text="Agregar\nPedido", command=self.salir_y_agregar)
        self.b_agregar.deshabilitar_boton()
        self.b_agregar.pack(side="left", expand=True)

        self.b_cancelar = comp.Boton(panel, text="Cancelar")
        self.b_cancelar.config(command=self.destroy)
        self.b_cancelar.pack(side="left", expand=True)


    def actualizar_tabla(self, event):
        self.id_menu_seleccionado = None
        self.menu_seleccionado = ""
        self.precio_individual = 0
        self.menu_seleccionado_label.config(text=f"Menu Seleccionado: {self.menu_seleccionado}")

        self.b_aumentar.deshabilitar_boton()
        self.b_disminuir.deshabilitar_boton()
        self.b_agregar.deshabilitar_boton()

        if self.buscador_entry.get() != "":
            self.tabla.recharge_data(self.datos_inventario.inner_join_menu_venta(like=self.buscador_entry.get()))
        else:
            self.tabla.recharge_data(self.datos_inventario.inner_join_menu_venta())


    def seleccionar_elemento(self, event):
        curItem = self.tabla.focus()
        valores = self.tabla.item(curItem)["values"]

        if valores:
            self.id_menu_seleccionado = valores[0]
            self.menu_seleccionado = valores[1]
            self.precio_individual = valores[2]

            self.cantidad = 1
            self.precio = self.precio_individual

            if not self.is_selected:
                self.is_selected = True
                self.b_agregar.habilitar_boton()
                self.b_aumentar.habilitar_boton()

            self.b_disminuir.deshabilitar_boton()
            self.menu_seleccionado_label.config(text=f"Menu Seleccionado: {self.menu_seleccionado}")
            self.cantidad_label.config(text=f"Cantidad: {self.cantidad}")
            self.precio_label.config(text=f"Precio: ${self.precio}") 
        else:
            self.is_selected = False


    def aumentar_cantidad(self):
        if self.cantidad == 1:
            self.b_disminuir.habilitar_boton()
        
        self.cantidad += 1
        self.precio += self.precio_individual

        self.cantidad_label.config(text=f"Cantidad: {self.cantidad}")
        self.precio_label.config(text=f"Precio: ${self.precio}")


    def dismiunir_cantidad(self):
        self.cantidad -= 1
        self.precio -= self.precio_individual
        self.cantidad_label.config(text=f"Cantidad: {self.cantidad}")
        self.precio_label.config(text=f"Precio: ${self.precio}")
        
        if self.cantidad == 1:
            self.b_disminuir.deshabilitar_boton()


    def salir_y_agregar(self):
        values = (self.menu_seleccionado, self.precio, self.cantidad)

        self.destroy()
        self.parent.agregar_pedido_a_tabla(id=self.id_menu_seleccionado, values=values)
