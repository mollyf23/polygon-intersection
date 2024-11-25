import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Bentley_Ottman import intersection_BentleyOttman
import time
from Point import Point
from Polygon import Polygon

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

        # Results and intersection points section
        self.create_results_section(self.tab_without_plot)
        intersection_frame = ttk.LabelFrame(self.tab_with_plot, text="Intersection Points")
        intersection_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.intersection_plot = tk.Text(intersection_frame, height=10, wrap="word")
        self.intersection_plot.pack(fill="both", expand=True, padx=5, pady=5)

        intersection_frame2 = ttk.LabelFrame(self.tab_without_plot, text="Intersection Points")
        intersection_frame2.pack(pady=10, padx=10, fill="both", expand=True)

        self.intersection_noplot = tk.Text(intersection_frame2, height=10, wrap="word")
        self.intersection_noplot.pack(fill="both", expand=True, padx=5, pady=5)


    def create_input_panel(self, parent, draw):
        # panel for input
        input_panel = ttk.Frame(parent)
        input_panel.pack(pady=10, padx=10, fill="x")

        # Polygon 1 input
        ttk.Label(input_panel, text="Polygon 1 Points (x1,y1 x2,y2 ...):").grid(row=0, column=0)
        poly1_entry = ttk.Entry(input_panel, width=50)
        poly1_entry.grid(row=0, column=1, padx=5)                     

        # Polygon 2 input
        ttk.Label(input_panel, text="Polygon 2 Points (x1,y1 x2,y2 ...):").grid(row=1, column=0)
        poly2_entry = ttk.Entry(input_panel, width=50)
        poly2_entry.grid(row=1, column=1, padx=5)

        # Plot Button
        #the draw boolean determines if it will run with drawing enabled    
        bentley_ottman_button = ttk.Button(input_panel, text="Bentley Ottman", command=lambda: self.bentley_ottman(draw, poly1_entry, poly2_entry)).grid(row=2, column=0, pady=5, padx=(30,10))
        sh_button = ttk.Button(input_panel, text="Sutherland Hodgman", command=lambda: self.sutherland_hodgman(draw, poly1_entry, poly2_entry)).grid(row=2, column=1, pady=5, padx=(30,10))


    def create_results_section(self, parent):
        # Results section
        results_frame = ttk.Frame(parent)
        results_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(results_frame, text="Algorithm").grid(row=0, column=0, padx=30)
        ttk.Label(results_frame, text="Time Taken (ms)").grid(row=2, column=0, padx=30)

        # Labels for timing results
        self.bentley_ottman_time_label = ttk.Label(results_frame, text="Not computed")
        self.bentley_ottman_time_label.grid(row=2, column=1, padx=5)

        self.sutherland_hodgman_time_label = ttk.Label(results_frame, text="Not computed")
        self.sutherland_hodgman_time_label.grid(row=2, column=2, padx=5)

        # Algorithm names
        ttk.Label(results_frame, text="Bentley Ottman").grid(row=0, column=1, padx=30)
        ttk.Label(results_frame, text="Sutherland Hodgman").grid(row=0, column=2, padx=30)

    def parse_points(self, points_str):
        try:
            points = [tuple(map(float, point.split(','))) for point in points_str.strip().split()]
            return points
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input format: {e}")
            return None

    def display_intersection_points(self, points, results_display):
        results_display.delete(1.0, tk.END)
        if points:
            for point in points:
                results_display.insert(tk.END, f"{point}\n")
        else:
            results_display.insert(tk.END, "No intersection points found.\n")

    def bentley_ottman(self, draw, poly_points1, poly_points2):
        start_time = time.perf_counter()

        poly1_points = self.parse_points(poly_points1.get())
        poly2_points = self.parse_points(poly_points2.get())
        if not poly1_points or not poly2_points:
            return

        events = intersection_BentleyOttman(self.ax, poly1_points, poly2_points, draw)

        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.bentley_ottman_time_label.config(text=f"{elapsed_time:.2f} ms")

        if (draw): self.display_intersection_points(events, self.intersection_plot)
        else: self.display_intersection_points(events, self.intersection_noplot)

    def sutherland_hodgman(self, draw, poly_points1, poly_points2):
        #    Create polygon from first set of points.
        poly1_points = self.parse_points(poly_points1.get())

        pts = []
        for i in range(0, len(poly1_points[0]), 2):
            pts.append(Point(poly1_points[0][i], poly1_points[0][i + 1]))

        clipper_pts = Polygon(pts)

        #    Create polygon from first set of points.
        poly2_points = self.parse_points(poly_points2.get())
        pts = []
        for i in range(0, len(poly2_points[0]), 2):
            pts.append(Point(poly2_points[0][i], poly2_points[0][i + 1]))
        
        polygon_pts = Polygon(pts)
        
        #    Draw the original two polygons.
        self.ax.clear()
        clipper_pts.plot(self.ax, "g")
        polygon_pts.plot(self.ax, "b")

        start_time = time.perf_counter()

        events = polygon_pts.intersection_SH(polygon_pts, clipper_pts)
        
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.sutherland_hodgman_time_label.config(text=f"{elapsed_time:.2f} ms")
        
        events[len(events) - 1].plot(self.ax, 'r')
        
        '''    ANIMATION SEDCTION
        #for e in events:
        for i in range(len(events)):
            if i != 0:
                events[i - 1].clearPlot()
                
            events[i].plot(self.ax, 'r')
        
            plt.pause(2)
            #self.ax.clear()
        '''
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonIntersectionGui(root)
    root.mainloop()

