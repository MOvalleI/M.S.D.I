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
        self.id_seleccionado = None
        self.menu_seleccionado = ""
        self.tamaño_seleccionado = None

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

    
    def agregar_buscador(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Buscar Menu por Nombre", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16))
        label.pack()

        self.buscador_entry = tk.Entry(panel)
        self.buscador_entry.bind("<KeyRelease>", self.actualizar_tabla)
        self.buscador_entry.pack(expand=True)

    
    def agregar_tabla(self):
        panel_tabla = tk.Frame(self, background=self.bgcolor)
        panel_tabla.pack(expand=True, fill="both", pady=10)

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
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.menu_seleccionado_label = tk.Label(panel, text=f"Menu Seleccionado: {self.menu_seleccionado}", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16))
        self.menu_seleccionado_label.pack(expand=True)


    def agregar_cantidad(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.cantidad_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Cantidad: {self.cantidad}")
        self.cantidad_label.pack(side="left", expand=True, padx=5)

        self.b_aumentar = comp.Boton(panel, text="/\\")
        self.b_aumentar.config(command=self.aumentar_cantidad)
        self.b_aumentar.pack(side="left", expand=True, padx=5)

        self.b_disminuir = comp.Boton(panel, text="\\/")
        self.b_disminuir.config(command=self.dismiunir_cantidad, state="disabled")
        self.b_disminuir.pack(side="left", expand=True, padx=5)

    
    def agregar_precio(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.precio_label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Precio: ${self.precio}")
        self.precio_label.pack(side="left", expand=True)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_agregar = comp.Boton(panel, text="Agregar\nPedido")
        self.b_agregar.config(state="disabled", command=self.salir_y_agregar)
        self.b_agregar.pack(side="left", expand=True)

        self.b_cancelar = comp.Boton(panel, text="Cancelar")
        self.b_cancelar.config(command=self.destroy)
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
