import tkinter as tk
from PIL import Image, ImageTk
import gui.Login
import gui.Ventas.AgregarVentas as av
import gui.Ventanas as ven
import gui.Inventario.Agregar as iai
import gui.Inventario.Eliminar as iei
import gui.Inventario.Ver as ivi
import gui.Componentes as comp
import gui.Menu.VisualizarMenu as vm
import gui.Menu.AgregarMenu as am
import gui.Ventas.VerVentas as vv
import gui.Otros.VerDatos as vod
import gui.Usuarios.AgregarUsuario as au
import gui.Usuarios.VerUsuarios as vu
import gui.Usuarios.EliminarUsuarios as eu
import gui.Otros.AgregarDatos as ad
import gui.Perfil.MenuPerfil as mp
import gui.Menu.EliminarMenu as em
import gui.Menu.ModificarMenu as mm
import gui.Opciones.ModificarLocal as ml
import gui.Ventas.GenerarReporte as gr


IMG_VENTAS = "./img/iconos/ventas.png"
IMG_MENU = "./img/iconos/menu.png"
IMG_INVENTARIO = "./img/iconos/inventario.png"
IMG_OTROS = "./img/iconos/otros.png"
IMG_USUARIOS = "./img/iconos/usuario.png"
IMG_OPCIONES = "./img/iconos/opciones.png"

BGBUTTON = "gray"
FGBUTTON = "white"

