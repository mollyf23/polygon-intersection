from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from Point import Point
from Segment import Segment
import matplotlib.pyplot as plt

#helper functions so that we can draw on the matplotlib as we run the algorithm
def draw_point(ax: Axes, point: Point, color="red", marker="o"):
    x, y = (point.x(), point.y())
    point = ax.plot(x, y, c=color, marker=marker)
    ax.figure.canvas.draw()  
    ax.figure.canvas.flush_events()  
    plt.pause(1)
    return point[0]  

def draw_segment(ax: Axes, segment: Segment, color="red", linewidth=1):
    (x1, y1) = (segment.leftEndPoint().x(), segment.leftEndPoint().y())
    (x2, y2) = (segment.rightEndPoint().x(), segment.rightEndPoint().y())
    line: Line2D = ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth)
    ax.figure.canvas.draw()  
    ax.figure.canvas.flush_events()  
    plt.pause(1)  
    return line[0]

def draw_polygon(ax: Axes, poly_points, color="black", linewidth=1):
    if poly_points:
        x1, y1 = zip(*poly_points)
        ax.plot(x1 + (x1[0],), y1 + (y1[0],), marker='o', color=color, linewidth=linewidth)
        ax.figure.canvas.draw()  
        ax.figure.canvas.flush_events()  

#find intersection point
def draw_intersection_point(ax, event):
    draw_point(ax, event.point,color="yellow")
    line: Line2D = getLineByEndpoints(ax, event.segment.leftEndPoint(), event.segment.rightEndPoint(), "red") #segment 
    line2: Line2D = getLineByEndpoints(ax, event.segment2.leftEndPoint(), event.segment2.rightEndPoint(),"red") #segment 
    if (line): line.remove()
    if (line2): line2.remove()
    segnew = Segment(event.segment.rightEndPoint(), event.point) #new version of the segment before intersection
    seg2new = Segment(event.segment2.rightEndPoint(), event.point) #new version of the segment before intersection
    draw_segment(ax, segnew)
    draw_segment(ax, seg2new)
    return

#remove segments from before the intersection
def draw_intersection_event(ax, event):
    line: Line2D = getLineByEndpoints(ax, event.segment.leftEndPoint(), event.point, "red") #segment until intersection
    line2: Line2D = getLineByEndpoints(ax, event.segment2.leftEndPoint(), event.point, "red") #segment until intersection
    if (line): line.remove()
    if (line2): line2.remove()
    segEnew = Segment(event.point, event.segment.rightEndPoint()) #new version of the segment after intersection
    segAnew = Segment(event.point, event.segment2.rightEndPoint()) #new version of the segment after intersection
    draw_segment(ax, segEnew)
    draw_segment(ax, segAnew)
    return

def draw_left_endpoint(ax: Axes, event):
    point: Line2D = draw_point(ax, event.point)
    draw_segment(ax, event.segment)
    point.remove() #remove point at end of event
    return

def draw_right_endpoint(ax: Axes, event):
    line: Line2D = getLineByEndpoints(ax, event.segment.leftEndPoint(), event.segment.rightEndPoint(), "red")
    if (line): line.remove() #remove red line because its done
    point = draw_point(ax, event.point, color="green")
    plt.pause(.5)
    line = draw_segment(ax, event.segment, color="green")
    point.remove() #remove point at end of event
    line.set_color("black")
    return

def getLineByEndpoints(ax, leftEndpoint, rightEndpoint, color):
    for line in ax.lines:
        xdata, ydata = line.get_xdata(), line.get_ydata()

        if ((len(xdata)> 1 and len(ydata) > 1) and (xdata[0], ydata[0], xdata[1], ydata[1]) == (leftEndpoint.x(), leftEndpoint.y(), rightEndpoint.x(), rightEndpoint.y()) and line.get_color() == color):
            return line
