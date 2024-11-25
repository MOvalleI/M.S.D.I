import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
import gui.Perfil.CambiarFoto as cf
import gui.Perfil.CambiarDatos as cd

class MenuPerfil(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__( titulo_ventana = "Perfil", titulo = "Perfil")

        self.datos = datos

        self.usuarios = self.datos["Usuarios"]

        self.usuario_logueado = self.datos["Usuario_Logueado"]
        self.nombre_usuario = self.usuario_logueado["Nombre"]
        self.rol_usuario = self.usuario_logueado["Rol"]
        self.pfp_usuario = self.usuario_logueado["Pfp"]

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.configurar_pfp()
        self.agregar_datos()
        self.agregar_opciones()

        b_volver = comp.Boton(self, text="Volver", command=self.volver)
        b_volver.pack(expand=True, pady=20)

        self.centrar_ventana()

    
    def configurar_pfp(self):
        pfp = self.usuarios.buscar_imagen_por_id(self.pfp_usuario)
        self.configurar_logo_bytes(pfp)

    
    def agregar_datos(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        label_nombre = tk.Label(panel, text=f"Nombre de Usuario:\n{self.nombre_usuario}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label_nombre.pack(expand=True, pady=10)


        rol = self.usuarios.buscar_nombre_tipo_por_id(self.rol_usuario)

        label_rol = tk.Label(panel, text=f"Rol de Usuario:\n {rol}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label_rol.pack(expand=True, pady=10)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        b_cambiar_nombre = comp.Boton(panel, text="Cambiar\nNombre", command=self.abrir_cambiar_nombre)
        b_cambiar_nombre.pack(expand=True, side="left")

        b_cambiar_passwd = comp.Boton(panel, text="Cambiar\nContraseña", command=self.abrir_cambiar_passwd)
        b_cambiar_passwd.pack(expand=True, side="left")

        b_cambiar_pfp = comp.Boton(panel, text="Cambiar Foto\nde Perfil", command=self.abrir_cambiar_foto)
        b_cambiar_pfp.pack(expand=True, side="left")


    def abrir_cambiar_foto(self):
        cf.CambiarFoto(parent=self, datos=self.datos)


    def abrir_cambiar_nombre(self):
        cd.CambiarNombreUsuario(self, datos=self.datos)


    def abrir_cambiar_passwd(self):
        cd.CambiarPasswdUsuario(self, datos=self.datos)


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)