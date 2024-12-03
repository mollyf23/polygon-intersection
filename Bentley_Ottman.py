from matplotlib.axes import Axes
from gui_helpers import draw_left_endpoint, draw_right_endpoint, draw_intersection_point,draw_polygon, draw_intersection_event
import heapq
from Point import Point
from Segment import Segment
from SweepLineStatus import SweepLineStatus

class Event:
    point: Point
    segment: Segment
    segment2: Segment #for intersection points, segment below

    def __init__(self, point: Point, segment: Segment, segment2: Segment = None):
        self.point = point
        if (segment and segment2):
            if (segment.comparator(segment2) < 0):
                self.segment = segment2
                self.segment2 = segment
            else:
                self.segment = segment
                self.segment2 = segment2
        else:
            self.segment = segment
            self.segment2 = None

    #override less than function for event queue sorting
    def __lt__(self, other):
        if (self.point.x() == other.point.x()):
            #right endpoints should go last so we dont delete stuff before its used 
            if (self.point == self.segment.rightEndPoint() and other.point != other.segment.rightEndPoint()):
                return False
            elif (self.point != self.segment.rightEndPoint() and other.point == other.segment.rightEndPoint()):
                return True
            else:
                if (self.segment.rightEndPoint().x() == other.segment.rightEndPoint().x()):
                    return self.point.y() < other.point.y()
                else: return self.segment.rightEndPoint().x() < other.segment.rightEndPoint().x()
                
        else:    
            return self.point.x() < other.point.x()
    
    #override equal function for member function 
    def __eq__(self, other):
        return self.point == other.point
    
    def __str__(self):
        return self.point

def intersection_BentleyOttman(ax: Axes, list1, list2, draw):  
    if (draw):
        ax.cla()
        draw_polygon(ax, list1, "black")
        draw_polygon(ax, list2, "black")
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
        if (event_queue.is_leftendpoint(event)):
            if (draw):
                draw_left_endpoint(ax, event)
            segE: Segment = event.segment
            sweep_line_status.insert(segE)
            segA = sweep_line_status.above(segE)
            segB = sweep_line_status.below(segE)

            #find intersection events
            if (segA is not None and segE.intersects(segA, True)):
                event = Event(segE.intersection(segA), segE, segA)
                if (draw):
                    draw_intersection_point(ax, event)
                event_queue.insert(event)
            if ((segB is not None and segE.intersects(segB, True)) and ((segA is None) or (segA is not None and segB != segA))):
                event = Event(segE.intersection(segB), segE, segB)
                if (draw):
                    draw_intersection_point(ax, event)
                event_queue.insert(event)
        #right endpoint
        elif (event_queue.is_rightendpoint(event)):
            segE: Segment = event.segment
            segA = sweep_line_status.above(segE)
            segB = sweep_line_status.below(segE)
            if (draw):
                draw_right_endpoint(ax, event)
            sweep_line_status.delete(segE)

            #find intersection events
            if (segA is not None and segB is not None and segA.intersects(segB, True)):
                event = Event(segA.intersection(segB), segA, segB)
                if (not event_queue.member(event)):
                    event_queue.insert(event)
                    if (draw):
                        draw_intersection_point(ax, event)
        #intersection point
        else:
            output.append(event.point)
            segE1 = event.segment
            segE2 = event.segment2
            swap(sweep_line_status, event, segE1, segE2)

            segA = sweep_line_status.above(segE2)
            segB = sweep_line_status.below(segE1)
            if (draw): draw_intersection_event(ax, event)
             #find intersection events
            if (segA is not None and segE2.intersects(segA, True)):
                event = Event(segE2.intersection(segA), segE2, segA)
                if (not event_queue.member(event)):
                    if (draw):
                        draw_intersection_point(ax, event)
                    event_queue.insert(event)
            if (segB is not None and segE1.intersects(segB, True)):
                event = Event(segE1.intersection(segB), segE1, segB)
                if (not event_queue.member(event)):
                    event_queue.insert(event)
                    if (draw):
                        draw_intersection_point(ax, event)
            
    return output


def segment_builder(list, endpoints):
    for i in range(len(list)):
        x1, y1 = list[i]
        x2, y2 = list[(i + 1) % len(list)] 
        point1 = Point(x1,y1)
        point2 = Point(x2,y2)
        #sort points left to right
        if (point1.x() < point2.x() or (point1.x() == point2.x() and point1.y() < point2.y())):
            segment = Segment(point1,point2)
        else:       
            segment = Segment(point2,point1)
        
        endpoint1 = Event(point1, segment)
        endpoint2 = Event(point2, segment)
        endpoints.append(endpoint1)
        endpoints.append(endpoint2)



def swap(sweep_line_status, event, segE1: Segment, segE2: Segment):
        sweep_line_status.delete(segE2)
        sweep_line_status.delete(segE1)
        segE1.endPoints[0] = event.point
        segE2.endPoints[0] = event.point
        sweep_line_status.insert(segE1)
        sweep_line_status.insert(segE2)

        
class EventQueue:
    def __init__(self, events):
        self.queue = events
        self.intersection_helper = {}
        heapq.heapify(self.queue)
    
    def min(self):
        return heapq.heappop(self.queue)
    
    def nextEvent(self):
        return self.queue[0]

    def insert(self, event):
        self.intersection_helper[(event.point.x(), event.point.y())] = True
        heapq.heappush(self.queue, event)

    def member(self, event):
        return self.intersection_helper.get((event.point.x(), event.point.y())) == True

    def is_leftendpoint(self, event: Event):
        return (event.segment2 is None and event.segment.leftEndPoint() == event.point)
    
    def is_rightendpoint(self, event: Event):
        return (event.segment2 is None and event.segment.rightEndPoint() == event.point)
