import matplotlib.pyplot as plt

import numpy as np
from Point import Point
from Segment import Segment
import math

'''
Created on Sep 14, 2024

@author: Gregory Allen
'''

class Polygon:
    vertices = []
    
    def __init__(self, vertices):
        for pt in vertices:
            if not isinstance(pt, Point):
                raise TypeError("The vertices must all be Point objects.")
        
        self.vertices = vertices

    def vertex(self, i):
        if i >= 0 and i < len(self.vertices):
            return self.vertices[i]

    def size(self):
        return len(self.vertices)
    
    def plot(self, figure, canvas, color):
        x = []
        y = []
    
        
        for p in self.vertices:
            x.append(p.x())
            y.append(p.y())

        x.append(self.vertices[0].x())
        y.append(self.vertices[0].y())
        
        figure.plot(x, y, marker='o', linestyle='-', color = color, markersize=8, linewidth=2)

        # Label the plot
        canvas.title('Polygon Plot Example')
        canvas.xlabel('X-axis')
        canvas.ylabel('Y-axis')
        
        # Show the plot
        canvas.grid(True)
        canvas.show(block = False)
        
        canvas.pause(1)

    def __len__(self):
        return len(self.vertices)
    
    # Function to clip all the edges w.r.t one clip edge of clipping area
    def clip(self, poly_points, clip1, clip2, canvas):
        new_points = []
        new_poly_size = 0
    
        #    Loop through all the vertices in the polygon, .
        for i in range(len(poly_points)):
            #    Get the index of the next vertex so we're looping through the edges.
            k = (i+1) % len(poly_points)
    
            clipEdge = Segment(clip1, clip2)
            polyEdge = Segment(poly_points.vertex(i), poly_points.vertex(k))
    
            # Calculate which side of the clipper line the first point is on.
            #i_pos = (clip2.x()-clip1.x()) * (poly_points.vertex(i).y()-clip1.y()) - (clip2.y()-clip1.y()) * (poly_points.vertex(i).x()-clip1.x())
            i_pos = clipEdge.side(polyEdge.leftEndPoint())
            
            # Calculate which side of the clipper line the second point is on.
            k_pos = clipEdge.side(polyEdge.rightEndPoint())
            #k_pos = (clip2.x()-clip1.x()) * (poly_points.vertex(k).y()-clip1.y()) - (clip2.y()-clip1.y()) * (poly_points.vertex(k).x()-clip1.x())
    
            # Case 1 : When both points are inside the clipping polygon
            if i_pos < 0 and k_pos < 0:
                # Only second point is added
                new_points.append(poly_points.vertex(k))
                new_poly_size += 1
    
            # Case 2: When only first point is outside
            elif i_pos >= 0 and k_pos < 0:
                # Point of intersection with edge and the second point are added
                new_points.append(clipEdge.intersection(polyEdge))
                
                new_poly_size += 1
                new_points.append(poly_points.vertex(k))
                new_poly_size += 1
    
            # Case 3: When only second point is outside
            elif i_pos < 0 and k_pos >= 0:
                # Only point of intersection with edge is added
                new_points.append(clipEdge.intersection(polyEdge))
                new_poly_size += 1
    
            # Case 4: When both points are outside
            else:
                pass  # No points are added, but we add a pass statement to avoid the IndentationError

        # Copying new points into a separate array and changing the no. of vertices
        clipped_poly_points = []
        for i in range(new_poly_size):
            clipped_poly_points.append(new_points[i])

        return Polygon(clipped_poly_points)


    #    Function to implement Sutherland–Hodgman algorithm
    #    clipper_points    polygon    the polygon to be intersected with the one represented by the object.
    def intersection_SH(self, poly_points, clipper_points, fig, canvas):
        clipper_size = clipper_points.size()
    
        #    Loop through the vertices.
        for i in range(clipper_size):
            #    Get the index of the next vertex.  In effect, we're looping through the sides that make up the polygon.
            k = (i+1) % clipper_size
        
            #    Pass the polygon being clipped and the end points of the current edge to the clipping function.
            poly_points = self.clip(poly_points, clipper_points.vertex(i), clipper_points.vertex(k), canvas)
            
            f = canvas.figure
#            poly_points.plot(ax, canvas, 'r')
            
        # Printing vertices of clipped polygon
        if len(poly_points) == 0:
            print("no intersection")
        
        else:
            for i in range(len(poly_points)):
                print(poly_points.vertex(i))
    
        return poly_points

#    Points for the polygon.
clipper_pts = Polygon([Point(0,0), Point(10, 0), Point(0, 10)])
poly_pts = Polygon([Point(1,1), Point(11, 1), Point(1, 11)])

#    poly contained in clip so result is poly.
clipper_pts = Polygon([Point(-1, -1), Point(2, -1), Point(2, 2), Point(-1, 2)])
poly_pts = Polygon([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])

#    no intersection
clipper_pts = Polygon([Point(-1, -1), Point(-1, -2), Point(-3, -2), Point(-3, -1)])
poly_pts = Polygon([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])

#    Points for the polygon.
clipper_pts = Polygon([Point(0,0), Point(1, 0), Point(1, 1), Point(0, 1)])
poly_pts = Polygon([Point(1-math.sqrt(2),.5), Point(.5, math.sqrt(2)), Point(math.sqrt(2), .5), Point(.5, 1 - math.sqrt(2))])

fig, ax = plt.subplots()
#plt.figure(figsize=(10, 10))

clipper_pts = Polygon([Point(0, 0), Point(2, 0), Point(2, 1), Point(1, 1), Point(1, 2), Point(3, 2), Point(3, 3), Point(0,3)])
clipper_pts.plot(ax, plt, 'b')
poly_pts.plot(ax, plt, 'g')
intersection = poly_pts.intersection_SH(poly_pts, clipper_pts, fig, plt)
intersection.plot(ax, plt, 'r')

plt.show()