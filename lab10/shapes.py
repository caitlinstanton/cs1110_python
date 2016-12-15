# shapes.py
# Walker M. White (wmw2)
# November 1, 2013
"""Basic Shape classes for Lab 10.

You should not modify this module at all.  All of the classes in this assignment are 
subclasses of Parallelogram, the last class in this module."""
# Import a bunch of Kivy stuff
import kivy
import kivy.graphics.instructions
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.context_instructions import Color
import kivy.graphics.vertex_instructions as vert

from kivy.metrics import dp

# To help with drawing.
import colormodel
import math

# Helper function for preconditions
def _isnumber(x):
    """Returns: True if x a float or int, False otherwise"""
    return type(x) in [int,float]


class Shape(Widget):
    """Instances represent a Shape object to be drawn in Kivy.
   
    This base class provides much of the features for drawing, but it does not actually 
    draw anything itself.  Only subclasses of Shape draw anything, by overriding the 
    method resetShape(). You will never make an instance of class Shape directly.
   
    INSTANCE ATTRIBUTES (Not counting those inherited from Widget):
        _x:  x-coordinate of bottom left corner [int or float]
        _y:  y-coordinate of bottom left corner [int or float]
        _color: shape color [RGB object]
    
    These attributes are hidden and may only be accessed via getters and setters
    """
   
    # GETTERS AND SETTERS FOR ATTRIBUTES
    # COLOR (MUTABLE)
    def getColor(self):
        """Returns: The color of this shape"""
        return self._color
   
    def setColor(self,value):
        """Sets the color for this shape.
        
        Parameter value: The outline color
        Precondition: value is an RGB object."""
        assert isinstance(value,colormodel.RGB), `value`+' is not a color object'
        self._color = value
    
    # X (IMMUTABLE)
    def getX(self):
        """Returns: The x coordinate of the top left"""
        # We inherit x and y from widget
        return self.x
    
    # X (IMMUTABLE)
    def getY(self):
        """Returns: The y coordinate of the top left"""
        # We inherit x and y from widget
        return self.y
    
    
    # INITIALIZER
    def __init__(self, x, y):
        """Initializer: Create a shape at position (x, y)
        
        Parameter x: The x-coordinate of the shape position
        Precondition: x is a number (int or float)
        
        Parameter y: The y-coordinate of the shape position
        Precondition: y is a number (int or float)"""
        assert _isnumber(x), `x`+' is not a number' 
        assert _isnumber(y), `y`+' is not a number'
        Widget.__init__(self,pos=(x,y))
        self.setColor(colormodel.BLACK)
    
    
    # OPERATIONS
    def __str__(self): 
        """Returns: String descriptor of this Shape
      
        Will be overridden in all subclasses."""
        return '('+str(self.getX())+', '+str(self.getY())+')'
    
    
    # OTHER METHODS
    def resetShape(self):
        """Draw this shape using the Kivy canvas
      
        Will be overridden in all subclasses."""
        pass


class Line(Shape):
    """Instances are a line segment in 2D space.
    
    INSTANCE ATTRIBUTES (In addition to those from Shape):
        _dx: Length of line along x-axis [int or float]
        _dy: Length of line along y-axis [int or float]
    
    These attributes are hidden and may only be accessed via getters
    """
    
    # GETTERS AND SETTERS FOR ATTRIBUTES
    
    # DX (IMMUTABLE)
    def getDX(self):
        """Returns: Length of line along x-axis"""
        return self._dx
    
    # DY (IMMUTABLE)
    def getDY(self):
        """Returns: Length of line along y-axis"""
        return self._dy
    
    
    # INITIALIZER
    def __init__(self, x0, y0, x1, y1):
        """Initializer: a line segment from (x0,y0) to (x1,y1)
        
        As Line is a subclass of shape, it anchors the shape at (x0,y0) and defines 
        dx, dy as the difference between (x1,y1) and (x0,y0).
        
        Parameter x0: The x-coordinate of the line start
        Precondition: x0 is a number (int or float)
        
        Parameter y0: The y-coordinate of the line start
        Precondition: y0 is a number (int or float)
        
        Parameter x1: The x-coordinate of the line end
        Precondition: x1 is a number (int or float)
        
        Parameter y1: The y-coordinate of the line end
        Precondition: y1 is a number (int or float)"""
        self._dx = x1-x0
        self._dy = y1-y0
        Shape.__init__(self,x0, y0)
        self.size = (self._dx,self._dy)
    
    
    # OPERATIONS
    def __str__(self):
        """Return: A string description of this line."""
        return ('line at '+ Shape.__str__(self) +
                ' to (' + str(self.getX()+self.getDX()) +
                ', '    + str(self.getY()+self.getDY()) + ')')
    
    
    # OTHER METHODS
    def draw(self):
        """Draw this shape using the Kivy canvas"""
        x1 = self.getX()+self.getDX()
        y1 = self.getY()+self.getDY()
        
        # Draw the line
        self.canvas.clear()
        gl_color = self._color.glColor()
        color = Color(gl_color[0],gl_color[1],gl_color[2],gl_color[3])
        self.canvas.add(color)
        
        line = kivy.graphics.vertex_instructions.Line(points=[dp(self.getX()), dp(self.getY()), dp(x1), dp(y1)])
        self.canvas.add(line)


