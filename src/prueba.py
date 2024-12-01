import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

def seleccionar_fecha():
    def obtener_fecha(event):
        # Obtener la fecha seleccionada
        fecha_seleccionada = calendario.get_date()
        # Actualizar la entrada principal con la fecha seleccionada
        fecha.set(fecha_seleccionada)
        # Cerrar la ventana del calendario
        ventana_calendario.destroy()

    # Crear una nueva ventana para el calendario
    ventana_calendario = tk.Toplevel()
    ventana_calendario.title("Seleccionar Fecha")

    # Configurar el calendario
    calendario = Calendar(ventana_calendario, date_pattern="yyyy-mm-dd")
    calendario.pack(pady=10)

    # Vincular el evento <<CalendarSelected>> al calendario
    calendario.bind("<<CalendarSelected>>", obtener_fecha)

def deseleccionar_fecha():
    # Restablecer la fecha en la entrada a un valor predeterminado
    fecha.set("Seleccione una fecha")
    # Si deseas limpiar el calendario también:
    calendario.selection_clear()

# Ventana principal
root = tk.Tk()
root.title("Seleccionar Fecha")

# Variable para almacenar la fecha seleccionada
fecha = tk.StringVar(value="Seleccione una fecha")

# Entrada para mostrar la fecha seleccionada
entrada_fecha = ttk.Entry(root, textvariable=fecha, state="readonly", width=20)
entrada_fecha.pack(pady=10)

# Botón para abrir el calendario
btn_abrir_calendario = ttk.Button(root, text="Abrir Calendario", command=seleccionar_fecha)
btn_abrir_calendario.pack(pady=10)

# Botón para deseleccionar la fecha
btn_deseleccionar = ttk.Button(root, text="Deseleccionar Fecha", command=deseleccionar_fecha)
btn_deseleccionar.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
