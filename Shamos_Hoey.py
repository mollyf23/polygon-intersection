from gui_helpers import draw_point, draw_segment
import heapq
from sortedcontainers import SortedList
from Point import Point
from Segment import Segment

class Event:
    point: Point
    segment: Segment
    segment2: Segment #for intersection points, segment below

    def __init__(self, point: Point, segment: Segment, segment2: Segment = None):
        self.point = point
        self.segment = segment
        self.segment2 = segment2

    #override less than function for event queue sorting
    def __lt__(self, other):
        if self.point.x() == other.point.x():
            return self.point.y() < other.point.y()
        return self.point.x() < other.point.x()
    
    #override equal function for member function 
    def __eq__(self, other):
        return self.point.x() == other.point.x() and self.point.y() == other.point.y()

def intersection_ShamosHoey(ax, list1, list2):  
    endpoints = []
    #use helper method to populate
    segment_builder(list1, endpoints)
    segment_builder(list2, endpoints)

    #initialize event queue
    event_queue = EventQueue(endpoints) #this will sort them into a heap
    sweep_line_status = SweepLineStatus()
    output = []

    while (len(event_queue.queue) > 0):
        event = event_queue.min()
        #left endpoint
        if (event_queue.is_leftendpoint(event)):
            segE: Segment = event.segment
            sweep_line_status.insert(segE)
            segA = sweep_line_status.above(segE)
            segB = sweep_line_status.below(segE)

            #find intersection events
            if (segA != None and segE.intersects(segA, True)):
                event = Event(segE.intersection(segA), segE, segA)
                event_queue.insert(event)
            if (segB != None and segE.intersects(segB, True)):
                event = Event(segE.intersection(segB), segE, segB)
                event_queue.insert(event)
        #right endpoint
        elif (event_queue.is_rightendpoint(event)):
            segE: Segment = event.segment
            segA = sweep_line_status.above(segE)
            segB = sweep_line_status.below(segE)
            sweep_line_status.delete(segE)

            #find intersection events
            if (segA != None and segB != None and segA.intersects(segB, True)):
                event = Event(segA.intersection(segB), segA, segB)
                if (not event_queue.member(event)):
                    event_queue.insert(event)
        #intersection point
        else:
            output.append(event)
            segE1 = event.segment
            segE2 = event.segment2
            segA = sweep_line_status.above(segE1)
            segB = sweep_line_status.below(segE2)
             #find intersection events
            if (segA != None and segE1.intersects(segA, True)):
                event = Event(segE1.intersection(segA), segE1, segA)
                if (not event_queue.member(event)):
                    event_queue.insert(event)
            if (segB != None and segE2.intersects(segB, True)):
                event = Event(segE2.intersection(segB), segE2, segB)
                if (not event_queue.member(event)):
                    event_queue.insert(event)
            #swap the two intersecting lines
            sweep_line_status.swap(segE1, segE2)
    return output

def segment_builder(list, endpoints):
    for i in range(len(list)):
        x1, y1 = list[i]
        x2, y2 = list[(i + 1) % len(list)] 
        point1 = Point(x1,y1)
        point2 = Point(x2,y2)
        segment = Segment(point1,point2)
        endpoint1 = Event(point1, segment)
        endpoint2 = Event(point2, segment)
        endpoints.append(endpoint1)
        endpoints.append(endpoint2)

class SweepLineStatus:
    def __init__(self):
        #store segment info by using the endpoint info
        self.current_x = None
        self.segments = SortedList(key=lambda segment: segment.get_y_from_x(self.current_x))

    def insert(self, segment: Segment):
        self.segments.add(segment)

    def delete(self, segment: Segment):
        self.segments.remove(segment)

    #find segment above
    def above(self, segment: Segment):
        i = self.segments.index(segment)
        if (i < self.segments.count):
            return self.segments[i+1]
        return None

    #find segment below
    def below(self, segment: Segment):
        i = self.segments.index(segment)
        if (-1 < i):
            return self.segments[i-1]
        return None

    def set_current_x(self, x):
        self.current_x = x

    def swap(self, segE1, segE2):
            if (self.segments.index(segE1) > self.segments.index(segE2)):
                self.delete(segE1)
                self.delete(segE2)
                self.insert(segE2)
                self.insert(segE1)
            else:
                self.delete(segE2)
                self.delete(segE1)
                self.insert(segE1)
                self.insert(segE2)


class EventQueue:
    def __init__(self, events):
        self.queue = events
        heapq.heapify(self.queue)
    
    def min(self):
        return heapq.heappop(self.queue)
    
    def nextEvent(self):
        return self.queue[0]

    def insert(self, event):
        heapq.heappush(self.queue, event)

    def member(self, event):
        return event in self.queue

    def is_leftendpoint(self, event: Event):
        return (event.segment.lefttEndPoint.x() == event.point.x() and event.segment.lefttEndPoint.y() == event.point.y())
    
    def is_rightendpoint(self, event: Event):
        return (event.segment.rightEndPoint.x() == event.point.x() and event.segment.rightEndPoint.y() == event.point.y())
