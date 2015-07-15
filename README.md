# convex-hull
An algorithm for cycling through the most exterior coordinates in a two-dimensional plane.

The challenge: when given a randomized series of points contained within an array, create a function that contains all coordinates by painting lines to connect only the most exterior points.

For this exercise, I use the "SwamPy" Turtles Graphics package, written by Allen Downey and found here: http://www.greenteapress.com/thinkpython/swampy/.

My solution: I begin by creating a function for the Turtle class to compare two points within a Cartesian point and return a numeric value that communicates which point is greater (or if they are equal).

    def assess_turn(self,p1,p2):
        """ Returns whether p1 is to the left (+1) or to the right (-1)
            of p2, when looking at them from the turtle's current 
            location.  If they are in line, returns 0 instead.  """

        return self.location.turn(p1,p2)
        
        
I then build my primary convex hull algorithm in the form of a function, corral:

    def corral(self,points):
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

To test, open seq.py, corral.py, Stack.py, TurtleCanvas.py, and Turtle.py, and run corral.py in your command line.
