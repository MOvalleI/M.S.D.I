import tkinter as tk
from PIL import Image, ImageTk

FLECHA_IZQUIERDA = r".\src\img\botones\flecha-izquierda.png"

class View(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.image = Image.open(FLECHA_IZQUIERDA)
        resz = self.image.resize((50, 50))
        self.image_tik = ImageTk.PhotoImage(resz)
        b = tk.Button(self, text=" Página Anterior", image=self.image_tik, compound="left")
        b.pack(side="top")

if __name__ == "__main__":
    root = tk.Tk()
    view = View(root)
    view.pack(side="top", fill="both", expand=True)
    root.mainloop()