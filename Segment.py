from Point import Point
import math

'''
Created on Oct 23, 2024

@author: offic
'''
#    Class to hold the coordinates of a point, e.g. the vertex of a polygon.
class Segment:
    endPoints = []
    
    LEFT = -1
    RIGHT = 1
    COLINEAR = 0
    
    def __init__(self, left, right):
        #    VALIDATION
        if not isinstance(left, Point):
            raise TypeError("The left end point must be a Point object.")
        elif not isinstance(right, Point):
            raise TypeError("The right end point must be a Point object.")
        
        #    Store valid results
        self.endPoints = [left, right]

    def __eq__(self, sgmnt):
        if not (isinstance(sgmnt, Segment)):
            raise TypeError("The input value has to be a Segment object.")
        
        return self.leftEndPoint == sgmnt.leftEndPoint and self.rightEndPoint == sgmnt.rightEndPoint

    #    Determines if the given point is to the left or right of the segment.
    def side(self, pt):
        if not isinstance(pt, Point):
            raise TypeError("The input value has to be a Point object.")
        
        area = self.endPoints[0].x() * self.endPoints[1].y( )- self.endPoints[0].y() * self.endPoints[1].x()
        area -= pt.x() * self.endPoints[1].y() - pt.y() * self.endPoints[1].x()
        area += pt.x() * self.endPoints[0].y() - pt.y() * self.endPoints[0].x()
        
        if area == 0:
            return self.COLINEAR
        elif area < 0:
            return self.RIGHT
        else:
            return self.LEFT
        
    def leftEndPoint(self):
        return self.endPoints[0]
    
    def rightEndPoint(self):
        return self.endPoints[1]
    
    def length(self):
        return math.sqrt((self.endPoints[0].x() - self.endPoints[1].x()) ** 2 + (self.endPoints[0].y() - self.endPoints[1].y()) ** 2)
    
    def intersects(self, seg, ignoreEndpoints):
        if not isinstance(seg, Segment):
            raise TypeError("The input value has to be a Segment object.")

        #    Check for the special case where one of the end points math.
        if not ignoreEndpoints and (self.endPoints[0] == seg.leftEndPoint() or self.endPoints[0] == seg.rightEndPoint() or self.endPoints[1] == seg.leftEndPoint() or self.endPoints[1] == seg.rightEndPoint()):
            return True
        
        #    Check for intersection.
        else:
            return (self.side(seg.leftEndPoint()) * self.side(seg.rightEndPoint())) + (seg.side(self.leftEndPoint()) * seg.side(self.rightEndPoint())) == -2
    
        #return (self.side(seg.leftEndPoint()) * self.side(seg.rightEndPoint()))

    def intersection(self, s):
        numX = (self.endPoints[0].x() * self.endPoints[1].y() - self.endPoints[0].y() * self.endPoints[1].x()) * (s.endPoints[0].x() - s.endPoints[1].x()) - (self.endPoints[0].x() - self.endPoints[1].x()) * (s.endPoints[0].x() * s.endPoints[1].y() - s.endPoints[0].y() * s.endPoints[1].x())
        den = (self.endPoints[0].x() - self.endPoints[1].x()) * (s.endPoints[0].y() - s.endPoints[1].y()) - (self.endPoints[0].y() - self.endPoints[1].y()) * (s.endPoints[0].x() - s.endPoints[1].x())
    
        numY = (self.endPoints[0].x() * self.endPoints[1].y() - self.endPoints[0].y()*self.endPoints[1].x()) * (s.endPoints[0].y() - s.endPoints[1].y()) - (self.endPoints[0].y() - self.endPoints[1].y()) * (s.endPoints[0].x() * s.endPoints[1].y() - s.endPoints[0].y() * s.endPoints[1].x())
        
        return Point(numX / den, numY / den)        
    
    def get_y_from_x(self, x):
        if self.leftEndPoint().x() == self.rightEndPoint().x():  #vertical line segment
            return min(self.leftEndPoint().y(), self.rightEndPoint().y())
        else:
            #use slope to find y at the current x
            return self.leftEndPoint().y() + (self.rightEndPoint().y() - self.leftEndPoint().y()) * (x - self.leftEndPoint().x()) / (self.rightEndPoint().x() - self.leftEndPoint().x())
    
s1 = Segment(Point(0, 0), Point(4, 0))
s2 = Segment(Point(0, 0), Point(1, -1))

