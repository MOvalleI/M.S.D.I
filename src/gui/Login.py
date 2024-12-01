import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
from PIL import Image, ImageTk
import io
import data.Registro as r
import datetime


BG_IMAGE = "./img/logos/Imagen fondo para login.png"


class Login(tk.Tk):
    def __init__(self, datos: dict = None):
        super().__init__()

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuarios = self.datos_usuarios.obtener_datos_usuarios()

        self.id_usuario_seleccionado = None
        self.usuario_seleccionado = None

        self.ocultar_passwd = True

        self.selected_panel = None

        self.paneles = []

        self.num_pagina = 0
        self.ids_usuarios = []

        self.modo = "passwd" # Valores Posibles: 'passwd' - 'patron'

        self.label_not_user = None

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
        self.panel_cuadro_usuarios = tk.Frame(self, background=ven.BGCOLOR, width=1080, height=600)
        self.panel_cuadro_usuarios.propagate(False)
        self.panel_cuadro_usuarios.place(x=100, y=50)

        text = "Iniciar Sesión  |  Selecciona a tu usuario"

        label_inicio = tk.Label(self.panel_cuadro_usuarios, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 24), text=text)
        label_inicio.pack(expand=True)

        self.agregar_botones_paginas()
        self.canvas_usuarios()
        self.agregar_botones()


    def agregar_botones_paginas(self):
        panel_botones = tk.Frame(self.panel_cuadro_usuarios, background=ven.BGCOLOR)
        panel_botones.pack(fill="x")

        self.b_izquierda = comp.BotonFlecha(panel_botones, text="  Página\n  Anterior", command=lambda: self.cambiar_pagina(-1), direction="izquierda")
        self.b_izquierda.deshabilitar_boton()
        self.b_izquierda.pack(side="left")

        self.b_derecha = comp.BotonFlecha(panel_botones, text="Página  \nSiguiente  ", command=lambda: self.cambiar_pagina(1), direction="derecha")
        self.b_derecha.pack(side="right")


    def canvas_usuarios(self):
        self.user_canvas = tk.Canvas(self.panel_cuadro_usuarios, background=ven.BGCOLOR)
        self.user_canvas.config(highlightthickness=0)
        self.user_canvas.pack(expand=True, fill="both")

        for id in self.usuarios.keys():
            self.ids_usuarios.append(id)

        self.cambiar_pagina(1)
            

    def pintar_pagina(self, num_pagina):
        yPos = 10
        xPos = 50
        square_size = 128

        inicio = 0
        fin = 12

        if num_pagina > 1:
            inicio = 12*(num_pagina-1)
            fin = 12*num_pagina

        if fin > len(self.ids_usuarios):
            fin = len(self.ids_usuarios)

        for i in range(inicio, fin):
            self.agregar_usuario(self.user_canvas, self.ids_usuarios[i], self.usuarios[self.ids_usuarios[i]][0], square_size, yPos - 10, xPos)
            xPos += square_size + 40 

            if (i+1)%6 == 0:
                xPos = 50  
                yPos += square_size + 40


    def cambiar_pagina(self, num: int):
        self.num_pagina += num

        for panel_id in self.paneles:
            self.user_canvas.delete(panel_id)

        # Limpiar la lista de identificadores de paneles
        self.paneles.clear()

        self.pintar_pagina(self.num_pagina)

        if self.num_pagina == 1:
            self.b_izquierda.deshabilitar_boton()
        else:
            self.b_izquierda.habilitar_boton()

        if ((len(self.ids_usuarios) + 12 - 1) // 12) == self.num_pagina:
            self.b_derecha.deshabilitar_boton()
        else:
            if self.num_pagina != 1:
                self.b_derecha.habilitar_boton()
            else:
                self.b_derecha.deshabilitar_boton()



    def agregar_usuario(self, root: tk.Canvas, id: int, user: str, size: int, yPos: int, xPos: int) -> None:
        panel = tk.Frame(self.panel_cuadro_usuarios, background=ven.BGCOLOR, width=size, height=size)
        panel.id = id

        blob = self.datos_usuarios.buscar_imagen_por_id(self.usuarios[id][3])

        pfp = Image.open(io.BytesIO(blob))
        pfp_res = pfp.resize((110, 110))
        pfp_tk = ImageTk.PhotoImage(pfp_res)

        image_label = tk.Label(panel, image=pfp_tk, background="white")
        image_label.image = pfp_tk
        image_label.pack(expand=True)

        name_label = tk.Label(panel, text=user.replace(" ", "\n"), font=(ven.DEFAULT_FONT, 12))
        name_label.config(background=ven.BGCOLOR, foreground="white")
        name_label.pack(fill="x", pady=5, padx=25)

        panel.username = user

        image_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        name_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        panel.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))

        panel.place(width=size, height=size, x=50)
        panel_id = root.create_window(xPos, yPos, anchor="nw", window=panel)

        self.paneles.append(panel_id)


    def agregar_botones(self):
        self.panel_botones = tk.Frame(self.panel_cuadro_usuarios, background=ven.BGCOLOR, width=1080, height=130)
        self.panel_botones.pack(expand=True, fill="both")

        self.b_ingresar_datos = comp.Boton(self.panel_botones, text="Ingresar Datos\nManualmente", command=self.ingresar_datos)
        self.b_ingresar_datos.pack(expand=True)


    def agregar_usuario_seleccionado(self):
        self.panel_ingresar_datos = tk.Frame(self, background=ven.BGCOLOR, width=1080, height=600)
        self.panel_ingresar_datos.place(x=100, y=50)
        self.panel_ingresar_datos.propagate(False)

        label_inicio = tk.Label(self.panel_ingresar_datos, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 24), text="Iniciar Sesión")
        label_inicio.pack(expand=True)

        self.panel_pfp = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        self.panel_pfp.pack(expand=True)

        blob = self.datos_usuarios.buscar_imagen_por_id(self.usuarios[self.id_usuario_seleccionado][3])

        pfp = Image.open(io.BytesIO(blob))
        resized_pfp = pfp.resize((96, 96))
        pfp_tk = ImageTk.PhotoImage(resized_pfp)

        label_pfp = tk.Label(self.panel_pfp, image=pfp_tk, width=100, height=100)
        label_pfp.image = pfp_tk
        label_pfp.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        username = tk.Label(self.panel_pfp, text=self.usuario_seleccionado, font=(ven.DEFAULT_FONT, 26), background=ven.BGCOLOR, foreground="white")
        username.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        self.agregar_entry_passwd()
        self.agregar_modo_patron()
        self.agregar_botones_ingresar()


    def agregar_ingresar_datos(self):
        self.panel_ingresar_datos = tk.Frame(self, background=ven.BGCOLOR, width=1080, height=600)
        self.panel_ingresar_datos.place(x=100, y=50)
        self.panel_ingresar_datos.propagate(False)

        label_inicio = tk.Label(self.panel_ingresar_datos, background=ven.BGCOLOR, foreground=ven.FGCOLOR, font=(ven.DEFAULT_FONT, 24), text="Iniciar Sesión")
        label_inicio.pack(expand=True)

        self.agregar_entry_usuario()
        self.agregar_entry_passwd()
        self.agregar_modo_patron()
        self.agregar_botones_ingresar()


    def agregar_entry_usuario(self):
        self.user_panel = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        self.user_panel.pack(expand=True, fill="both")

        self.user_panel.columnconfigure(0, weight=1)  # La única columna debe expandirse
        self.user_panel.rowconfigure((0,1,2,3), weight=1)  # Cada fila debe expandirse

        label = tk.Label(self.user_panel, text="Ingrese su Nombre de Usuario:", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="white") 
        label.grid(column=0, row=0, sticky="nsew")

        self.user_entry = comp.CampoTexto(self.user_panel)
        self.user_entry.config(width=50)
        self.user_entry.grid(column=0, row=1)

        self.label_not_user = tk.Label(self.user_panel, text="", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="red")
        self.label_not_user.grid(column=0, row=2, sticky="nsew")
        self.label_not_user.grid_forget()


    def agregar_entry_passwd(self):
        self.passwd_panel = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        if self.selected_panel is None:
            self.passwd_panel.pack(expand=True, fill="both", after=self.user_panel)
        else:
            self.passwd_panel.pack(expand=True, fill="both", after=self.panel_pfp)


        self.passwd_panel.columnconfigure(0, weight=1)  # La única columna debe expandirse
        self.passwd_panel.rowconfigure((0,1,2,3), weight=1)  # Cada fila debe expandirse

        label = tk.Label(self.passwd_panel, text="Ingrese su contraseña", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="white") 
        label.grid(column=0, row=0, sticky="nsew")

        self.passwd_entry = comp.CampoTexto(self.passwd_panel)
        self.passwd_entry.config(show="*", width=50)
        self.passwd_entry.grid(column=0, row=1)

        self.label_not_passwd = tk.Label(self.passwd_panel, text="", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="red")
        self.label_not_passwd.grid(column=0, row=2, sticky="nsew")
        self.label_not_passwd.grid_forget()
        
        self.mostrar_passwd_panel = tk.Frame(self.passwd_panel, background=ven.BGCOLOR)
        self.mostrar_passwd_panel.grid(column=0, row=3)

        self.cb_passwd = tk.Checkbutton(self.mostrar_passwd_panel, command=self.mostrar_passwd, background=ven.BGCOLOR)
        label_cb = tk.Label(self.mostrar_passwd_panel, text="Mostrar Contraseña", font=(ven.DEFAULT_FONT, 16), background=ven.BGCOLOR, foreground="white")

        self.cb_passwd.grid(column=0, row=0, sticky="nsew")
        label_cb.grid(column=1, row=0, sticky="nsew")

    
    def agregar_modo_patron(self):
        self.patron_panel = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        self.patron_panel.pack_forget()

        label = tk.Label(self.patron_panel, background=ven.BGCOLOR, foreground="white", font=(ven.DEFAULT_FONT, 16), text="Dibuje el Patrón para Iniciar Sesión")
        label.pack(pady=5)

        self.label_patron_error = tk.Label(self.patron_panel, background=ven.BGCOLOR, foreground="red", font=(ven.DEFAULT_FONT, 14), text="")
        self.label_patron_error.pack(pady=5)

        self.patron = comp.PatternUnlockApp(self.patron_panel, self.iniciar_sesion_patron)
        self.patron.pack(pady=5)

    
    def mensaje_passwd_incorrecto(self):
        self.label_not_passwd.grid_forget()

        if self.passwd_entry.get() != "":
            self.label_not_passwd.config(text="* Contraseña Incorrecta.")
        else:
            self.label_not_passwd.config(text="* Campo Obligatorio.")

        self.label_not_passwd.grid(column=0, row=2)


    def mensaje_user_incorrecto(self):
        self.label_not_user.grid_forget()

        if self.user_entry.get() != "":
            self.label_not_user.config(text="* El usuario no existe.")
        else:
            self.label_not_user.config(text="* Campo Obligatorio.")

        self.label_not_user.grid(column=0, row=2)

    
    def cambiar_modo(self):
        if self.modo == "passwd" and self.selected_panel is None:
            self.passwd_panel.pack_forget()
            self.patron_panel.pack(expand=True, after=self.user_panel, fill="both")
            self.b_iniciar.pack_forget()
            self.b_modo.config(text="Escribir\nContraseña")
            self.modo = "patron"
        elif self.modo == "patron" and self.selected_panel is None:
            self.patron_panel.pack_forget()
            self.passwd_panel.pack(expand=True, fill="both", after=self.user_panel)
            self.b_iniciar.pack(expand=True, side="left", before=self.b_modo)
            self.b_modo.config(text="Dibujar\nPatrón")
            self.modo = "passwd"
        elif self.modo == "passwd" and self.selected_panel is not None:
            self.passwd_panel.pack_forget()
            self.patron_panel.pack(expand=True, after=self.panel_pfp, fill="both")
            self.b_iniciar.pack_forget()
            self.b_modo.config(text="Escribir\nContraseña")
            self.modo = "patron"
        else:
            self.patron_panel.pack_forget()
            self.passwd_panel.pack(expand=True, fill="both", after=self.panel_pfp)
            self.b_iniciar.pack(expand=True, side="left", before=self.b_modo)
            self.b_modo.config(text="Dibujar\nPatrón")
            self.modo = "passwd"


    def agregar_botones_ingresar(self):
        botones_panel = tk.Frame(self.panel_ingresar_datos, background=ven.BGCOLOR)
        botones_panel.pack(expand=True, fill="both")

        self.b_iniciar = comp.Boton(botones_panel, text="Iniciar\nSesión", command=lambda :self.iniciar_sesion(self.passwd_entry.get()))
        self.b_iniciar.pack(expand=True, side="left")

        self.b_modo = comp.Boton(botones_panel, text="Dibujar\nPatrón", command=self.cambiar_modo)
        self.b_modo.pack(expand=True, side="left")

        self.b_volver = comp.Boton(botones_panel, text="Volver", command=self.volver)
        self.b_volver.pack(expand=True, side="left")

        self.bind("<Return>", lambda e:self.iniciar_sesion(self.passwd_entry.get(), event=e))
        self.bind("<Escape>", lambda e: self.volver(event=e))


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


    def mensaje_patron_incorrecto(self):
        self.label_patron_error.config(text="* Patrón Incorrecto")


    def volver(self, event=None):
        self.panel_ingresar_datos.destroy()
        self.panel_cuadro_usuarios.place(x=100, y=50)
        self.selected_panel = None

    
    def on_panel_click(self, event, panel):
        if self.selected_panel is not None:
            self.selected_panel.selected = False

        # Marcar el nuevo panel seleccionado
        panel.selected = True
        self.selected_panel = panel  # Actualizar el panel seleccionado

        self.usuario_seleccionado = panel.username
        self.id_usuario_seleccionado = panel.id

        self.panel_cuadro_usuarios.place_forget()
        self.agregar_usuario_seleccionado()


    def iniciar_sesion(self, passwd: str, event=None):
        if not self.selected_panel:
            self.id_usuario_seleccionado = self.datos_usuarios.buscar_id_por_nombre(self.user_entry.get())

        if self.id_usuario_seleccionado == 0:
            self.mensaje_user_incorrecto()
        else:
            if self.datos_usuarios.verificar_passwd(self.id_usuario_seleccionado, passwd):
                self.destroy()
                
                self.crear_diccionario()
                
                i.Inicio(datos=self.datos)
            else:
                self.mensaje_passwd_incorrecto()


    def iniciar_sesion_patron(self, patron: str):
        if not self.selected_panel:
            self.id_usuario_seleccionado = self.datos_usuarios.buscar_id_por_nombre(self.user_entry.get())

        if self.id_usuario_seleccionado == 0:
            self.mensaje_user_incorrecto()
        else:
            if self.label_not_user: 
                self.label_not_user.config(text="")
            if self.datos_usuarios.verificar_patron(self.id_usuario_seleccionado, patron):
                self.destroy()
                
                self.crear_diccionario()
                
                i.Inicio(datos=self.datos)
            else:
                self.mensaje_patron_incorrecto()

    
    def crear_diccionario(self):
        sesion = r.Sesion()

        fecha_inicio = datetime.datetime.now().strftime("%Y-%m-%d")
        hora_inicio = datetime.datetime.now().strftime("%H:%M:%S")

        sesion.registrar_inicio_sesion(fecha_inicio, hora_inicio)

        registro = r.ArbolAcciones()

        self.datos["Usuario_Logueado"] = {
            "ID": self.id_usuario_seleccionado,
            "Nombre": self.usuario_seleccionado,
            "Rol": self.usuarios[self.id_usuario_seleccionado][2],
            "Pfp": self.usuarios[self.id_usuario_seleccionado][3],
            "Registro": registro,
            "Sesion": sesion
        }