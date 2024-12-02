import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import io
from PIL import Image, ImageTk
import gui.Login as l



class CambiarFoto(ven.VentanaTopLevel):
    def __init__(self, parent, datos):
        super().__init__(parent, titulo="Cambiar Foto\nde Perfil", titulo_ventana="Cambiar Foto de Perfil")

        self.parent = parent

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.pfp = self.datos["Usuarios"].obtener_datos_fotos()
        self.usuario_logueado = self.datos["Usuario_Logueado"]

        self.selected_panel = None

        self.id_foto_seleccionada = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.resizable(False, False)
        

        self.agregar_titulo()
        self.panel_fotos()
        self.agregar_opciones()

        self.centrar_ventana()


    def panel_fotos(self):
        panel_label = tk.Frame(self, background=self.bgcolor)
        panel_label.pack(expand=True, fill="both", pady=20)

        label = tk.Label(panel_label, text="Selecciona una Foto de Perfil:", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.pack(expand=True)

        self.canvas = tk.Canvas(self, highlightthickness=0, background=self.bgcolor)
        self.canvas.pack(expand=True, fill="both")

        size = 100

        for i in self.pfp.keys():
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

        blob = self.pfp[id_foto][0]

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


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        self.b_aplicar = comp.Boton(panel, text="Cambiar Foto", command=None)
        self.b_aplicar.deshabilitar_boton()
        self.b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")


    def on_panel_click(self, event, panel):
        if self.selected_panel is not None:
            self.selected_panel.label.configure(bg="white")
            self.selected_panel.selected = False

        # Marcar el nuevo panel seleccionado
        panel.selected = True
        panel.label.configure(bg="blue")
        self.selected_panel = panel  # Actualizar el panel seleccionado

        self.id_foto_seleccionada = panel.id

        self.b_aplicar.habilitar_boton()


    def cambiar_foto(self):
        if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Cambiar\nsu Foto de Perfil?", titulo_ventana="Cambiar Foto Perfil").obtener_respuesta():
            if self.datos_usuarios.modificar_pfp_usuario(self.usuario_logueado["ID"], self.id_foto_seleccionada):
                ven.VentanaAvisoTL(self, titulo_ventana="Foto de Perfil Actualizada", texto="Foto de Perfil Actualizada.\nCerrando Sesión...").wait_window()
                self.datos_usuarios.recargar_datos()
                self.datos["Usuarios"] = self.datos_usuarios
                self.datos.pop("Usuario_Logueado", None)
                self.datos.pop("Opcion_Inicio", None)
                self.destroy()
                self.parent.destroy()
                l.Login(datos=self.datos)
            else:
                ven.VentanaAvisoTL(self, titulo_ventana="Error", texto="No se pudo actualizar la Foto.\nIntentelo de nuevo Más Tarde.").wait_window()
                self.destroy()