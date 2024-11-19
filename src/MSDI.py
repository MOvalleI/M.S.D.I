import data.InventarioDB as idb
import data.Usuarios as u
import gui.Login as l
import gui.Login2 as l2

def init():
    datos_inventario = idb.InventarioDB()
    datos_usuarios = u.Usuarios()

    datosDB = {
        "Inventario": datos_inventario,
        "Usuarios": datos_usuarios
    }

    root = l2.Login(datos=datosDB)
    root.mainloop()
    datos_inventario.cerrar()

init()