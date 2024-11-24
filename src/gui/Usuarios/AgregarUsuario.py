import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i


class AgregarUsuario(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Agregar Nuevo\nUsuario", titulo_ventana="Agregar Nuevo Usuario")

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuario_logueado = self.datos["Usuario_Logueado"]
        self.roles = self.datos_usuarios.obtener_datos_tipo()

        self.ocultar_passwd = True

        self.desc_rol = ""

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_nombre_entry()
        self.agregar_entry_passwd()
        self.agregar_opcion_rol()
        self.agregar_opciones()

        self.centrar_ventana()
        

    def agregar_nombre_entry(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Nombre de Usuario:")
        label.pack(expand=True, pady=5)

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.config(width=50)
        self.nombre_entry.pack(expand=True, pady=5)


    def agregar_entry_passwd(self):
        passwd_panel = tk.Frame(self, background=self.bgcolor)
        passwd_panel.pack(expand=True, fill="both", pady=10)

        passwd_panel.columnconfigure(0, weight=1)  # La única columna debe expandirse
        passwd_panel.rowconfigure((0,1,2,3), weight=1)  # Cada fila debe expandirse

        label = tk.Label(passwd_panel, text="Contraseña: ", font=(self.font, 16), background=self.bgcolor, foreground=self.fgcolor) 
        label.grid(column=0, row=0, sticky="nsew")

        self.passwd_entry = comp.CampoTexto(passwd_panel)
        self.passwd_entry.config(show="*", width=50)
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
        panel = tk.Frame(self, background=self.bgcolor)
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
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_agregar = comp.Boton(panel, text="Agregar\nUsuario", command=self.volver)
        b_agregar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.volver)
        b_cancelar.pack(expand=True, side="left")

    
    def mostrar_passwd(self):
        if self.ocultar_passwd:
            self.passwd_entry.config(show="")
            self.ocultar_passwd = False
        else:
            self.passwd_entry.config(show="*")
            self.ocultar_passwd = True


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)