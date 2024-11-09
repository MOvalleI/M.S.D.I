import tkinter as tk
import tkinter.ttk as ttk

class VerInventario(tk.Tk):
    def __init__(self, datos: dict=None):
        super().__init__()


    
    def configurar_ventana(self):
        self.title("Ver Inventario")

if __name__=="__main__":
    a = VerInventario()
    a.mainloop()