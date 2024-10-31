import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

DEFAULT_PFP = "./img/default.jpg"
BG_IMAGE = "./img/Imagen fondo para login.png"
LOGO = "./img/Letras El ricon de los 4 diablitos.png"
USERNAMES = ["Admin", "Jose", "Eustacio", "Anaconda", "suelto", "otro", "otro mas"]

class Canvas(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Prueba de Canvas")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)

        # Posiciones iniciales para dibujar los cuadrados en el canvas
        self.yPos = 20
        self.square_sides = 300 # Tamaño de los cuadrados

        # Tamaño del rectangulo donde se ingresan los datos
        self.rec_canv_width = 772
        self.rec_canv_height = 620

        left_panel = self.crear_panel_izquierdo(root=self)
        left_panel.grid(column=0, row=0, sticky="nwse")


        right_panel = self.crear_panel_derecho(root=self)
        right_panel.grid(column=1, row=0, sticky="nswe", columnspan=2)

        self.bind("<MouseWheel>", self.accion_rueda_mouse)


    def crear_panel_izquierdo(self, root: tk.Tk) -> tk.Frame:
        panel = tk.Frame(root)

        panel.grid_rowconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=8)
        panel.grid_columnconfigure(0, weight=1)

        users_entry = tk.Entry(panel)
        users_entry.grid(column=0, row=0)

        self.users_panel = self.crear_panel_usuarios(root=panel)
        self.users_panel.grid(column=0, row=1, sticky="nswe")

        return panel


    def crear_panel_usuarios(self, root: tk.Frame) -> tk.Frame:
        panel = tk.Frame(root)

        self.canvas = tk.Canvas(panel, width=0)
        self.canvas.pack(fill="both", expand=True)

        for i in range(len(USERNAMES)):
            self.agregar_usuario(self.canvas, i, USERNAMES[i], self.square_sides, self.yPos)
            self.yPos += self.square_sides + 10

        scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview, width=20)
        scrollbar.pack(fill="y", side="right")

        self.canvas.config(yscrollcommand=scrollbar.set) 
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        return panel


    def agregar_usuario(self, root: tk.Canvas, id: int, user: str, size: int, yPos: int) -> None:
        panel = tk.Frame(root)

        panel.id = id

        pfp = Image.open(DEFAULT_PFP)
        pfp_tk = ImageTk.PhotoImage(pfp)

        image_label = tk.Label(panel, image=pfp_tk)
        image_label.image = pfp_tk
        image_label.pack(expand=True)

        name_label = tk.Label(panel, text=user, anchor="center", font=("Segoe ui", 16))
        name_label.str_id = user
        name_label.pack(expand=True, fill="x", pady=5)

        panel.place(width=size, height=size, x=50)
        root.create_window(20, yPos, anchor="nw", window=panel)


    def crear_panel_derecho(self, root: tk.Tk) -> tk.Frame:
        panel = tk.Frame(self)

        bg_canvas = tk.Canvas(panel, width=1030, height=720, background="grey")

        background_image = Image.open(BG_IMAGE)
        resized_img = background_image.resize((1030, 720))
        background_image_tk = ImageTk.PhotoImage(resized_img)

        bg_canvas.image = background_image_tk
        bg_canvas.create_image(0, 0, anchor="nw", image=background_image_tk)
        bg_canvas.place(x=0, y=0)

        return panel


    def limpiar_canvas(canvas) -> None:
        for widget in canvas.winfo_children():
            widget.destroy()  # Elimina cada widget del canvas

    
    def accion_rueda_mouse(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta//120)), "units")



if __name__ == "__main__":
    root = Canvas()
    root.mainloop()