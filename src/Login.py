import tkinter as tk
from PIL import Image, ImageTk

class Login(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Login")

        self.users_list = ["Admin", "Jose", "Eustacio", "Anaconda"]
        self.users_panel_list = []
        self.selected_panel = None  # Variable para guardar el panel seleccionado

        self.geometry("1024x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        users_panel = tk.Frame(self)
        users_panel.grid(column=0, row=0, rowspan=3, sticky="nsew")

        self.user_entry = tk.Entry(users_panel)
        self.user_entry.pack(pady=(0, 10))  # Reducir padding vertical

        self.another_panel = tk.Frame(users_panel)
        self.another_panel.pack(expand=True, fill="both")

        # Cambios aquí para reducir el espacio entre canvas y scrollbar
        self.canvas = tk.Canvas(self.another_panel, highlightthickness=0)  # Eliminar borde alrededor del canvas
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.another_panel, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Vincular el evento de la rueda del mouse
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        for i in range(len(self.users_list)):
            self.crear_panel_usuario(self.inner_frame, self.users_list[i], i)

    def crear_panel_usuario(self, root: tk.Frame, nombre: str, id: int) -> None:
        panel = tk.Frame(root, bd=1, relief="solid")
        panel.id = id
        panel.selected = False  # Inicialmente no seleccionado

        # Cargar la imagen y ajustarla a 50x50
        image = Image.open("./src/img/default user.jpg")
        image_resized = image.resize((128, 128))

        photo = ImageTk.PhotoImage(image_resized)

        # Crear un Label para la imagen
        image_label = tk.Label(panel, image=photo)
        image_label.image = photo
        image_label.pack(pady=(0, 2))  # Reducir padding entre imagen y texto

        # Hacer clic en la imagen también selecciona el panel
        image_label.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))

        # Crear un Label para el texto
        text_label = tk.Label(panel, text=nombre)
        text_label.pack()

        panel.bind("<Button-1>", lambda e: self.on_panel_click(e, panel))

        self.users_panel_list.append(panel)
        panel.pack(pady=(0, 2))  # Reducir espacio entre los paneles

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta//120)), "units")

    def on_panel_click(self, event, panel):
        # Desmarcar el panel seleccionado previamente
        if self.selected_panel is not None:
            self.selected_panel.selected = False
            self.selected_panel.configure(bg="SystemButtonFace")  # Color por defecto

        # Marcar el nuevo panel seleccionado
        panel.selected = True
        panel.configure(bg="lightblue")  # Color de selección
        self.selected_panel = panel  # Actualizar el panel seleccionado
        print(f"Panel {panel.id} clicked")

if __name__ == "__main__":
    root = Login()
    root.mainloop()
