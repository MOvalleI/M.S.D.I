import tkinter as tk
from PIL import Image, ImageTk

LOGO = "./img/logo_128x128.png"
BGCOLOR = "#1e1e1e"
FGCOLOR = "white"
DEFAULT_FONT = "Segoe UI"


class VentanaPrincipal(tk.Tk):
    def __init__(self, logo: str=LOGO, layer: str="pack", titulo_ventana: str="Ventana Principal", titulo: str="Ventana", bgcolor: str=BGCOLOR, fgcolor: str=FGCOLOR, font: str = DEFAULT_FONT):
        super().__init__()

        self.titulo_ventana = titulo_ventana
        self.titulo = titulo

        self.bgcolor = bgcolor
        self.fgcolor = fgcolor

        self.logo = logo
        self.font = font

        self.layer = layer

        self.title(self.titulo_ventana)
        self.config(background=self.bgcolor)
        

    def agregar_titulo(self):
        self.panel_logo = tk.Frame(self, background=self.bgcolor)
        match self.layer:
            case "grid":
                self.panel_logo.grid(column=0, row=0)
            case "place":
                self.panel_logo.place(x=0, y=0)
            case _:
                self.panel_logo.pack(expand=True)

        logo = Image.open(self.logo)
        logo_tk = ImageTk.PhotoImage(logo)

        self.label_logo = tk.Label(self.panel_logo, image=logo_tk, background=self.bgcolor)
        self.label_logo.image = logo_tk
        self.label_logo.grid(row=0, column=0, sticky="nsew", padx=30)

        self.label_titulo = tk.Label(self.panel_logo, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 20), text=self.titulo)
        self.label_titulo.grid(row=0, column=1, sticky="nsew", padx=30)
        

    def configurar_titulo(self, texto: str):
        self.titulo = texto
        self.label_logo.config(text=self.titulo)

    
    def configurar_logo(self, ruta_logo: str):
        self.logo = ruta_logo

        logo = Image.open(self.logo)
        logo_tk = ImageTk.PhotoImage(logo)

        self.label_logo.config(image=logo_tk)
        self.label_logo.image = logo_tk


class VentanaTopLevel(tk.Toplevel):
    def __init__(self, parent: tk.Tk = None, logo: str=LOGO, layer: str="pack", titulo_ventana: str="Ventana Principal", titulo: str="Ventana", bgcolor: str=BGCOLOR, fgcolor: str=FGCOLOR, font: str = DEFAULT_FONT):
        super().__init__(parent)

        self.logo = logo
        self.titulo_ventana = titulo_ventana
        self.titulo = titulo
        self.layer = layer
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.font = font

        self._configurar_ventana()

    def _configurar_ventana(self):
        self.config(background=self.bgcolor)
        self.resizable(False, False)


    def agregar_titulo(self):
        self.panel_logo = tk.Frame(self, background=self.bgcolor)
        match self.layer:
            case "grid":
                self.panel_logo.grid(column=0, row=0)
            case "place":
                self.panel_logo.place(x=0, y=0)
            case _:
                self.panel_logo.pack(expand=True)

        logo = Image.open(self.logo)
        logo_tk = ImageTk.PhotoImage(logo)

        self.label_logo = tk.Label(self.panel_logo, image=logo_tk, background=self.bgcolor)
        self.label_logo.image = logo_tk
        self.label_logo.grid(row=0, column=0, sticky="nsew", padx=30)

        self.label_titulo = tk.Label(self.panel_logo, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 20), text=self.titulo)
        self.label_titulo.grid(row=0, column=1, sticky="nsew", padx=30)
        

    def configurar_titulo(self, texto: str):
        self.titulo = texto
        self.label_logo.config(text=self.titulo)

    
    def configurar_logo(self, ruta_logo: str):
        self.logo = ruta_logo

        logo = Image.open(self.logo)
        logo_tk = ImageTk.PhotoImage(logo)

        self.label_logo.config(image=logo_tk)
        self.label_logo.image = logo_tk


if __name__== "__main__":
    root = VentanaPrincipal()
    root.mainloop()