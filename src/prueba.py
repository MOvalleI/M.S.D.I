import tkinter as tk
import textwrap





# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo con salto de línea")

# Texto largo que quieres mostrar en el label
texto_largo = "ahola ladsa"

# Establece el ancho máximo de la línea
ancho_maximo = 15

# Usamos textwrap para envolver el texto
texto_envuelto = texto_largo.replace(" ", "\n")

# Crear un label y asignarle el texto envuelto
label = tk.Label(root, text=texto_envuelto, font=("Arial", 12))
label.pack(padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()
