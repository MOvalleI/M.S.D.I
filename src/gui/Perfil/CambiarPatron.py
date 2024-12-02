import tkinter as tk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i
import gui.Login as l


class Patron(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuario_logueado = self.datos["Usuario_Logueado"]

        self.nuevo_patron = None

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        ancho = 550
        alto = 565

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.agregar_titulo()
        self.agregar_patron()
        self.agregar_opciones()

    
    def agregar_patron(self):
        self.panel_patron = tk.Frame(self, background=self.bgcolor)
        self.panel_patron.pack(expand=True, fill="both")

        self.label = tk.Label(self.panel_patron, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 20), text="Dibuje el Patrón Actual para Continuar:")
        self.label.pack(expand=True, pady=10)

        self.patron_actual = comp.PatternUnlockApp(self.panel_patron, command=self.comprobar_patron_actual)
        self.patron_actual.pack(expand=True, pady=10)

    
    def comprobar_patron_actual(self, patron: str):
        if self.datos_usuarios.verificar_patron(self.usuario_logueado["ID"], patron):
            self.agregar_nuevo_patron()
            self.label.config(foreground=self.fgcolor, text="Dibuje su Nuevo Patrón de Desbloqueo:")
        else:
            self.label.config(foreground="red", text="* Patrón Incorrecto. Vuelva a Dibujar el Patrón")



    def agregar_nuevo_patron(self):
        self.patron_actual.destroy()
        self.patron_actual = comp.PatternUnlockApp(self.panel_patron, command=self.comprobar_nuevo_patron)
        self.patron_actual.pack(expand=True, pady=10)

    
    def comprobar_nuevo_patron(self, patron: str):
        if self.patron_actual.pattern is None:
            self.label.config(foreground=self.fgcolor, text="Vuelva a Dibujar el Nuevo Patrón para Confirmar:")
            self.patron_actual.pattern = patron
        else:
            if patron == self.patron_actual.pattern:
                self.nuevo_patron = patron
                self.cambiar_patron()
            else:
                self.label.config(foreground="red", text="* El Patrón Dibujado no es Correcto\nVuelva a Dibujar un Nuevo Patrón")
                self.patron_actual.pattern = None


    def cambiar_patron(self):
        print(f"Ancho: {self.winfo_width()}, Alto: {self.winfo_height()}")
        if ven.VentanaConfirmacion(self, texto="¿Seguro que desea Cambiar\nsu Patrón de Desbloqueo?", titulo_ventana="Cambiar Patrón").obtener_respuesta():
            if self.datos_usuarios.modificar_patron_usuario(self.usuario_logueado["ID"], self.nuevo_patron):
                ven.VentanaAvisoTL(self, titulo_ventana="Patrón Actualizado", texto="Patrón de Desbloqueo Actualizado\nCerrando Sesión...").wait_window()
                self.datos_usuarios.recargar_datos()
                self.datos["Usuarios"] = self.datos_usuarios
                self.datos.pop("Usuario_Logueado", None)
                self.datos.pop("Opcion_Inicio", None)
                self.destroy()
                l.Login(datos=self.datos)
            else:
                ven.VentanaAvisoTL(self, titulo_ventana="Error", texto="No se pudo actualizar el Patrón.\nIntentelo denuevo más Tarde").wait_window()
                self.volver()


    def agregar_opciones(self):
        self.b_cancelar = comp.Boton(self, text="Cancelar", command=self.volver)
        self.b_cancelar.pack(expand=True, pady=10)

    
    def volver(self, event=None):
        self.destroy()
        i.Inicio(datos=self.datos)