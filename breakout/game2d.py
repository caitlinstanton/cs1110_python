# game2d.py
# Walker M. White (wmw2)
# November 14, 2015
"""Module to provide simple 2D game support.

This module provides all of the classes that are to use (or subclass) to create your game. 
DO NOT MODIFY THE CODE IN THIS FILE.  See the online documentation in Assignment 7 for 
more guidance.  It includes information not displayed in this module."""

# Basic Kivy Modules
import kivy
import kivy.app

# Lower-level kivy modules to support animation
from kivy.graphics import *
from kivy.graphics.instructions import *
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.clock  import Clock
from kivy.metrics import dp

# Widgets necessary for some technical workarounds
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

# Additional miscellaneous modules
import os, sys, os.path
import numpy as np
import colormodel

# User-defined resources
FONT_PATH  = str(os.path.join(os.path.dirname(__file__), 'Fonts'))
SOUND_PATH = str(os.path.join(os.path.dirname(__file__), 'Sounds'))
IMAGE_PATH = str(os.path.join(os.path.dirname(__file__), 'Images'))

import kivy.resources
kivy.resources.resource_add_path(FONT_PATH)
kivy.resources.resource_add_path(SOUND_PATH)
kivy.resources.resource_add_path(IMAGE_PATH)


################# TYPING HELPER FUNCTIONS #################
pass
# #mark TYPING HELPER FUNCTIONS

def  _same_side(p1, p2, a, b):
    """Returns: True if p1, p2 are on the same side of segment ba.
    
    Parameter p1: A point
    Precondition: p1 is a 2-element sequence of numbers (int or float)
    
    Parameter p2: A point
    Precondition: p2 is a 2-element sequence of numbers (int or float)
    
    Parameter a: One end of a line segment
    Precondition: a is a 2-element sequence of numbers (int or float)
    
    Parameter b: Another end of a line segment
    Precondition: b is a 2-element sequence of numbers (int or float)
    """
    ba = np.append(np.subtract(b,a),[0])
    cp1 = np.cross(ba,np.subtract(p1,a))
    cp2 = np.cross(ba,np.subtract(p2,a))
    return np.dot(cp1,cp2) >= 0


def _in_triangle(p, t):
    """Returns: True if p is in triangle t
    
    Parameter p: A point
    Precondition: p is a 2-element sequence of numbers (int or float)

    Parameter t: A triangle (defined by 3 vertices)
    Precondition: t is a 6-element sequence of numbers (int or float)
    """
    return (_same_side(p, t[0:2], t[2:4], t[4:6]) and
            _same_side(p, t[2:4], t[0:2], t[4:6]) and
            _same_side(p, t[4:6], t[0:2], t[2:4]))


def _is_num(x):
    """Returns: True if x is an int or float; False otherwise.
    
    Parameter x: The value to test
    Precondition: NONE"""
    return type(x) in [int,float]


def _is_num_tuple(t,size):
    """Returns: True if t is a sequence of numbers; False otherwise.
    
    If the sequence is not of the given size, it also returns False.
    
    Parameter t: The value to test
    Precondition: NONE
    
    Parameter size: The size of the sequence
    Precondition: size is an int >= 0
    """
    try:
        return len(t) == size and reduce(lambda x, y: x and y, map(lambda z: type(z) in [int, float], t))

    except:
        return False


def _is_point_tuple(t,msize):
    """Returns: True if t is a point sequence (i.e. even sequence of numbers)
    
    The point tuple must be size greater than msize, or the function returns False.
    
    Parameter t: The value to test
    Precondition: NONE
    
    Parameter msize: The minimum size of the sequence
    Precondition: msize is an int >= 0
    """
    try:
        return len(t) % 2 == 0 and len(t) > msize and \
            reduce(lambda x, y: x and y, map(lambda z: type(z) in [int, float], t))
    except:
        return False


def _is_gobject_list(g):
    """Returns: True if g is a sequence of GObjects
    
    Parameter g: The value to test
    Precondition: NONE
    """
    try:
        return len(g) >= 0 and reduce(lambda x, y: x and y, map(lambda z: isinstance(z,GObject), g))
    except:
        return False


def _is_color(c):
    """Returns: True if c represents a color
    
    As with Turtles, colors may be colormodel objects or strings.  They may also
    be sequences of 3 or 4 elements.  In the case of the latter, the elements
    of the sequence must all be in the range 0..1.
    
    Parameter c: The value to test
    Precondition: NONE
    """
    if type(c) in [colormodel.RGB, colormodel.HSV]:
        return True
    
    if type(c) in [tuple, list] and 3 <= len(c) <= 4:
        return reduce(lambda x, y: x and y, map(lambda z: type(z) in [int, float] and 0 <= z <= 1, c))
    
    return type(c) == str and c in colormodel._TK_COLOR_MAP


def _is_image_file(name):
    """Returns: True if name is the name of an image file
    
    Parameter name: A file name
    Precondition: NONE"""
    if type(name) != str:
        return False
    
    return os.path.exists(IMAGE_PATH+'/'+name)


def _is_font_file(name):
    """Returns: True if name is the name of an font file
    
    Parameter name: A file name
    Precondition: NONE"""
    if type(name) != str:
        return False
    
    return os.path.exists(FONT_PATH+'/'+name)


def _is_sound_file(name):
    """Returns: True if name is the name of an font file.
    
    Parameter name: A file name
    Precondition: NONE"""
    if type(name) != str:
        return False
    
    return os.path.exists(SOUND_PATH+'/'+name)


################# GEOMETRY PRIMITIVES #################
pass
# #mark GEOMETRY PRIMITIVES

