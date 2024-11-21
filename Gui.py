import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Shamos_Hoey import intersection_ShamosHoey
import time 



class PolygonIntersectionGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Plotter")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        # Tab 1: With matplotlib figure
        self.tab_with_plot = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_with_plot, text="Visualize")

        # Tab 2: Without matplotlib figure
        self.tab_without_plot = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_without_plot, text="Compare Time Efficiency")

        self.create_input_panel(self.tab_with_plot, True)
        self.create_input_panel(self.tab_without_plot, False)

        # use a matplotlib figure to show the algorithms
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Polygons")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, self.tab_with_plot)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=10, padx=10)
        self.create_results_section(self.tab_without_plot)

    def create_input_panel(self, parent, draw):
        # panel for input
        self.input_panel = ttk.Frame(parent)
        self.input_panel.pack(pady=10, padx=10, fill="x")

        # Polygon 1 input
        ttk.Label(self.input_panel, text="Polygon 1 Points (x1,y1 x2,y2 ...):").grid(row=0, column=0)
        self.poly1_entry = ttk.Entry(self.input_panel, width=50)
        self.poly1_entry.grid(row=0, column=1, padx=5)                     

        # Polygon 2 input
        ttk.Label(self.input_panel, text="Polygon 2 Points (x1,y1 x2,y2 ...):").grid(row=1, column=0)
        self.poly2_entry = ttk.Entry(self.input_panel, width=50)
        self.poly2_entry.grid(row=1, column=1, padx=5)

        # Plot Button
        #the draw boolean determines if it will run with drawing enabled    
        self.shamos_hoey_button = ttk.Button(self.input_panel, text="Shamos Hoey", command=lambda: self.shamos_hoey(draw)).grid(row=2, column=0, pady=5, padx=(30,10))
        self.sh_button = ttk.Button(self.input_panel, text="Shermann Hotchman", command=lambda: self.shamos_hoey(draw)).grid(row=2, column=1, pady=5, padx=(30,10))


    def create_results_section(self, parent):
        # Results section
        results_frame = ttk.Frame(parent)
        results_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(results_frame, text="Algorithm").grid(row=0, column=0, padx=30)
        ttk.Label(results_frame, text="Time Taken (ms)").grid(row=2, column=0, padx=30)

        # Labels for timing results
        self.shamos_hoey_time_label = ttk.Label(results_frame, text="Not computed")
        self.shamos_hoey_time_label.grid(row=2, column=1, padx=5)

        self.shermann_hotchman_time_label = ttk.Label(results_frame, text="Not computed")
        self.shermann_hotchman_time_label.grid(row=2, column=2, padx=5)

        # Algorithm names
        ttk.Label(results_frame, text="Shamos Hoey").grid(row=0, column=1, padx=30)
        ttk.Label(results_frame, text="Shermann Hotchman").grid(row=0, column=2, padx=30)
        
    def parse_points(self, points_str):
        #Parse a string of points into a list of tuples.
        try:
            points = [tuple(map(float, point.split(','))) for point in points_str.strip().split()]
            return points
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input format: {e}")
            return None

    def shamos_hoey(self, draw):
        start_time = time.perf_counter()
        poly1_points = self.parse_points(self.poly1_entry.get())
        poly2_points = self.parse_points(self.poly2_entry.get())
        events = intersection_ShamosHoey(self.ax, poly1_points, poly2_points)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.shamos_hoey_time_label.config(text=f"{elapsed_time:.2f} ms")
        for e in events:
            print(f"{e.point}",)


if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonIntersectionGui(root)
    root.mainloop()
    