# PRIMARY CLASS FOR THIS LAB
class Parallelogram(Shape):
    """Instances are a general parallelogram
    
    The parallelogram has a horizontal length l1 and other length l2.  The leaning factor 
    is measured by d.  For example, the parallelogram below has leaning factor d = 0.
    
                 ___________________ 
                 |                  |
           (x,y) |__________________|
                
    
    This next parallelogram has a negative leaning factor. d is the number of pixels 
    from the top-left corner to the leftmost part of the parallelogram.
    
                   ___________________
                  /                  /
           (x,y) /__________________/
    
    Finally, this last parallelogram has a positive leaning factor d. d is the number of
    pixels from the leftmost part of the parallelogram to its bottom-left corner 
    
                  ___________________
                  \                  \
           (x,y)   \__________________\
    
    INSTANCE ATTRIBUTES (In addition to those from Shape):
        _l1: Length of horizontal side  [int or float > 0]
        _l2: Length of OTHER side [int or float > 0]
        _d:  Leaning factor [int or float >= 0]
    
    ADDITIONAL INVARIANTS:
    If the parallelogram is left-leaning, _d >= 0 and the bottom line start _d units to 
    the right of point (x,y). If the parallelogram is right-leaning, _d is negative and 
    the top line starts abs(_d) units to the right of point (x,y)"""
    
    # GETTERS AND SETTERS FOR ATTRIBUTES
    
    # L1 (IMMUTABLE)
    def getL1(self):
        """Returns: Length of horizontal side"""
        return self._l1
    
    # L2 (IMMUTABLE)
    def getL2(self):
        """Returns: Length of OTHER side"""
        return self._l2
    
    # D (IMMUTABLE)
    def getD(self):
        """Returns: Leaning factor"""
        return self._d
    
    
    # INITIALIZER
    def __init__(self, x, y, l1, l2, d):
        """Initializer: Makes a parallelogram at (xp, yp) 
        
        The parallelogram has side lengths l1 (horizontal side) and l2. It is d 
        pixels from (x, y)
        
        Parameter x: The x-coordinate of the parallelogram anchor
        Precondition: x is a number (int or float)
        
        Parameter y: The y-coordinate of the parallelogram anchor
        Precondition: y is a number (int or float)
        
        Parameter l1: The horizontal length of the parallelogram
        Precondition: l1 is a number (int or float) >= 0
        
        Parameter l2: The 'other' length of the parallelogram
        Precondition: l2 is a number (int or float) >= 0
        
        Parameter d: The leaning factor of the parallelogram
        Precondition: d is a number (int or float)"""
        # Only need to check the new things.
        assert _isnumber(l1), `l1`+' is not a number' 
        assert _isnumber(l2), `l2`+' is not a number' 
        assert _isnumber(d), `d`+' is not a number' 
        assert l1 >= 0, `l1`+' is negative' 
        assert l2 >= 0, `l2`+' is negative' 
        self._l1 = l1
        self._l2 = l2
        self._d = d
        
        # This checks the preconditions of x, y
        Shape.__init__(self, x, y)
    
    
    # OPERATIONS
    def __str__(self):
        """Return: String description of this parallelogram"""
        return ('parallelogram at '+ Shape.__str__(self) +
                ', sides ' + str(self.getL1()) + ' and ' + str(self.getL2()) +
                ', distance ' + str(self.getD()) + ' from ' + str(self.getX()))
    
    
    # OTHER METHODS
    def draw(self):
        """Draw this shape using the Kivy canvas"""
        if self.canvas is None:
            return
        
        # Set xt and xb to the horizontal coordinates of left pt 
        # of top and bottom lines
        xb = self.getX()+self.getD()
        xt = self.getX()
        if (self.getD() < 0):
            xb = self.getX()
            xt = self.getX()-self.getD()
        
        
        # Set yt to the vertical coordinate of the bottom left point
        yt = self.getY()+int(round(math.sqrt(self.getL2()*self.getL2() - self.getD()*self.getD())))
        yb = self.getY()
        
        # Prepare the canvas for drawing
        self.canvas.clear()
        
        # Check to see if this is a rectangle
        if hasattr(self,'getFill'):
            gl_color = self.getFill().glColor()
            color = Color(gl_color[0],gl_color[1],gl_color[2],gl_color[3])
            self.canvas.add(color)
            
            rect = vert.Rectangle(pos=map(dp,self.pos), size=(dp(self.getL1()),dp(self.getL2())))
            self.canvas.add(rect)
        
        # Draw the four lines
        gl_color = self._color.glColor()
        color = Color(gl_color[0],gl_color[1],gl_color[2],gl_color[3])
        self.canvas.add(color)
        
        line = kivy.graphics.vertex_instructions.Line(points=[dp(xt), dp(yt), dp(xt+self.getL1()), dp(yt)])
        self.canvas.add(line)
        line = kivy.graphics.vertex_instructions.Line(points=[dp(xt+self.getL1()), dp(yt), dp(xb+self.getL1()), dp(yb)])
        self.canvas.add(line)
        line = kivy.graphics.vertex_instructions.Line(points=[dp(xb+self.getL1()), dp(yb), dp(xb), dp(yb)])
        self.canvas.add(line)
        line = kivy.graphics.vertex_instructions.Line(points=[dp(xb), dp(yb), dp(xt), dp(yt)])
        self.canvas.add(line)
