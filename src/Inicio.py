import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import Login
import Agregar.Ventas as av

LOGO = "./img/logo_128x128.png"

IMG_VENTAS = "./img/ventas.png"
IMG_MENU = "./img/menu.png"
IMG_INVENTARIO = "./img/inventario.png"

BGCOLOR = "#1e1e1e"
ANOTHERBGCOLOR = "black"
DEFAULT_FONT = "Segoe UI"

BGBUTTON = "gray"
FGBUTTON = "white"

class Inicio(tk.Tk):
    def __init__(self, datos: dict):
        super().__init__()

        self.datos = datos

        self.usuario_logueado = datos["Usuario_Logueado"]["Nombre"]
        self.rol_usuario = datos["Usuario_Logueado"]["Rol"]

        self.opciones_seleccionada = "Ventas"

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.title("Inicio")
        self.geometry("500x600")
        self.resizable(False, False)
        self.config(background=BGCOLOR)
        self.protocol("WM_DELETE_WINDOW", self.salir)

        self.agregar_titulo()
        self.agregar_botones_opciones()

    
    def agregar_titulo(self):
        panel_logo = tk.Frame(self, background=BGCOLOR)
        panel_logo.pack(expand=True)

        logo = Image.open(LOGO)
        logo_tk = ImageTk.PhotoImage(logo)

        label_logo = tk.Label(panel_logo, image=logo_tk, background=BGCOLOR)
        label_logo.image = logo_tk
        label_logo.grid(row=0, column=0, sticky="nsew", padx=30)

        label_logo = tk.Label(panel_logo, background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 20), text=f"Bienvenido\n{self.usuario_logueado}")
        label_logo.grid(row=0, column=1, sticky="nsew", padx=30)

    
    def agregar_botones_opciones(self):
        button_panel = tk.Frame(self, background=BGCOLOR)
        button_panel.pack(fill="x", expand=True)

        self.button_ventas = tk.Button(button_panel, text="Ver Opciones\nde Ventas", anchor="center", command=lambda: self.cambiar_opciones("Ventas"), background=BGBUTTON, foreground=FGBUTTON)
        self.button_menu = tk.Button(button_panel, text="Ver Opciones\nde Menu", anchor="center", command=lambda: self.cambiar_opciones("Menu"), background=BGBUTTON, foreground=FGBUTTON)
        self.button_inventario = tk.Button(button_panel, text="Ver Opciones\nde Inventario", anchor="center", command=lambda: self.cambiar_opciones("Inventario"), background=BGBUTTON, foreground=FGBUTTON)

        self.button_ventas.pack(expand=True, side="left")
        self.button_menu.pack(expand=True, side="left")
        self.button_inventario.pack(expand=True, side="left")

        self.agregar_panel_opciones()

        panel_opciones = tk.Frame(self, background=BGCOLOR)
        panel_opciones.pack(expand=True, fill="x", pady=20)

        self.button_ventas = tk.Button(panel_opciones, text="Perfil", anchor="center", command=lambda: self.cambiar_opciones("Ventas"), background=BGBUTTON, foreground=FGBUTTON)
        self.button_menu = tk.Button(panel_opciones, text="Cerrar\nSesión", anchor="center", command=self.cerrar_sesion, background=BGBUTTON, foreground=FGBUTTON)
        self.button_inventario = tk.Button(panel_opciones, text="Salir", anchor="center", command=self.salir, background=BGBUTTON, foreground=FGBUTTON)

        self.button_ventas.pack(side="left", expand=True)
        self.button_menu.pack(side="left", expand=True)
        self.button_inventario.pack(side="left", expand=True)


    def agregar_panel_opciones(self):
        self.panel_opciones = tk.Frame(self, background=BGCOLOR, pady=50)
        self.panel_opciones.pack(expand=True, fill="both")

        self.panel_opciones.grid_columnconfigure(0, weight=1)
        self.panel_opciones.grid_columnconfigure(1, weight=1)
        self.panel_opciones.grid_columnconfigure(2, weight=1)
        self.panel_opciones.grid_rowconfigure(0, weight=1)
        self.panel_opciones.grid_rowconfigure(1, weight=1)

        self.configurar_botones(self.panel_opciones)


    def configurar_botones(self, root: tk.Frame):
        self.boton_agregar = tk.Button(root, background=BGBUTTON, foreground=FGBUTTON)
        self.boton_ver = tk.Button(root, background=BGBUTTON, foreground=FGBUTTON)
        self.boton_eliminar = tk.Button(root, background=BGBUTTON, foreground=FGBUTTON)
        self.boton_modificar = tk.Button(root, background=BGBUTTON, foreground=FGBUTTON)

        match self.opciones_seleccionada:
            case "Ventas":
                logo = IMG_VENTAS
                agregar_text = "Registrar Venta"
                ver_text = "Ver Venta"
                eliminar_text = ""
                modificar_text = ""
                self.boton_agregar.config(command=self.abrir_agregar_ventas)
                self.boton_ver.config(command=None)
                self.boton_agregar.grid(row=0, column=1, rowspan=2)
                self.boton_ver.grid(row=0, column=2, rowspan=2)
            case "Menu": 
                logo = IMG_MENU
                agregar_text = "Agregar Menu"
                ver_text = "Ver Menu"
                eliminar_text = "Eliminar Menu"
                modificar_text = "Modificar Menu"
            case "Inventario": 
                logo = IMG_INVENTARIO
                agregar_text = "Agregar Inventario"
                ver_text = "Ver Inventario"
                eliminar_text = "Eliminar Inventario"
                modificar_text = "Modificar Inventario"

        icono = Image.open(logo)
        icono_resized = icono.resize((128, 128))
        icono_tk = ImageTk.PhotoImage(icono_resized)

        label = tk.Label(root, image=icono_tk, background=BGCOLOR)
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
        av.Ventas(datos=self.datos)

    
    def salir(self):
        if messagebox.askyesno(title="Salir", message="¿Seguro que deseas salir?"):
            self.destroy()

    
    def cerrar_sesion(self):
        if messagebox.askyesno(title="Salir", message="¿Seguro que deseas cerrar sesión?"):
            self.destroy()
            self.datos.pop("Usuario_Logueado", None)
            Login.Login(datos=self.datos)

    
if __name__ == "__main__":
    a = Inicio()
    a.mainloop()