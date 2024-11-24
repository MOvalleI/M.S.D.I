import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i

class MenuPerfil(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__( titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.datos = datos

        self.usuarios = self.datos["Usuarios"]

        self.usuario_logueado = self.datos["Usuario_Logueado"]
        self.nombre_usuario = self.usuario_logueado["Nombre"]
        self.pfp_usuario = self.usuario_logueado["Pfp"]

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.configurar_pfp()
        self.agregar_nombre()
        self.agregar_opciones()

        b_volver = comp.Boton(self, text="Volver", command=self.volver)
        b_volver.pack(expand=True, pady=10)

        self.centrar_ventana()

    
    def configurar_pfp(self):
        pfp = self.usuarios.buscar_imagen_por_id(self.pfp_usuario)
        self.configurar_logo_bytes(pfp)

    
    def agregar_nombre(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, text=f"Nombre de Usuario:\n{self.nombre_usuario}", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.pack(expand=True)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_cambiar_nombre = comp.Boton(panel, text="Cambiar\nNombre", command=None)
        b_cambiar_nombre.pack(expand=True, side="left")

        b_cambiar_passwd = comp.Boton(panel, text="Cambiar\nContraseña", command=None)
        b_cambiar_passwd.pack(expand=True, side="left")

        b_cambiar_pfp = comp.Boton(panel, text="Cambiar Foto\nde Perfil", command=None)
        b_cambiar_pfp.pack(expand=True, side="left")


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)