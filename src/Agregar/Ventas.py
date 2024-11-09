import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from PIL import Image, ImageTk
import Inicio as i
import Agregar.ModificarPedido as mp
import gui.Ventanas as ven

import Agregar.Pedido as p


LOGO = "./img/logo_128x128.png"
BGCOLOR = "#1e1e1e"
ANOTHERBGCOLOR = "black"
DEFAULT_FONT = "Segoe UI"


class Ventas(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Registrar\nVenta", titulo_ventana="Registrar Venta")

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.precio_total = 0

        self.menu_seleccionado = None
        self.cantidad_seleccionada = None
        self.precio_seleccionado = None
        self.tamaño_seleccionado = None
        self.id_seleccionado = None

        self.precio_modificado = False

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.config(background=self.bgcolor)
        self.geometry("500x700")

        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()

        self.label_precio = tk.Label(self, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=f"Precio Total: ${self.precio_total}")
        self.label_precio.pack(expand=True)

        self.botones_modificar_tabla()
        self.botones_confirmacion()


    def agregar_tabla(self):
        panel_tabla = tk.Frame(self, background=self.bgcolor)
        panel_tabla.pack(expand=True, fill="both")

        panel_tabla.grid_rowconfigure(0, weight=1)
        panel_tabla.grid_columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(panel_tabla, columns=("Nombre", "Precio", "Cantidad", "Tamaño"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Tamaño", text="Tamaño")

        self.tabla.column("Nombre", width=100)
        self.tabla.column("Precio", width=50)
        self.tabla.column("Cantidad", width=50)
        self.tabla.column("Tamaño", width=50)

        self.scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_menu)


    def botones_modificar_tabla(self):
        button_panel = tk.Frame(self, background=self.bgcolor)
        button_panel.pack(expand=True, fill="x")

        b_agregar = tk.Button(button_panel, text="Agregar\nPedido", command=self.abrir_agregar_pedido)
        b_agregar.pack(expand=True, side="left")

        self.b_modificar = tk.Button(button_panel, text="Modificar Pedido\nSeleccionado", anchor="center", state="disabled", command=self.abrir_modificar_pedido)
        self.b_modificar.pack(expand=True, side="left")

        self.b_eliminar = tk.Button(button_panel, text="Eliminar Pedido\nSeleccionado", anchor="center", state="disabled")
        self.b_eliminar.pack(expand=True, side="left")

    
    def botones_confirmacion(self):
        button_panel = tk.Frame(self, background=self.bgcolor)
        button_panel.pack(expand=True, fill="x")

        b_confirmar = tk.Button(button_panel, text="Registrar Venta", command=self.registrar_venta)
        b_confirmar.pack(expand=True, side="left")

        b_cancelar = tk.Button(button_panel, text="Cancelar", anchor="center", command=self.volver)
        b_cancelar.pack(expand=True, side="left")

    
    def abrir_agregar_pedido(self):
        p.Pedido(parent=self, datos_inventario=self.datos_inventario)


    def abrir_modificar_pedido(self):
        self.precio_total -= self.precio_seleccionado
        mp.ModificarPedido(parent=self, id=self.id_seleccionado, values=(self.menu_seleccionado, self.precio_seleccionado, self.cantidad_seleccionada, self.tamaño_seleccionado))
        

    def registrar_venta(self):
        if msg.askyesno(title="¿Registrar Venta?", message="¿Está seguro de registrar esta venta?"):
            self.datos["Inventario"] = self.datos_inventario
            self.volver()


    def agregar_pedido_a_tabla(self, id: int, values: tuple):
        self.tabla.insert("", tk.END, values=values, iid=id)
        self.precio_total += values[1]
        self.label_precio.config(text=f"Precio Total: ${self.precio_total}")


    def actualizar_pedido(self, id: int, values: tuple, event=None):
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
            self.tamaño_seleccionado = valores[3]
        else:
            self.id_seleccionado = None

            self.menu_seleccionado = None
            self.precio_seleccionado = None
            self.cantidad_seleccionada = None
            self.tamaño_seleccionado = None

        self.activar_botones()

    
    def actualizar_precio_total(self):
        pass

    
    def activar_botones(self):
        if self.menu_seleccionado:
            self.b_modificar.config(state="active")
            self.b_eliminar.config(state="active")
        else:
            self.b_modificar.config(state="disabled")
            self.b_eliminar.config(state="disabled")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)
    

    
if __name__ == "__main__":
    a = Ventas()
    a.mainloop()