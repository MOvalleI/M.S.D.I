import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from PIL import Image, ImageTk
import BuscadorDB as bi


LOGO = "./img/logo_128x128.png"
BGCOLOR = "#1e1e1e"
ANOTHERBGCOLOR = "black"
DEFAULT_FONT = "Segoe UI"


class ModificarPedido(tk.Toplevel):
    def __init__(self, parent: tk.Tk, id: int, values: tuple):
        super().__init__(master = parent)
        
        self.parent = parent

        self.id = id

        self.nombre = values[0]
        self.precio = values[1]
        self.cantidad = values[2]
        self.tamaño = values[3]

        self.precio_individual = int(self.precio / self.cantidad)

        self.configurar_ventana()
    
    def configurar_ventana(self):
        self.title("Modificar Pedido")

        self.agregar_titulo()
        self.agregar_nombre()
        self.agregar_cantidad()
        self.agregar_precio()
        self.agregar_opciones()


    def agregar_titulo(self):
        panel_logo = tk.Frame(self, background=BGCOLOR)
        panel_logo.pack(expand=True)

        logo = Image.open(LOGO)
        logo_tk = ImageTk.PhotoImage(logo)

        label_logo = tk.Label(panel_logo, image=logo_tk, background=BGCOLOR)
        label_logo.image = logo_tk
        label_logo.grid(row=0, column=0, sticky="nsew", padx=30)

        label_logo = tk.Label(panel_logo, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 20), text="Modificar\nPedido", anchor="center")
        label_logo.grid(row=0, column=1, sticky="nsew", padx=30)

    
    def agregar_nombre(self):
        panel_datos = tk.Frame(self, background=BGCOLOR)
        panel_datos.pack(expand=True, fill="both")

        texto_nombre = f"Menu Seleccionado: {self.nombre}"
        nombre_label = tk.Label(panel_datos, background=BGCOLOR, foreground="white", anchor="center", font=(DEFAULT_FONT, 16), text=texto_nombre)
        nombre_label.pack(expand=True)

    
    def agregar_cantidad(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.cantidad_label = tk.Label(panel, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16), text=f"Cantidad: {self.cantidad}")
        self.cantidad_label.pack(side="left", expand=True)

        self.b_aumentar = tk.Button(panel, text="/\\", command=self.aumentar_cantidad)
        self.b_aumentar.pack(side="left", expand=True)

        self.b_disminuir = tk.Button(panel, text="\\/", command=self.dismiunir_cantidad, state="disabled")
        self.b_disminuir.pack(side="left", expand=True)

    
    def agregar_precio(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.precio_label = tk.Label(panel, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16), text=f"Precio: ${self.precio}")
        self.precio_label.pack(side="left", expand=True)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.b_agregar = tk.Button(panel, text="Modificar", anchor="center", command=self.salir_y_modificar)
        self.b_agregar.pack(side="left", expand=True)

        self.b_cancelar = tk.Button(panel, text="Cancelar", anchor="center", command=self.destroy)
        self.b_cancelar.pack(side="left", expand=True)


    def aumentar_cantidad(self):
        if self.cantidad == 1:
            self.b_disminuir.config(state="active")
        
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
            self.b_disminuir.config(state="disabled")


    def salir_y_modificar(self):
        values = (self.nombre, self.precio, self.cantidad, self.tamaño)

        self.destroy()
        self.parent.actualizar_pedido(id=self.id, values=values)



