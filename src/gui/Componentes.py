import tkinter as tk
import tkinter.ttk as ttk
import re
from PIL import Image, ImageTk

BUTTONACTIVEIMAGE = "./img/botones/botonsalchicha.png"
BUTTONDISABLEIMAGE = "./img/botones/botonsalchicha5.png"
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

        self.is_active = True

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


    def configurar(self, **kwargs):
        for clave, valor in kwargs.items():
            setattr(self, clave, valor)

        self._configurar_boton()

    
    def deshabilitar_boton(self):
        self.image = BUTTONDISABLEIMAGE
        self.image_tk = self._configurar_imagen()
        self.config(image=self.image_tk, command=self._funcion_vacia)
        self.update()
        self.is_active = False

    
    def habilitar_boton(self):
        self.image = BUTTONACTIVEIMAGE
        self.image_tk = self._configurar_imagen()
        self.config(image=self.image_tk, command=self.command)
        self.update()
        self.is_active = True


    def _funcion_vacia(self):
        pass




FLECHA_IZQUIERDA = "./img/botones/flecha-izquierda.png"
FLECHA_DERECHA = "./img/botones/flecha-derecha.png"
FLECHA_IZQUIERDA_DESHAB = "./img/botones/flecha_izquierda_deshab.png"
FLECHA_DERECHA_DESHAB = "./img/botones/flecha_derecha_deshab.png"


class BotonFlecha(tk.Button):
    """
    Esta clase configurará el tamaño y la imágen de un botón, asi como su fuente, 
    tamaño de letra y otras configuraciones.
    """
    def __init__(self, master: tk.Widget, direction: str, text: str="", width: int=100, height: int=50, image: str=BUTTONACTIVEIMAGE, font: str=BUTTONFONT, font_size: int=10, command=None):
        super().__init__(master=master)

        self.master = master
        self.text = text
        self.width = width
        self.height = height
        self.image = image
        self.font = font
        self.font_size = font_size
        self.command = command
        self.direction = direction

        self.is_active = True

        self._configurar_boton()


    def _configurar_boton(self):
        if self.direction == "izquierda":
            image_tk = self._configurar_imagen_fi()
            self.config(compound="left")
        else:
            image_tk = self._configurar_imagen_fd()
            self.config(compound="right")

        self.config(command=self.command)
        self.config(width=self.width, height=self.height)
        self.config(image=image_tk, borderwidth=0, background=BUTTONBG, highlightthickness=0, activebackground=BUTTONBG)
        self.config(cursor="hand2")
        self.config(text=self.text, foreground="white", font=(self.font, self.font_size, "bold"))
        self.image_tk = image_tk


    def _configurar_imagen_fi(self):
        imagen = Image.open(FLECHA_IZQUIERDA)
        imagen_resized = imagen.resize((self.width - 75, self.height))
        image_tk = ImageTk.PhotoImage(imagen_resized)
        return image_tk
    

    def _configurar_imagen_fid(self):
        imagen = Image.open(FLECHA_IZQUIERDA_DESHAB)
        imagen_resized = imagen.resize((self.width - 75, self.height))
        image_tk = ImageTk.PhotoImage(imagen_resized)
        return image_tk
    
    
    def _configurar_imagen_fd(self):
        imagen = Image.open(FLECHA_DERECHA)
        imagen_resized = imagen.resize((self.width - 75, self.height))
        image_tk = ImageTk.PhotoImage(imagen_resized)
        return image_tk
    
    
    def _configurar_imagen_fdd(self):
        imagen = Image.open(FLECHA_DERECHA_DESHAB)
        imagen_resized = imagen.resize((self.width - 75, self.height))
        image_tk = ImageTk.PhotoImage(imagen_resized)
        return image_tk


    def configurar(self, **kwargs):
        for clave, valor in kwargs.items():
            setattr(self, clave, valor)

        self._configurar_boton()

    
    def deshabilitar_boton(self):
        if self.direction == "izquierda":
            self.image = FLECHA_IZQUIERDA_DESHAB
            self.image_tk = self._configurar_imagen_fid()
        else:
            self.image = FLECHA_DERECHA_DESHAB
            self.image_tk = self._configurar_imagen_fdd()

        self.config(image=self.image_tk, command=self._funcion_vacia)
        self.update()
        self.is_active = False

    
    def habilitar_boton(self):
        if self.direction == "izquierda":
            self.image = FLECHA_IZQUIERDA
            self.image_tk = self._configurar_imagen_fi()
        else:
            self.image = FLECHA_DERECHA
            self.image_tk = self._configurar_imagen_fd()

        self.config(image=self.image_tk, command=self.command)
        self.update()
        self.is_active = True


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
        return re.match(r"^.*$", texto) is not None


    def validar_int(self, texto: str):
        return re.match("^[0-9]*$", texto) is not None


    def validar_float(self, texto: str):
        if texto == "" or re.match(r"^[0-9]+(\.[0-9]*)?$", texto):
            return True
        return False
    

    def set(self, texto):
        """
        Establece el texto que se muestra en el Campo de Texto.
        """

        self.delete('0', 'end')
        self.insert('0', texto)


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
            row_id = self.insert(parent='', index=tk.END, values=tuple(row))

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


class PatternUnlockApp(tk.Frame):
    def __init__(self, parent, pattern = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.radius = 20
        self.padding = 50

        self.pattern = pattern

        self.points = []
        self.lines = []
        self.selected_points = []
        self.current_line = None

        self.canvas = tk.Canvas(self, width=300, height=300, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.draw_grid()

        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw_grid(self):
        width = self.canvas.winfo_reqwidth()
        height = self.canvas.winfo_reqheight()

        step_x = (width - 2 * self.padding) // 2
        step_y = (height - 2 * self.padding) // 2

        for row in range(3):
            for col in range(3):
                x = self.padding + col * step_x
                y = self.padding + row * step_y
                point_id = self.canvas.create_oval(
                    x - self.radius, y - self.radius,
                    x + self.radius, y + self.radius,
                    fill="gray", outline="black"
                )
                self.points.append((point_id, x, y))

    def on_drag(self, event):
        for point_id, x, y in self.points:
            if point_id not in self.selected_points:
                if (x - self.radius <= event.x <= x + self.radius and
                        y - self.radius <= event.y <= y + self.radius):
                    self.selected_points.append(point_id)
                    self.canvas.itemconfig(point_id, fill="blue")
                    if len(self.selected_points) > 1:
                        last_x, last_y = self.points[self.selected_points[-2] - 1][1:]
                        self.lines.append(
                            self.canvas.create_line(last_x, last_y, x, y, fill="blue", width=2)
                        )
                    break

        if self.selected_points:
            last_x, last_y = self.points[self.selected_points[-1] - 1][1:]
            if self.current_line:
                self.canvas.delete(self.current_line)
            self.current_line = self.canvas.create_line(
                last_x, last_y, event.x, event.y, fill="blue", width=2
            )

    def on_release(self, event):
        for point in self.points:
            self.canvas.itemconfig(point[0], fill="gray")
        for line in self.lines:
            self.canvas.delete(line)
        if self.current_line:
            self.canvas.delete(self.current_line)
        
        selected_pattern = str(self.selected_points)

        if self.pattern:
            if selected_pattern == self.pattern:
                print(True)
            else:
                print(False)
        else:
            self.pattern = selected_pattern
            
        self.selected_points.clear()
        self.lines.clear()
        self.current_line = None

    def get_pattern(self):
        return self.pattern

    def set_pattern(self):
        self.pattern = None
