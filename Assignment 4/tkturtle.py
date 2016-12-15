# tkturtle.py (TCL/Tk Version)
# Walker M. White (wmw2)
# August 20, 2015
"""Cornell implementation of the Tk Turtle

This module is preferable to the default turtle module for several reasons.  
First, it makes it easier to support simultaneous turtle windows.  Second, it 
provides support for custom color models.  Finally, the attributes and methods 
have been streamlined to make them easier to understand for beginners."""
import colormodel
import turtle
import os

# Necessary to retrieve pen graphic
_PATH = os.path.dirname(colormodel.__file__)

# Private class.  Not publicly available. Emulates the Screen singleton.
class _Window(turtle.TurtleScreen):
    """Internal private class to emulate the Screen singleton"""
    
    # PRIVATE ATTRIBUTES:
    #    _root:    Reference to the turtle screen root
    #    _canvas:  Reference to the internal drawing canvas
    #    _title:   Reference to the window title bar
    
    
    # BUILT-IN METHODS
    # Copy of turtle.Screen, as non-singleton
    def __init__(self,x=100,y=100,width=800,height=800):
        """**Constructor**: creates a copy of turtle.Screen, as a non-singleton
        
            :param x: initial x coordinate (default 0)
            **Precondition**: int > 0
            
            :param y: initial y coordinate (default 0)
            **Precondition**: int > 0
        
            :param width: initial window width (default 800)
            **Precondition**: int > 0
        
            :param height: initial window height (default 800)
            **Precondition**: int > 0
        
            :param scale: initial window scale (default 0.75)
            **Precondition**: float > 0
        
        All parameters are optional."""
        self._title = turtle._CFG["title"]
        self._root = turtle._Root()
        self._root.title(self._title)
        self._root.ondestroy(self._destroy)
        
        canvwidth  = turtle._CFG["canvwidth"]
        canvheight = turtle._CFG["canvheight"]
        self._root.setupcanvas(width, height, canvwidth, canvheight)
        self._canvas = self._root._getcanvas()
        
        turtle.TurtleScreen.__init__(self, self._canvas)
        self._setup(width, height, x, y)
    
    
    def _setup(self, width=turtle._CFG["width"], height=turtle._CFG["height"],
              startx=turtle._CFG["leftright"], starty=turtle._CFG["topbottom"]):
        """Sets the size and position of the main window.
        
            :param x: initial x coordinate (default 0)
            **Precondition**: int > 0
            
            :param y: initial y coordinate (default 0)
            **Precondition**: int > 0
        
            :param width: initial window width (default 800)
            **Precondition**: int > 0
        
            :param height: initial window height (default 800)
            **Precondition**: int > 0
        
            :param scale: initial window scale (default 0.75)
            **Precondition**: float > 0
        
        All parameters are optional."""
        if not hasattr(self._root, "set_geometry"):
            return
        
        sw = self._root.win_width()
        sh = self._root.win_height()
        if isinstance(width, float) and 0 <= width <= 1:
            width = sw*width
        if startx is None:
            startx = (sw - width) / 2
        if isinstance(height, float) and 0 <= height <= 1:
            height = sh*height
        if starty is None:
            starty = (sh - height) / 2
        self._root.set_geometry(width, height, startx, starty)
        self.update()
    
    def _destroy(self):
        """Destroys this window and its associated assets"""
        root = self._root
        turtle.Turtle._pen = None
        turtle.Turtle._screen = None
        self._root = None
        self._canvas = None
        turtle.TurtleScreen._RUNNING = True
        root.destroy()


