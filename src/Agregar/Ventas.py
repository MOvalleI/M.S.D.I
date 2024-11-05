import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from PIL import Image, ImageTk
import Inicio as i

import Agregar.Pedido as p


LOGO = "./img/logo_128x128.png"
BGCOLOR = "#1e1e1e"
ANOTHERBGCOLOR = "black"
DEFAULT_FONT = "Segoe UI"


class Ventas(tk.Tk):
    def __init__(self, datos: dict):
        super().__init__()

        self.datos = datos
        self.datos_inventario = self.datos["Inventario"]

        self.precio_total = 0

        self.configurar_ventana()


    def configurar_ventana(self):
        self.title("Registrar Venta")
        self.resizable(False, False)
        self.config(background=BGCOLOR)
        self.geometry("500x700")

        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()

        self.label_precio = tk.Label(self, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16), text=f"Precio Total: ${self.precio_total}")
        self.label_precio.pack(expand=True)

        self.botones_modificar_tabla()
        self.botones_confirmacion()

        
    def agregar_titulo(self):
        panel_logo = tk.Frame(self, background=BGCOLOR)
        panel_logo.pack(expand=True)

        logo = Image.open(LOGO)
        logo_tk = ImageTk.PhotoImage(logo)

        label_logo = tk.Label(panel_logo, image=logo_tk, background=BGCOLOR)
        label_logo.image = logo_tk
        label_logo.grid(row=0, column=0, sticky="nsew", padx=30)

        label_logo = tk.Label(panel_logo, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 20), text="Registrar\nVenta", anchor="center")
        label_logo.grid(row=0, column=1, sticky="nsew", padx=30)


    def agregar_tabla(self):
        panel_tabla = tk.Frame(self, background=BGCOLOR)
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


    def botones_modificar_tabla(self):
        button_panel = tk.Frame(self, background=BGCOLOR)
        button_panel.pack(expand=True, fill="x")

        b_agregar = tk.Button(button_panel, text="Agregar\nPedido", command=self.abrir_agregar_pedido)
        b_agregar.pack(expand=True, side="left")

        b_modificar = tk.Button(button_panel, text="Modificar Pedido\nSeleccionado", anchor="center", state="disabled")
        b_modificar.pack(expand=True, side="left")

        b_modificar = tk.Button(button_panel, text="Eliminar Pedido\nSeleccionado", anchor="center", state="disabled")
        b_modificar.pack(expand=True, side="left")

    
    def botones_confirmacion(self):
        button_panel = tk.Frame(self, background=BGCOLOR)
        button_panel.pack(expand=True, fill="x")

        b_confirmar = tk.Button(button_panel, text="Registrar Venta", command=self.registrar_venta)
        b_confirmar.pack(expand=True, side="left")

        b_cancelar = tk.Button(button_panel, text="Cancelar", anchor="center", command=self.volver)
        b_cancelar.pack(expand=True, side="left")

    
    def abrir_agregar_pedido(self):
        p.Pedido(parent=self, datos_inventario=self.datos_inventario)


    def registrar_venta(self):
        if msg.askyesno(title="¿Registrar Venta?", message="¿Está seguro de registrar esta venta?"):
            self.datos["Inventario"] = self.datos_inventario
            self.volver()


    def agregar_pedido_a_tabla(self, id: int, values: tuple):
        self.tabla.insert("", tk.END, values=values, iid=id)
        self.precio_total += values[1]
        self.label_precio.config(text=f"Precio Total: ${self.precio_total}")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)
    

    
if __name__ == "__main__":
    a = Ventas()
    a.mainloop()