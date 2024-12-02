import tkinter as tk
import tkinter.ttk as ttk
import gui.Componentes as comp
import gui.Ventanas as ven
import gui.Inicio as i


class EliminarUsuarios(ven.VentanaPrincipal):
    def __init__(self, datos: dict):
        super().__init__(titulo="Eliminar Usuario", titulo_ventana="Eliminar\nUsuario")

        self.datos = datos
        self.datos_usuarios = self.datos["Usuarios"]
        self.usuarios = self.datos_usuarios.obtener_datos_usuarios()

        self.usuario_logueado = self.datos["Usuario_Logueado"]

        self.usuario_seleccionado = None

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

        

        self.tabla = comp.CustomTreeview(panel)
        self.tabla.create_table(head=["Nombre de Usuario", "Rol"])
        self.tabla.añadir_scrollbarv(1)
        self.agregar_datos()

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_usuario)
        
        self.tabla.pack(expand=True)


    def agregar_datos(self):
        usuarios = []

        for id_usuario in self.usuarios.keys():
            if self.usuarios[id_usuario][2] != 1 and self.usuario_logueado["Rol"] == 1 :
                usuarios.append([])
                usuarios[-1].append(self.usuarios[id_usuario][0])
                usuarios[-1].append(self.datos_usuarios.buscar_nombre_tipo_por_id(self.usuarios[id_usuario][2]))
            elif self.usuarios[id_usuario][2] == 3 and self.usuario_logueado["Rol"] == 2:
                usuarios.append([])
                usuarios[-1].append(self.usuarios[id_usuario][0])
                usuarios[-1].append(self.datos_usuarios.buscar_nombre_tipo_por_id(self.usuarios[id_usuario][2]))

        self.tabla.add_data(usuarios)

    
    def agregar_opciones(self):
        panel = tk.Frame(self, background=self.bgcolor)
        panel.pack(expand=True, fill="both", pady=10)

        self.b_eliminar = comp.Boton(panel, text="Eliminar Usuario\nSeleccionado", command=self.eliminar_usuario)
        self.b_eliminar.deshabilitar_boton()
        self.b_eliminar.pack(expand=True, side="left")

        b_filtrar = comp.Boton(panel, text="Filtrar", command=None)
        b_filtrar.pack(expand=True, side="left")

        b_volver = comp.Boton(panel, text="Volver", command=self.volver)
        b_volver.pack(expand=True, side="left")


    def seleccionar_usuario(self, event):
        curItem = self.tabla.focus()
        valores = self.tabla.item(curItem)["values"]

        print(valores)

        self.usuario_seleccionado = valores[0]
        self.b_eliminar.habilitar_boton()


    def eliminar_usuario(self):
        if ven.VentanaConfirmacion(self, texto="¿Seguro que desea\nEliminar este Usuario?", titulo_ventana="Eliminar Usuario").obtener_respuesta():
            if self.datos_usuarios.eliminar_usuario_existente(self.usuario_seleccionado):
                self.actualizar_tabla()
                self.datos_usuarios.recargar_datos()
                self.datos["Usuarios"] = self.datos_usuarios
                ven.VentanaAvisoTL(self, texto="¡Usuario Eliminado Exitosamente!", titulo_ventana="Eliminar Usuario").wait_window()
                self.volver()
            else:
                ven.VentanaAvisoTL(self, texto="¡No se pudo Eliminar el Usuario!", titulo_ventana="Error").wait_window()

        
    def actualizar_tabla(self):
        usuarios = []

        for id_usuario in self.usuarios.keys():
            if self.usuarios[id_usuario][2] != 1 and self.usuario_logueado["Rol"] == 1 :
                usuarios.append([])
                usuarios[-1].append(self.usuarios[id_usuario][0])
                usuarios[-1].append(self.datos_usuarios.buscar_nombre_tipo_por_id(self.usuarios[id_usuario][2]))
            elif self.usuarios[id_usuario][2] == 3 and self.usuario_logueado["Rol"] == 2:
                usuarios.append([])
                usuarios[-1].append(self.usuarios[id_usuario][0])
                usuarios[-1].append(self.datos_usuarios.buscar_nombre_tipo_por_id(self.usuarios[id_usuario][2]))

        self.tabla.recharge_data(usuarios)

    
    def volver(self):
        self.destroy()
        i.Inicio(datos=self.datos)