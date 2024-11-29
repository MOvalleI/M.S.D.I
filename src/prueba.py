import tkinter as tk

class prueba(tk.Tk):
    def __init__(self):
        super().__init__()

        self.agregar_pin()


    def agregar_pin(self):
        self.pin = PatternUnlockApp(self)
        self.pin.pack(expand=True)



class PatternUnlockApp(tk.Frame):
    def __init__(self, parent, pattern = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.radius = 20
        self.padding = 50

        self.pattern = pattern

        self.points = []
        self.lines = []
        self.selected_points = []
        self.current_line = None

        self.canvas = tk.Canvas(self, width=300, height=300, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.draw_grid()

        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw_grid(self):
        width = self.canvas.winfo_reqwidth()
        height = self.canvas.winfo_reqheight()

        step_x = (width - 2 * self.padding) // 2
        step_y = (height - 2 * self.padding) // 2

        for row in range(3):
            for col in range(3):
                x = self.padding + col * step_x
                y = self.padding + row * step_y
                point_id = self.canvas.create_oval(
                    x - self.radius, y - self.radius,
                    x + self.radius, y + self.radius,
                    fill="gray", outline="black"
                )
                self.points.append((point_id, x, y))

    def on_drag(self, event):
        for point_id, x, y in self.points:
            if point_id not in self.selected_points:
                if (x - self.radius <= event.x <= x + self.radius and
                        y - self.radius <= event.y <= y + self.radius):
                    self.selected_points.append(point_id)
                    self.canvas.itemconfig(point_id, fill="blue")
                    if len(self.selected_points) > 1:
                        last_x, last_y = self.points[self.selected_points[-2] - 1][1:]
                        self.lines.append(
                            self.canvas.create_line(last_x, last_y, x, y, fill="blue", width=2)
                        )
                    break

        if self.selected_points:
            last_x, last_y = self.points[self.selected_points[-1] - 1][1:]
            if self.current_line:
                self.canvas.delete(self.current_line)
            self.current_line = self.canvas.create_line(
                last_x, last_y, event.x, event.y, fill="blue", width=2
            )

    def on_release(self, event):
        for point in self.points:
            self.canvas.itemconfig(point[0], fill="gray")
        for line in self.lines:
            self.canvas.delete(line)
        if self.current_line:
            self.canvas.delete(self.current_line)
        
        selected_pattern = str(self.selected_points)

        if self.pattern:
            if selected_pattern == self.pattern:
                print(True)
            else:
                print(False)
        else:
            self.pattern = selected_pattern
            
        self.selected_points.clear()
        self.lines.clear()
        self.current_line = None

    def get_pattern(self):
        return self.pattern

    def set_pattern(self):
        self.pattern = None
        
if __name__ == "__main__":
    root = prueba()

    root.mainloop()