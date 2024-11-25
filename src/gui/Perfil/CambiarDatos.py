import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven

class CambiarNombreUsuario(ven.VentanaTopLevel):
    def __init__(self, parent, datos):
        super().__init__(parent,titulo_ventana = "Cambiar Nombre de Usuario", titulo = "Cambiar Nombre\nde Usuario")

        self.datos = datos
        self.usuario = self.datos["Usuario_Logueado"]

        self.ocultar_passwd = True

        self.nombre_warning_text = ""
        self.passwd_warning_text = ""

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)

        self.agregar_titulo()
        self.agregar_entry_nombre()
        self.agregar_entry_passwd()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_entry_nombre(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure((0,1,2), weight=1)

        label = tk.Label(panel, text="Nuevo Nombre de Usuario:", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.grid(column=0, row=0)

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.config(width=25)
        self.nombre_entry.grid(column=0, row=1)

        self.nombre_warning = tk.Label(panel, text=self.nombre_warning_text, foreground="red", background=self.bgcolor, font=(self.font, 14))

    
    def agregar_entry_passwd(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure((0,1,2,3), weight=1)

        label = tk.Label(panel, text="Ingresar Contraseña Actual:", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.grid(column=0, row=0)

        self.passwd_entry = comp.CampoTexto(panel)
        self.passwd_entry.config(width=25, show="*")
        self.passwd_entry.grid(column=0, row=1)

        self.passwd_warning = tk.Label(panel, text=self.passwd_warning_text, foreground="red", background=self.bgcolor, font=(self.font, 14))

        panel_boton = tk.Frame(panel, background=self.bgcolor)
        panel_boton.grid(column=0, row=3)

        cb = tk.Checkbutton(panel_boton, background=self.bgcolor, command=self.mostrar_passwd)
        cb.pack(side="left")

        label_boton = tk.Label(panel_boton, text="Mostrar Contraseña", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 14))
        label_boton.pack(side="left")


    def mostrar_passwd(self):
        if self.ocultar_passwd:
            self.passwd_entry.config(show="")
            self.ocultar_passwd = False
        else:
            self.passwd_entry.config(show="*")
            self.ocultar_passwd = True


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        self.b_aplicar = comp.Boton(panel, text="Aplicar Cambios", command=None)
        self.b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")


class CambiarPasswdUsuario(ven.VentanaTopLevel):
    def __init__(self, parent, datos):
        super().__init__(parent,titulo_ventana = "Cambiar Contraseña", titulo = "Cambiar Contraseña")

        self.datos = datos
        self.usuario = self.datos["Usuario_Logueado"]

        self.ocultar_passwd_old = True
        self.ocultar_passwd_new = True

        self.passwd_warning_text = ""

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)

        self.agregar_titulo()
        self.agregar_entry_passwd_old()
        self.agregar_entry_passwd_new()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_entry_passwd_old(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure((0,1,2,3), weight=1)

        label = tk.Label(panel, text="Ingrese la Contraseña Anterior:", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.grid(column=0, row=0)

        self.old_passwd_entry = comp.CampoTexto(panel)
        self.old_passwd_entry.config(width=25, show="*")
        self.old_passwd_entry.grid(column=0, row=1)

        self.old_passwd_warning = tk.Label(panel, text=self.passwd_warning_text, foreground="red", background=self.bgcolor, font=(self.font, 14))

        panel_boton = tk.Frame(panel, background=self.bgcolor)
        panel_boton.grid(column=0, row=3)

        cb = tk.Checkbutton(panel_boton, background=self.bgcolor, command=self.mostrar_passwd_old)
        cb.pack(side="left")

        label_boton = tk.Label(panel_boton, text="Mostrar Contraseña", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 14))
        label_boton.pack(side="left")

    
    def agregar_entry_passwd_new(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure((0,1,2,3), weight=1)

        label = tk.Label(panel, text="Ingresar Contraseña Actual:", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 16))
        label.grid(column=0, row=0)

        self.new_passwd_entry = comp.CampoTexto(panel)
        self.new_passwd_entry.config(width=25, show="*")
        self.new_passwd_entry.grid(column=0, row=1)

        self.new_passwd_warning = tk.Label(panel, text=self.passwd_warning_text, foreground="red", background=self.bgcolor, font=(self.font, 14))

        panel_boton = tk.Frame(panel, background=self.bgcolor)
        panel_boton.grid(column=0, row=3)

        cb = tk.Checkbutton(panel_boton, background=self.bgcolor, command=self.mostrar_passwd_new)
        cb.pack(side="left")

        label_boton = tk.Label(panel_boton, text="Mostrar Contraseña", foreground=self.fgcolor, background=self.bgcolor, font=(self.font, 14))
        label_boton.pack(side="left")


    def mostrar_passwd_old(self):
        if self.ocultar_passwd_old:
            self.old_passwd_entry.config(show="")
            self.ocultar_passwd_old = False
        else:
            self.old_passwd_entry.config(show="*")
            self.ocultar_passwd_old = True
    
    
    def mostrar_passwd_new(self):
        if self.ocultar_passwd_new:
            self.new_passwd_entry.config(show="")
            self.ocultar_passwd_new = False
        else:
            self.new_passwd_entry.config(show="*")
            self.ocultar_passwd_new = True


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=20)

        self.b_aplicar = comp.Boton(panel, text="Aplicar Cambios", command=self.temp)
        self.b_aplicar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")

    
    def mensaje_passwd_old_incorrecto(self):
        self.old_passwd_warning.grid_forget()

        if self.old_passwd_entry.get() != "":
            self.old_passwd_warning.config(text="* Contraseña Incorrecta.")
        else:
            self.old_passwd_warning.config(text="* Campo Obligatorio.")

        self.old_passwd_warning.grid(column=0, row=2)

    
    def mensaje_passwd_new_incorrecto(self):
        self.new_passwd_warning.grid_forget()

        if self.new_passwd_entry.get() == "":
            self.new_passwd_warning.config(text="* Campo Obligatorio.")
            self.new_passwd_warning.grid(column=0, row=2)
        else:
            self.new_passwd_warning.grid_forget()



    # TODO: Cambiar este metodo por el de cambiar contraseña
    def temp(self):
        self.mensaje_passwd_old_incorrecto()        
        self.mensaje_passwd_new_incorrecto()        
        