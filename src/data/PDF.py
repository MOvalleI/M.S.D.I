import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from PIL import ImageGrab
from io import BytesIO

class PDF_Boleta():
    def __init__(self, consultor, imagen, dimensiones_imagen):
        self.datos = consultor
        self.imagen = imagen
        self.dimensiones = dimensiones_imagen
        
        encabezados = ['Nombre', 'Cantidad Vendida', 'Ganancia']

        name = "Boleta.pdf"

        data = [["Hola","Hola","Hola"],["Hola","Hola","Hola"],["Hola","Hola","Hola"]]

        self.generar_pdf(data, encabezados, name)
        
    def check_page_break(self, y, line_height, c):
        if y < line_height:
            c.showPage()
            c.setFont("Helvetica", 12)
            return 750  # Reiniciar la posición y
        return y

    # Función para generar el PDF
    def generar_pdf(self, datos, encabezados, name):
        c = canvas.Canvas(name, pagesize=letter)

        # Dibujar el título centrado
        c.setFont("Helvetica-Bold", 24)
        title = "Boleta del dia " + str(datetime.now().strftime("%d/%m/%Y"))
        title_width = c.stringWidth(title, "Helvetica-Bold", 24)
        c.drawString((letter[0] - title_width) / 2, 750, title)
    
        # Configuración de la fuente y tamaño del texto
        c.setFont("Helvetica", 12)
        
        # Coordenadas iniciales para el texto
        width, height = letter
        x = 50
        y = 710
        line_height = 20  # Altura de cada línea de texto

        # Dibujar encabezados
        for number in range(3):
            if number == 0:
                position = x
            elif number == 1:
                position = 380
            elif number == 2:
                position = width - x - c.stringWidth(encabezados[number])
        
            c.drawString(position, y, encabezados[number])
        
        y -= line_height
        
        # Dibujar los datos
        for conjunto in datos:
            conjunto = tuple(conjunto)
            for number in range(3):
                if number == 0:
                    position = x
                    c.drawString(position, y, f"{conjunto[number]}")
                elif number == 1:
                    position = 380
                    c.drawString(position, y, f"{conjunto[number]}")
                elif number == 2:
                    position = width - x - c.stringWidth(f"${conjunto[number]}")
                    c.drawString(position, y, f"${conjunto[number]}")

            y -= line_height
            y = self.check_page_break(y, line_height, c)
    
        # Calcular y dibujar el precio final
        precio_final = self.precio_total()
        precio_final_texto = f"Precio Total: ${precio_final}"
    
        y -= line_height
        y = self.check_page_break(y, line_height, c)
        c.drawString(width - x - c.stringWidth(precio_final_texto), y, precio_final_texto)

        #Dibujar firma
        y -= line_height
        y = self.check_page_break(y, self.dimensiones[1] + line_height, c)
        c.drawString(x, y, "Firma: ")
        y -= line_height
        c.drawImage(self.imagen, x, y - self.dimensiones[1], self.dimensiones[0], self.dimensiones[1])       
    
        # Guardar el PDF
        c.save()

    def precio_total(self):
        return 10
    
    
class DibujarFirma(tk.Frame):
    def __init__(self, parent, datosDB, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.datosDB = datosDB
        
        self.last_x = 0
        self.last_y = 0

        self.canvas = tk.Canvas(self, width=300, height=150, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw(self, event):
        x = event.x
        y = event.y
        
        if not self.last_x and not self.last_y:
            self.last_x = x
            self.last_y = y
            
        self.canvas.create_line(self.last_x,self.last_y,x,y,fill="blue")
        
        self.last_x = x
        self.last_y = y

    def on_release(self, event):
        self.last_x = 0
        self.last_y = 0

    def draw_delete(self):
        self.canvas.delete("all")
        self.lines.clear()

    def pasar_al_PDF(self):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        image = ImageGrab.grab(bbox=(x, y, x+width, y+height))

        image_buffer = BytesIO()
        
        image.save(image_buffer, format="PNG")

        image_buffer.seek(0)
        
        PDF_Boleta(consultor = self.datosDB["Inventario"], imagen = ImageReader(image_buffer), dimensiones_imagen = (width, height))