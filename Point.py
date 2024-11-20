import math

'''
Created on Sep 14, 2024

@author: offic
'''
#    Class to hold the coordinates of a point, e.g. the vertex of a polygon.
class Point:
    coordinates = []
    
    LEFT = -1
    RIGHT = 1
    COLINEAR = 0
    
    def __init__(self, x, y):
        #    VALIDATION
        if not isinstance(x, (int, float, complex)) or isinstance(x, bool):
            raise TypeError("The x value must be numeric.")
        elif not isinstance(y, (int, float, complex)) or isinstance(y, bool):
            raise TypeError("The y value must be numeric.")
        
        #    Store valid results
        self.coordinates = [x, y]
    
    #    Return the x-coordinate of the point.
    def x(self):
        return self.coordinates[0]
    
    #    Return the y-coordinate of the point.
    def y(self):
        return self.coordinates[1]

    def distanceTo(self, pt):
        if not isinstance(pt, Point):
            raise TypeError("The input value has to be a Point object.")

        return math.sqrt((self.coordinates[0] - pt.x())**2+(self.coordinates[1] - pt.y())**2)
    
    #    Determines if self is to the left or right of the directed line from pt1 to pt2.
    def side(self, pt1, pt2):
        if not (isinstance(pt1, Point) and isinstance(pt2, Point)):
            raise TypeError("The input value has to be a Point object.")
        
        area = pt1.x() * pt2.y( )- pt1.y() * pt2.x()
        area -= self.coordinates[0] * pt2.y() - self.coordinates[1] * pt2.x()
        area += self.coordinates[0] * pt1.y() - self.coordinates[1] * pt1.x()
        
        if area == 0:
            return self.COLINEAR
        elif area < 0:
            return self.RIGHT
        else:
            return self.LEFT
    
    #    Returns the angle from self->pt1 to self->pt2
    def angle(self, pt1, pt2):
        if not (isinstance(pt1, Point) and isinstance(pt2, Point)):
            raise TypeError("The input value has to be a Point object.")
        
        dp = (pt1.x() - self.coordinates[0]) * (pt2.x() - self.coordinates[0]) + (pt1.y() - self.coordinates[1]) * (pt2.y() - self.coordinates[1])
        dp /= math.sqrt((pt1.x() - self.coordinates[0])**2 + (pt1.y() - self.coordinates[1])**2)
        dp /= math.sqrt((pt2.x() - self.coordinates[0])**2 + (pt2.y() - self.coordinates[1])**2)

        return math.acos(dp)
    
    def __eq__(self, pt):
        if not (isinstance(pt, Point)):
            raise TypeError("The input value has to be a Point object.")
        
        return pt.x() == self.x() and pt.y() == self.y()
    
    def __gt__(self, pt):
        if not (isinstance(pt, Point)):
            raise TypeError("The input value has to be a Point object.")

        if self.x() == pt.x():
            return self.y() > pt.y()
        
        return self.x() > pt.x()
    
    def __ge__(self, pt):
        if not (isinstance(pt, Point)):
            raise TypeError("The input value has to be a Point object.")

        return self.x() == pt.x() or self > pt

    def __lt__(self, pt):
        if not (isinstance(pt, Point)):
            raise TypeError("The input value has to be a Point object.")

        if self.x() == pt.x():
            return self.y() < pt.y()
        
        return self.x() < pt.x()
    
    def __le__(self, pt):
        if not (isinstance(pt, Point)):
            raise TypeError("The input value has to be a Point object.")

        return self.x() == pt.x() or self < pt

    def __str__(self):
        return "(" + str(self.coordinates[0]) + ", " + str(self.coordinates[1]) + ")"