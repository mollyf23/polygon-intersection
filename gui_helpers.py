from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from Point import Point
from Segment import Segment
import matplotlib.pyplot as plt

#helper functions so that we can draw on the matplotlib as we run the algorithm
def draw_point(ax: Axes, point: Point, color="red", marker="o", size=5):
    x, y = (point.x(), point.y())
    ax.scatter(x, y, c=color, s=size)
    ax.figure.canvas.draw()  
    ax.figure.canvas.flush_events()  
    plt.pause(1)  

def draw_segment(ax: Axes, segment: Segment, color="red", linewidth=1):
    (x1, y1) = (segment.leftEndPoint().x(), segment.leftEndPoint().y())
    (x2, y2) = (segment.rightEndPoint().x(), segment.rightEndPoint().y())
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth)
    ax.figure.canvas.draw()  
    ax.figure.canvas.flush_events()  
    plt.pause(1)  


def draw_polygon(ax: Axes, poly_points, color="black"):
    if poly_points:
        x1, y1 = zip(*poly_points)
        ax.plot(x1 + (x1[0],), y1 + (y1[0],), marker='o')
        ax.figure.canvas.draw()  
        ax.figure.canvas.flush_events()  
        plt.pause(1)  

#for shamos hoey
def draw_intersection_point(ax, event, segE, segA):
    draw_point(ax, event.point,color="yellow")
    draw_segment(ax, segE, color="yellow")
    draw_segment(ax, segA, color="yellow")
    #todo: cut off chunk of segment
    return

def draw_left_endpoint(ax, event):
    draw_point(ax, event.point)
    draw_segment(ax, event.segment)
    return

def draw_right_endpoint(ax, event):
    draw_point(ax, event.point)
    #todo: erase segment
    return