class Inicio(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Inicio", titulo_ventana="Inicio")

        self.datos = datos

        self.usuario_logueado = datos["Usuario_Logueado"]["Nombre"]
        self.rol_usuario = datos["Usuario_Logueado"]["Rol"]

        if "Opcion_Inicio" in self.datos:
            self.opciones_seleccionada = self.datos["Opcion_Inicio"]
        else:
            self.opciones_seleccionada = "Ventas"
            self.datos["Opcion_Inicio"] = self.opciones_seleccionada


        self.num_pagina = 1

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.salir)
        self.geometry("600x600")

        self.centrar_ventana()
        self.agregar_titulo()
        self.agregar_botones_paginas()
        self.agregar_panel_opciones()
        self.agregar_opciones()

    
    def agregar_botones_paginas(self):
        button_panel = tk.Frame(self, background=self.bgcolor)
        button_panel.pack(fill="x", expand=True)


        self.flechas_panel = tk.Frame(button_panel, background=self.bgcolor)
        self.flechas_panel.pack(fill="x", expand=True, pady=10)
            
        self.b_izquierda = comp.BotonFlecha(self.flechas_panel, direction="izquierda", text="  Página\n  Anterior")
        self.b_izquierda.configurar(command = lambda: self.configurar_pagina(-1))
        self.b_izquierda.deshabilitar_boton()
        self.b_izquierda.pack(side="left", anchor="w", expand=True)

        self.label_pagina = tk.Label(self.flechas_panel, text=f"Página {self.num_pagina}", background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 18))
        self.label_pagina.pack(expand=True, side="left", anchor="center")

        self.b_derecha = comp.BotonFlecha(self.flechas_panel, direction="derecha", text="Página  \nSiguiente  ")
        self.b_derecha.configurar(command = lambda: self.configurar_pagina(1))
        self.b_derecha.pack(side="left", anchor="e", expand=True)

        self.agregar_pagina_2()
        self.ocultar_pagina()
        self.agregar_pagina_1()

    
    def agregar_pagina_1(self):
        self.pagina1 = tk.Frame(self, background=self.bgcolor)
        self.pagina1.pack(fill="x", expand=True, after=self.flechas_panel, pady=10)

        self.button_venta = comp.Boton(self.pagina1, text="Ver Opciones\nde Venta")
        self.button_venta.config(command=lambda: self.cambiar_opciones("Ventas"))
        self.button_venta.pack(side="left", expand=True)

        self.button_menu = comp.Boton(self.pagina1, text="Ver Opciones\nde Menu")
        self.button_menu.config(command=lambda: self.cambiar_opciones("Menu"))
        self.button_menu.pack(side="left", expand=True)

        self.button_inventario = comp.Boton(self.pagina1, text="Ver Opciones\nde Inventario")
        self.button_inventario.config(command=lambda: self.cambiar_opciones("Inventario"))
        self.button_inventario.pack(side="left", expand=True)


    def agregar_pagina_2(self):
        self.pagina2 = tk.Frame(self, background=self.bgcolor)
        self.pagina2.pack(fill="x", expand=True, after=self.flechas_panel, pady=10)

        self.button_otros = comp.Boton(self.pagina2, text="Ver Opciones de\nOtros Datos")
        self.button_otros.config(command=lambda: self.cambiar_opciones("Otros"))
        self.button_otros.pack(expand=True, side="left", padx=3)

        if self.rol_usuario != 3:
            self.button_usuarios = comp.Boton(self.pagina2, text="Ver Opciones\nde Usuarios")
            self.button_usuarios.config(command=lambda: self.cambiar_opciones("Usuarios"))
            self.button_usuarios.pack(expand=True, side="left", padx=3)

        if self.rol_usuario == 1:
            self.button_opciones = comp.Boton(self.pagina2, text="Ver Opciones\nde Local")
            self.button_opciones.config(command=lambda: self.cambiar_opciones("Opciones"))
            self.button_opciones.pack(expand=True, side="left", padx=3)


    def ocultar_pagina(self):
        if self.num_pagina == 2:
            self.pagina1.pack_forget()
        else:
            self.pagina2.pack_forget()
        

    def mostrar_pagina(self):
        if self.num_pagina == 2:
            self.pagina2.pack(fill="x", expand=True, after=self.flechas_panel, pady=10)
        else:
            self.pagina1.pack(fill="x", expand=True, after=self.flechas_panel, pady=10)


    def configurar_pagina(self, num: int):
        self.num_pagina += num
        if self.num_pagina == 1:
            self.ocultar_pagina()
            self.mostrar_pagina()
            self.b_izquierda.deshabilitar_boton()
            self.b_derecha.habilitar_boton()
        else:
            self.ocultar_pagina()
            self.mostrar_pagina()
            self.b_izquierda.habilitar_boton()
            self.b_derecha.deshabilitar_boton()
        self.label_pagina.config(text=f"Página {self.num_pagina}")


    def agregar_panel_opciones(self):
        self.panel_opciones = tk.Frame(self, background=self.bgcolor, pady=50, borderwidth=5)
        self.panel_opciones.pack(expand=True, fill="both", pady=10)

        self.panel_opciones.grid_columnconfigure(0, weight=1)
        self.panel_opciones.grid_columnconfigure(1, weight=1)
        self.panel_opciones.grid_columnconfigure(2, weight=1)
        self.panel_opciones.grid_rowconfigure(0, weight=1)
        self.panel_opciones.grid_rowconfigure(1, weight=1)

        self.configurar_botones(self.panel_opciones)


    def configurar_botones(self, root: tk.Frame):
        self.boton_agregar = comp.Boton(root)
        self.boton_ver = comp.Boton(root)
        self.boton_eliminar = comp.Boton(root)
        self.boton_modificar = comp.Boton(root)

        match self.opciones_seleccionada:
            case "Menu": 
                logo = IMG_MENU
                agregar_text = "Agregar\nMenu"
                ver_text = "Ver\nMenu"
                eliminar_text = "Eliminar\nMenu"
                modificar_text = "Modificar\nMenu"
                self.boton_ver.config(command=self.abrir_ver_menu)
                self.boton_agregar.config(command=self.abrir_agregar_menu)
                self.boton_eliminar.config(command=self.abrir_eliminar_menu)
                self.boton_modificar.config(command=self.abrir_modificar_menu)
            case "Inventario": 
                logo = IMG_INVENTARIO
                agregar_text = "Agregar\nProducto"
                ver_text = "Ver\nInventario"
                eliminar_text = "Eliminar\nProducto"
                modificar_text = "Modificar\nProducto"
                self.boton_agregar.config(command=self.abrir_agregar_producto)
                self.boton_eliminar.config(command=self.abrir_eliminar_producto)
                self.boton_ver.config(command=self.abrir_ver_inventario)
            case "Otros":
                logo = IMG_OTROS
                agregar_text = "Agregar\nOtros Datos"
                ver_text = "Ver\nOtros Datos"
                eliminar_text = "Eliminar\nOtros Datos"
                modificar_text = "Modificar\nOtros Datos"
                self.boton_agregar.config(command=self.abrir_agregar_otro)
                self.boton_eliminar.config(command=lambda : self.abrir_ver_otros(accion="Eliminar"))
                self.boton_ver.config(command=lambda : self.abrir_ver_otros(accion="Ver"))
                self.boton_modificar.config(command=lambda : self.abrir_ver_otros(accion="Modificar"))
            case "Usuarios":
                logo = IMG_USUARIOS
                agregar_text = "Agregar Nuevo\nUsuario"
                ver_text = "Ver\nUsuarios"
                eliminar_text = "Eliminar\nUsuario"
                modificar_text = ""
                self.boton_agregar.config(command=self.abrir_agregar_usuario)
                self.boton_eliminar.config(command=self.abrir_eliminar_usuario)
                self.boton_ver.config(command=self.abrir_ver_usuarios)
            case "Opciones":
                logo = IMG_OPCIONES
                agregar_text = ""
                ver_text = ""
                eliminar_text = ""
                modificar_text = "Modificar Local\ndel Programa"
                self.boton_modificar.config(command=self.abrir_modificar_local)
            case _:
                logo = IMG_VENTAS
                agregar_text = "Registrar\nVenta"
                ver_text = "Ver Ventas\nRegistradas"
                eliminar_text = "Generar Reporte\ndel Día"
                modificar_text = "Generar Reporte\ndel Mes"
                self.boton_agregar.config(command=self.abrir_agregar_ventas)
                self.boton_ver.config(command=self.abrir_ver_ventas)
                self.boton_eliminar.config(command=self.abrir_generar_reporte_dia)
                self.boton_modificar.config(command=self.abrir_generar_reporte_mes)
                

        icono = Image.open(logo)
        icono_resized = icono.resize((128, 128))
        icono_tk = ImageTk.PhotoImage(icono_resized)

        label = tk.Label(root, image=icono_tk, background=self.bgcolor)
        label.image = icono_tk
        label.grid(row=0, column=0, rowspan=2, sticky="nswe")

        self.boton_agregar.config(text=agregar_text)
        self.boton_ver.config(text=ver_text)
        self.boton_eliminar.config(text=eliminar_text)
        self.boton_modificar.config(text=modificar_text)
        
        if self.rol_usuario==3 and self.opciones_seleccionada == "Inventario":
            self.boton_ver.grid(row=0, column=1, columnspan=2)
            self.boton_modificar.grid(row=1, column=1, columnspan=2)
        elif self.rol_usuario==3 and self.opciones_seleccionada == "Menu":
            self.boton_ver.grid(row=0, column=1, columnspan=2, rowspan=2)
        elif self.opciones_seleccionada == "Ventas":
            self.boton_agregar.grid(row=0, column=1)
            self.boton_ver.grid(row=0, column=2)
            self.boton_eliminar.grid(row=1, column=1)
            self.boton_modificar.grid(row=1, column=2)
        elif self.rol_usuario==3 and self.opciones_seleccionada == "Otros":
            self.boton_ver.grid(row=0, column=1, rowspan=2, columnspan=2)
        elif self.opciones_seleccionada == "Usuarios":
            self.boton_ver.grid(row=0, column=2)
            self.boton_agregar.grid(row=0, column=1)
            self.boton_eliminar.grid(row=1, column=1, columnspan=2)
        elif self.opciones_seleccionada == "Opciones":
            self.boton_modificar.grid(row=1, column=1, columnspan=2)
        else:
            self.boton_ver.grid(row=0, column=2)
            self.boton_modificar.grid(row=1, column=2)
            self.boton_agregar.grid(row=0, column=1)
            self.boton_eliminar.grid(row=1, column=1)
        

    def cambiar_opciones(self, tipo: str):
        for widget in self.panel_opciones.winfo_children():
            widget.destroy()  # Elimina cada widget del canvas

        self.opciones_seleccionada = tipo
        self.datos["Opcion_Inicio"] = self.opciones_seleccionada
        self.configurar_botones(self.panel_opciones)


    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(fill="both", expand=True, pady=10)

        b_perfil = comp.Boton(panel, text="Perfil", command=self.abrir_menu_perfil)
        b_perfil.pack(expand=True, side="left")

        b_cerrar_sesion = comp.Boton(panel, text="Cerrar\nSesión", command=self.cerrar_sesion)
        b_cerrar_sesion.pack(expand=True, side="left")
        
        b_salir = comp.Boton(panel, text="Salir", command=self.salir)
        b_salir.pack(expand=True, side="left")


    def abrir_agregar_ventas(self):
        self.destroy()
        av.AgregarVentas(datos=self.datos)


    def abrir_agregar_menu(self):
        self.destroy()
        am.AgregarMenu(datos=self.datos)


    def abrir_agregar_producto(self):
        self.destroy()
        iai.Agregar(datos=self.datos)


    def abrir_agregar_usuario(self):
        self.destroy()
        au.AgregarUsuario(datos=self.datos)


    def abrir_agregar_otro(self):
        self.destroy()
        ad.AgregarDatos(datos=self.datos)

    
    def abrir_eliminar_producto(self):
        self.destroy()
        iei.Eliminar(datos=self.datos)


    def abrir_eliminar_usuario(self):
        self.destroy()
        eu.EliminarUsuarios(datos=self.datos)


    def abrir_ver_menu(self):
        self.destroy()
        vm.VisualizarMenu(datos=self.datos)


    def abrir_eliminar_menu(self):
        self.destroy()
        em.Eliminar(datos=self.datos)


    def abrir_ver_usuarios(self):
        self.destroy()
        vu.VerUsuarios(datos=self.datos)

    
    def abrir_ver_ventas(self):
        self.destroy()
        vv.VerVentas(datos=self.datos)


    def abrir_ver_inventario(self):
        self.destroy()
        ivi.VerInventario(datos=self.datos)
    
    def abrir_ver_otros(self, accion: str):
        self.destroy()
        vod.VerDatos(datos=self.datos, accion=accion)

    
    def abrir_menu_perfil(self):
        self.destroy()
        mp.MenuPerfil(datos=self.datos)
    
    
    def abrir_modificar_menu(self):
        self.destroy()
        mm.Modificar(datos=self.datos)


    def abrir_modificar_local(self):
        self.destroy()
        ml.ModificarLocal(datos=self.datos)


    def abrir_generar_reporte_dia(self):
        self.destroy()
        gr.Generar(datos=self.datos, tipo="dia")
    
    def abrir_generar_reporte_mes(self):
        self.destroy()
        gr.Generar(datos=self.datos, tipo="mes")
    
    
    def salir(self):
        if ven.VentanaConfirmacion(self, texto="¿Seguro que deseas salir?", titulo_ventana="Salir", opcion1="Salir").obtener_respuesta():
            self.destroy()

    
    def cerrar_sesion(self):
        if ven.VentanaConfirmacion(self, texto="¿Seguro que deseas cerrar sesión?", titulo_ventana="Cerrar Sesión", opcion1="Cerrar Sesión").obtener_respuesta():
            self.destroy()
            self.datos.pop("Usuario_Logueado", None)
            self.datos.pop("Opcion_Inicio", None)
            gui.Login.Login(datos=self.datos)

        
    def actualizar_datos_usuario(self):
        pass

    
if __name__ == "__main__":
    a = Inicio()
    a.mainloop()