import tkinter as tk
import tkinter.ttk as ttk
import re
from PIL import Image, ImageTk

BUTTONIMAGE = "./img/botonsalchicha.png"
BUTTONBG = "#1e1e1e"
BUTTONFG = "#3a110c"
BUTTONFONT = "Segoe UI"


"""
Módulo que contiene subclases de Widgets de tkinter, implementando
configuraciones especificas para el programa.
"""

class Boton(tk.Button):
    """
    Esta clase configurará el tamaño y la imágen de un botón, asi como su fuente, 
    tamaño de letra y otras configuraciones.
    """
    def __init__(self, master: tk.Widget, text: str="", width: int=125, height: int=50, image: str=BUTTONIMAGE, font: str=BUTTONFONT, font_size: int=10):
        super().__init__(master=master)

        self.master = master
        self.text = text
        self.width = width
        self.height = height
        self.image = image
        self.font = font
        self.font_size = font_size

        self._configurar_boton()


    def _configurar_boton(self):
        image_tk = self._configurar_imagen()
        self.config(width=self.width, height=self.height)
        self.config(image=image_tk, borderwidth=0, background=BUTTONBG, highlightthickness=0, activebackground=BUTTONBG)
        self.config(cursor="hand2")
        self.config(text=self.text, compound="center", foreground=BUTTONFG, font=(self.font, self.font_size, "bold"))
        self.image_tk = image_tk


    def _configurar_imagen(self):
        imagen = Image.open(self.image)
        imagen_resized = imagen.resize((self.width, self.height))
        image_tk = ImageTk.PhotoImage(imagen_resized)
        return image_tk


    def configurar(self, text: str=None, width: int=None, height: int=None, image: str=None, font: str=None, font_size: int=None):
        if text:
            self.text = text
        if width:
            self.width = width
        if height:
            self.height = height
        if image:
            self.image = image
        if font:
            self.font = font
        if font_size:
            self.font_size = font_size

        self._configurar_boton()


class CampoTexto(tk.Entry):
    """
    Subclase de tk.Entry que permite restringir
    el contenido que se ingresa al campo de texto.
    Por defecto, admite todo tipo de caracteres.

    Los tipos disponibles son:
        str: Permite ingresar todo tipo de caracteres, salvo aquellos caracteres que no sean vaĺidos dentro del programa.
        int: Permite ingresar solo números enteros positivos.
        float: Permite ingresar tanto números enteros positivos como números decimales positivos.
    """
    def __init__(self, master: tk.Widget, tipo: str="str"):
        super().__init__(master)

        self.master = master

        # El tipo restringe los caracteres que se pueden ingresar
        # Tipos validos: str, int, float
        self.tipo = tipo
        self.configurar_campo()


    def configurar_tipo(self, tipo: str):
        self.tipo = tipo
        self.configurar_campo()


    def configurar_campo(self):
        match self.tipo:
            case "str":
                cmd = (self.master.register(self.validar_str), "%P")
                self.config(validate="key", validatecommand=cmd)
            case "int":
                cmd = (self.master.register(self.validar_int), "%P")
                self.config(validate="key", validatecommand=cmd)
            case "float":
                cmd = (self.master.register(self.validar_float), "%P")
                self.config(validate="key", validatecommand=cmd)


    def validar_str(self, texto: str):
        return re.match("^[a-zA-Z0-9]*$", texto) is not None


    def validar_int(self, texto: str):
        return re.match("^[0-9]*$", texto) is not None


    def validar_float(self, texto: str):
        if texto == "" or re.match(r"^[0-9]+(\.[0-9]*)?$", texto):
            return True
        return False


class Lista(ttk.Combobox):
    """
    Clase en contrucción.
    Subclase de ttk.Combobox que integra funcionalidades de busqueda.
    """
