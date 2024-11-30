import data.InventarioDB as idb
import data.Usuarios as u
import gui.Login as l
import gui.Ventanas as ven

class MSDI:
    def __init__(self):
        self.datos_inventario = None
        self.datos_usuarios = None
        self.ventana_cargando()

        if self.datos_inventario is not None: 
            self.datos_inventario.cerrar()

        if self.datos_usuarios is not None: 
            self.datos_inventario.cerrar_conexion()
        

    def ventana_cargando(self):
        self.loading = ven.VentanaAvisoRoot(titulo_ventana="M.S.D.I | Micro Sistema de Inventario", tipo=ven.TIPO_AVISO_2, texto="Conectando con la base de\ndatos de 'Inventario'")
        self.loading.after(200, self.inicializar)
        self.loading.mainloop()

    def inicializar(self):
        try:
            self.loading.aumentar_progreso(33)
            datos_inventario = idb.InventarioDB()

            self.loading.aumentar_progreso(33)
            self.loading.configurar_texto("Conectando con la base de\ndatos de 'Usuario'")
            datos_usuarios = u.UsuariosDB()

            datosDB = {
                "Inventario": datos_inventario,
                "Usuarios": datos_usuarios
            }

            self.loading.aumentar_progreso(34)
            self.loading.destroy()
            l.Login(datos=datosDB)
        except Exception as e:
            print(e)
            self.loading.destroy()
            root = ven.VentanaAvisoRoot(titulo_ventana="¡Ha Ocurrido un Error!")
            root.configurar_texto("No se pudo conectar\na la base de datos")
            

if __name__ == "__main__":
    MSDI()

