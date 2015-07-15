from math import sin,cos
from tkinter import *
from Turtle import Turtle, Position2D, Segment2D

class TurtleCanvas(Frame):

  def draw_grid(self):

    graph_paper_bg = '#c0d0a0'
    graph_paper_fg = '#80b060'
    major_grid_lines = 8 # this needs to be even
    minor_grid_lines = 5

    grid_lines = major_grid_lines * minor_grid_lines + 1
    scale = (self.size - 2.0 * self.border_size) / (grid_lines - 1)

    min_x = self.border_size 
    max_x = self.size - self.border_size
    min_y = self.border_size
    max_y = self.size - self.border_size
    self.canvas.create_rectangle(0.0,0.0,self.size,self.size,
                                 outline=graph_paper_fg, \
                                 fill=graph_paper_bg)
    
    center_x = self.size / 2.0
    center_y = self.size / 2.0

    for i in range(-(grid_lines//2), +grid_lines//2 + 1):
      y = center_y + i * scale
      if i % minor_grid_lines == 0:
        self.canvas.create_line(min_x,y,max_x,y,fill=graph_paper_fg,width=2)
      else:
        self.canvas.create_line(min_x,y,max_x,y,fill=graph_paper_fg,width=1)

    for i in range(-(grid_lines//2), +grid_lines//2 + 1):
      x = center_x + i * scale
      if i % minor_grid_lines == 0:
        self.canvas.create_line(x,min_y,x,max_y,fill=graph_paper_fg,width=2)
      else:
        self.canvas.create_line(x,min_y,x,max_y,fill=graph_paper_fg,width=1)

  def draw_turtle(self,turtle):
    center_x = self.size / 2.0
    center_y = self.size / 2.0

    turtle_x = center_x + turtle.location.x
    turtle_y = center_y - turtle.location.y

    turtle_head_color = '#508000'
    self.canvas.create_oval(turtle_x + 12.0 * cos(turtle.heading_radians) - 5.0, \
                            turtle_y - 12.0 * sin(turtle.heading_radians) + 5.0, \
                            turtle_x + 12.0 * cos(turtle.heading_radians) + 5.0, \
                            turtle_y - 12.0 * sin(turtle.heading_radians) - 5.0, \
                            fill = turtle_head_color, \
                            outline = turtle_head_color)

    turtle_body_color = '#50b000'
    self.canvas.create_oval(turtle_x - 10.0, \
                            turtle_y + 10.0, \
                            turtle_x + 10.0, \
                            turtle_y - 10.0, \
                            fill = turtle_body_color, \
                            outline = turtle_body_color)

  def draw_segment(self,segment,ink):
    center_x = self.size / 2.0
    center_y = self.size / 2.0

    x1 = center_x + segment.start.x
    y1 = center_y - segment.start.y
    x2 = center_x + segment.end.x
    y2 = center_y - segment.end.y

    self.canvas.create_line(x1,y1,x2,y2,fill=ink,width=2)

  def draw_mark(self,loc,ink):
    center_x = self.size / 2.0
    center_y = self.size / 2.0

    x1 = center_x + loc.x - 5.0
    y1 = center_y - loc.y - 5.0
    x2 = center_x + loc.x + 5.0
    y2 = center_y - loc.y + 5.0

    self.canvas.create_oval(x1,y1,x2,y2,fill=ink,width=0)

  def render(self):
      """ Renders the state of the simuation on the tkinter canvas. """

      self.canvas.delete('all')
      self.draw_grid()
      for (segment,ink) in self.segments:
        self.draw_segment(segment,ink)
      for (loc,ink) in self.marks:
        self.draw_mark(loc,ink)
      for turtle in self.turtles:
        self.draw_turtle(turtle)
      self.update()

  def add_segment(self,seg,ink):
    pair = (seg,ink)
    self.segments.append(pair)

  def add_mark(self,loc,ink):
    pair = (loc,ink)
    self.marks.append(pair)

  def add_turtle(self,turtle):
    self.turtles.append(turtle)

  #
  # __init__ - constructs a new Grid instance 
  #
  def __init__(self):

    self.size = 500
    self.border_size = 50
    self.turtles = []
    self.segments = []
    self.marks = []

    # initialize the display
    self.root = Tk()
    self.root.title('MATH 121 Turtle Canvas')
    Frame.__init__(self, self.root)
    self.canvas = Canvas(self.root, width=self.size, height=self.size)
    self.canvas.pack()
    self.pack()
    
    self.render()
