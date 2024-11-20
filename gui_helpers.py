from matplotlib.axes import Axes
from Point import Point
from Segment import Segment

#helper functions so that we can draw on the matplotlib as we run the algorithm
def draw_point(ax: Axes, point: Point, color="red", marker="o", size=5):
    x, y = (point.x(), point.y())
    ax.scatter(x, y, c=color, s=size)
    ax.figure.canvas.draw()

def draw_segment(ax: Axes, segment: Segment, color="red", linewidth=1):
    (x1, y1) = (segment.leftEndPoint().x(), segment.leftEndPoint().y())
    (x2, y2) = (segment.rightEndPoint().x(), segment.rightEndPoint().y())
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth)
    ax.figure.canvas.draw()
