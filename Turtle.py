from math import sin, cos, pi, asin, acos, sqrt
from time import sleep
from Stack import Stack

class Position2D:

    def __init__(self, x=0.0, y=0.0):
        """ Initialize a new position, with default coordinates 
            placing it at the origin. """
        self.x = x
        self.y = y

    def __add__(self, offset):
        """ Compute the position resulting from an offset. """
        return Position2D(self.x + offset.dx, self.y + offset.dy)

    def __sub__(self, other):
        """ Compute the offset between two positions. """
        return Offset2D(self.x - other.x, self.y - other.y)

    def __str__(self):
        """ Build a text string for the position. """
        return '@[' \
                + ('%.4f' % self.x) \
                + ',' \
                + ('%.4f' % self.y) \
                + ']'

    def compare(self,other):
        """ Uses lexicographic ordering to compare two points. """
        if self.x < other.x:
            return -1
        elif self.x > other.x:
            return 1
        elif self.y < other.y:
            return -1
        elif self.y > other.y:
            return 1
        else:
            return 0

    def __cmp__(self,other):
        return self.compare(other)

    def __eq__(self,other):
        return self.compare(other) == 0

    def __ne__(self,other):
        return self.compare(other) != 0

    def __lt__(self,other):
        return self.compare(other) < 0

    def __gt__(self,other):
        return self.compare(other) > 0

    def __le__(self,other):
        return self.compare(other) <= 0

    def __ge__(self,other):
        return self.compare(other) >= 0

    def turn(self, p1, p2):
        """ Checks whether one point is left of another point.  """
        
        cross = (p1 - self) * (p2 - self)
        if cross > 0: return 1
        elif cross < 0: return -1
        else: return 0

    __repr__ = __str__


class Offset2D:

    def __init__(self, fst, snd, polar=False):
        """ Initialize a new offset using either cartesian coordinates
            or polar coordinates. """
        if polar:
            self.dx = fst * cos(snd)
            self.dy = fst * sin(snd)
        else:
            self.dx = fst
            self.dy = snd

    def __add__(self, other):
        """ Compose two offsets to compute their aggregate offset. """
        return Offset2D(self.dx + other.dx, self.dy + other.dy)

    def __abs__(self):
        """ Compute the length of an offset. """
        return sqrt(self.dx * self.dx + self.dy * self.dy)

    def __str__(self):
        """ Build a text string for the position. """
        return '+<' \
                + ('%.4f' % self.x) \
                + ',' \
                + ('%.4f' % self.y) \
                + '>'

    def __mul__(self,other):
        """ Returns the cross product of this and another offset. """
        return self.dx * other.dy - self.dy * other.dx

    __repr__ = __str__


class Segment2D:

    def __init__(self, p1, p2):
        """ Initialize a new location (with default coordinates 
            placing it at the origin. """
        self.start = p1
        self.end = p2

    def __abs__(self):
        """ Compute the length of the segment. """
        return abs(self.end - self.start)

    def __str__(self):
        """ Build a text string for the position. """
        return '<' + str(self.start) + '--' + str(self.end) + '>'

    __repr__ = __str__


class Turtle:

    # delay shared by all turtles in the system
    delay = 0.1
    
    def __init__(self, name='sven', canvas = None):
        """ Initialize the components of a new Turtle instance. 

            The turtle is placed at the origin, heading to the east.
            Its pen is initially up.

        """
        self.name = name
        self.stack = Stack()
        self.canvas = canvas

        self.heading = 0.0
        self.location = Position2D()
        self.penDown = False
        self.ink = '#b04060'

        if self.canvas: self.canvas.add_turtle(self)
        self.advance_frame()

    @property
    def heading_radians(self):
        return 2.0*pi*self.heading/360.0

    def advance_frame(self):
        if self.canvas:
            self.canvas.render()
            sleep(self.delay)

    def clone(self):
        t = Turtle(self.name + ' clone')
        t.mimic(self)
        return t

    def mimic(self,t):
        self.heading = t.heading
        self.location = t.location
        self.penDown = t.penDown
        self.ink = t.ink

    def save(self):
        self.stack.push(self.clone())

    def restore(self):
        t = self.stack.pop()
        self.mimic(t)
        self.advance_frame()

    def turn(self, angle):
        self.heading = self.heading + angle
        self.advance_frame()

    def left(self, angle=90.0):
        """ Turn the turtle clockwise a certain number of degrees. """
        self.turn(angle)

    def right(self, angle=90.0):
        """ Turn the turtle counterclockwise a certain number of degrees. """
        self.turn(-angle)

    def forward(self, distance):
        """ Move the turtle forward according to its heading. """
        offset = Offset2D(distance,self.heading_radians,True)
        self.move_to(self.location+offset)
        if self.penDown and self.canvas:
            s = Segment2D(p1,p2)
            self.canvas.add_segment(s,self.ink)
        self.location = p2
        self.advance_frame()

    def move_to(self, position):
        """ Move the turtle to some specified position """
        p1 = self.location
        p2 = position
        if self.penDown and self.canvas:
            s = Segment2D(p1,p2)
            self.canvas.add_segment(s,self.ink)
        self.location = p2
        self.advance_frame()

    def mark(self):
        self.canvas.add_mark(self.location,self.ink)
        self.advance_frame()

    def up(self):
        self.penDown = False

    def down(self):
        self.penDown = True

    def run(self,pgm,scale,turn):
        for cmd in pgm.split(' '):
            if cmd == 'forward':
                self.forward(scale)
            elif cmd == 'left':
                self.left(turn)
            elif cmd == 'right':
                self.right(turn)
            elif cmd == 'save':
                self.save()
            elif cmd == 'restore':
                self.restore()
            elif cmd == 'up':
                self.up()
            elif cmd == 'down':
                self.down()
            elif cmd == 'mark':
                self.mark()
            # skips non-command strings

    def distance_to(self,position):
        """ Returns the dsitance between the turtle and the position. """
        return abs(position - self.location)


    def assess_turn(self,p1,p2):
        """ Returns whether p1 is to the left (+1) or to the right (-1)
            of p2, when looking at them from the turtle's current 
            location.  If they are in line, returns 0 instead.  """

        return self.location.turn(p1,p2)

    
    def corral(self,points):
        """ This is the method for Project 3 option #1.  """
        self.save()

        for p in points:
            self.move_to(p)
            self.mark()

        # FIND THE FIRST POINT ON THE HULL
        p0 = min(points)
        self.move_to(p0)

        self.down()

        # create two variables to compare points, with
        # p being the turtle's starting location
        p = p0
        q = 0

        # begin cycling through the hull
        while q != p0:

            # look at each point other than the turtle's current position...
            for x in points if x != p:

                # ...and compare turns from current position to find the next
                # point along the hull.
                if self.assess_turn(p,x) == -1:

                    # assign q the point that is leftmost
                    q = x
                
            # draw to that point
            self.move_to(q)

            # update the turtle's position p by changing
            # it to be q
            p = q

        self.up()
        self.restore()


    def __str__(self):
        if self.penDown:
            state = 'drawing '
        else:
            state = ''
        return '< \''+self.name+'\' '+str(self.location)+' '+state+'>'

    __repr__ = __str__

