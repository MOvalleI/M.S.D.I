import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
from PIL import Image, ImageTk
import io


BG_IMAGE = "./img/Imagen fondo para login.png"


class Login(tk.Tk):
    def __init__(self, datos: dict = None):
        super().__init__()

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuarios = self.datos_usuarios.obtener_datos_usuarios()

        self.ocultar_passwd = True

        self.selected_panel = None

        self.configurar_ventana()


    def configurar_ventana(self):
        ancho = 1280
        alto = 720
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.resizable(False, False)

        self.agregar_fondo()
        self.agregar_cuadro_usuarios()



    def agregar_fondo(self):
        self.panel_bg = tk.Frame(self, background=ven.BGCOLOR)

        bg_canvas = tk.Canvas(self.panel_bg, width=1280, height=720, background=ven.BGCOLOR)

        background_image = Image.open(BG_IMAGE)
        resized_img = background_image.resize((1280, 720))
        background_image_tk = ImageTk.PhotoImage(resized_img)

        bg_canvas.image = background_image_tk
        bg_canvas.create_image(0, 0, anchor="nw", image=background_image_tk)
        bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.panel_bg.pack(expand=True, fill="both")
        self.panel_bg.lower()

    
    def agregar_cuadro_usuarios(self):
        self.panel_cuadro_usuarios = tk.Frame(self, background=ven.BGCOLOR, width=1080, height=520)
        self.panel_cuadro_usuarios.propagate(False)
        self.panel_cuadro_usuarios.place(x=100, y=100)

        label_inicio = tk.Label(self.panel_cuadro_usuarios, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 24), text="Iniciar Sesión")
        label_inicio.pack(expand=True)

        self.canvas_usuarios()

        self.agregar_botones()


    def canvas_usuarios(self):
        self.user_canvas = tk.Canvas(self.panel_cuadro_usuarios, background=ven.BGCOLOR)
        self.user_canvas.pack(expand=True, fill="both")

        yPos = 10
        xPos = 50
        square_size = 128

        # for i in range(14):
        #     self.cuadrados(self.user_canvas, xPos=xPos, yPos=yPos)
            
        #     xPos += square_size + 10 
        
        #     if (i + 1) % 7 == 0:  
        #         xPos = 50  
        #         yPos += square_size + 20

        for id in self.usuarios.keys():
            self.agregar_usuario(self.user_canvas, id, self.usuarios[id][0], square_size, yPos - 10, xPos)
            xPos += square_size + 10 

            if (id + 1) % 7 == 0:  
                xPos = 50  
                yPos += square_size + 20


    def cuadrados(self, canvas: tk.Canvas, xPos: int, yPos: int):
        canvas.create_rectangle(xPos, yPos, xPos+128, yPos+128, fill="red")


    def agregar_usuario(self, root: tk.Canvas, id: int, user: str, size: int, yPos: int, xPos: int) -> None:
        panel = tk.Frame(self.panel_cuadro_usuarios, background=ven.BGCOLOR)

        panel.id = id

        blob = self.datos_usuarios.buscar_imagen_por_id(self.usuarios[id][3])

        pfp = Image.open(io.BytesIO(blob))
        pfp_res = pfp.resize((100, 100))
        pfp_tk = ImageTk.PhotoImage(pfp_res)

        image_label = tk.Label(panel, image=pfp_tk, background="white")
        image_label.image = pfp_tk
        image_label.pack(expand=True)

        name_label = tk.Label(panel, text=user, anchor="center", font=(ven.DEFAULT_FONT, 14))
        name_label.config(background=ven.BGCOLOR, foreground="white")
        name_label.pack(expand=True, fill="x", pady=5, padx=25)

        panel.username = user

        image_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        name_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        panel.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))

        panel.place(width=size, height=size, x=50)
        root.create_window(xPos, yPos, anchor="nw", window=panel)


    def agregar_botones(self):
        self.panel_botones = tk.Frame(self.panel_cuadro_usuarios, background=ven.BGCOLOR, width=1080, height=130)
        self.panel_botones.pack(expand=True, fill="both")

        self.b_ingresar_datos = comp.Boton(self.panel_botones, text="Ingresar Datos\nManualmente", command=self.ingresar_datos)
        self.b_ingresar_datos.pack(expand=True)


    def agregar_usuario_seleccionado(self):
        self.panel_ingresar_datos = tk.Frame(self, background=ven.BGCOLOR, width=1080, height=520)
        self.panel_ingresar_datos.place(x=100, y=100)

        label_inicio = tk.Label(self.panel_ingresar_datos, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 24), text="Iniciar Sesión")
        label_inicio.pack(expand=True)

        # TODO: Agregar aqui el pfp y el username

        self.agregar_entry_passwd()
        self.agregar_botones_ingresar()


    def agregar_ingresar_datos(self):
        self.panel_ingresar_datos = tk.Frame(self, background=ven.BGCOLOR, width=1080, height=520)
        self.panel_ingresar_datos.place(x=100, y=100)
        self.panel_ingresar_datos.propagate(False)

        label_inicio = tk.Label(self.panel_ingresar_datos, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 24), text="Iniciar Sesión")
        label_inicio.pack(expand=True)

        # Nombre
        panel_nombre = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        panel_nombre.pack(expand=True, fill="both")

        label_nombre = tk.Label(panel_nombre, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 14), text="Nombre de Usuario:")
        label_nombre.pack(pady=5)

        self.nombre_entry = comp.CampoTexto(panel_nombre)
        self.nombre_entry.config(width=50)
        self.nombre_entry.pack(pady=5)

        self.agregar_entry_passwd()
        self.agregar_botones_ingresar()


    def agregar_entry_passwd(self):
        passwd_panel = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        passwd_panel.pack(expand=True, fill="both")

        passwd_panel.columnconfigure(0, weight=1)  # La única columna debe expandirse
        passwd_panel.rowconfigure(0, weight=1)  # Cada fila debe expandirse
        passwd_panel.rowconfigure(1, weight=1)
        passwd_panel.rowconfigure(2, weight=1)
        passwd_panel.rowconfigure(3, weight=1)

        label = tk.Label(passwd_panel, text="Ingrese su contraseña", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="white") 
        label.grid(column=0, row=0, sticky="nsew")

        self.passwd_entry = comp.CampoTexto(passwd_panel)
        self.passwd_entry.config(show="*", width=50)
        self.passwd_entry.grid(column=0, row=1)

        self.label_not_passwd = tk.Label(passwd_panel, text="", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="red")
        self.label_not_passwd.grid(column=0, row=2, sticky="nsew")
        self.label_not_passwd.grid_forget()
        
        self.mostrar_passwd_panel = tk.Frame(passwd_panel, background=ven.BGCOLOR)
        self.mostrar_passwd_panel.grid(column=0, row=3)

        self.cb_passwd = tk.Checkbutton(self.mostrar_passwd_panel, command=self.mostrar_passwd, background=ven.BGCOLOR)
        label_cb = tk.Label(self.mostrar_passwd_panel, text="Mostrar Contraseña", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="white")

        self.cb_passwd.grid(column=0, row=0, sticky="nsew")
        label_cb.grid(column=1, row=0, sticky="nsew")

    
    def mensaje_passwd_incorrecto(self):
        self.label_not_passwd.grid_forget()

        if self.passwd_entry.get() != "":
            self.label_not_passwd.config(text="* Contraseña Incorrecta.")
        else:
            self.label_not_passwd.config(text="* Campo Obligatorio.")

        self.label_not_passwd.grid(column=0, row=2)


    def agregar_botones_ingresar(self):
        botones_panel = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        botones_panel.pack(expand=True, fill="both")

        self.b_iniciar = comp.Boton(botones_panel, text="Iniciar\nSesión", command=self.iniciar_sesion)
        self.b_iniciar.pack(expand=True, side="left")

        self.b_volver = comp.Boton(botones_panel, text="Volver", command=self.volver)
        self.b_volver.pack(expand=True, side="left")


    def mostrar_passwd(self):
        if self.ocultar_passwd:
            self.passwd_entry.config(show="")
            self.ocultar_passwd = False
        else:
            self.passwd_entry.config(show="*")
            self.ocultar_passwd = True


    def ingresar_datos(self):
        self.panel_cuadro_usuarios.place_forget()
        self.agregar_ingresar_datos()

    
    def volver(self):
        self.panel_ingresar_datos.destroy()
        self.panel_cuadro_usuarios.place(x=100, y=100)

    
    def on_panel_click(self, event, panel):
        if self.selected_panel is not None:
            self.selected_panel.selected = False
            self.selected_panel.configure(bg=ven.BGCOLOR)

        # Marcar el nuevo panel seleccionado
        panel.selected = True
        panel.configure(bg="lightblue")  # Color de selección
        self.selected_panel = panel  # Actualizar el panel seleccionado

        self.usuario_seleccionado = panel.username
        self.id_usuario_seleccionado = panel.id



    def iniciar_sesion(self):
        if 2==1:
            pass
        else:
            self.mensaje_passwd_incorrecto()


        
        


