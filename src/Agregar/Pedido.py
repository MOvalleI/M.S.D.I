import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from PIL import Image, ImageTk
import BuscadorDB as bi


LOGO = "./img/logo_128x128.png"
BGCOLOR = "#1e1e1e"
ANOTHERBGCOLOR = "black"
DEFAULT_FONT = "Segoe UI"


class Pedido(tk.Toplevel):
    def __init__(self, parent: tk.Tk, datos_inventario: dict):
        super().__init__(master=parent)

        self.parent = parent

        self.datos_inventario = datos_inventario

        self.cantidad = 1
        self.precio_individual = 0
        self.precio = 0
        self.id_seleccionado = None
        self.menu_seleccionado = ""
        self.tamaño_seleccionado = None

        self.is_selected = False

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.grab_set()
        self.title("Agregar Pedido")
        self.config(background=BGCOLOR)

        self.agregar_titulo()
        self.agregar_buscador()
        self.agregar_tabla()
        self.agregar_menu_seleccionado()
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

        label_logo = tk.Label(panel_logo, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 20), text="Agregar\nPedido", anchor="center")
        label_logo.grid(row=0, column=1, sticky="nsew", padx=30)

    
    def agregar_buscador(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both", pady=20)

        label = tk.Label(panel, text="Buscar Menu por Nombre", background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16))
        label.pack()

        self.buscador_entry = tk.Entry(panel)
        self.buscador_entry.bind("<KeyRelease>", self.actualizar_tabla)
        self.buscador_entry.pack(expand=True)

    
    def agregar_tabla(self):
        panel_tabla = tk.Frame(self, background=BGCOLOR)
        panel_tabla.pack(expand=True, fill="both")

        panel_tabla.grid_rowconfigure(0, weight=1)
        panel_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(panel_tabla, columns=("Nombre", "Precio", "Tamaño"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Tamaño", text="Tamaño")

        self.tabla.column("Nombre", width=100)
        self.tabla.column("Precio", width=50)
        self.tabla.column("Tamaño", width=50)

        self.scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_elemento)

        self.actualizar_tabla(event=None)

    
    def agregar_menu_seleccionado(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.menu_seleccionado_label = tk.Label(panel, text=f"Menu Seleccionado: {self.menu_seleccionado}", background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16))
        self.menu_seleccionado_label.pack(expand=True)


    def agregar_cantidad(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.cantidad_label = tk.Label(panel, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16), text=f"Cantidad: {self.cantidad}")
        self.cantidad_label.pack(side="left", expand=True)

        self.b_aumentar = tk.Button(panel, text="/\\", command=self.aumentar_cantidad)
        self.b_aumentar.pack(side="left", expand=True)

        self.b_disminuir = tk.Button(panel, text="\\/", command=self.dismiunir_cantidad)
        self.b_disminuir.pack(side="left", expand=True)

    
    def agregar_precio(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.precio_label = tk.Label(panel, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16), text=f"Precio: ${self.precio}")
        self.precio_label.pack(side="left", expand=True)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=BGCOLOR)
        panel.pack(expand=True, fill="both")

        self.b_agregar = tk.Button(panel, text="Agregar\nPedido", anchor="center", state="disabled", command=self.salir_y_agregar)
        self.b_agregar.pack(side="left", expand=True)

        self.b_cancelar = tk.Button(panel, text="Cancelar", anchor="center", command=self.destroy)
        self.b_cancelar.pack(side="left", expand=True)


    def actualizar_tabla(self, event):
        self.tabla.delete(*self.tabla.get_children())

        if self.buscador_entry.get() == "":
            for id_menu in self.datos_inventario.Menu.keys():
                nombre = self.datos_inventario.Menu[id_menu][0]
                precio = self.datos_inventario.Menu[id_menu][1]
                tamaño = bi.BuscadorDB.buscar_tamano_por_id(self.datos_inventario.Tamaños, self.datos_inventario.Menu[id_menu][3])

                self.tabla.insert("", tk.END, iid=id_menu, values=(nombre, precio, tamaño))
        else:
            for id_menu in self.datos_inventario.Menu.keys():
                nombre = self.datos_inventario.Menu[id_menu][0]
                if self.buscador_entry.get().lower() in nombre.lower():
                    precio = self.datos_inventario.Menu[id_menu][1]
                    tamaño = bi.BuscadorDB.buscar_tamano_por_id(self.datos_inventario.Tamaños, self.datos_inventario.Menu[id_menu][3])

                    self.tabla.insert("", tk.END, iid=id_menu, values=(nombre, precio, tamaño))


    def seleccionar_elemento(self, event):
        self.id_seleccionado = self.tabla.selection()[0]  

        
        item = self.tabla.item(self.id_seleccionado)
        valores = item['values']

        self.menu_seleccionado = valores[0]
        self.precio_individual = valores[1]
        self.tamaño_seleccionado = valores[2]

        self.cantidad = 1
        self.precio = self.precio_individual

        if not self.is_selected:
            self.is_selected = True
            self.b_agregar.config(state="active")

        self.menu_seleccionado_label.config(text=f"Menu Seleccionado: {self.menu_seleccionado}")
        self.cantidad_label.config(text=f"Cantidad: {self.cantidad}")
        self.precio_label.config(text=f"Precio: ${self.precio}")


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


    def salir_y_agregar(self):
        values = (self.menu_seleccionado, self.precio, self.cantidad, self.tamaño_seleccionado)

        self.destroy()
        self.parent.agregar_pedido_a_tabla(id=self.id_seleccionado, values=values)
