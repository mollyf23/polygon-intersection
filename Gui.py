import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class PolygonIntersectionGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Plotter")

        # panel for input
        self.input_panel = ttk.Frame(self.root)
        self.input_panel.pack(pady=10, padx=10, fill="x")

        # Polygon 1
        ttk.Label(self.input_panel, text="Polygon 1 Points (x1,y1 x2,y2 ...):").grid(row=0, column=0)
        self.poly1_entry = ttk.Entry(self.input_panel, width=50)
        self.poly1_entry.grid(row=0, column=1, padx=5)

        # Polygon 2
        ttk.Label(self.input_panel, text="Polygon 2 Points (x1,y1 x2,y2 ...):").grid(row=1, column=0)
        self.poly2_entry = ttk.Entry(self.input_panel, width=50)
        self.poly2_entry.grid(row=1, column=1, padx=5)

        # Plot Button
        self.plot_button = ttk.Button(self.input_panel, text="Plot Polygons", command=self.shamos_hoey_test)
        self.plot_button.grid(row=2, column=0, columnspan=2, pady=5)

        # use a matplotlib figure to show the algorithms
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Polygons")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=10, padx=10)

    def parse_points(self, points_str):
        #Parse a string of points into a list of tuples.
        try:
            points = [tuple(map(float, point.split(','))) for point in points_str.strip().split()]
            return points
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input format: {e}")
            return None
        

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonIntersectionGui(root)
    root.mainloop()
    
