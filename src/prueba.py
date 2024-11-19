import gui.Login2
import data.Usuarios as u

datos_usuarios = u.Usuarios()

datos = {
    "Usuarios": datos_usuarios
}

a = gui.Login2.Login(datos=datos)
a.mainloop()



# import tkinter as tk
# from tkinter import font

# root = tk.Tk()

# # Crear una fuente de tamaño 24
# custom_font = font.Font(family="Impact", size=24)

# # Medir el ancho de un carácter específico, por ejemplo, "W"
# char_width = custom_font.measure("I")
# print(f"El ancho del carácter 'I' es: {char_width} píxeles")
# char_width = custom_font.measure("N")
# print(f"El ancho del carácter 'N' es: {char_width} píxeles")

# # Medir el ancho de una cadena de texto
# text_width = custom_font.measure("Iniciar Sesión")
# print(f"El ancho del texto 'Iniciar Sesión' es: {text_width} píxeles")

# root.mainloop()


# import sys

# def encontrar_divisores(n: int):
#     divisores = []

#     div = 1

#     while div <= n/2:
#         if n % div == 0:
#           divisores.append(div)
#         div += 1

#     return divisores



# def mostrar_divisores(div: list):
#     print()
#     print("Los divisores distintos de n son:")
#     for i in div:
#         if not i==div[-1]:
#             print(f"{i} - ", end='')
#         else:
#             print(i)

#     print()
#     print(f"Divisor Mayor: {i}")
#     print()


# mostrar_divisores(encontrar_divisores(int(sys.argv[1])))