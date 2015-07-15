from Turtle import *                                                                  
from TurtleCanvas import *

ps = [Position2D(100,30),Position2D(-30,-20),Position2D(0,50),Position2D(153,100),Position2D(-330,50),Position2D(-110,-40),Position2D(-42,-70),Position2D(110,-30),Position2D(-75,50), Position2D(80,20), Position2D(60,-10)]

t = Turtle('bob',TurtleCanvas())
t.corral(ps)

input('Press [RETURN] to exit.\n')