class GPoint(object):
    """Instances are points in 2D space.
    
    This class is used primarily for recording and handling mouse locations.  However,
    it may also be used for geometry calculations in conjunction with `GMatrix`."""
    
    # PROPERTIES 
    @property
    def x(self):
        """The x coordinate of the point.
        
        **Invariant**: Must be an int or float."""
        return self._x
    
    @x.setter
    def x(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._x = float(value)
    
    @property
    def y(self):
        """The y coordinate of the point.
        
        **Invariant**: Must be an int or float."""
        return self._y
    
    @y.setter
    def y(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._y = float(value)
    
    # METHODS
    def __init__(self, x=0, y=0):
        """**Constructor**: creates a new GPoint value (x,y).
        
            :param x: initial x value
            **Precondition**: value is an int or float.
        
            :param y: initial y value
            **Precondition**: value is an int or float.
        
        All values are 0.0 by default.        
        """
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        """**Returns**: True if self and other are equivalent GPoint. 
        
        This method uses np to test whether the coordinates are 
        "close enough".  It does not require exact equality for floats.
        
            :param other: value to compare against
        """        
        return (type(other) == GPoint and np.allclose(self.list(),other.list()))
    
    def __ne__(self, other):
        """**Returns**: True if self and other are not equivalent GPoint. 
        
            :param other: value to compare against
        """
        return not self == other
    
    def __str__(self):
        """**Returns**: Readable String representation of this GPoint. """
        return "("+str(self.x)+","+str(self.y)+")"
    
    def __repr__(self):
        """**Returns**: Unambiguous String representation of this GPoint. """
        return "%s%s" % (self.__class__,self.__str__())
    
    def list(self):
        """**Returns**: A python list with the contents of this GPoint."""
        return [self.x,self.y]
    
    def __add__(self, other):
        """**Returns**: the sum of self and other.
        
        The value returned has the same type as self (so it is either
        a GPoint or is a subclass of GPoint).  The contents of this object
        are not altered.
        
            :param other: tuple value to add
            **Precondition**: value has the same type as self.
        """
        assert (type(other) == type(self)), "value %(value)s is not a of type %(type)s" \
            % {'value': `other`, 'type':`type(self)`}
        result = copy.copy(self)
        result.x += other.x
        result.y += other.y
        return result
    
    def __sub__(self, other):
        """**Returns**: the vector from tail to self.
        
        The value returned is a GPoint representing a vector with this point at its head.
        
            :param other: the tail value for the new Vector
            **Precondition**: value is a Point object.
        """
        assert (type(other) == type(self)), "value %(value)s is not a of type %(type)s" \
            % {'value': `other`, 'type':`type(self)`}
        result = copy.copy(self)
        result.x -= other.x
        result.y -= other.y
        return result
    
    def __mul__(self, scalar):
        """**Returns**: the scalar multiple of self and other.
        
        The value returned is a new GPoint.  The contents of this GPoint
        are not altered.
        
            :param scalar: scalar to multiply by
            **Precondition**: value is an int or float.
        """
        assert _is_num(scalar), "value %s is not a number" % `scalar`
        result = copy.copy(self)
        result.x *= scalar
        result.y *= scalar
        result.z *= scalar
        return result
    
    def __rmul__(self, scalar):
        """**Returns**: the scalar multiple of self and other.
        
        The value returned is a new GPoint.  The contents of this GPoint
        are not altered.
        
            :param scalar: scalar to multiply by
            **Precondition**: value is an int or float.
        """
        return self.__mul__(scalar)
    
    def interpolate(self, other, alpha):
        """**Returns**: the interpolation of self and other via alpha.
        
        The value returned has the same type as self (so it is either
        a GPoint or is a subclass of GPoint).  The contents of this object
        are not altered. The resulting value is 
        
            alpha*self+(1-alpha)*other 
        
        according to GPoint addition and scalar multiplication.
        
            :param other: tuple value to interpolate with
            **Precondition**: value has the same type as self.
        
            :param alpha: scalar to interpolate by
            **Precondition**: value is an int or float.
        """
        assert (type(other) == type(self)), "value %(value)s is not a of type %(type)s" \
            % {'value': `other`, 'type':`type(self)`}
        assert (type(alpha) in [int,float]), "value %s is not a number" % `alpha`
        return alpha*self+(1-alpha)*other
    
    def distanceTo(self, other):
        """**Returns**: the Euclidean distance from this point to other
        
            :param other: value to compare against
            **Precondition**: value is a Tuple3D object.
        """
        return np.sqrt((self.x-other.x)*(self.x-other.x)+
                          (self.y-other.y)*(self.y-other.y))


class GMatrix(object):
    """Instances are homongenous matrices for graphics transforms.
    
    This class is backed by np for fast computation.  There are no publicly accessible 
    attributes, as it is not safe to access the internals."""
    
    def __init__(self):
        """**Constructor**: creates a new 4x4 identify matrix"""
        self._data = np.identity(4, dtype=np.float32)
    
    def __str__(self):
        """**Returns**: A string representation of this matrix"""
        return str(self._data)
    
    def __repr__(self):
        """**Returns**: An unambiguous string representation of this matrix"""
        return str(self.__class__)+str(self)
    
    def __mul__(self,other):
        """**Returns**: a new Matrix that is the premultiplication of this and other.
        
        This operation pre-multiplies the matrix on the right.  As a result, this
        allows us to read graphics operations left to right (which is more natural)
        
            :param other: the matrix to pre-multiply
            **Precondition**: a Matrix object
        """
        m = GMatrix()
        np.dot(other._data,self._data,m._data)
        return m
    
    def __imul__(self,other):
        """Premultiplies this matrix by other in place
        
        This operation pre-multiplies the matrix on the right.  As a result, this
        allows us to read graphics operations left to right (which is more natural)
        
            :param other: the matrix to pre-multiply
            **Precondition**: a Matrix object
        """
        tmp = np.dot(other._data,self._data)
        np.copyto(self._data,tmp)
    
    def copy(self):
        """**Returns**: a copy of this Matrix"""
        m = GMatrix()
        np.copyto(m._data,self._data)
        return m
    
    def inverse(self):
        """**Returns**: the inverse of this matrix"""
        m = GMatrix()
        np.copyto(m._data,np.linalg.inv(self._data))
        return m
    
    def invert(self):
        """Inverts this matrix in place"""
        np.copyto(self._data,np.linalg.inv(self._data))
        return self
    
    def transpose(self):
        """**Returns**: the transpose of this matrix"""
        m = GMatrix()
        np.copyto(m._data,np.transpose(self._data))
        return m
    
    def translate(self,x=0,y=0,z=0):
        """Translates this matrix (in-place) by the given amount
        
            :param x: x-coordinate of translation (default 0)
            **Precondition**: an int or float
            
            :param y: y-coordinate of translation (default 0)
            **Precondition**: an int or float
            
            :param z: z-coordinate of translation (default 0)
            **Precondition**: an int or float
        """
        r = np.identity(4, dtype=np.float32)
        r[0,3] = x
        r[1,3] = y
        r[2,3] = z
        tmp = np.dot(self._data,r)
        np.copyto(self._data,tmp)
    
    def rotate(self,ang=0,x=0,y=0,z=0):
        """Rotates this matrix (in place) about the given axis
        
        The rotation angle is given in degrees, not radians.  Rotation is 
        counterclockwise around the angle of rotation.
        
            :param angle: angle of rotation in degrees (default 0)
            **Precondition**: an int or float
            
            :param x: x-coordinate of rotation axis (default 0)
            **Precondition**: an int or float
            
            :param y: y-coordinate of rotation axis (default 0)
            **Precondition**: an int or float
            
            :param z: z-coordinate of rotation axis (default 0)
            **Precondition**: an int or float
        """
        # Formula taken from https://en.wikipedia.org/wiki/Rotation_matrix
        c = np.cos(np.radians(ang))
        s = np.sin(np.radians(ang))
        f = 1-c
        r = np.identity(4, dtype=np.float32)
        r[0] = [x*x*f+c,   x*y*f-z*s, x*z*f+y*s, 0]
        r[1] = [y*x*f+z*s, y*y*f+c,   y*z*f-x*s, 0]
        r[2] = [z*x*f-y*s, z*y*f+x*s, z*z*f+c,   0]
        tmp = np.dot(self._data,r)
        np.copyto(self._data,tmp)
    
    def scale(self,x=1,y=1,z=1):
        """Scales this matrix (in-place) by the given amount
        
            :param x: x-coordinate of the scale (default 1)
            **Precondition**: an int or float
            
            :param y: y-coordinate of the scale (default 1)
            **Precondition**: an int or float
            
            :param z: z-coordinate of the scale (default 1)
            **Precondition**: an int or float
        """
        s = np.identity(4, dtype=np.float32)
        s[0,0] = x
        s[1,1] = y
        s[2,2] = z
        tmp = np.dot(self._data,s)
        np.copyto(self._data,tmp)
    
    def _transform(self,x=0,y=0,z=0):
        """**Returns**: The given point transformed by this matrix
        
        The value returned is a tuple.
        
            :param x: x-coordinate to transform (default 0)
            **Precondition**: an int or float
            
            :param y: y-coordinate to transform (default 0)
            **Precondition**: an int or float
            
            :param z: z-coordinate to transform (default 0)
            **Precondition**: an int or float
        """
        b = np.array([x,y,z,1], dtype=np.float32)
        tmp = np.dot(self._data,b)
        return map(float,tuple(tmp[:-1]))
    
    def transform(self,point):
        """**Returns**: The given point transformed by this matrix
        
        The value returned is a GPoint.
        
            :param point: the point to transform
            **Precondition**: a GPoint
        """
        b = np.array([point.x,point.y,0,1], dtype=np.float32)
        tmp = np.dot(self._data,b)
        return GPoint(float(tmp[0]),float(tmp[1]))


################# RECTANGULAR PRIMITIVES #################
pass 
# #mark RECTANGULAR PRIMITIVES

class GObject(object):
    """Instances provide basic geometry information for drawing to a `GView`
    
    You should never make a `GObject` directly.  Instead, you should use one 
    of the subclasses: `GRectangle`, `GEllipse`, `GImage`, `GLabel`, `GTriangle`,
    `GPolygon`, or `GPath`."""
    
    # MUTABLE PROPERTIES 
    @property
    def x(self):
        """The horizontal coordinate of the object center.
        
        **Invariant**: Must be an int or float."""
        return self._trans.x
    
    @x.setter
    def x(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._trans.x = float(value)
        self._mtrue = False
    
    @property
    def y(self):
        """The vertical coordinate of the object center..
        
        **Invariant**: Must be an int or float."""
        return self._trans.y
    
    @y.setter
    def y(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._trans.y = float(value)
        self._mtrue = False
    
    @property
    def width(self):
        """The horizontal width of this shape. 
        
        Positive values go to the right.
        
        **Invariant**: Must be an int or float > 0.""" 
        return self._width
    
    @width.setter
    def width(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        assert value > 0, 'value %s is not positive' % `value`
        self._width = float(value)
        if self._defined:
            self._reset()
    
    @property
    def height(self):
        """The vertical height of this shape. 
        
        Positive values go up.
        
        **Invariant**: Must be an int or float > 0.""" 
        return self._height
    
    @height.setter
    def height(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        assert value > 0, 'value %s is not positive' % `value`
        self._height = float(value)
        if self._defined:
            self._reset()
    
    @property
    def scale(self):
        """The scaling factor of this shape.
        
        The scale is a fast way to cause a shape to grow or shrink in size. Essentially,
        the object will multiple the width and height by the scale.  So a scale less than
        1 will shrink the object, while a scale greater than 1 will enlarge the object.
        
        The scale may either be a single number, or a pair of two numbers.  If it is
        a single number, it will scale the width and height by the same amount. If it is
        a pair, it will scale the width by the first value, and the height by the second.
        
        **Invariant**: Must be either a number (int or float) or a pair of numbers.""" 
        return (self._scale.x,self._scale.y)
    
    @scale.setter
    def scale(self,value):
        # Do some checking here
        assert _is_num(value) or _is_num_tuple(value,2), \
                'value %s is not a valid scaling factor' % `value`
        if _is_num(value):
            self._scale.x = float(value)
            self._scale.y = float(value)
        else:
            self._scale.x = float(value[0])
            self._scale.y = float(value[1])
        self._mtrue = False
    
    @property
    def angle(self):
        """The angle of rotation about the center.
        
        The angle is measured in degrees (not radians) counter-clockwise.
        
        **Invariant**: Must be an int or float.""" 
        return self._rotate.angle
    
    @angle.setter
    def angle(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = np.allclose([self._rotate.angle],[value])
        self._rotate.angle = float(value)
        if not diff:
            self._mtrue = False
    
    @property
    def fillcolor(self):
        """The object fill color.
        
        This value is used to color the backgrounds or, in the case of solid shapes, 
        the shape interior.
        
        The default representation of color in GObject is a 4-element list of floats 
        between 0 and 1 (representing r, g, b, and a).  As with the Turtle, you may also
        assign color an `RGB` or `HSV` object from `colormodel`, or a string with a valid 
        color name. If you chose either of these alternate representations (a string or 
        an object from `colormodel`), Python will automatically convert the result into 
        a 4-element list.
        
        **Invariant**: Must be a 4-element list of floats between 0 and 1."""
        return self._fillcolor.rgba
    
    @fillcolor.setter
    def fillcolor(self,value):
        assert _is_color(value), 'value %s is not a valid color' % `value`
        if type(value) in [tuple, list] and len(value) == 3:
            value = list(value)+[1.0]
        elif type(value) in [colormodel.RGB, colormodel.HSV]:
            value = value.glColor()
        elif type(value) == str:
            if value[0] == '#':
                value = colormodel.RGB.CreateWebColor(c).glColor()
            else:
                value = colormodel.RGB.CreateName(c).glColor()
        
        self._fillcolor = Color(value[0],value[1],value[2],value[3])
        if self._defined:
            self._reset()
    
    @property
    def linecolor(self):
        """The object line color.
        
        The default representation of color in GObject is a 4-element list of floats 
        between 0 and 1 (representing r, g, b, and a).  As with the Turtle, you may also
        assign color an `RGB` or `HSV` object from `colormodel`, or a string with a valid 
        color name. If you chose either of these alternate representations (a string or 
        an object from `colormodel`), Python will automatically convert the result into 
        a 4-element list.
        
        **Invariant**: Must be a 4-element list of floats between 0 and 1."""
        return self._linecolor.rgba
    
    @linecolor.setter
    def linecolor(self,value):
        assert _is_color(value), 'value %s is not a valid color' % `value`
        if type(value) in [tuple, list] and len(value) == 3:
            value = list(value)+[1.0]
        elif type(value) in [colormodel.RGB, colormodel.HSV]:
            value = value.glColor()
        elif type(value) == str:
            if value[0] == '#':
                value = colormodel.RGB.CreateWebColor(c).glColor()
            else:
                value = colormodel.RGB.CreateName(c).glColor()
        
        self._linecolor = Color(value[0],value[1],value[2],value[3])
        if self._defined:
            self._reset()
    
    @property
    def name(self):
        """The name of this object.
        
        This value is for debugging purposes only.  If you name an object, the name
        will appear when you convert the object to a string.  This will allow you to 
        tell which object is which in your watches.
        
        **Invariant**: Must be a string or None."""
        return self._name
    
    @name.setter
    def name(self,value):
        assert value is None or type(value) == str, 'value %s is not a valid name' % `value`
        self._name = value
    
    # DERIVED PROPERTIES
    @property
    def left(self):
        """The left edge of this shape.
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `x-width/2`.  Otherwise, it is the left-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the left
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.x-self.width/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[0]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[0]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[0]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[0]
        return min(p0,p1,p2,p3)
    
    @left.setter
    def left(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.left
        self.x += diff
    
    @property
    def right(self):
        """The right edge of this shape.
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `x+width/2`.  Otherwise, it is the right-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the right
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.x+self.width/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[0]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[0]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[0]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[0]
        return max(p0,p1,p2,p3)
    
    @right.setter
    def right(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.right
        self.x += diff
    
    @property
    def top(self):
        """The vertical coordinate of the top edge.
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `y+height/2`.  Otherwise, it is the top-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the top
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.y+self.height/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[1]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[1]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[1]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[1]
        return max(p0,p1,p2,p3)
    
    @top.setter
    def top(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.top
        self.y += diff
    
    @property
    def bottom(self):
        """The vertical coordinate of the bottom edge.
        
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `y-height/2`.  Otherwise, it is the bottom-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the bottom
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.y-self.height/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[1]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[1]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[1]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[1]
        return min(p0,p1,p2,p3)
    
    
    @bottom.setter
    def bottom(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.bottom
        self.y += diff
    
    
    # IMMUTABLE PROPERTIES
    @property
    def matrix(self):
        """The transformation matrix for this object
        
        This value is constructed dynamically as needed.  It should only be used
        internally to this file.
        
        **Invariant**: Either a GMatrix or None"""
        if not self._mtrue or self._matrix is None:
            self._matrix = GMatrix()
            self._matrix.translate(self._trans.x,self._trans.y)
            self._matrix.rotate(self._rotate.angle,z=1)
            self._matrix.scale(self._scale.x,self._scale.y)
            self._invrse = GMatrix()
            self._invrse.scale(1.0/self._scale.x,1.0/self._scale.y)
            self._invrse.rotate(-self._rotate.angle,z=1)
            self._invrse.translate(-self._trans.x,-self._trans.y)
            self._mtrue = True
        return self._matrix
    
    @property
    def inverse(self):
        """The transformation matrix for this object
        
        This value is constructed dynamically as needed.  It should only be used
        internally to this file.
        
        **Invariant**: Either a GMatrix or None"""
        if not self._mtrue or self._matrix is None:
            self._matrix = GMatrix()
            self._matrix.translate(self._trans.x,self._trans.y)
            self._matrix.rotate(self._rotate.angle,z=1)
            self._matrix.scale(self._scale.x,self._scale.y)
            self._invrse = GMatrix()
            self._invrse.scale(1.0/self._scale.x,1.0/self._scale.y)
            self._invrse.rotate(-self._rotate.angle,z=1)
            self._invrse.translate(-self._trans.x,-self._trans.y)
            self._mtrue = True
        return self._invrse
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new GObject to be drawn.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes.  For example, to initialize 
        the x position and the fill color, use the constructor call
        
            GObject(x=2,fillcolor=colormodel.RED)
        
        You do not need to provide the keywords as a dictionary. The ** in the parameter 
        `keywords` does that automatically.
        
        Any attribute of this class may be used as a keyword. The argument must satisfy 
        the invariants of that attribute. See the list of attributes of this class for 
        more information."""
        # Set the properties.
        self._defined = False
        
        # Create the Kivy transforms for position and size
        self._trans  = Translate(0,0,0)
        self._rotate = Rotate(angle=0,axis=(0,0,1))
        self._scale  = Scale(1,1,1)
        
        # Now update these with the keywords; size first
        if 'width'  in keywords:
            self.width  = keywords['width'] 
        else:
            self._width = 1
        
        if 'height' in keywords:
            self.height = keywords['height'] 
        else:
            self._height = 1
        
        # Then angle
        if 'angle' in keywords:
            self.angle = keywords['angle']
        
        # Finally, (relative) position
        if 'x' in keywords:
            self.x = keywords['x']
        elif 'left' in keywords:
            self.left = keywords['left']
        elif 'right' in keywords:
            self.right = keywords['right']
        
        if 'y' in keywords:
            self.y = keywords['y']
        elif 'bottom' in keywords:
            self.bottom = keywords['bottom']
        elif 'top' in keywords:
            self.top = keywords['top']
        
        # Top it off with color
        self.fillcolor = keywords['fillcolor'] if 'fillcolor' in keywords else (1,1,1,1)
        self.linecolor = keywords['linecolor'] if 'linecolor' in keywords else (0,0,0,1)
        
        # Add a name for debugging
        self.name = keywords['name'] if 'name' in keywords else None
    
    def __str__(self):
        """**Returns**: A string representation of this object."""
        if self.name is None:
            s = '['
        else:
            s = '[name=%s,' % self.name
        return '%s,center=(%s,%s),width=%s,height=%s,angle=%s]' \
                % (s,`self.x`,`self.y`,`self.height`,`self.width`,`self.angle`)
    
    def __repr__(self):
        """**Returns**: An unambiguous representation of this object."""
        return str(self.__class__)+str(self)
    
    # PUBLIC METHODS
    def contains(self,x,y):
        """**Returns**: True if this shape contains the point (x,y), False otherwise.
        
            :param x: x coordinate of point to check
            **Precondition**: an int or float
            
            :param y: y coordinate of point to check
            **Precondition**: an int or float
        
        By default, this method just checks the bounding box of the shape.
        
        **Warning**: Accessing this value on a rotated object may slow down your
        framerate significantly.
        """
        if self._rotate.angle == 0.0:
            return abs(x-self.x) < self.width/2.0 and abs(y-self.y) < self.height/2.0
        
        p = self.matrix.inverse()._transform(x,y)
        return abs(p[0]) < self.width/2.0 and abs(p[1]) < self.height/2.0
    
    def transform(self,point):
        """**Returns**: The given point transformed to local coordinate system
        
            :param point: the point to transform
            **Precondition**: a GPoint or a pair of numbers (int or float)
        
        This method is important for mouse selection.  It helps you understand where
        in the shape the selection takes place.  In the case of objects with children,
        lik e`GScene`, this method is necessary to properly use the contains method
        on the children.
        
        The value returned is a GPoint."""
        if isinstance(point,GPoint):
            return self.inverse.transform(point)
        else:
            assert len(point) == 2 and _is_num_tuple(point,2)
            p = self.inverse._transform(point[0],point[2])
            return GPoint(p[0],p[1])
    
    
    def draw(self, view):
        """Draw this shape in the provide view.
        
            :param view: view to draw to
            **Precondition**: an *instance of* `GView`
        
        Ideally, the view should be the one provided by `GameApp`."""
        view.draw(self._cache)
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        self._cache = InstructionGroup()
        self._cache.add(PushMatrix())
        self._cache.add(self._trans)
        self._cache.add(self._rotate)
        self._cache.add(self._scale)


class GRectangle(GObject):
    """Instances represent a solid rectangle.
    
    As with `GObject`, the attributes x and y refer to the center of the rectangle. This
    is so that when you rotate the rectangle, it spins about the center.
    
    The interior (fill) color of this rectangle is `fillcolor`, while `linecolor`
    is the color of the border.
    
    The only new property for this class is `linewidth`, which controls the width of
    the border around the rectangle.  For all other properties, see the documentation
    for `GObject`."""
    
    # MUTABLE PROPERTIES 
    @property
    def linewidth(self):
        """The width of the exterior line of this shape.
        
        Setting this to 0 means that the rectangle has no border.
        
        **Invariant**: Must be an int or float >= 0."""
        return self._linewidth
    
    @linewidth.setter
    def linewidth(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        assert value >= 0, 'value %s is negative' % `value`
        self._linewidth = value
        if self._defined:
            self._reset()
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new solid rectangle
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a 
        list of keyword arguments that initialize various attributes. For 
        example, to create a red square centered at (0,0), use the constructor call
        
            GRectangle(x=0,y=0,width=10,height=10,fillcolor=colormodel.RED)
        
        This class supports the all same keywords as `GObject` plus the additional
        keyword `linewidth`."""
        self._defined = False
        self.linewidth = keywords['linewidth'] if 'linewidth' in keywords else 0.0
        # Always delay the call to parent class, to avoid reset
        GObject.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        x = -self.width/2.0
        y = -self.height/2.0
        
        fill = Rectangle(pos=(x,y), size=(self.width, self.height))
        self._cache.add(self._fillcolor)
        self._cache.add(fill)
        
        if self.linewidth > 0:
            line = Line(rectangle=(x,y,self.width,self.height),joint='miter',
                        close=True,width=self.linewidth)
            self._cache.add(self._linecolor)
            self._cache.add(line)
        
        self._cache.add(PopMatrix())


class GEllipse(GRectangle):
    """Instances represent a solid ellipse.
    
    The ellipse is the largest one that can be drawn inside of a rectangle whose 
    bottom center is at (x,y), with the given width and height.  The interior 
    (fill) color of this ellipse is `fillcolor`, while `linecolor` is the color 
    of the border.
    
    This class has exactly the same properties as `GRectangle`.  See the documentation
    of that class and `GObject` for a complete list of properties."""
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new solid ellipse
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of
        keyword arguments that initialize various attributes. For example, to create a 
        red circle centered at (0,0), use the constructor call
        
            GEllipse(x=0,y=0,width=10,height=10,fillcolor=colormodel.RED)
        
        This class supports the all same keywords as `GRectangle`."""
        GRectangle.__init__(self,**keywords)
    
    
    # PUBLIC METHODS
    def contains(self,x,y):
        """**Returns**: True if this shape contains the point (x,y), False otherwise.
        
            :param x: x coordinate of point to check
            **Precondition**: an int or float
            
            :param y: y coordinate of point to check
            **Precondition**: an int or float
        
        This method is better than simple rectangle inclusion.  It checks that the point 
        is within the proper radius as well.
        
        **Warning**: Accessing this value on a rotated object may slow down your
        framerate significantly.
        """
        rx = self.width/2.0
        ry = self.height/2.0
        if self._rotate.angle == 0.0:
            dx = (x-self.x)*(x-self.x)/(rx*rx)
            dy = (y-self.y)*(y-self.y)/(ry*ry)
        else:
            p = self.matrix.inverse()._transform(x,y)
            dx = p[0]*p[0]/(rx*rx)
            dy = p[1]*p[1]/(ry*ry)
        
        return (dx+dy) <= 1.0
    
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        x = -self.width/2.0
        y = -self.height/2.0
        
        fill = Ellipse(pos=(x,y), size=(self.width,self.height))
        self._cache.add(self._fillcolor)
        self._cache.add(fill)
        
        if self._linewidth > 0:
            line = Line(ellipse=(x,y,self.width,self.height),close=True,width=self.linewidth)
            self._cache.add(self._linecolor)
            self._cache.add(line)
        
        self._cache.add(PopMatrix())


class GImage(GRectangle):
    """Instances represents a rectangular image.
    
    The image is given by a JPEG, PNG, or GIF file whose name is stored in the attribute 
    `source`.  Image files should be stored in the **Images** directory so that Kivy can 
    find them without the complete path name.
    
    This class acts much like is parent `GRectangle` and shares all of the same properties.
    As with that class, you can add a border to the rectangle if you want, using the
    attribute `linewidth`.
    
    If the attributes `width` and `height` do not agree with the actual size of the image, 
    the image is scaled to fit.Furthermore, if you define `fillcolor`, Kivy will tint 
    your image by the given color.`
    
    If the image supports transparency, then this object can be used to represent 
    irregular shapes.  However, the `contains` method still treats this shape as a 
    rectangle.
    """
    
    # MUTABLE PROPERTIES
    @property
    def source(self):
        """The source file for this image.
        
        **Invariant**. Must be a string refering to a valid file."""
        return self._source

    @source.setter
    def source(self,value):
        assert value is None or _is_image_file(value), 'value %s is not an image file' % `value`
        self._source = value
        if self._defined:
            self._reset()
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new rectangle image
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to load the 
        image `beach-ball.png`, use the constructor
        
            GImage(x=0,y=0,width=10,height=10,source='beach-ball.png')
        
        This class supports the all same keywords as `GRectangle`; the only new keyword
        is `source`.  See the documentation of `GRectangle` and `GObject` for the other
        supported keywords."""
        self._defined = False
        self.source = keywords['source'] if 'source' in keywords else None
        GRectangle.__init__(self,**keywords)
        self._defined = True
    
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        x = -self.width/2.0
        y = -self.height/2.0
        
        fill = Rectangle(pos=(x,y), size=(self.width, self.height),source=self.source)
        self._cache.add(self._fillcolor)
        self._cache.add(fill)
        
        if self.linewidth > 0:
            line = Line(rectangle=(x,y,self.width,self.height),joint='miter',close=True,width=self.linewidth)
            self._cache.add(self._linecolor)
            self._cache.add(line)
        
        self._cache.add(PopMatrix())


class GLabel(GRectangle):
    """Instances represent an (uneditable) text label
    
    This object is exactly like a GRectangle, except that it has the possibility of
    containing some text.
    
    The attribute `text` defines the text content of this label.  Uses of the escape 
    character '\\n' will result in a label that spans multiple lines.  As with any
    `GRectangle`, the background color of this rectangle is `fillcolor`, while 
    `linecolor` is the color of the text.
    
    The text itself is aligned within this rectangle according to the attributes `halign` 
    and `valign`.  See the documentation of these attributes for how alignment works.  
    There are also attributes to change the point size, font style, and font name of the 
    text. The `width` and `height` of this label will grow to ensure that the text will 
    fit in the rectangle, no matter the font or point size.
    
    To change the font, you need a .ttf (TrueType Font) file in the Fonts folder; refer 
    to the font by filename, including the .ttf. If you give no name, it will use the 
    default Kivy font.  The `bold` attribute only works for the default Kivy font; for 
    other fonts you will need the .ttf file for the bold version of that font.  See the
    provided `ComicSans.ttf` and `ComicSansBold.ttf` for an example."""
    
    # MUTABLE PROPERTIES
    @property
    def font_size(self):
        """Size of the text font in points.
        
        **Invariant**: Must be a positive number (int or float)"""
        return self._fsize
    
    @font_size.setter
    def font_size(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._fsize = value
        self._label.font_size = value
        self._label.texture_update()
    
    @property
    def font_name(self):
        """File name for the .ttf file to use as a font
        
        **Invariant**: Must be a string referring to a .ttf file in folder Fonts"""
        return self._label.font_name
    
    @font_name.setter
    def font_name(self,value):
        assert _is_font_file(value), 'value %s is not a font name' % `value`
        self._label.font_name = value
        self._label.texture_update()
    
    @property
    def bold(self):
        """Boolean indicating whether or not the text should be bold.
        
        This value only works on the default Kivy font.  It does not work on custom
        .ttf files.  In that case, you need the bold version of the .ttf file.  See 
        `ComicSans.ttf` and `ComicSansBold.ttf` for an example.
        
        **Invariant**: Must be a boolean"""
        return self._label.bold

    @bold.setter
    def bold(self,value):
        assert type(value) == bool, `value`+' is not a bool'
        self._label.bold = value
        self._label.texture_update()

    @property
    def text(self):
        """Text for this label.
        
        The text in the label is displayed as a single line, or broken up into multiple 
        lines in the presence of the escape character '\\n'. The `width` and `height` of 
        this label will grow to ensure that the text will fit in the rectangle.
        
        **Invariant**: Must be a string"""
        return self._label.text
    
    @text.setter
    def text(self,value):
        assert type(value) == str, 'value %s is not a string' % `value`
        self._label.text = value
        self._label.texture_update()
    
    @property
    def halign(self):
        """Horizontal alignment for this label.
        
        The text is horizontally anchored inside of the label rectangle at either the 
        left, the right or the center.  This means that as the size of the label 
        increases, the text will still stay rooted at that anchor.  By default, the
        text is centered.
        
        **Invariant**: Must be one of 'left', 'right', or 'center'"""
        return self._halign
    
    @halign.setter
    def halign(self,value):
        assert value in ('left','right','center'), 'value %s is not a valid horizontal alignment' % `value`
        self._halign = value
        self._label.halign = value
        if self._defined:
            self._reset()
    
    @property
    def valign(self):
        """Vertical alignment for this label.
        
        The text is vertically anchored inside of the label rectangle at either the top, 
        the bottom or the middle.  This means that as the size of the label increases, 
        the text will still stay rooted at that anchor.  By default, the text is in
        the middle.
        
        **Invariant**: Must be one of 'top', 'bottom', or 'middle'"""
        return self._valign
    
    @valign.setter
    def valign(self,value):
        assert value in ('top','middle','bottom'), 'value %s is not a valid vertical alignment' % `value`
        self._valign = value
        self._label.valign = value
        if self._defined:
            self._reset()
    
    
    # REDEFINED PROPERTIES
    @property
    def x(self):
        """The horizontal coordinate of the object center.
        
        **Invariant**: Must be an int or float."""
        return self._trans.x
    
    @x.setter
    def x(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._trans.x = float(value)
        self._mtrue = False
        self._hanchor = 'center'
        self._ha = value
    
    @property
    def y(self):
        """The vertical coordinate of the object center..
        
        **Invariant**: Must be an int or float."""
        return self._trans.y
    
    @y.setter
    def y(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        self._trans.y = float(value)
        self._mtrue = False
        self._vanchor = 'center'
        self._hv = value
    
    @property
    def left(self):
        """The left edge of this shape.
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `x-width/2`.  Otherwise, it is the left-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the left
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.x-self.width/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[0]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[0]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[0]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[0]
        return min(p0,p1,p2,p3)
    
    @left.setter
    def left(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.left
        self.x += diff
        self._hanchor = 'left'
        self._ha = value
    
    @property
    def right(self):
        """The right edge of this shape.
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `x+width/2`.  Otherwise, it is the right-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the right
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.x+self.width/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[0]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[0]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[0]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[0]
        return max(p0,p1,p2,p3)
    
    @right.setter
    def right(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.right
        self.x += diff
        self._hanchor = 'right'
        self._ha = value
    
    @property
    def top(self):
        """The vertical coordinate of the top edge.
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `y+height/2`.  Otherwise, it is the top-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the top
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.y+self.height/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[1]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[1]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[1]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[1]
        return max(p0,p1,p2,p3)
    
    @top.setter
    def top(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.top
        self.y += diff
        self._vanchor = 'top'
        self._hv = value
    
    @property
    def bottom(self):
        """The vertical coordinate of the bottom edge.
        
        
        The value depends on the current angle of rotation. If rotation is 0, it is
        `y-height/2`.  Otherwise, it is the bottom-most value of the bounding box.
        
        Changing this value will shift the center of the object so that the bottom
        edge matches the new value.
        
        **Warning**: Accessing this value on a rotated object will slow down your
        framerate significantly.
        
        **Invariant**: Must be an int or float."""
        if self._rotate.angle == 0.0:
            return self.y-self.height/2.0
        
        p0 = self.matrix._transform(self.x-self.width/2.0, self.y-self.height/2.0)[1]
        p1 = self.matrix._transform(self.x+self.width/2.0, self.y-self.height/2.0)[1]
        p2 = self.matrix._transform(self.x+self.width/2.0, self.y+self.height/2.0)[1]
        p3 = self.matrix._transform(self.x-self.width/2.0, self.y+self.height/2.0)[1]
        return min(p0,p1,p2,p3)
    
    
    @bottom.setter
    def bottom(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        diff = value-self.bottom
        self.y += diff
        self._vanchor = 'bottom'
        self._hv = value
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new text label.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to create a 
        label containing the word 'Hello', use the constructor call
        
            GLabel(text='Hello')
        
        This class supports the same keywords as `GRectangle`, as well as additional 
        attributes for the text properties (e.g. font size and name)."""
        self._defined = False
        self._hanchor = 'center'
        self._vanchor = 'center'
        
        self._label = Label(**keywords)
        self._label.size_hint = (None,None)
        
        self.linewidth = keywords['linewidth'] if 'linewidth' in keywords else 0.0
        self.halign = keywords['halign'] if 'halign' in keywords else 'center'
        self.valign = keywords['valign'] if 'valign' in keywords else 'middle'
        
        GObject.__init__(self,**keywords)
        self._reset()
        self._defined = True
        self._label.bind(texture_size=self._callback)
    
    def __str__(self):
        """**Returns**: A string representation of this object."""
        if self.name is None:
            s = '['
        else:
            s = '[name=%s,' % self.name
        return '%s,text=%s,center=(%s,%s),angle=%s]' \
                % (s,`self.text`,`self.x`,`self.y`,`self.angle`)
    
    # HIDDEN METHODS
    def _callback(self,instance=None,value=None):
        """Workaround to deal with parameter requirements for callbacks"""
        if self._defined:
            self._reset()
    
    def _reset(self):
        """Resets the drawing cache"""
        # Set up the label at the center.
        self._label.size = self._label.texture_size
        self._label.center = (0,0)
        self._label.color = self.linecolor
        
        # Resize the outside if necessary
        self._defined = False
        self.width  = max(self.width, self._label.width)
        self.height = max(self.height,self._label.height)
        self._defined = True
        
        # Reset the absolute anchor
        if self._hanchor == 'left':
            self._trans.x = self._ha+self.width/2.0
        elif self._hanchor == 'right':
            self._trans.x = self._ha-self.width/2.0
        
        # Reset the absolute anchor
        if self._vanchor == 'top':
            self._trans.y = self._hv-self.height/2.0
        elif self._vanchor == 'bottom':
            self._trans.y = self._hv+self.height/2.0
        
        # Reset the label anchor.
        if self.halign == 'left':
            self._label.x = -self.width/2.0
        elif self.halign == 'right':
            self._label.right = self.width/2.0
        
        # Reset the label anchor.
        if self.valign == 'top':
            self._label.top = self.height/2.0
        elif self.valign == 'bottom':
            self._label.bottom = -self.height/2.0
        
        GObject._reset(self)
        x = -self.width/2.0
        y = -self.height/2.0
        
        fill = Rectangle(pos=(x,y), size=(self.width,self.height))
        self._cache.add(self._fillcolor)
        self._cache.add(fill)
        self._cache.add(self._label.canvas)
        
        if self._linewidth > 0:
            line = Line(rectangle=(x,y,self.width,self.height),joint='miter',close=True,width=self.linewidth)
            self._cache.add(self._linecolor)
            self._cache.add(line)
        
        self._cache.add(PopMatrix())


################# PATH PRIMITIVES #################
pass 
# #mark PATH PRIMITIVES

class GPath(GObject):
    """Instances represent a sequence of line segments
    
    The path is defined by the `points` attribute which is an (even) sequence of 
    alternating x and y values. When drawn in a `GView` object, the line starts from 
    one x-y pair in `points` and goes to the next x-y pair.  If `points` has length 2n, 
    then the result is n-1 line segments.
    
    The object uses the attribute `linecolor` to determine the color of the line and the
    attribute `linewidth` to determine the width.  The attribute `fillcolor` is unused 
    (even though it is inherited from `GObject`).
    
    The attributes `width` and `height` are present in this object, but they are now
    read-only.  These values are computed from the list of points.
    
    On the other hand, the attributes `x` and `y` are used.  By default, these values
    are 0.  However, if they are nonzero, then Python will add them to all of the points
    in the path, shifting the path accordingly.
    """
    
    # MUTABLE PROPERTIES
    @property
    def points(self):
        """The sequence of points that make up this line.
        
        **Invariant**: Must be a sequence (list or tuple) of int or float. 
        The length of this sequence must be even with length at least 4."""
        return self._points
    
    @points.setter
    def points(self,value):
        assert _is_point_tuple(value,2),'value %s is not a valid list of points' %  `value`
        self._points = tuple(value)
        if self._defined:
            self._reset()
    
    @property
    def linewidth(self):
        """The width of this path.
        
        Setting this value to 0 means that the path is invisible.
        
        **Invariant**: Must be an int or float >= 0."""
        return self._linewidth
    
    @linewidth.setter
    def linewidth(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        assert value >= 0, 'value %s is negative' % `value`
        self._linewidth = value
        if self._defined:
            self._reset()
    
    
    # IMMUTABLE PROPERTIES
    @property
    def width(self):
        """The horizontal width of this path. 
        
        The value is the width of the smallest bounding box that contains all of the
        points in the line AND the origin (0,0).
        
        **Invariant**: Must be an int or float > 0.""" 
        px = self.points[::2]+(0,0)
        return 2*max(max(px),-min(px))
    
    @property
    def height(self):
        """The vertical height of this path. 
        
        The value is the height of the smallest bounding box that contains all of the
        points in the line AND the origin (0,0).
        
        **Invariant**: Must be an int or float > 0.""" 
        py = self.points[1::2]+(0,0)
        return 2*max(max(py),-min(py))
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new sequence of line segments.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to create a 
        line from (0,0) to (2,3) with width 2, use the constructor call
        
            GLine(points=[0,0,2,3],linewidth=2)
        
        This class supports the same keywords as `GObject`, though some of them are 
        unused, as the `width` and `height` attributes are now immutable.  The primary
        keywords for this class are `points`, `linecolor`, and `linewidth`."""
        self._defined = False
        self.linewidth = keywords['linewidth'] if 'linewidth' in keywords else 1.0
        self.points = keywords['points'] if 'points' in keywords else (0,0,10,10)
        GObject.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    
    # PUBLIC METHODS
    def contains(self,x,y):
        """**Returns**: True if this path contains the point (x,y), False otherwise.
        
            :param x: x coordinate of point to check
            **Precondition**: an int or float
            
            :param y: y coordinate of point to check
            **Precondition**: an int or float
        
        This method always returns `False` as a `GPath` has no interior."""
        return False
    
    def near(self,x,y):
        """**Returns**: True if this path is near the point (x,y), False otherwise.
        
            :param x: x coordinate of point to check
            **Precondition**: an int or float
            
            :param y: y coordinate of point to check
            **Precondition**: an int or float
        
        To determine if (x,y) is near the path, we compute the minimum distances
        from (x,y) to the path.  If this distance is less than e-6, we return True."""
        size = len(self.points)/2
        epsilon = 1e-6
        for ii in range(size-1):
            p = self.points[2*ii  :2*ii+2]
            q = self.points[2*ii+2:2*ii+4]
            if p == q:
                test = np.sqrt((q[0]-x)*(q[0]-x)+(q[1]-y)*(q[1]-y)) < epsilon
            else:
                num = abs((q[0]-p[0])*x-(q[1]-p[1])*y+q[0]*p[1]-p[0]*q[1])
                den = np.sqrt((q[0]-p[0])*(q[0]-p[0])+(q[1]-p[1])*(q[1]-p[1]))
                test = num/den
            if test:
                return True
        
        return self.contains(x,y)
    
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        self._cache.add(self._linecolor)
        line = Line(points=self.points,cap='round',joint='round',width=self.linewidth)
        self._cache.add(line)
        self._cache.add(PopMatrix())


class GTriangle(GPath):
    """Instances represent a solid triangle.
    
    The triangle is defined as a sequence of three point. Just as with the `GPath` class
    (which is the parent of this class), it has an attribute `point` which represents
    this points as an even-length sequence of ints or floats.
    
    The interior (fill) color of this triangle is `fillcolor`, while `linecolor`
    is the color of the border.  If `linewidth` is set to 0, then the border is 
    not visible.
    
    As with `GPath`, the attributes `x` and `y` may be used to shift the triangle 
    position. By default, these values are 0.  However, if they are nonzero, then Python 
    will add them to the triangle vertices.  Similarly, the attributes `width` and 
    `height` are immutable, and are computed directly from the points"""
    
    # MUTABLE PROPERTIES
    @property
    def points(self):
        """The sequence of vertices that make up this trianle.
        
        **Invariant**: Must be a sequence (list or tuple) of int or float. 
        The length of this sequence must be exactly 6."""
        return self._points
    
    @points.setter
    def points(self,value):
        assert _is_num_tuple(value,6),'value %s is not a valid list of points' %  `value`
        self._points = tuple(value)
        if self._defined:
            self._reset()
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new solid triangle.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to create a 
        red triangle with vertices (0,0), (2,3), and (0,4), use the constructor call
        
            GTriangle(points=[0,0,2,3,0,4],fillcolor=colormodel.RED)
        
        As with `GPath` the `width` and `height` attributes of this class are both
        immutable.  They are computed from the list of points."""
        self._defined = False
        self.linewidth = keywords['linewidth'] if 'linewidth' in keywords else 0.0
        self.points = keywords['points'] if 'points' in keywords else (-100,-58,0,116,100,-58)
        GObject.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    
    # PUBLIC METHODS
    def contains(self,x,y):
        """**Returns**: True if this shape contains the point (x,y), False otherwise.
        
            :param x: x coordinate of point to check
            **Precondition**: an int or float
            
            :param y: y coordinate of point to check
            **Precondition**: an int or float
        
        This method uses a standard test for triangle inclusion."""
        return _in_triangle((x,y),self._points)
    
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        
        vertices = ()
        for x in range(3):
            # Need to tack on degenerate texture coords
            vertices += self.points[2*x:2*x+2]+(0,0)
        mesh = Mesh(vertices=vertices, indices=range(3), mode='triangle_strip')
        self._cache.add(self._fillcolor)
        self._cache.add(mesh)
        
        if self.linewidth > 0:
            line = Line(points=self.points,joint='miter',close=True,width=self.linewidth)
            self._cache.add(self._linecolor)
            self._cache.add(line)
        
        self._cache.add(PopMatrix())


class GPolygon(GPath):
    """Instances represent a solid polygon.  
    
    The polygon is a triangle fan from the center of the polyon to the vertices in the
    attribute `points`. The center of the polygon is always the point (0,0), unless 
    you reassign the attributes `x` and `y`.  However, as with `GPath`, if you assign
    the attributes `x` and `y`, then Python will shift all of the vertices by that 
    same amount. Hence the polygon vertices must be defined as triangle fan centered at 
    the origin.
    
    The interior (fill) color of this triangle is `fillcolor`, while `linecolor`
    is the color of the border.  If `linewidth` is set to 0, then the border is 
    not visible.
    
    The polygon may also be textured by specifying a source image. The texture coordinates 
    of each vertex will be relative to the size of the image.  For example, if the image 
    is 64x64, then the quad polygon (-32,-32,-32,32,32,32,32,-32) will be a rectangle 
    equal to the image.  You can adjust the size of the source image with the attributes
    `source_width` and `source_height`. If the polygon is larger than the image, then the 
    texture will repeat.

    As with `GPath`, the attributes `width` and `height` are immutable, and are computed 
    directly from the points"""
    
    # MUTABLE PROPERTIES
    @property
    def points(self):
        """The sequence of points that make up this polygon.
        
        **Invariant**: Must be a sequence (list or tuple) of int or float. 
        The length of this sequence must be even with length at least 6."""
        return self._points
    
    @points.setter
    def points(self,value):
        assert _is_point_tuple(value,4),'value %s is not a valid list of points' % `value`
        self._points = tuple(value)
        if self._defined:
            self._reset()
    
    @property
    def source(self):
        """The source image for texturing this polygon
        
        **Invariant**. Must be a string refering to a valid file."""
        return self._source

    @source.setter
    def source(self,value):
        assert value is None or _is_image_file(value), 'value %s is not an image file' % `value`
        self._source = value
        if self._defined:
            self._reset()
    
    @property
    def source_width(self):
        """The width to scale the source image.
        
        The texture coordinates of each vertex will be relative to the size of the image.  
        For example, if the image is 64x64, then the polygon (-32,-32,-32,32,32,32,32,-32) 
        will be a rectangle equal to the image.
        
        This attribute allows you to resize the image for these texture coordinates. So
        if the image is 512x64, setting this value to 64 will be as if the image was 
        originally 64x64. If this value is None, the Python will use the normal width
        of the image file
        
        **Invariant**. Must be a number (int or float) > 0 or None."""
        return self._source_width
    
    @source_width.setter
    def source_width(self,value):
        assert value is None or _is_num(value), 'value %s is not a valid width' % `value`
        self._source_width = None
        if self._defined:
            self._reset()
    
    @property
    def source_height(self):
        """The height to scale the source image.
        
        The texture coordinates of each vertex will be relative to the size of the image.  
        For example, if the image is 64x64, then the polygon (-32,-32,-32,32,32,32,32,-32) 
        will be a rectangle equal to the image.
        
        This attribute allows you to resize the image for these texture coordinates. So
        if the image is 64x512, setting this value to 64 will be as if the image was 
        originally 64x64. If this value is None, the Python will use the normal width
        of the image file
        
        **Invariant**. Must be a number (int or float) > 0 or None."""
        return self._source_width
    
    @source_height.setter
    def source_height(self,value):
        assert value is None or _is_num(value), 'value %s is not a valid width' % `value`
        self._source_height = None
        if self._defined:
            self._reset()
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new solid polyon
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to create a 
        hexagon, use the constructor call
        
            GPolygon(points=[87,50,0,100,-87,50,-87,-50,0,-100,87,-50])
        
        As with `GPath` the `width` and `height` attributes of this class are both
        immutable.  They are computed from the list of points."""
        self._defined = False
        self.linewidth = keywords['linewidth'] if 'linewidth' in keywords else 0.0
        self.points = keywords['points'] if 'points' in keywords else (-100,-58,0,116,100,-58)
        self.source = keywords['source'] if 'source' in keywords else None
        self.source_width  = keywords['source_width']  if 'source_width'  in keywords else None
        self.source_height = keywords['source_height'] if 'source_height' in keywords else None
        GObject.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    
    # PUBLIC METHODS
    def contains(self,x,y):
        """**Returns**: True if this shape contains the point (x,y), False otherwise.
        
            :param x: x coordinate of point to check
            **Precondition**: an int or float
            
            :param y: y coordinate of point to check
            **Precondition**: an int or float
        
        This method cycles through each triangle in the triangle fan and tests each 
        triangle for inclusion."""
        found = False
        for i in xrange(4,len(self._points),2):
            t = (0,0)+self.points[i-4:i]
            found = found or _in_triangle((x,y),t)
        
        return found
    
    
    # HIDDEN METHODS
    def _make_mesh(self):
        """Creates the mesh for this polygon"""
        size = len(self.points)/2
        try:
            texture = Image(source=self.source).texture
            texture.wrap = 'repeat'
            tw = float(texture.width)  if self.source_width is None else self.source_width
            th = float(texture.height) if self.source_height is None else self.source_height
            
            # Centroid at 0, with texture centered
            verts = (0,0,0.5,0.5) 
            
            # Create the fan.
            for x in range(size):
                pt = self.points[2*x:2*x+2]
                self._verts += pt+(pt[0]/tw+0.5,pt[1]/th+0.5)
            
            # Come back to the beginning
            pt = self.points[0:2]
            verts += pt+(pt[0]/tw+0.5,pt[1]/th+0.5)
            self._mesh = Mesh(vertices=verts, indices=range(size+2), mode='triangle_fan', texture=texture)
        except BaseException as e:
            # Make all texture coordinates degnerate
            verts = (0,0,0,0) 
            for x in range(size):
                verts += self.points[2*x:2*x+2]+(0,0)
            verts += self.points[0:2]+(0,0)
            self._mesh = Mesh(vertices=verts, indices=range(size+2), mode='triangle_fan')
    
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        self._make_mesh()
        
        self._cache.add(self._fillcolor)
        self._cache.add(self._mesh)
        
        if self.linewidth > 0:
            line = Line(points=self.points,joint='miter',close=True,width=self.linewidth)
            self._cache.add(self._linecolor)
            self._cache.add(line)
        
        self._cache.add(PopMatrix())


################# SCENE GRAPH #################
pass 
# #mark SCENE GRAPH


class GScene(GObject):
    """Instances are a node in a scene graph.
    
    A scene graph node is just a collection of GObjects.  By placing them in the scene
    graph node, you can rotate and translate them all at once.  Scene graphs are a 
    sophisticated concept that allow you to do advanced animation.
    
    As `GScene` is a subclass of `GObject` you can nest scene graph nodes inside of
    other scene graph nodes.  The result is a tree structure.
    
    The attributes `width` and `height` are present in this object, but they are now
    read-only.  These values are computed from the list of GObjects stored in the scene.
    
    All GObjects stored in a GScene are drawn as if the point (x,y) is the origin.
    """
    
    # MUTABLE PROPERTIES
    @property
    def children(self):
        """The list of GObjects stores in this scene.
        
        The objects are drawn as if (x,y) is the origin.  Therefore, changing the 
        attributes `x` and `y` will shift all of the children on the screen.
        
        **Invariant**: Must be a list or tuple of GObjects (possibly empty)"""
        return tuple(self._children)
    
    @children.setter
    def children(self,value):
        assert _is_gobject_list(value), 'value %s is not a list of GObjects' % `value`
        self._children = list(value)
        if self._defined:
            self._reset()
    
    
    # IMMUTABLE PROPERTIES
    @property
    def width(self):
        """The horizontal width of this path. 
        
        The value is the width of the smallest bounding box that contains all of the
        objects in this scene (and the center)
        
        **Invariant**: Must be an int or float > 0.""" 
        max = 0
        for x in self.children:
            w = x.x+x.width/2.0
            if w > max:
                max = w
        return max*2
    
    @property
    def height(self):
        """The vertical height of this path. 
        
        The value is the height of the smallest bounding box that contains all of the
        objects in this scene (and the center)
        
        **Invariant**: Must be an int or float > 0.""" 
        max = 0
        for x in self.children:
            h = x.y+x.height/2.0
            if h > max:
                max = h
        return max*2
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates a new scene graph node
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to create a 
        scene with shapes rect, tri, and circ, call the constructor
        
            GScene(children=[rect,tri,circ])
        
        This class supports the same keywords as `GObject`, though some of them are 
        unused, as the `width` and `height` attributes are now immutable."""
        self._defined = False
        self.children = keywords['children'] if 'children' in keywords else []
        GObject.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    
    # HIDDEN METHODS
    def _reset(self):
        """Resets the drawing cache"""
        GObject._reset(self)
        for x in self.children:
            self._cache.add(x._cache)
        self._cache.add(PopMatrix())

################# SOUND CLASSES #################
pass 
# #mark SOUND CLASSES

class Sound(object):
    """Instances are a sound object that can be played.
    
    A sound is a WAV file that can be played on command via the method `play`.  While 
    some platforms may support MP3s, we can only guarantee that WAVs work on all 
    platforms. In order for Kivy to find a WAV or OGG file, you should put it in the
    **Sounds** directory.  Sounds in that folder can be referenced directly by name.
    
    When a sound is played, it cannot be played again until it finishes, or is stopped.  
    This means that if you want multiple, simultaneous sound effects from the same WAV 
    file.you will need to create multiple Sound objects.
    """
    # This class is a simply replacement for the built-in Kivy Sound class.  It is a
    # little better with error handling, since GStreamer appears to be quite unreliable.
    
    # MUTABLE PROPERTIES
    @property
    def volume(self):
        """The current sound volume.
        
        1 means full volume, 0 means mute.  The default value is 1.
        
        **Invariant**: Must float in the range 0..1."""
        return self._sound.volume
    
    @volume.setter
    def volume(self,value):
        assert type(value) in [int, float] and value >= 0 and value <= 1, \
            'value %s is not a valid volume' % `value`
        self._sound.volume = value
    
    # IMMUTABLE PROPERTIES
    @property
    def source(self):
        """The source file for this sound. 
        
        **Immutable**: This value cannot be changed after the sound is loaded.
        
        **Invariant**: Must be a nonempty string.""" 
        return self._source
    
    def __init__(self,source):
        """**Constructor**: Loads a new sound from a file.
        
            :param source: The string providing the name of a sound file
            **Precondition**: source is the name of a valid sound file
        """
        assert _is_sound_file(source), 'source %s is not a sound file' % `filename`
        self._source = source
        self._sound  = SoundLoader.load(source)
        if self._sound is None:
            raise IOError('Module game2d cannot read the file %s' % `source`)
    
    def play(self):
        """Plays this sound.
        
        The sound will play until completion, or interrupted by another sound"""
        self._sound.play()


class SoundLibrary(object):
    """Instances are a dictionary that maps sounds to Sound objects.
    
    This class implements to the dictionary interface to make it easier to load
    sounds and manage them.  To load a sound, simply assign it to the library
    object, as follows:
    
        soundlib['soundname'] = 'soundfile.wav'
    
    The sound library will load the sound and map it to 'soundname' as the key.
    To play the sound, we access it as follows:
    
        soundlib['soundname'].play()
    """
    
    def __init__(self):
        """**Constructor**: Creates a new, empty sound library."""
        if not _INITIALIZED:
            init()
        self._data = {}
    
    def __len__(self):
        """**Returns**: The number of sounds in this library."""
        return len(self._data)
    
    def __getitem__(self, key):
        """**Returns**: The Sound object for the given sound name.
            
            :param key: The key identifying a sound object
            **Precondition**:: key is a string.
        """
        return self._data[key]
    
    def __setitem__(self, key, filename):
        """Creates a sound object from the file filename and assigns it the given name.
            
            :param key: The key identifying a sound object
            **Precondition**:: key is a string.
            
            :param filename: The name of the file containing the sound source
            **Precondition**:: filename is the name of a valid sound file.
        
        """
        assert is_sound_file(filename), `filename`+' is not a sound file'
        self._data[key] = Sound(filename)
    
    def __delitem__(self, key):
        """Deletes the Sound object for the given sound name.
            
            :param key: The key identifying a sound object
            **Precondition**:: key is a string.
        """
        del self._data[key]
    
    def __iter__(self):
        """**Returns**: The iterator for this sound dictionary."""
        return self._data.iterkeys()
    
    def iterkeys(self):
        """**Returns**: The key iterator for this sound dictionary."""
        return self._data.iterkeys()


################# VIEW CLASSES #################
pass 
# #mark VIEW CLASSES

class GInput(object):
    """Instances represent an input handler
    
    An input handler receives mouse and keyboard information, and makes it available
    to the user.  To access mouse information, simply access the attribute `touch`.
    To access keyboard information, use the method `is_key_down`.
    
    **You should never construct an object of this class**.  Creating a new instance
    of this class will not properly hook it up to the keyboard and mouse.  Instead, 
    you should only use the one provided in the `input` attribute of `GameApp`. See the 
    class `GameApp` for more information.
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def touch_enabled(self):
        """Whether the touch (mouse) interface is currently enabled.
        
        Setting this value to False will disable all mouse clicks or drags. The value is
        True by default.
        
        **Invariant**: Must be a bool"""
        return self._touch_enabled
    
    @touch_enabled.setter
    def touch_enabled(self,value):
        assert type(value) == bool, 'value %s is not a bool' % `value`
        if value and not self._touch_enabled:
            self._enable_touch()
        elif not value and self._touch_enabled:
            self._disable_touch()
        self._touch_enabled = value
    
    @property
    def keyboard_enabled(self):
        """Whether the keyboard interface is currently enabled.
        
        Setting this value to False will disable all key presses. The value is
        True by default.
        
        **Invariant**: Must be a bool"""
        return self._keyboard_enabled
    
    @keyboard_enabled.setter
    def keyboard_enabled(self,value):
        assert type(value) == bool, 'value %s is not a bool' % `value`
        if value and not self._keyboard_enabled:
            self._enable_keyboard()
        elif not value and self._keyboard_enabled:
            self._disable_keyboard()
        self._keyboard_enabled = value
    
    
    # IMMUTABLE ATTRIBUTES
    @property
    def touch(self):
        """The current (x,y) coordinate of the mouse, if pressed.
        
        This method only returns coordinates if the mouse button is pressed.
        If the mouse button is not pressed it returns None. The origin (0,0)
        corresponds to the bottom left corner of the application window.
        
        There is currently no way to get the location of the mouse when
        the button is not pressed.  This a limitation of Kivy.
        
        **Immutable**: This value cannot be altered.
        
        **Invariant**: Must be either a GPoint or None (if there is no touch)."""
        if self._touch is None:
            return None
        
        return GPoint(self._touch.x/dp(1),self._touch.y/dp(1))
    
    @property
    def key_count(self):
        """The number of keys currently held down.
        
        This attribute is a quick way to check whether the user has pressed any keys.
        
        **Immutable**: This value cannot be altered.
        
        **Invariant**: Must be an int > 0."""
        return self._keycount
        
    @property
    def keys(self):
        """The list of keys that are currently held down.
        
        Using this attribute is much slower than the method `is_key_down`.  You should
        use that method when you want to test a specific key.  This attribute is primarily
        for debugging.
        
        **Immutable**: This value cannot be altered.
        
        **Invariant**: Must be a list of strings (possibly empty)"""
        return tuple(k for (k,v) in self._keystate.iteritems() if v)
    
    
    # BUILT-IN METHODS
    def __init__(self):
        """**Constructor**: Creates a new input handler
        
        This constructor does very little.  It does not hook up the handler to the
        mouse or keyboard.  That functionality happens behind the scenes with hidden
        methods.  You should only use  use the object provided in the `input` attribute 
        of `GameApp`. See the class `GameApp` for more information."""
        self._view  = None
        self._touch = None
        self._keyboard = None
        
        self._touch_enabled = True
        self._keyboard_enabled = True
        
        self._keystate = {}
        self._keycount = 0
    
    
    # PUBLIC METHODS
    def is_key_down(self,key):
        """**Returns**: True if the key is currently held down.
        
            :param key: the key to test
            **Precondition**: Must be a string.
        
        The key is a string describing the key pressed.  For example, to determine 
        whether the right-arrow key is pressed, use the method call 
        `input.is_key_down('right')`.  Similarly the method call
        `input.is_key_down('w')` will indicate whether the W key is pressed.
        
        For a complete list of key names, see the 
        `Kivy documentation <http://kivy.org/docs/_modules/kivy/core/window.html>`_.
        """
        return key in self._keystate and self._keystate[key]
    
    def is_touch_down(self):
        """**Returns**: True if the mouse is currently held down.
        
        If this method returns True, the attribute `touch` is guaranteed to not be
        None."""
        return not self._touch is None
    
    
    # HIDDEN METHODS
    def _register(self,view):
        """Registers the view with this input handler; activating it.
        
            :param view: the view to register.
            **Precondition**: Must be a GView.
        
        The input handler can only have one view at a time.  If there is an active
        view, it will unregister it first before registering the new one.
        """
        self._view = view
        if self.touch_enabled:
            self._enable_touch()
        if self.keyboard_enabled:
            self._enable_keyboard()
    
    def _enable_touch(self):
        """Enables touch events for this input handler"""
        if self._view is None:
            return
        self._view.bind(on_touch_down=self._capture_touch)
        self._view.bind(on_touch_move=self._capture_touch)
        self._view.bind(on_touch_up=self._release_touch)
    
    def _disable_touch(self):
        """Disables touch events for this input handler"""
        if self._view is None:
            return
        self._view.unbind(on_touch_down=self._capture_touch)
        self._view.unbind(on_touch_move=self._capture_touch)
        self._view.unbind(on_touch_up=self._release_touch)
        self._touch = None
    
    def _enable_keyboard(self):
        """Enables keyboard events for this input handler"""
        if self._view is None:
            return
        from kivy.core.window import Window
        self._keyboard = Window.request_keyboard(self._disable_keyboard, self._view, 'text')
        self._keyboard.bind(on_key_down=self._capture_key)
        self._keyboard.bind(on_key_up=self._release_key)
    
    def _disable_keyboard(self):
        """Disables keyboard events for this input handler"""
        if self._view is None:
            return
        self._keyboard.unbind(on_key_down=self._capture_key)
        self._keyboard.unbind(on_key_up=self._release_key)
        self._keyboard = None
        self._keystate = {}
        self._keycount = 0
    
    def _capture_key(self, keyboard, keycode, text, modifiers):
        """Captures a simple keypress and adds it to the key dictionary.
        
            :param keyboard: reference to the keyboard
            **Precondition**: Must be a Keyboard.
        
            :param keycode: the key pressed
            **Precondition**: Must be a pair of an int (keycode) and a string
        
            :param text: the text associated with the key
            **Precondition**: Must be a string
        
            :param modifiers: the modifiers associated with the press
            **Precondition**: Must be a list of key codes
        """
        k = keycode[1]
        # Need to handle the case where a release was dropped
        if not k in self._keystate or not self._keystate[k]:
            self._keycount += 1
        self._keystate[k] = True
        return True
    
    def _release_key(self, keyboard, keycode):
        """Releases a simple keypress and removes it from the key dictionary.
        
            :param keyboard: reference to the keyboard
            **Precondition**: Must be a Keyboard.
        
            :param keycode: the key pressed
            **Precondition**: Must be a pair of an int (keycode) and a string
        """
        self._keystate[keycode[1]] = False
        self._keycount -= 1
        return True
    
    def _capture_touch(self,view,touch):
        """Captures a the current mouse position if button is pressed.
        
            :param view: reference to the view window
            **Precondition**: Must be a GView.
        
            :param touch: the information about the mouse press
            **Precondition**: Must be a TouchEvent
        """
        self._touch = touch
        #self._touch.grab(self)
    
    def _release_touch(self,view,touch):
        """Releases a the current mouse position from memory.
        
            :param view: reference to the view window
            **Precondition**: Must be a GView.
        
            :param touch: the information about the mouse release
            **Precondition**: Must be a TouchEvent
        """
        self._touch = None


class GView(FloatLayout):
    """Instances are a view class for a `GameApp` application.
    
    This is the class that you will use to draw shapes to the screen.  Simply pass your
    `GObject` instances to the `draw` method.  You must do this every animation frame,
    as the game is constantly clearing the window.
    
    **You should never construct an object of this class**.  Creating a new instance
    of this class will not properly display it on the screen.  Instead, you should 
    only use the one provided in the `input` attribute of `GameApp`. See the  class 
    `GameApp` for more information.
    """
    
    
    # BUILT-IN METHODS
    def __init__(self):
        """**Constructor**: Creates a new view for display
        
        This constructor does very little.  It does not hook up the view to the game
        window.  That functionality happens behind the scenes with hidden methods.  
        You should only use use the object provided in the `view` attribute  of 
        `GameApp`. See the class `GameApp` for more information."""
        FloatLayout.__init__(self)
        self._frame = InstructionGroup()
        self.bind(pos=self._reset)
        self.bind(size=self._reset)
        self._reset()
    
    
    # PUBLIC METHODS
    def draw(self,cmd):
        """Draws the given Kivy graphics command to this view.
        
            :param cmd: the command to draw
            **Precondition**: Must be a Kivy graphics command
        
        You should never call this method, since you do not understand raw Kivy graphics
        commands.  Instead, you should use the `draw` method in `GObject` instead."""
        self._frame.add(cmd)
    
    def clear(self):
        """Clears the contents of the view.
        
        This method is called for you automatically at the start of the animation
        frame.  That way, you are not drawing images on top of one another."""
        self._frame.clear()
    
    
    # HIDDEN METHODS
    def _reset(self,obj=None,value=None):
        """Resets the view canvas in response to a resizing event"""
        self.canvas.clear()
        self.canvas.add(Color(1,1,1))
        self.canvas.add(Rectangle(pos=self.pos,size=self.size))
        # Work-around for Retina Macs
        self.canvas.add(Scale(dp(1),dp(1),dp(1)))
        self.canvas.add(self._frame)


################# PRIMARY APP CLASS #################
pass 
# #mark PRIMARY APP CLASS

class GameApp(kivy.app.App):
    """Instances are a controller class for a simple game application.
    
    This is the primary class for creating a game.  To implement a game, you subclass
    this class and override three methods.  The three methods are as follows:
    
    **start**: This method initializes the game state, defining all of the game 
    attributes.  This method is like __init__ except that you should not override that 
    method.  Overriding __init__ will break your game. Hence we have provided build as 
    an alternative.
    
    **update**: This method updates the game state at the start of every animation
    frame.  Any code that moves objects or processes user input (keyboard or mouse)
    goes in this method.
    
    **draw**: This method draws all of the objects to the screen.  The only 
    thing you should have in this method are calls to `self.view.draw()`.
    """
    
    # MUTABLE ATTRIBUTES
    @property
    def fps(self):
        """The number of frames-per-second to animate
        
        By default this value is 60 FPS. However, we cannot guarantee that the FPS is 
        achievable.  If you are having performance stuttering, you might want to drop
        this value to 30 FPS instead.
        
        **Invariant**: Must be an int or float > 0."""
        return self._fps
    
    @fps.setter
    def fps(self,value):
        assert _is_num(value), 'value %s is not a number' % `value`
        assert value > 0, 'value %s is not positive' % `value`
        Clock.unschedule(self._refresh)
        self._fps = value
        Clock.schedule_interval(self._refresh,1.0/self._fps)
    
    
    # IMMUTABLE PROPERTIES
    @property
    def width(self):
        """The window width
        
        **Invariant**: Must be an int or float > 0."""
        return self._gwidth
    
    @property
    def height(self):
        """The window height
        
        **Invariant**: Must be an int or float > 0."""
        return self._gheight
    
    @property
    def view(self):
        """The Game view.
        
        Use the `draw` method  in this attribute to display any `GObject` instance 
        on the screen.  See the class `GView` for more information.
        
        **Invariant**: Must be instance of GView."""
        return self._view
    
    @property
    def input(self):
        """The Game input handler.
        
        Use this attribute to get information about the mouse and keyboard.  See the
        class `GInput` for more information.
        
        **Invariant**: Must be instance of GInput."""
        return self._input
    
    
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """**Constructor**: Creates, but does not start, a new game.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of
        keyword arguments that initialize various attributes. The primary user defined 
        attributes are the window `width` and `height`. For example, to create a game 
        that fits inside of a 400x400 window, the constructor
        
            Game(width=400,height=400)
        
        The game window will not show until you start the game. To start the game, use 
        the method `run()`.
        
        **You will never call the constructor or `run` yourself.  That is handled for 
        you in the provided code."""
        w = keywords['width']  if  'width' in keywords else 0.0
        h = keywords['height'] if 'height' in keywords else 0.0
        f = keywords['fps']    if 'fps'    in keywords else 60.0

        assert _is_num(w), 'width %s is not a number' % `w`
        assert _is_num(h), 'height %s is not a number' % `h`
        assert _is_num(f), 'fps %s is not a number' % `value`
        assert f > 0, 'fps %s is not positive' % `value`

        self._gwidth = w
        self._gheight = h
        self._fps = f
        Config.set('graphics', 'width', str(self.width))
        Config.set('graphics', 'height', str(self.height))
        
        # Tell Kivy to build the application
        kivy.app.App.__init__(self,**keywords)
    
    
    # PUBLIC METHODS
    def build(self):
        """Initializes the graphics window.
        
        This is a Kivy reserved method.  It is part of the Kivy application process.  
        It should **never** be overridden."""
        self._view = GView()
        self._view.size_hint = (1,1)
        self._input = GInput()
        self._input._register(self._view)
        return self.view
    
    def run(self):
        """Displays the game window and start the game.
        
        This is a Kivy reserved method.  It is part of the Kivy application process.  
        It should **never** be overridden."""
        Clock.schedule_once(self._bootstrap,-1)
        kivy.app.App.run(self)
    
    def stop(self):
        """Closes the game window and exit Python.
        
        This is a Kivy reserved method.  It is part of the Kivy application process.  
        It should **never** be overridden."""
        kivy.app.App.stop(self)
        sys.exit(0)
    
    def start(self):
        """Initializes the game state, creating a new game.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running.  You should use
        it to initialize any game specific attributes. **Never overridden
        the built-in method __init__**"""
        pass
    
    def update(self,dt):
        """Updates the state of the game one animation frame.
        
            :param dt: time in seconds since last update
            **Precondition**: a number (int or float)
        
        This method is called 60x a second (depending on the `fps`) to provide on-screen 
        animation. Any code that moves objects or processes user input (keyboard or mouse)
        goes in this method.
        
        Think of this method as the body of the loop.  You will need to add attributes
        that represent the current animation state, so that they can persist across
        animation frames.  These attributes should be initialized in `start`.
        """
        pass
    
    def draw(self):
        """Draws the game objects on the screen.
        
        Every single object that you draw will need to be an attribute of the `GameApp`
        class.  This method should largely be a sequence of calls to `self.view.draw()`.
        """
        pass
    
    
    # HIDDEN METHODS
    def _bootstrap(self,dt):
        """Bootstraps the clock scheduler for the game..
        
        This method is a callback-proxy for method `start`.  It handles important issues 
        behind the scenes, particularly with setting the FPS"""
        Clock.schedule_interval(self._refresh,1.0/self.fps)
        self.start()
    
    def _refresh(self,dt):
        """Processes a single animation frame.
        
            :param dt: time in seconds since last update
            **Precondition**: a number (int or float)
        
        This method a callback-proxy for the methods `update` and `draw`.  It handles
        important issues behind the scenes, particularly with clearing the window."""
        self.view.clear()
        self.update(dt)
        self.draw()
    
    
