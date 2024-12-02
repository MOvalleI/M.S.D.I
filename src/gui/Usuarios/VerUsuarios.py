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

        usuarios = self.datos_usuarios.obtener_usuarios_filtro()

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=["Nombre de Usuario", "Rol"])
        self.tabla.añadir_scrollbarv(1)
        self.tabla.add_data(usuarios)
        self.tabla.pack(expand=True)


    def recargar_informacion(self, nombre=None, id_rol=None):
        usuarios = self.datos_usuarios.obtener_usuarios_filtro(nombre, id_rol)
        self.tabla.recharge_data(usuarios)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_filtrar = comp.Boton(panel, text="Filtrar", command=self.abrir_filtrar)
        b_filtrar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")

    
    def abrir_filtrar(self):
        Filtrar(self)


    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)


class Filtrar(ven.VentanaTopLevel):
    def __init__(self, parent = None):
        super().__init__(parent, titulo_ventana = "Ventana Principal", titulo = "Ventana")

        self.parent = parent

        self.rol_seleccionado = None

        self.configurar_ventana()


    def configurar_ventana(self):
        self.agregar_titulo()
        self.agregar_entry_usuario()
        self.agregar_lista_roles()
        self.agregar_opciones()


    def agregar_entry_usuario(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Nombre de Usuario:")
        label.pack(pady=5)

        self.nombre_entry = comp.CampoTexto(panel)
        self.nombre_entry.config(width=25)
        self.nombre_entry.pack(pady=5)


    def agregar_lista_roles(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        label = tk.Label(panel, background=self.bgcolor, foreground=self.fgcolor, font=(self.font, 16), text="Rol:")
        label.pack(pady=5)

        roles = self.parent.datos_usuarios.obtener_datos_tipo()

        valores = ["(nada)"]

        for valor in roles.keys():
            valores.append(roles[valor][0])

        valores.pop(1) # Elimina el Administrador de la lista

        self.lista_roles = ttk.Combobox(panel, values=valores)
        self.lista_roles.config(state="readonly")
        self.lista_roles.pack(pady=5)
        self.lista_roles.current(0)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        b_filtrar = comp.Boton(panel, text="Aplicar\nFiltro", command=self.filtrar)
        b_filtrar.pack(expand=True, side="left")

        b_cancelar = comp.Boton(panel, text="Cancelar", command=self.destroy)
        b_cancelar.pack(expand=True, side="left")


    def filtrar(self):
        nombre = self.nombre_entry.get()

        if nombre == "":
            nombre = None

        rol = self.lista_roles.get()

        if rol != "(nada)":
            id_rol = self.parent.datos_usuarios.buscar_id_tipo_por_nombre(rol)
        else:
            id_rol = None

        self.destroy()
        self.parent.recargar_informacion(nombre, id_rol)
        
