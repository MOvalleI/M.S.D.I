import tkinter as tk
import tkinter.ttk as ttk
import re
from PIL import Image, ImageTk

BUTTONACTIVEIMAGE = "./img/botonsalchicha.png"
BUTTONDISABLEIMAGE = "./img/botonsalchicha5.png"
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
    def __init__(self, master: tk.Widget, text: str="", width: int=125, height: int=50, image: str=BUTTONACTIVEIMAGE, font: str=BUTTONFONT, font_size: int=10, command=None):
        super().__init__(master=master)

        self.master = master
        self.text = text
        self.width = width
        self.height = height
        self.image = image
        self.font = font
        self.font_size = font_size
        self.command = command

        self._configurar_boton()


    def _configurar_boton(self):
        image_tk = self._configurar_imagen()
        self.config(command=self.command)
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

    
    def deshabilitar_boton(self):
        self.image = BUTTONDISABLEIMAGE
        self.image_tk = self._configurar_imagen()
        self.config(image=self.image_tk, command=self._funcion_vacia)
        self.update()

    
    def habilitar_boton(self):
        self.image = BUTTONACTIVEIMAGE
        self._configurar_imagen()
        self.config(image=self.image_tk, command=self.command)
        self.update()


    def _funcion_vacia(self):
        pass


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


class CustomTreeview(ttk.Treeview):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.parent = parent
        
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="white",
                             bordercolor="black",
                             lightcolor="black",
                             darkcolor="black")
        self.style.layout("Custom.Treeview", [('Treeview.field', {'sticky': 'nswe'})])
        self.configure(style="Custom.Treeview")

    def create_table(self, head, side='top', width=150) -> None:
        self.config(columns=head, show='headings')
        for col in head:
            self.column(col, anchor='center', width=width)
            self.heading(col, text=col, anchor='center')

    def add_data(self, data):
        for i, row in enumerate(data):
            row_id = self.insert(parent='', index=tk.END, values=row)

            tag = 'evenrow' if i % 2 == 0 else 'oddrow'

            self.tag_configure(tag, background='#d3d3d3' if tag == 'evenrow' else '#ffffff')

            self.item(row_id, tags=(tag,))

    def recharge_data(self, data):
        for item in self.get_children():
            self.delete(item)

        self.add_data(data)

    def añadir_scrollbarv(self, indicador):
        if indicador == 1 or indicador == 3:
            scrollbarv = tk.Scrollbar(self, orient='vertical', command=self.yview)
            scrollbarv.place(relx=1, rely=0, relheight=1, anchor='ne')
            self.configure(yscrollcommand=scrollbarv.set)
        
        if indicador == 2 or indicador == 3:
            scrollbarh = tk.Scrollbar(self, orient='horizontal', command=self.xview)
            scrollbarh.place(relx=0, rely=1, relwidth=1, anchor='sw')
            self.configure(xscrollcommand=scrollbarh.set)