class Window(object):
    """Instances are GUI windows that support turtle graphics
    
    You should construct a Window object before constructing a Turtle or Pen.  
    You will only need one Window object for the entire assignment.
    """
    # PRIVATE ATTRIBUTES:
    #    _frame: The backing store for this window
    
    
    # MUTABLE PROPERTIES
    @property
    def x(self):
        """The x coordinate for top left corner of window
        
        **Invariant**: x must be an int > 0"""
        return self._x
    
    @x.setter
    def x(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0), "value %s is negative" % `value`
        self._x = value
        self._reshape()
    
    @property
    def y(self):
        """The y coordinate for top left corner of window
        
        **Invariant**: y must be an int > 0"""
        return self._y
    
    @y.setter
    def y(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0), "value %s is negative" % `value`
        self._y = value
        self._reshape()
    
    @property
    def width(self):
        """The width of the window in pixels
        
        **Invariant**: width must be an int > 0"""
        return self._width
    
    @width.setter
    def width(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0), "value %s is negative" % `value`
        self._width = value
        self._reshape()
    
    @property
    def height(self):
        """The height of the window in pixels
        
        **Invariant**: height must be an int > 0"""
        return self._height
    
    @height.setter
    def height(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0), "value %s is negative" % `value`
        self._height = value
        self._reshape()
    
    @property
    def title(self):
        """The title displayed at top of window bar
        
        **Invariant**: title must be a string"""
        return self._frame._title
    
    @title.setter
    def title(self,value):
        assert (type(value) == str), "value %s is not a string" % `value`
        self._frame._root.title(value)
        self._frame._title = value
    
    @property
    def resizable(self):
        """Whether or not the Window supports user resizing
        
        **Invariant**: resizable must be a bool"""
        return self._frame._root.resizable() == '1 1'
    
    @resizable.setter
    def resizable(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        self._resizable = value
        flag = 1 if value else 0
        self._frame._root.resizable(flag, flag)
    
    @property
    def refresh(self):
        """How often to refresh the screen when drawing the turtle
        
        **Invariant**: refresh must be an int >= 0"""
        return self._refresh
    
    @refresh.setter
    def refresh(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0), "value %s is negative" % `value`
        self._refresh = value
        self._frame.tracer(value,0)
    
    # IMMUTABLE PROPERTIES
    @property
    def turtles(self):
        """The list of all turtles attached to this Window
        
        *This attribute may not be altered directly*"""
        return self._turtles[:]

    @property
    def pens(self):
        """The list of all pens attached to this Window
        
        *This attribute may not be altered directly*"""
        return self._pencils[:]

    @property
    def shapes(self):
        """The list containing all supported turtle shapes
        
        *This attribute may not be altered directly*"""
        return self._frame.getshapes()
    
    
    # BUILT-IN METHODS
    def __init__(self,x=100,y=100,width=800,height=800):
        """**Constructor**: creates a new Window to support turtle graphics
        
            :param x: initial x coordinate (default 100)
            **Precondition**: int
            
            :param y: initial y coordinate (default 100)
            **Precondition**: int
        
            :param width: initial window width (default 800)
            **Precondition**: int
        
            :param height: initial window height (default 800)
            **Precondition**: int
        
        All parameters are optional."""
        assert (type(x) == int), "x-coordinate %s is not an int" % `x`
        assert (x > 0), "x-coordinate %s is negative" % `x`
        assert (type(y) == int), "y-coordinate %s is not an int" % `y`
        assert (y > 0), "y-coordinate %s is negative" % `y`
        assert (type(width) == int), "width %s is not an int" % `width`
        assert (width > 0), "width %s is negative" % `width`
        assert (type(height) == int), "height %s is not an int" % `height`
        assert (height > 0), "height %s is negative" % `height`
        
        self._frame = _Window(x,y,width,height)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.refresh = 1
        
        # Initialize the lists
        self._turtles = []
        self._pencils = []
        
        try:
            self._frame.addshape('pen.gif' if _PATH == '' else os.path.join(_PATH,'pen.gif'))
        except turtle.TurtleGraphicsError as e:
            print 'Attempt to use pencil graphic failed'
            print e
    
    def __del__(self):
        """Destroys this window and its associated assets"""
        try:
            self._frame._destroy()
        except:
            pass
        self._turtles = []
        self._pencils = []
        del self._frame

    # FRIEND METHODS
    def _reshape(self):
        """Resize this window to the current set dimensions"""
        self._frame._setup(width=self._width,height=self._height,
                           startx=self._x,starty=self._y)
    
    def _addTurtle(self,turt):
        """Add a turtle to this window.
            
            :param turt: the graphics turtle
            **Precondition**: turt is not already in this Window
        """
        assert (type(turt) == Turtle), "Parameter %s is not a valid Turtle object" % `turt`
        self._turtles.append(turt)
    
    def _addPen(self,pen):
        """Add a pen to this window.
            
            :param pen: the graphics pen
            **Precondition**: pen is not already in this Window
        """
        assert (type(pen) == Pen), "Parameter %s is not a valid graphics pen" % `turt`
        self._pencils.append(pen)
    
    def _removeTurtle(self,turt):
        """Remove a turtle from this window.
            
            :param turt: the graphics turtle
            **Precondition**: turt is in this Window > 0
        """
        if turt in self._turtles:
            self._turtles.remove(turt)
    
    def _removePen(self,pen):
        """Remove a pen from this window.
            
            :param pen: the graphics pen
            **Precondition**: pen is in this Window > 0
        """
        if pen in self._pencils:
            self._pencils.remove(pen)
    
    
    # PUBLIC METHODS
    def clear(self):
        """Erase the contents of this Window
        
        All Turtles and Pens are eliminated from the Window.
        Any attempt to use a previously created Turtle or Pen
        will fail."""
        self._frame.clear()
        self._turtles = []
        self._gpens = []

    def bye(self):
        """Closes the graphics Window, deleting all assets"""
        self._frame._destroy()
        self._turtles = []
        self._gpens = []
        del self._frame

    def beep(self):
        """Plays an OS specific alert sound"""
        self._frame._root.bell()

    def iconify(self):
        """Shrinks the window down to an icon, effectively hiding it"""
        self._frame._root.iconify()

    def deiconify(self):
        """Expands the window from an icon so that it is visible"""
        self._frame._root.deiconify()

    def setMaxSize(self,width,height):
        """Sets the maximum size for this window
        
        Any attempt to resize a dimension beyond the maximum size will fail.
            
            :param width: the maximum window width
            **Precondition**: width is an int > 0
            
            :param height: the maximum height width
            **Precondition**: height is an int > 0
        """
        assert (type(width) == int), "width %s is not an int" % `width`
        assert (width > 0), "width %s is negative" % `width`
        assert (type(height) == int), "height %s is not an int" % `height`
        assert (height > 0), "height %s is negative" % `height`
        self._frame._root.maxsize(width,height)

    def setMinSize(self,width,height):
        """Sets the minimum size for this window
        
        Any attempt to resize a dimension below the minimum size will fail.
            
            :param width: the minimum window width
            **Precondition**: width is an int > 0
            
            :param height: the minimum height width
            **Precondition**: height is an int > 0
        """
        assert (type(width) == int), "width %s is not an int" % `width`
        assert (width > 0), "width %s is negative" % `width`
        assert (type(height) == int), "height %s is not an int" % `height`
        assert (height > 0), "height %s is negative" % `height`
        self._frame._root.minsize(width,height)
    
    # UNSUPPORTED METHODS
    def flush(self):
        """Unsupported method for compatibility"""
        pass
    
    def stroke(self, path, clr):
        """Unsupported method for compatibility"""
        pass
    
    def fill(self, path, clr):
        """Unsupported method for compatibility"""
        pass
    
    def write(self, fname):
        """Unsupported method for compatibility"""
        pass


# TURTLE HELPERS
def _is_turtle_color(c):
    """**Returns**: True if c is a valid color value.
    
    Turtles accept RGB, HSV, strings (for named colors), or tuples.
        
        :param c: a potential color value
    """
    return (type(c) == colormodel.RGB or
            type(c) == colormodel.HSV or
            type(c) == str or
            type(c) == tuple)


def _to_turtle_color(c):
    """**Returns**: The given color value, converted to an internal format
    
    This method allows us to support all color formats, while using a single
    color format for the backend.
    
    For the PyX backend, the unified color is a Tk-supported color value
    
            :param c: the color value
            **Precondition**: is_turtle_color(c) must be True
    """
    return c.tkColor() if (type(c) == colormodel.RGB or type(c) == colormodel.HSV) else c


class Turtle(object):
    """Instances represent a graphics turtle.
    
    A graphics turtle is a pen that is controlled by direction and movement.  
    The turtle is a cursor that that you control by moving it left, right, 
    forward, or backward.  As it moves, it draws a line of the same color as 
    the Turtle.
   """ 
    # PRIVATE ATTRIBUTES:
    #    _screen: Reference to the Tkinter drawing canvas
    #    _turtle: Reference to the TK turtle primitive
    
    
    # MUTABLE PROPERTIES
    @property
    def heading(self):
        """The heading of this turtle in degrees.
        
        Heading is measured counter clockwise from due east.
        
        **Invariant**: Value must be a float"""
        return float(self._turtle.heading())
    
    @heading.setter
    def heading(self,value):
        assert type(value) in [int, float], "value %s is not a valid number" % `value`
        self._turtle.setheading(value)
    
    @property
    def speed(self):
        """The animation speed of this turtle.
        
        The speed is an integer from 0 to 10. Speed = 0 means that no animation
        takes place. The methods forward/back makes turtle jump and likewise
        left/right make the turtle turn instantly.
        
        Speeds from 1 to 10 enforce increasingly faster animation of line
        drawing and turtle turning. 1 is the slowest speed while 10 is the
        fastest (non-instantaneous) speed.
        
        **Invariant**: Value must be an integer value in the range 0..10."""
        return self._turtle.speed()
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 or value <= 10), "value %s is outside the range 0..10" % `value`
        self._turtle.speed(value)

    @property
    def color(self):
        """The color of this turtle.
        
        All subsequent draw commands (forward/back) draw using this color.
        If the color changes, it only affects future draw commands, not
        past ones.
        
        **Invariant**: Value must be either a string with a color name, a
        3 element tuple of floats between 0 and 1 (inclusive), or an object
        in an additive color model (e.g. RGB or HSV)."""
        return self._color
    
    @color.setter
    def color(self,value):
        assert (_is_turtle_color(value)), "value %s is not a valid color input" % `value`
        self._turtle.color(_to_turtle_color(value))
        self._color = self._turtle.color()[0]
    
    @property
    def visible(self):
        """Indicates whether the turtle's icon is visible.
        
        Drawing commands will still work while the turtle icon is hidden.
        There will just be no indication of the turtle's current location
        on the screen.
        
        **Invariant**: Value must be a bool"""
        return self._turtle.isvisible()
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        if value and not self._turtle.isvisible():
            self._turtle.showturtle()
        elif not value and self._turtle.isvisible():
            self._turtle.hideturtle()
    
    @property
    def drawmode(self):
        """Indicates whether the turtle is in draw mode.
        
        All drawing calls are active if an only if this mode is True
        
        **Invariant**: Value must be a bool"""
        return self._turtle.isdown()
    
    @drawmode.setter
    def drawmode(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        if value and not self._turtle.isdown():
            self._turtle.pendown()
        elif not value and self._turtle.isdown():
            self._turtle.penup()
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """The x-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.xcor()
    
    @property
    def y(self):
        """The y-coordinate of this turtle.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.ycor()
    
    
    # BUILT-IN METHODS
    def __init__(self,screen,position=(0, 0), color='red', heading=180, speed=0):
        """**Constructor**: Creates a new turtle to draw on the given screen.
            
            :param screen: window object that turtle will draw on.
            **Precondition**: object of type Window.
            
            :param position: initial turtle position (origin is screen center)
            **Precondition**: 2D tuple of floats or ints.
            
            :param color: initial turtle color (default red)
            **Precondition**: either a string with a color name, a 3 element
            tuple of floats between 0 and 1 (inclusive), or an object in an
            additive color model (e.g. RGB or HSV).
            
            :param heading: initial turtle directions (default 180)
            **Precondition**: a float or int
            
            :param speed: initial turtle speed (default 0)
            **Precondition**: a int between 0 and 10, inclusive
        
        The argument ``screen`` is not optional."""
        assert type(screen) == Window, "parameter $s is not a Window object" % `screen`
        assert (_is_turtle_color(color)), "paramter %s is not a valid color input" % `color`
        self._turtle = turtle.RawTurtle(screen._frame)
        self._turtle.hideturtle()

        self._screen = screen
        screen._addTurtle(self)
        self._turtle.shape('turtle')
        self._turtle.penup()
        self.color = color
        self._turtle.setposition(position)
        self._turtle.setheading(heading)
        self._turtle.speed(speed)
        self._turtle.pendown()
        self._turtle.showturtle()
    
    def __repr__(self):
        """**Returns**: An unambiguous string representation of this turtle. """
        return str(self.__class__)+str(self)
    
    def __str__(self):
        """**Returns**: A readable string representation of this turtle. """
        return 'Turtle[position={}, color={}, heading={}]'.format((self.x,self.y), self.color, self.heading)
    
    def __del__(self):
        """Deletes this turtle object. """
        self.clear()
        self._screen._removeTurtle(self)
        del self._turtle
    
    
    # PUBLIC METHODS
    def forward(self,distance):
        """Moves the turtle forward by the given amount.
        
            :param distance: distance to move in pixels
            **Precondition**: a float or int
        
        This method draws a line if drawmode is True."""
        assert (type(distance) in [int, float]), "parameter distance:%s is not a valid number" % `distance`
        self._turtle.forward(distance)
    
    def backward(self,distance):
        """Moves the turtle backward by the given amount.
        
            :param distance: distance to move in pixels
            **Precondition**: a float or int
        
        This method draws a line if drawmode is True."""
        assert (type(distance) in [int, float]), "parameter distance:%s is not a valid number" % `distance`
        self._turtle.backward(distance)
    
    def right(self,degrees):
        """Turns the turtle to the right by the given amount.
        
            :param degrees: amount to turn right in degrees
            **Precondition**: a float or int
        
        Nothing is drawn when this method is called."""
        assert (type(degrees) in [int, float]), "parameter degrees:%s is not a valid number" % `distance`
        self._turtle.right(degrees)
    
    def left(self,degrees):
        """Turns the turtle to the left by the given amount.
        
            :param degrees: amount to turn left in degrees
            **Precondition**: a float or int
        
        Nothing is drawn when this method is called."""
        assert (type(degrees) in [int, float]), "parameter degrees:%s is not a valid number" % `distance`
        self._turtle.left(degrees)
    
    def move(self,x,y):
        """Moves the turtle to given position without drawing.
        
            :param x: new x position for turtle
            **Precondition**: a float or int
        
            :param y: new y position for turtle
            **Precondition**: a float or int
        
        This method does not draw, regardless of the drawmode."""
        assert (type(x) in [int, float]), "parameter x:%s is not a valid number" % `x`
        assert (type(y) in [int, float]), "parameter y:%s is not a valid number" % `y`
        d = self._turtle.isdown()
        if d:
            self._turtle.penup()
        self._turtle.setposition(x,y)
        if d:
            self._turtle.pendown()
    
    def clear(self):
        """Deletes the turtle's drawings from the window.
        
        This method does not move the turtle or alter its attributes."""
        self._turtle.clear()
    
    def reset(self):
        """Deletes the turtle's drawings from the window.
        
        This method re-centers the turtle and resets all attributes to their 
        default values."""
        self._turtle.clear()
        self._turtle.setposition((0,0))        
        self._turtle.shape('turtle')
        self.color = 'red'
        self.heading = 180
        self.speed = 0
    
    def flush(self):
        """Unsupported method for compatibility"""
        pass


class Pen(object):
    """Instances represent a graphics pen.
    
    A graphics pen is like a turtle except that it does not have a heading, 
    and there is no drawmode attribute. Instead, the pen relies on explicit 
    drawing commands such as drawLine or drawCircle.
    
    Another difference with the pen is that it can draw solid shapes.  The 
    pen has an attribute called ``fill``.  When this attribute is set to True, 
    it will fill the insides of any polygon traced by its drawLine method.  
    However, the fill will not be completed until fill is set to False, or
    the move method is invoked."""
    # PRIVATE ATTRIBUTES:
    #    _screen: Reference to the Tkinter drawing canvas
    #    _turtle: Reference to the TK turtle primitive
    
    
    # MUTABLE PROPERTIES
    @property
    def speed(self):
        """The animation speed of this pen.
        
        The speed is an integer from 0 to 10. Speed = 0 means that
        no animation takes place. The drawLine and drawCircle
        methods happen instantly with no animation.

        Speeds from 1 to 10 enforce increasingly faster animation of line
        drawing. 1 is the slowest speed while 10 is the fastest
        (non-instantaneous) speed.

        **Invariant**: Value must be an integer value in the range 0..10."""
        return self._turtle.speed()
    
    @speed.setter
    def speed(self,value):
        assert (type(value) == int), "value %s is not an int" % `value`
        assert (value >= 0 or value <= 10), "value %s is outside the range 0..10" % `value`
        self._turtle.speed(value)
    
    @property
    def fill(self):
        """The fill status of this pen.
        
        If the fill status is True, then the pen will fill the insides
        of any polygon or circle subsequently traced by its drawLine
        or drawCircle method. If the attribute changes, it only affects
        future draw commands, not past ones. Switching this attribute
        between True and False allows the pen to draw both solid and
        hollow shapes.
        
        **Invariant**: Value must be an bool."""
        return self._turtle.fill()
    
    @fill.setter
    def fill(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        self._turtle.fill(value)
        # Make the pen state relative to fill.
        #if value and not self._turtle.isdown():
        #    self._turtle.pendown()
        #elif not value and self._turtle.isdown():
        #    self._turtle.penup()
    
    @property
    def color(self):
        """Silent, unsupported property requested by a beta tester"""
        assert False, 'Pen does not have a color; use pencolor or fillcolor'
    
    @color.setter
    def color(self,value):
        assert False, 'Pen does not have a color; use pencolor or fillcolor'
    
    @property
    def pencolor(self):
        """The pen color of this pen.
        
        The pen color is used for drawing lines and circles.  All subsequent
        draw commands draw using this color. If the color changes, it only
        affects future draw commands, not past ones.
        
        This color is only used for lines and the border of circles.  It is 
        not the color used for filling in solid areas (if the ``fill`` attribute 
        is True).  See the attribute ``fillcolor`` for solid shapes.
        
        **Invariant**: Value must be either a string with a color name, a
        3 element tuple of floats between 0 and 1 (inclusive), or an object
        in an additive color model (e.g. RGB or HSV)."""
        return self._pencolor
    
    @pencolor.setter
    def pencolor(self,value):
        assert (_is_turtle_color(value)), "value %s is not a valid color input" % `value`
        self._turtle.color(_to_turtle_color(value),self._fillcolor)
        self._pencolor = self._turtle.color()[0]
    
    @property
    def fillcolor(self):
        """The fill color of this turtle.
        
        The fill color is used for filling in solid shapes. If the ``fill`` 
        attribute is True, all subsequent draw commands fill their insides using 
        this color.  If the color changes, it only affects future draw commands, 
        not past ones.
        
        This color is only used for filling in the insides of solid shapes.  It 
        is not the color used for the shape border.  See the attribute ``pencolor`` 
        for the border color.
        
        **Invariant**: Value must be either a string with a color name, a 3 element 
        tuple of floats between 0 and 1 (inclusive), or an object in an additive 
        color model (e.g. RGB or HSV)."""
        return self._fillcolor

    @fillcolor.setter
    def fillcolor(self,value):
        assert (_is_turtle_color(value)), "value %s is not a valid color input" % `value`
        self._turtle.color(self._pencolor,_to_turtle_color(value))
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[1]
    
    @property
    def visible(self):
        """Indicates whether the pen's icon is visible.
        
        Drawing commands will still work while the pen icon is hidden.
        There will just be no indication of the pen's current location
        on the screen.
        
        **Invariant**: Value must be a bool"""
        return self._turtle.isvisible()
    
    @visible.setter
    def visible(self,value):
        assert (type(value) == bool), "value %s is not a bool" % `value`
        if value and not self._turtle.isvisible():
            self._turtle.showturtle()
        elif not value and self._turtle.isvisible():
            self._turtle.hideturtle()
    
    
    @property
    def origin(self):
        """Represents the pen origin in the draw window.
        
        This property is used by the Window to reset the pen.
        This is a "friend" property and the invariant is not enforced.
        
        **Invariant**: Value is pair of numbers"""
        return self._origin
    
    @origin.setter
    def origin(self,value):
        self._origin = value
    
    
    # IMMUTABLE PROPERTIES
    @property
    def x(self):
        """The x-coordinate of this pen.
        
        To change the x coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.xcor()
    
    @property
    def y(self):
        """The y-coordinate of this pen.
        
        To change the y coordinate, use one of the drawing methods.
        
        *This attribute may not be (directly) altered*"""
        return self._turtle.ycor()
    
    
    # BUILT-IN METHODS
    def __init__(self,screen,position=(0, 0), color='red', speed=0):
        """**Constructor**: Creates a new pen to draw on the given screen.

            :param screen: window object that pen will draw on.
            **Precondition**: object of type Window.
            
            :param position: initial pen position (origin is screen center)
            **Precondition**: 2D tuple of floats or ints.
            
            :param color: initial pen and fill color (default red)
            **Precondition**: either a string with a color name, a 3 element
            tuple of floats between 0 and 1 (inclusive), or an object in an
            additive color model (e.g. RGB or HSV).
            
            :param speed: initial turtle speed (default 0)
            **Precondition**: a int between 0 and 10, inclusive
        
        The argument ``screen`` is not optional."""
        assert type(screen) == Window, "parameter $s is not a Window object" % `screen`
        assert (_is_turtle_color(color)), "paramter %s is not a valid color input" % `color`
        self._turtle = turtle.RawTurtle(screen._frame)
        self._turtle.hideturtle()
        
        self._screen = screen
        screen._addPen(self)
        try:
            self._turtle.shape('pen.gif' if _PATH == '' else _PATH+'/pen.gif')
        except turtle.TurtleGraphicsError as e:
            print 'Attempt to use pencil graphic failed'
            print e
        
        self._turtle.penup()
        self._turtle.setposition(position)
        self._turtle.color(color)
        self._turtle.speed(speed)
        self._turtle.pendown()
        self._turtle.showturtle()
        
        # Record current color
        # "pair" seems unused
        #pair = self._turtle.color() 
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[0]
    
    
    def __repr__(self):
        """**Returns**: An unambiguous string representation of this pen. """
        return str(self.__class__)+str(self)
        
    def __str__(self):
        """**Returns**: A readable string representation of this pen. """
        return 'Pen(position={}, pencolor={}, fillcolor={})'.format(self._turtle.position(), self.pencolor, self.fillcolor)
    
    def __del__(self):
        """Deletes this pen object. """
        self._screen._removePen(self)
        del self._turtle
    
    
    # DRAWING METHODS
    def move(self,x,y):
        """Moves the pen to given position without drawing.
        
            :param x: new x position for pen
            **Precondition**: a float or int
        
            :param y: new y position for pen
            **Precondition**: a float or int
        
        If the ``fill`` attribute is currently True, this method will complete 
        the fill before moving to the new region. The space between the original 
        position and (x,y) will not be connected."""
        assert (type(x) in [int, float]), "parameter x:%s is not a valid number" % `x`
        assert (type(y) in [int, float]), "parameter y:%s is not a valid number" % `y`
        fstate = self._turtle.fill()
        if fstate: # only need to do this if in mid-fill
            self._turtle.fill(False)
        self._turtle.penup()
        self._turtle.setposition(x,y)
        self._turtle.pendown()
        if fstate: # only need to do this if in mid-fill
            self._turtle.fill(True)
    
    def drawLine(self, dx, dy):
        """Draws a line segment (dx,dy) from the current pen position
        
            :param dx: change in the x position
            **Precondition**: a float or int
        
            :param dy: change in the y position
            **Precondition**: a float or int
        
        The line segment will run from (x,y) to (x+dx,y+dy), where
        (x,y) is the current pen position.  When done, the pen will
        be at position (x+dx,y+dy)"""
        assert (type(dx) in [int, float]), "parameter x:%s is not a valid number" % `dx`
        assert (type(dy) in [int, float]), "parameter y:%s is not a valid number" % `dy`
        x = self._turtle.xcor()
        y = self._turtle.ycor()
        self._turtle.setposition(x+dx, y+dy)
    
    def drawTo(self, x, y):
        """Draws a line from the current pen position to (x,y)
        
            :param x: finishing x position for line
            **Precondition**: a float or int
        
            :param y: finishing y position for line
            **Precondition**: a float or int
        
        When done, the pen will be at (x, y)."""
        assert (type(x) in [int, float]), "parameter x:%s is not a valid number" % `x`
        assert (type(y) in [int, float]), "parameter y:%s is not a valid number" % `y`
        self._turtle.setposition(x, y)
    
    def drawCircle(self, r):
        """Draw a circle of radius r centered on the pen.
        
            :param r: radius of the circle
            **Precondition**: a float or int
        
        The center of the circle is the current pen coordinates.
        When done, the position of the pen will remain unchanged"""
        assert (type(r) in [int, float]), "parameter r:%s is not a valid number" % `r`        
        x = self._turtle.xcor()
        y = self._turtle.ycor()
        
        # Move the pen into position
        fstate = self._turtle.pendown()
        if fstate:
            self._turtle.penup()
        self._turtle.setposition(x, y-r)
        if fstate:
            self._turtle.pendown()
        
        # Draw the circle and fill if necessary
        self._turtle.circle(r)
        self.flush()
        self._turtle.forward(0)
        
        # Return the pen to the position
        if fstate:
            self._turtle.penup()
        self._turtle.setposition(x, y)
        if fstate:
            self._turtle.pendown()
    
    
    # PUBLIC METHODS
    def clear(self):
        """Deletes the pen's drawings from the window.
        
        This method does not move the pen or alter its attributes."""
        self._turtle.clear()
    
    def reset(self):
        """Deletes the pen's drawings from the window.
        
        This method re-centers the pen and resets all attributes to their 
        default values."""
        self._turtle.clear()
        self._turtle.setposition((0,0))        
        try:
            self._turtle.shape('pen.gif')
        except:
            self._turtle.shape('classic')
        self._turtle.color('red')
        self.speed = 0
        
        #pair = self._turtle.color()
        self._pencolor = self._turtle.color()[0]
        self._fillcolor = self._turtle.color()[0]
    
    def flush(self):
        """Fills in the current drawing, but retains state.
        
        Normally, an object is not filled until you set the state to 
        False.  Calling this method executes this fill, without setting
        the state to False.  If fill is False, this method does nothing."""
        if self.fill:
            self._turtle.fill(False)
            self._turtle.fill(True)
