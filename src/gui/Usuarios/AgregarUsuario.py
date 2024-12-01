import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
from PIL import Image, ImageTk
import io


class AgregarUsuario(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar Nuevo\nUsuario", titulo_ventana="Agregar Nuevo Usuario")

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuario_logueado = self.datos["Usuario_Logueado"]
        self.roles = self.datos_usuarios.obtener_datos_tipo()
        self.fotos = self.datos["Usuarios"].obtener_datos_fotos()

        self.ocultar_passwd = True

        self.desc_rol = ""

        self.num_pagina = 1

        self.selected_panel = None

        self.nombre_usuario = None
        self.rol = None
        self.passwd = None
        self.patron = None
        self.pfp = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_pagina_1()
        self.agregar_opcion_rol()
        self.agregar_opciones()

        self.centrar_ventana()
        

    def agregar_pagina_1(self):
        "Pagina dedicada a el nombre, contraseña y rol"
        self.pagina1 = tk.Frame(self, background=self.bgcolor)
        self.pagina1.pack(expand=True, fill="both", pady=10)

        self.agregar_nombre_entry()
        self.agregar_entry_passwd()


    def agregar_pagina_2(self):
        "Pagina dedicada al patron de desbloqueo"
        self.pagina2 = tk.Frame(self, background=self.bgcolor)
        self.pagina2.pack(expand=True, fill="both", pady=10, before=self.panel_opciones)

        self.label_patron = tk.Label(self.pagina2, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 20), text="Dibuje el Patrón de Desbloqueo\npara el Nuevo Usuario")
        self.label_patron.pack(expand=True, pady=5)

        self.panel_patron = comp.PatternUnlockApp(self.pagina2, command=self.comprobar_patron)
        self.panel_patron.pack(pady=10)

    
    def comprobar_patron(self, patron: str):
        if self.patron is None:
            self.patron = patron
            self.label_patron.config(text="Vuelva a Dibujar el Patrón de Desbloqueo\npara Confirmar", foreground="white")
        else:
            if patron == self.patron:
                self.pagina2.pack_forget()
                self.agregar_pagina_3()
                self.b_agregar.pack(expand=True, side="left", before=self.b_cancelar)
                self.b_agregar.config(text="Agregar\nUsuario")
                self.b_agregar.deshabilitar_boton()
            else:
                self.label_patron.config(text="* Patrón Incorrecto\nVuelva a Dibujar un Patrón Nuevo", foreground="red")
                self.patron = None


    def agregar_pagina_3(self):
        "Pagina dedicada a la foto de perfil"
        self.pagina3 = tk.Frame(self, background=self.bgcolor)
        self.pagina3.pack(expand=True, fill="both", pady=10, before=self.panel_opciones)

        label = tk.Label(self.pagina2, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 20), text="Nombre de Usuario:")
        label.pack(expand=True, pady=5)

        self.panel_fotos()
        self.b_agregar.configurar(command=self.agregar_usuario)


    def panel_fotos(self):
        panel_label = tk.Frame(self.pagina3, background=self.bgcolor)
        panel_label.pack(expand=True, fill="both", pady=20)

        label = tk.Label(panel_label, text="Selecciona una Foto de Perfil:", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.pack(expand=True)

        self.canvas = tk.Canvas(self, highlightthickness=0, background=self.bgcolor)
        self.canvas.pack(expand=True, fill="both")

        size = 100

        print(self.fotos.keys())
        for i in self.fotos.keys():
            xPos, yPos = self.calcular_posicion(id=i)
            self.agregar_foto(size=size, id_foto=i, xPos=xPos, yPos=yPos)


    def calcular_posicion(self, id: int) -> tuple:
        match id % 4:
            case 1:
                return 60, 20
            case 2:
                return 220, 20
            case 3:
                return 60, 140
            case _:
                return 220, 140


    def agregar_foto(self, size: int, yPos: int, xPos: int, id_foto: int) -> None:
        panel = tk.Frame(self.canvas, background=ven.BGCOLOR, width=size+28, height=size+28)

        panel.id = id_foto

        blob = self.fotos[id_foto][0]

        pfp = Image.open(io.BytesIO(blob))
        pfp_res = pfp.resize((100, 100))
        pfp_tk = ImageTk.PhotoImage(pfp_res)

        image_label = tk.Label(panel, image=pfp_tk, background="white")
        image_label.image = pfp_tk
        image_label.pack(expand=True, fill="both")

        image_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))
        panel.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))

        panel.label = image_label

        panel.place(width=size+28, height=size+28, x=50)
        self.canvas.create_window(xPos, yPos, anchor="nw", window=panel)

    
    def on_panel_click(self, event, panel):
        if self.selected_panel is not None:
            self.selected_panel.label.configure(bg="white")
            self.selected_panel.selected = False

        # Marcar el nuevo panel seleccionado
        panel.selected = True
        panel.label.configure(bg="blue")
        self.selected_panel = panel  # Actualizar el panel seleccionado

        self.b_agregar.habilitar_boton()

        self.pfp = panel.id
        print(f"Selected: {panel.id}")
        print(f"pfp: {self.pfp}\n")


    def agregar_nombre_entry(self):
        user_panel = tk.Frame(self.pagina1, background=self.bgcolor)
        user_panel.pack(expand=True, fill="both", pady=10)

        user_panel.columnconfigure(0, weight=1)  # La única columna debe expandirse
        user_panel.rowconfigure((0,1,2,3), weight=1)  # Cada fila debe expandirse

        label = tk.Label(user_panel, text="Nombre de usuario: ", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor) 
        label.grid(column=0, row=0, sticky="nsew")

        self.user_entry = comp.CampoTexto(user_panel)
        self.user_entry.config(width=25)
        self.user_entry.grid(column=0, row=1)

        self.label_not_user = tk.Label(user_panel, text="", font=(self.font, 16), background=self.bgcolor, foreground="red")
        self.label_not_user.grid(column=0, row=2, sticky="nsew")
        self.label_not_user.grid_forget()


    def agregar_entry_passwd(self):
        passwd_panel = tk.Frame(self.pagina1, background=self.bgcolor)
        passwd_panel.pack(expand=True, fill="both", pady=10)

        passwd_panel.columnconfigure(0, weight=1)  # La única columna debe expandirse
        passwd_panel.rowconfigure((0,1,2,3), weight=1)  # Cada fila debe expandirse

        label = tk.Label(passwd_panel, text="Contraseña: ", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor) 
        label.grid(column=0, row=0, sticky="nsew")

        self.passwd_entry = comp.CampoTexto(passwd_panel)
        self.passwd_entry.config(show="*", width=25)
        self.passwd_entry.grid(column=0, row=1)

        self.label_not_passwd = tk.Label(passwd_panel, text="", font=(self.font, 16), background=self.bgcolor, foreground="red")
        self.label_not_passwd.grid(column=0, row=2, sticky="nsew")
        self.label_not_passwd.grid_forget()
        
        self.mostrar_passwd_panel = tk.Frame(passwd_panel, background=self.bgcolor)
        self.mostrar_passwd_panel.grid(column=0, row=3)

        self.cb_passwd = tk.Checkbutton(self.mostrar_passwd_panel, command=self.mostrar_passwd, background=self.bgcolor)
        label_cb = tk.Label(self.mostrar_passwd_panel, text="Mostrar Contraseña", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)

        self.cb_passwd.grid(column=0, row=0, sticky="nsew")
        label_cb.grid(column=1, row=0, sticky="nsew")


    def agregar_opcion_rol(self):
        panel = tk.Frame(self.pagina1, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text="Rol: ", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor)
        label.pack(expand=True, pady=5)

        self.lista_roles = ttk.Combobox(panel)
        self.lista_roles.config(state="readonly")
        self.configurar_lista_roles()
        self.lista_roles.pack(expand=True, pady=5)

        self.descripcion_rol = tk.Label(panel, text=self.desc_rol, font=(self.font, 12), background=self.bgcolor, foreground=self.fgcolor, wraplength=300)
        self.descripcion_rol.pack(expand=True, pady=5)
        self.configurar_descripcion()

        self.lista_roles.bind("<<ComboboxSelected>>", self.configurar_descripcion)

    
    def configurar_lista_roles(self):
        roles = []

        roles_dict = self.datos_usuarios.obtener_datos_tipo()

        for id_rol in roles_dict.keys():
            roles.append(roles_dict[id_rol][0])

        roles.pop(0)

        if self.usuario_logueado["Rol"] == 2:
            roles.pop(0)
            self.lista_roles.config(state="disabled")
            
        self.lista_roles.config(values=roles)
        self.lista_roles.current(0)


    def configurar_descripcion(self, event=None):
        rol = self.lista_roles.get()

        for id in self.roles.keys():
            if self.roles[id][0] == rol:
                self.desc_rol = self.roles[id][1]
                break

        self.descripcion_rol.config(text=self.desc_rol)


    def agregar_opciones(self):
        self.panel_opciones = tk.Frame(self, background=self.bgcolor)
        self.panel_opciones.pack(expand=True, fill="both", pady=10)

        self.b_agregar = comp.Boton(self.panel_opciones, text="Siguiente", command=self.comprobar_pagina_1)
        self.b_agregar.pack(expand=True, side="left")

        self.b_cancelar = comp.Boton(self.panel_opciones, text="Cancelar", command=self.volver)
        self.b_cancelar.pack(expand=True, side="left")

    
    def mostrar_passwd(self):
        if self.ocultar_passwd:
            self.passwd_entry.config(show="")
            self.ocultar_passwd = False
        else:
            self.passwd_entry.config(show="*")
            self.ocultar_passwd = True

    
    def comprobar_pagina_1(self):
        if self.user_entry.get() == "":
            self.label_not_user.config(text="* Campo Obligatorio")
            self.label_not_user.grid(column=0, row=2)
        else:
            self.label_not_user.grid_forget()

        if self.passwd_entry.get() == "":
            self.label_not_passwd.config(text="* Campo Obligatorio")
            self.label_not_passwd.grid(column=0, row=2)
        else:
            self.label_not_passwd.grid_forget()

        if self.user_entry.get() != "" and self.passwd_entry.get() != "":
            self.nombre_usuario = self.user_entry.get()
            self.passwd = self.passwd_entry.get()
            print()

            for id in self.roles.keys():
                if self.roles[id][0] == self.lista_roles.get():
                    self.rol = self.roles[id][0] 
                    break

            self.pagina1.pack_forget()
            self.b_agregar.pack_forget()
            self.agregar_pagina_2()


    def agregar_usuario(self):
        if ven.VentanaConfirmacion(self, texto="¿Esta Seguro que desea\nAgregar al Usuario?", titulo_ventana="Agregar Usuario").obtener_respuesta():
            self.datos_usuarios.agregar_nuevo_usuario(self.nombre_usuario, self.passwd, self.patron, self.rol, self.pfp)
            self.datos["Usuarios"] = self.datos_usuarios
            print(self.datos_usuarios.obtener_datos_usuarios()[7])
            self.volver()


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)

    
