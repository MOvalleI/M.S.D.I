import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import gui.Login
import gui.Ventas.AgregarVentas as av
import gui.Ventanas as ven
import gui.Inventario.Agregar as iai
import gui.Inventario.Eliminar as iei
import gui.Componentes as comp
import gui.Menu.VisualizarMenu as vm
import gui.Ventas.VerVentas as vv


IMG_VENTAS = "./img/ventas.png"
IMG_MENU = "./img/menu.png"
IMG_INVENTARIO = "./img/inventario.png"

BGBUTTON = "gray"
FGBUTTON = "white"

class Inicio(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Inicio", titulo_ventana="Inicio")

        self.datos = datos

        self.usuario_logueado = datos["Usuario_Logueado"]["Nombre"]
        self.rol_usuario = datos["Usuario_Logueado"]["Rol"]

        self.opciones_seleccionada = "Ventas"

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.geometry("520x600")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.salir)

        self.agregar_titulo()
        self.agregar_botones_opciones()

    
    def agregar_botones_opciones(self):
        button_panel = tk.Frame(self, background=self.bgcolor)
        button_panel.pack(fill="x", expand=True)

        self.button_ventas = comp.Boton(button_panel, text="Ver Opciones\nde Ventas")
        self.button_ventas.config(command=lambda: self.cambiar_opciones("Ventas"))

        self.button_inventario = comp.Boton(button_panel, text="Ver Opciones\nde Inventario")
        self.button_inventario.config(command=lambda: self.cambiar_opciones("Inventario"))

        self.button_menu = comp.Boton(button_panel, text="Ver Opciones\nde Menu")
        self.button_menu.config(command=lambda: self.cambiar_opciones("Menu"))

        self.button_otros = comp.Boton(button_panel, text="Ver Opciones de\nOtros Datos")
        self.button_otros.config(command=lambda: self.cambiar_opciones("Otros"))

        self.button_ventas.pack(expand=True, side="left")
        self.button_menu.pack(expand=True, side="left")
        self.button_inventario.pack(expand=True, side="left")
        self.button_otros.pack(expand=True, side="left")

        self.agregar_panel_opciones()

        panel_opciones = tk.Frame(self, background=self.bgcolor)
        panel_opciones.pack(expand=True, fill="x", pady=20)

        self.button_perfil = comp.Boton(panel_opciones, text="Perfil")
        self.button_perfil.config(command=None)

        self.button_cerrar_sesion = comp.Boton(panel_opciones, text="Cerrar\nSesión")
        self.button_cerrar_sesion.config(command=self.cerrar_sesion)

        self.button_salir = comp.Boton(panel_opciones, text="Salir")
        self.button_salir.config(command=self.salir)

        self.button_perfil.pack(side="left", expand=True)
        self.button_cerrar_sesion.pack(side="left", expand=True)
        self.button_salir.pack(side="left", expand=True)


    def agregar_panel_opciones(self):
        self.panel_opciones = tk.Frame(self, background=self.bgcolor, pady=50, borderwidth=5)
        self.panel_opciones.pack(expand=True, fill="both")

        self.panel_opciones.grid_columnconfigure(0, weight=1)
        self.panel_opciones.grid_columnconfigure(1, weight=1)
        self.panel_opciones.grid_columnconfigure(2, weight=1)
        self.panel_opciones.grid_rowconfigure(0, weight=1)
        self.panel_opciones.grid_rowconfigure(1, weight=1)

        self.configurar_botones(self.panel_opciones)


    def configurar_botones(self, root: tk.Frame):
        self.boton_agregar = comp.Boton(root)
        self.boton_ver = comp.Boton(root)
        self.boton_eliminar = comp.Boton(root)
        self.boton_modificar = comp.Boton(root)

        match self.opciones_seleccionada:
            case "Menu": 
                logo = IMG_MENU
                agregar_text = "Agregar\nMenu"
                ver_text = "Ver\nMenu"
                eliminar_text = "Eliminar\nMenu"
                modificar_text = "Modificar\nMenu"
                self.boton_ver.config(command=self.abrir_ver_menu)
            case "Inventario": 
                logo = IMG_INVENTARIO
                agregar_text = "Agregar\nInventario"
                ver_text = "Ver\nInventario"
                eliminar_text = "Eliminar\nInventario"
                modificar_text = "Modificar\nInventario"
                self.boton_agregar.config(command=self.abrir_agregar_producto)
                self.boton_eliminar.config(command=self.abrir_eliminar_producto)
            case "Otros":
                logo = IMG_INVENTARIO
                agregar_text = "Agregar\nInventario"
                ver_text = "Ver\nInventario"
                eliminar_text = "Eliminar\nInventario"
                modificar_text = "Modificar\nInventario"
                self.boton_agregar.config(command=self.abrir_agregar_producto)
                self.boton_eliminar.config(command=self.abrir_eliminar_producto)
            case _:
                logo = IMG_VENTAS
                agregar_text = "Registrar\nVenta"
                ver_text = "Ver Ventas\nRegistradas"
                eliminar_text = ""
                modificar_text = ""
                self.boton_agregar.config(command=self.abrir_agregar_ventas)
                self.boton_ver.config(command=self.abrir_ver_ventas)
                self.boton_ver.config(command=None)
                self.boton_agregar.grid(row=0, column=1, rowspan=2)
                self.boton_ver.grid(row=0, column=2, rowspan=2)

        icono = Image.open(logo)
        icono_resized = icono.resize((128, 128))
        icono_tk = ImageTk.PhotoImage(icono_resized)

        label = tk.Label(root, image=icono_tk, background=self.bgcolor)
        label.image = icono_tk
        label.grid(row=0, column=0, rowspan=2, sticky="nswe")

        self.boton_agregar.config(text=agregar_text)
        self.boton_ver.config(text=ver_text)
        self.boton_eliminar.config(text=eliminar_text)
        self.boton_modificar.config(text=modificar_text)
        
        if self.rol_usuario==3 and self.opciones_seleccionada == "Inventario":
            self.boton_ver.grid(row=0, column=1, columnspan=2)
            self.boton_modificar.grid(row=1, column=1, columnspan=2)
        elif self.rol_usuario==3 and self.opciones_seleccionada == "Menu":
            self.boton_ver.grid(row=0, column=1, columnspan=2, rowspan=2)
        elif self.opciones_seleccionada == "Ventas":
            self.boton_agregar.grid(row=0, column=1, rowspan=2)
            self.boton_ver.grid(row=0, column=2, rowspan=2)
        else:
            self.boton_ver.grid(row=0, column=2)
            self.boton_modificar.grid(row=1, column=2)
            self.boton_agregar.grid(row=0, column=1)
            self.boton_eliminar.grid(row=1, column=1)
        

    def cambiar_opciones(self, tipo: str):
        for widget in self.panel_opciones.winfo_children():
            widget.destroy()  # Elimina cada widget del canvas

        self.opciones_seleccionada = tipo
        self.configurar_botones(self.panel_opciones)


    def abrir_agregar_ventas(self):
        self.destroy()
        av.AgregarVentas(datos=self.datos)


    def abrir_agregar_producto(self):
        self.destroy()
        iai.Agregar(datos=self.datos)

    
    def abrir_eliminar_producto(self):
        self.destroy()
        iei.Eliminar(datos=self.datos)


    def abrir_ver_menu(self):
        self.destroy()
        vm.VisualizarMenu(datos=self.datos)

    
    def abrir_ver_ventas(self):
        self.destroy()
        vv.VerVentas(datos=self.datos)
    
    
    def salir(self):
        if messagebox.askyesno(title="Salir", message="¿Seguro que deseas salir?"):
            self.destroy()

    
    def cerrar_sesion(self):
        if messagebox.askyesno(title="Salir", message="¿Seguro que deseas cerrar sesión?"):
            self.destroy()
            self.datos.pop("Usuario_Logueado", None)
            gui.Login.Login(datos=self.datos)

    
if __name__ == "__main__":
    a = Inicio()
    a.mainloop()