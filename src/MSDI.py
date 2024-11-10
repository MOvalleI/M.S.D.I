import data.InventarioDB as idb
import data.Usuarios as u
import gui.Login as l
 
class MSDI:
    def __init__(self):
        datos_inventario = idb.InventarioDB()
        datos_usuarios = u.Usuarios()

        datosDB = {
            "Inventario": datos_inventario,
            "Usuarios": datos_usuarios
        }

        root = l.Login(datos=datosDB)
        root.mainloop()


if __name__ == "__main__":
    MSDI()