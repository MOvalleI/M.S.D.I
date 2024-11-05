import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import io
import Inicio

LOGO = "./img/Letras El ricon de los 4 diablitos.png"

BG_IMAGE = "./img/Imagen fondo para login.png"
BGCOLOR = "#1e1e1e"
ANOTHERBGCOLOR = "black"
DEFAULT_FONT = "Segoe UI"

class Login(tk.Tk):
    def __init__(self, datos: dict):
        super().__init__()

        self.datos = datos

        self.datos_usuarios = self.datos["Usuarios"]

        self.usuarios = self.datos_usuarios.obtener_datos_usuarios()

        # Posiciones iniciales para dibujar los cuadrados en el canvas
        self.yPos = 20
        self.square_sides = 300 # Tamaño de los cuadrados

        # Tamaño del rectangulo donde se ingresan los datos
        self.rec_canv_width = 772
        self.rec_canv_height = 620

        # Panel Seleccionado
        self.selected_panel = None

        self.usuario_seleccionado = None
        self.id_usuario_seleccionado = None

        self.panel_login = None

        # Indica si se muestra o no la contraseña
        self.ocultar_passwd = True

        self.configurar_ventana()

    
    def configurar_ventana(self) -> None:
        self.title("Iniciar Sesión")
        self.geometry("1280x720")
        self.resizable(False, False)

        self.configure(background=BGCOLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)

        left_panel = self.crear_panel_izquierdo(root=self)
        left_panel.grid(column=0, row=0, sticky="nwse")

        right_panel = self.crear_panel_derecho(root=self)
        right_panel.grid(column=1, row=0, sticky="nswe", columnspan=2)

        self.bind("<MouseWheel>", self.accion_rueda_mouse)
        

    def crear_panel_izquierdo(self, root: tk.Tk) -> tk.Frame:
        panel = tk.Frame(root, background=BGCOLOR, borderwidth=10)

        panel.grid_rowconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=8)
        panel.grid_columnconfigure(0, weight=1)

        buscador = self.crear_panel_buscador(panel)
        buscador.grid(column=0, row=0)

        self.users_panel = self.crear_panel_usuarios(root=panel)
        self.users_panel.grid(column=0, row=1, sticky="nswe")

        return panel
    

    def crear_panel_buscador(self, root: tk.Frame) -> tk.Frame:
        panel = tk.Frame(root, background=BGCOLOR)

        titulo = tk.Label(panel, text="Iniciar Sesión", anchor="center", background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 24))
        titulo.pack(pady=5)
        
        label = tk.Label(panel, text="Buscar Usuario:", anchor="center", background=BGCOLOR, foreground="white", font=(DEFAULT_FONT, 16))
        label.pack(pady=5)

        self.users_entry = tk.Entry(panel)
        self.users_entry.pack()
        self.users_entry.bind("<KeyRelease>", lambda event: self.buscar())

        return panel


    def crear_panel_usuarios(self, root: tk.Frame) -> tk.Frame:
        panel = tk.Frame(root, background=BGCOLOR)

        style = ttk.Style(root)
        style.theme_use("alt")  # Cambiar el tema (clam permite más personalización)
        style.configure("Vertical.TScrollbar", background=ANOTHERBGCOLOR, troughcolor="gray", arrowcolor="white", foreground="white")

        self.canvas = tk.Canvas(panel, width=0, height=0, background=BGCOLOR, border=0)
        self.canvas.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.canvas.config(yscrollcommand=self.scrollbar.set) 
        
        for id in self.usuarios.keys():
            self.agregar_usuario(self.canvas, id, self.usuarios[id][0], self.square_sides, self.yPos - 10)
            self.yPos += self.square_sides + 10

        self.canvas.config(scrollregion=(0, 0, self.canvas.bbox("all")[2], self.yPos), background=BGCOLOR)
        self.scrollbar.pack(fill="y", side="right")

        return panel


    def agregar_usuario(self, root: tk.Canvas, id: int, user: str, size: int, yPos: int) -> None:
        panel = tk.Frame(root, background=BGCOLOR)

        panel.id = id

        blob = self.datos_usuarios.buscar_imagen_por_id(self.usuarios[id][3])

        pfp = Image.open(io.BytesIO(blob))
        pfp_tk = ImageTk.PhotoImage(pfp)

        image_label = tk.Label(panel, image=pfp_tk, background="white")
        image_label.image = pfp_tk
        image_label.pack(expand=True)

        name_label = tk.Label(panel, text=user, anchor="center", font=(DEFAULT_FONT, 16))
        name_label.config(background=BGCOLOR, foreground="white")
        name_label.pack(expand=True, fill="x", pady=5, padx=25)

        panel.username = user

        image_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        name_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        panel.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))

        panel.place(width=size, height=size, x=50)
        root.create_window(20, yPos, anchor="nw", window=panel)


    def crear_panel_derecho(self, root: tk.Tk) -> tk.Frame:
        panel = tk.Frame(root, background=BGCOLOR)

        self.bg_canvas = tk.Canvas(panel, width=1030, height=720, background=BGCOLOR)

        background_image = Image.open(BG_IMAGE)
        resized_img = background_image.resize((1030, 720))
        background_image_tk = ImageTk.PhotoImage(resized_img)

        self.bg_canvas.image = background_image_tk
        self.bg_canvas.create_image(0, 0, anchor="nw", image=background_image_tk)
        self.bg_canvas.place(x=0, y=0)

        return panel
    

    def crear_rectangulo_login(self, root: tk.Canvas) -> tk.Frame:
        panel = tk.Frame(root, background=BGCOLOR, width=750, height=500)

        panel_user_info = tk.Frame(panel, background=BGCOLOR)
        panel_user_info.place(x=200, y=50)

        blob = self.datos_usuarios.buscar_imagen_por_id(self.usuarios[self.id_usuario_seleccionado][3])

        pfp = Image.open(io.BytesIO(blob))
        resized_pfp = pfp.resize((128, 128))
        pfp_tk = ImageTk.PhotoImage(resized_pfp)

        label_pfp = tk.Label(panel_user_info, image=pfp_tk, width=128, height=128)
        label_pfp.image = pfp_tk
        label_pfp.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        username = tk.Label(panel_user_info, text=self.usuario_seleccionado, font=(DEFAULT_FONT, 26), background=BGCOLOR, foreground="white")
        username.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        self.passwd_panel = self.agregar_entry_passwd(panel_user_info)
        self.passwd_panel.grid(row=1, column=0, padx=20, pady=50, columnspan=2)

        self.button_passwd = tk.Button(panel_user_info, text="Iniciar Sesión", command=lambda: self.iniciar_sesion(self.passwd_entry.get()))
        self.button_passwd.grid(column=0, row=2, columnspan=2)

        return panel


    def agregar_entry_passwd(self, root: tk.Frame) -> tk.Frame:
        passwd_panel = tk.Frame(root, background=BGCOLOR)

        label = tk.Label(passwd_panel, text="Ingrese su contraseña", font=(DEFAULT_FONT, 16), background=BGCOLOR, foreground="white") 
        label.grid(column=0, row=0)

        self.passwd_entry = tk.Entry(passwd_panel, show="*", width=50)
        self.passwd_entry.grid(column=0, row=1)

        self.label_not_passwd = tk.Label(passwd_panel, text="", font=(DEFAULT_FONT, 16), background=BGCOLOR, foreground="red")
        self.label_not_passwd.grid(column=0, row=2)
        self.label_not_passwd.grid_forget()
        
        self.mostrar_passwd_panel = tk.Frame(passwd_panel, background=BGCOLOR)
        self.mostrar_passwd_panel.grid(column=0, row=3)

        self.cb_passwd = tk.Checkbutton(self.mostrar_passwd_panel, command=self.mostrar_passwd, background=BGCOLOR)
        label_cb = tk.Label(self.mostrar_passwd_panel, text="Mostrar Contraseña", font=(DEFAULT_FONT, 16), background=BGCOLOR, foreground="white")

        self.cb_passwd.grid(column=0, row=0)
        label_cb.grid(column=1, row=0)

        return passwd_panel


    def mostrar_passwd(self):
        if self.ocultar_passwd:
            self.passwd_entry.config(show="")
            self.ocultar_passwd = False
        else:
            self.passwd_entry.config(show="*")
            self.ocultar_passwd = True


    def agregar_rectangulo_login(self):
        self.panel_login = self.crear_rectangulo_login(self.bg_canvas)
        self.panel_login.place(x=100, y=120)


    def on_panel_click(self, event, panel):
        if self.selected_panel is not None:
            self.selected_panel.selected = False
            self.selected_panel.configure(bg=BGCOLOR)
        
        self.bind('<Return>', lambda event: self.iniciar_sesion(self.passwd_entry.get()))

        # Marcar el nuevo panel seleccionado
        panel.selected = True
        panel.configure(bg="lightblue")  # Color de selección
        self.selected_panel = panel  # Actualizar el panel seleccionado

        self.usuario_seleccionado = panel.username
        self.id_usuario_seleccionado = panel.id

        if self.panel_login is not None:
            self.limpiar_login()

        self.agregar_rectangulo_login()


    def limpiar_canvas(self) -> None:
        for widget in self.canvas.winfo_children():
            widget.destroy()  # Elimina cada widget del canvas

    
    def limpiar_login(self) -> None:
        for widget in self.panel_login.winfo_children():
            widget.destroy()  # Elimina cada widget del canvas

    
    def accion_rueda_mouse(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta//120)), "units")


    def buscar(self):
        self.selected_panel = None
        regex = self.users_entry.get()
        self.limpiar_canvas()
        self.yPos = 20

        if not regex:
            self.usuarios = self.datos_usuarios.obtener_datos_usuarios()
        else:
            self.usuarios = self.datos_usuarios.buscar_datos_usuario(regex)

        for id in self.usuarios.keys():
            self.agregar_usuario(self.canvas, id, self.usuarios[id][0], self.square_sides, self.yPos - 10)
            self.yPos += self.square_sides + 10

        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview, style="Vertical.TScrollbar")
        self.canvas.config(yscrollcommand=self.scrollbar.set) 
        self.canvas.config(scrollregion=(0, 0, self.canvas.bbox("all")[2], self.yPos), background=BGCOLOR)
        self.scrollbar.pack(fill="y", side="right")


    def mensaje_passwd_incorrecto(self):
        self.label_not_passwd.grid_forget()

        if self.passwd_entry.get() != "":
            self.label_not_passwd.config(text="* Contraseña Incorrecta.")
        else:
            self.label_not_passwd.config(text="* Campo Obligatorio.")

        self.label_not_passwd.grid(column=0, row=2)

        
    def iniciar_sesion(self, passwd: str):
        if self.datos_usuarios.verificar_passwd(self.id_usuario_seleccionado, passwd):
            self.destroy()
            
            self.datos["Usuario_Logueado"] = {
                "ID": self.id_usuario_seleccionado,
                "Nombre": self.usuario_seleccionado,
                "Rol": self.usuarios[self.id_usuario_seleccionado][2]
            }
            
            Inicio.Inicio(datos=self.datos)
        else:
            self.mensaje_passwd_incorrecto()


if __name__ == "__main__":
    root = Login()
    root.mainloop()