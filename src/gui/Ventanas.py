import tkinter as tk
from PIL import Image, ImageTk
import gui.Componentes as comp
import io

LOGO = "./img/logos/logo_128x128.png"
BGCOLOR = "#1e1e1e"
FGCOLOR = "white"
DEFAULT_FONT = "Impact"


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
        self.label_titulo.config(text=self.titulo)

    
    def configurar_logo_ruta(self, ruta_logo: str):
        self.logo = ruta_logo

        logo = Image.open(self.logo)
        logo_tk = ImageTk.PhotoImage(logo)

        self.label_logo.config(image=logo_tk)
        self.label_logo.image = logo_tk

    
    def configurar_logo_bytes(self, bytes, size: int=128):
        self.logo = io.BytesIO(bytes)

        logo = Image.open(self.logo)
        logo_rezized = logo.resize((size, size))
        logo_tk = ImageTk.PhotoImage(logo_rezized)

        self.label_logo.config(image=logo_tk)
        self.label_logo.image = logo_tk


    def centrar_ventana(self):
        # Llamar a este método despues de agregar todos los componentes a la ventana

        self.update_idletasks()

        ancho = self.winfo_width()
        alto = self.winfo_height()

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"+{x}+{y}")


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
        self.grab_set()


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
        self.label_logo.update()

    
    def centrar_ventana(self):
        # Llamar a este método despues de agregar todos los componentes a la ventana

        self.update_idletasks()

        ancho = self.winfo_width()
        alto = self.winfo_height()

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"+{x}+{y}")


class VentanaConfirmacion(tk.Toplevel):
    def __init__(self, master: tk.Widget, texto: str, titulo_ventana: str = "¿Deseas Continuar?", opcion1: str="Continuar", opcion2: str="Cancelar"):
        super().__init__(master)

        self.respuesta = None

        self.texto = texto
        self.titulo_ventana = titulo_ventana

        self.bgcolor = BGCOLOR
        self.fgcolor = FGCOLOR
        self.font = DEFAULT_FONT

        self.opcion1 = opcion1
        self.opcion2 = opcion2

        self._configurar_ventana()

        self.wait_window()
    

    def _configurar_ventana(self):
        self.config(background=self.bgcolor)
        self.title(self.titulo_ventana)
        self.resizable(False, False)

        self.geometry("450x250")

        self.grab_set()

        self._agregar_texto()
        self._agregar_opciones()
        self._centrar_ventana()


    def _agregar_texto(self):
        panel_logo = tk.Frame(self, background=self.bgcolor)
        panel_logo.pack(expand=True, fill="both")

        logo = Image.open(LOGO)
        logo_tk = ImageTk.PhotoImage(logo)

        label_logo = tk.Label(panel_logo, image=logo_tk, background=self.bgcolor)
        label_logo.image = logo_tk
        label_logo.pack(expand=True, side="left")

        label_titulo = tk.Label(panel_logo, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text=self.texto, anchor="center")
        label_titulo.pack(expand=True, side="left")

    def _agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both")

        boton1 = comp.Boton(panel, text=self.opcion1, command=self._continuar)
        boton1.pack(expand=True, side="left")

        boton2 = comp.Boton(panel, text=self.opcion2, command=self.destroy)
        boton2.pack(expand=True, side="left")


    def _centrar_ventana(self):
        # Actualiza la ventana para calcular correctamente su tamaño
        self.update_idletasks()

        ancho = self.winfo_width()
        alto = self.winfo_height()

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"+{x}+{y}")


    def _continuar(self):
        self.respuesta = True
        self.destroy()


    def obtener_respuesta(self):
        return self.respuesta




if __name__== "__main__":
    root = VentanaPrincipal()
    root.mainloop()