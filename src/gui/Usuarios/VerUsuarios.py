import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i


class VerUsuarios(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Ver Usuarios", titulo_ventana="Ver Usuarios")

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuarios = self.datos_usuarios.obtener_datos_usuarios()

        self.configurar_ventana()

    
    def configurar_ventana(self):
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.volver)

        self.agregar_titulo()
        self.agregar_tabla()
        self.agregar_opciones()

        self.centrar_ventana()

    
    def agregar_tabla(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        usuarios = []

        for id_usuario in self.usuarios.keys():
            usuarios.append([])
            usuarios[-1].append(self.usuarios[id_usuario][0])
            usuarios[-1].append(self.datos_usuarios.buscar_nombre_tipo_por_id(self.usuarios[id_usuario][2]))


        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=["Nombre de Usuario", "Rol"])
        self.tabla.add_data(usuarios)
        self.tabla.pack(expand=True)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_filtrar = comp.Boton(panel, text="Filtrar", command=None)
        b_filtrar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")

    
    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)