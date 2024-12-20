import tkinter as tk
import gui.Ventanas as ven
import gui.Componentes as comp


class ModificarPedido(ven.VentanaTopLevel):
    def __init__(self, parent: tk.Tk, id: int, values: tuple):
        super().__init__(parent=parent, titulo="Modificar\nPedido", titulo_ventana="Modificar Pedido")
        
        self.parent = parent

        self.id = id

        self.nombre = values[0]
        self.precio = values[1]
        self.cantidad = values[2]

        self.precio_individual = int(self.precio / self.cantidad)

        self.configurar_ventana()
    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.config(background=self.bgcolor)

        self.protocol("WM_DELETE_WINDOW",self.cancelar)

        self.agregar_titulo()
        self.agregar_nombre()
        self.agregar_cantidad()
        self.agregar_precio()
        self.agregar_opciones()
        self.activar_boton_disminuir()

        self.centrar_ventana()

    
    def agregar_nombre(self):
        panel_datos = tk.Frame(self, background=self.bgcolor)
        panel_datos.pack(expand=True, fill="both")

        texto_nombre = f"Menu Seleccionado: {self.nombre}"
        nombre_label = tk.Label(panel_datos, background=self.bgcolor, foreground=self.fgcolor, anchor="center", font=(self.font, 16), text=texto_nombre)
        nombre_label.pack(expand=True)

    
    def agregar_cantidad(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        self.cantidad_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Cantidad: {self.cantidad}")
        self.cantidad_label.pack(side="left", expand=True)

        self.b_aumentar = comp.Boton(panel, text="/\\", command=self.aumentar_cantidad)
        self.b_aumentar.pack(side="left", expand=True)

        self.b_disminuir = comp.Boton(panel, text="\\/", command=self.dismiunir_cantidad)
        if self.cantidad == 1:
            self.b_disminuir.deshabilitar_boton()
        self.b_disminuir.pack(side="left", expand=True)

    
    def agregar_precio(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        self.precio_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Precio: ${self.precio}")
        self.precio_label.pack(side="left", expand=True)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        self.b_agregar = comp.Boton(panel, text="Modificar")
        self.b_agregar.config(command=self.salir_y_modificar)
        self.b_agregar.pack(side="left", expand=True)

        self.b_cancelar = comp.Boton(panel, text="Cancelar")
        self.b_cancelar.config(command=self.cancelar)
        self.b_cancelar.pack(side="left", expand=True)


    def aumentar_cantidad(self):
        self.cantidad += 1
        self.precio += self.precio_individual

        self.cantidad_label.config(text=f"Cantidad: {self.cantidad}")
        self.precio_label.config(text=f"Precio: ${self.precio}")

        self.b_disminuir.habilitar_boton()


    def dismiunir_cantidad(self):
        self.cantidad -= 1
        self.precio -= self.precio_individual
        self.cantidad_label.config(text=f"Cantidad: {self.cantidad}")
        self.precio_label.config(text=f"Precio: ${self.precio}")
        
        if self.cantidad == 1:
            self.b_disminuir.deshabilitar_boton()

    
    def activar_boton_disminuir(self):
        if self.cantidad > 1:
            self.b_disminuir.config(state="active")


    def salir_y_modificar(self):
        self.parent.precio_modificado = True

        values = (self.nombre, self.precio, self.cantidad)

        self.destroy()
        self.parent.actualizar_pedido(id=self.id, values=values)

    
    def cancelar(self):
        self.destroy()



