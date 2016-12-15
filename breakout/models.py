# models.py
# Caitlin Stanton (cs968), Andrew Denkewicz (ajd248)
# 12/06/2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getWidth(self):
        """Function to return the width of the paddle
        """
        return self.width

    def setWidth(self,value):
        """Function to set the width of the paddle

            value: new width of the paddle
            Precondition: value is an int or float greater than zero
        """
        assert (type(value) == int or type(value) == float) and value > 0
        self.width = value

    def getX(self):
        """Function to return the x value of the center of the paddle
        """
        return self.x

    def setX(self,value):
        """Function to set the x value of the center of the paddle

            value: new x value of the paddle
            Precondition: value is an int or float greater than or equal to zero
        """
        assert (type(value) == int or type(value) == float) and value >= 0
        self.x = value

    # INITIALIZER TO CREATE A NEW PADDLE

    def __init__(self):
        """**Constructor**: creates a new Paddle object, which is an extension
                            of the GRectangle class
        
            All values (x,y,width,height,color) are defined within constants.py,
            meaning no parameters are needed       
        """
        GRectangle.__init__(self)
        self.x=GAME_WIDTH/2
        self.y=PADDLE_OFFSET
        self.width=PADDLE_WIDTH
        self.height=PADDLE_HEIGHT
        self.fillcolor=colormodel.BLACK
        self.linecolor=colormodel.BLACK
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS

    def collides(self,ball):
        """Returns: True if the ball collides with the paddle

            Parameter ball: The ball to check
            Precondition: ball is of class Ball
        """
        assert isinstance(ball,Ball)
        ballX = ball.getXPosition()
        ballY = ball.getYPosition()
        r = ball.getRadius()
        return self.contains(ballX-r,ballY+r) or self.contains(ballX+r,ballY+r) or self.contains(ballX-r,ballY-r) or self.contains(ballX+r,ballY-r)
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    def changeLength(self,multiplier):
        """Function to change the length of a Paddle object by a specific
                multiplier

            multiplier: value that the length of the Paddle will be changed by
            Precondition: multiplier is an int or float not equal to 0
        """
        assert (type(multiplier) == int or type(multiplier) == float)
        assert multiplier != 0
        new_width = self.getWidth() * multiplier
        if new_width <= GAME_WIDTH/2:
            self.setX(GAME_WIDTH/2)
            self.setWidth(new_width)


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        

    _powerups   [int, random value between 0 and 5]
                represents the type of special attribute a Brick has

    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getPowerups(self):
        """Function to return the value of _powerups for a Brick
        """
        return self._powerups
    
    # INITIALIZER TO CREATE A BRICK

    def __init__(self,x,bottom,fillcolor):
        """**Constructor**: creates a new Brick object, which is an extension
                            of the GRectangle class
        
            :param x: initial x value of the center of the Brick
            **Precondition**: value is an int or float between 0 and GAME_WIDTH
        
            :param bottom: initial y value of the bottom of the Brick
            **Precondition**: value is an int or float between 0 and GAME_HEIGHT

            :param fillcolor: colormodel color for the Brick
            **Precondition**: valid value for colormodel      
        """
        assert (type(x) == int or type(x) == float)
        assert (x >= 0 and x <= GAME_WIDTH)
        assert (type(bottom) == int or type(bottom) == float)
        assert (bottom >= 0 and bottom <= GAME_HEIGHT)
        GRectangle.__init__(self)
        self.left=x
        self.bottom=bottom
        self.width=BRICK_WIDTH
        self.height=BRICK_HEIGHT
        temp = random.randint(0, 10)
        if temp < 9:
            self.fillcolor = fillcolor
            self._powerups = 0
        else:
            self.fillcolor = colormodel.BLACK
            self._powerups = random.randint(1,5)
        self.linecolor=fillcolor
    
    # METHOD TO CHECK FOR COLLISION

    def collides(self,ball):
        """Returns: True if the ball collides with this brick

            Parameter ball: The ball to check
            Precondition: ball is of class Ball
        """
        assert isinstance(ball,Ball)
        ballX = ball.getXPosition()
        ballY = ball.getYPosition()
        r = ball.getRadius()
        return (self.contains(ballX-r,ballY+r) or self.contains(ballX+r,ballY+r) 
            or self.contains(ballX-r,ballY-r) or self.contains(ballX+r,ballY-r))

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getVX(self):
        """Function to return the value of _vx for a Ball
        """
        return self._vx

    def getVY(self):
        """Function to return the value of _vy for a Ball
        """
        return self._vy

    def setVX(self,value):
        """Function to set the value of _vx for a Ball

            value: new _vx value
            Precondition: value is an int or float
        """
        assert type(value) == int or type(value) == float
        self._vx = value

    def setVY(self,value):
        """Function to set the value of _vy for a Ball

            value: new _vy value
            Precondition: value is an int or float
        """
        assert type(value) == int or type(value) == float
        self._vy = value

    def getXPosition(self):
        """Function to return the value of x for a Ball
        """
        return self.x

    def getYPosition(self):
        """Function to return the value of y for a Ball
        """
        return self.y
    
    def getRadius(self):
        """Function to return the value of radius for a Ball
        """
        return self.width

    # INITIALIZER TO SET RANDOM VELOCITY

    def __init__(self,x,y,vxVal):
        """**Constructor**: creates a new Ball object, which is an extension
                            of the GEllipse class
        
            :param x: initial x value of the center of the Ball
            **Precondition**: value is an int or float between 0 and GAME_WIDTH
        
            :param y: initial y value of the center of the Ball
            **Precondition**: value is an int or float between 0 and GAME_HEIGHT

            :param vxVal: value for the x velocity (_vx) of the Ball
            **Precondition**: value is an int or float   
        """
        assert (type(x) == int or type(x) == float)
        assert (x >= 0 and x <= GAME_WIDTH)
        assert (type(y) == int or type(y) == float)
        assert (y >= 0 and y <= GAME_HEIGHT)
        assert (type(vxVal) == int or type(vxVal) == float)
        GEllipse.__init__(self)
        self.x=x
        self.y=y
        self.width=BALL_RADIUS
        self.height=BALL_RADIUS
        self.fillcolor=colormodel.BLACK
        self._vx = vxVal #random.uniform(2.5,3.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -3.0
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    
    def updateBall(self):
        """Function to update the position of the Ball based on its _vx and _vy
            
            Adds the values of _vx and _vy to the Ball's current 
            x and y position
        """
        self.x = self.x+self._vx
        self.y=self.y+self._vy

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    def changeVelocity(self,multiplier):
        """Function to change the x velocity (_vx) of a Ball object by a specific
                multiplier

            multiplier: value that the x velocity of the Ball will be changed by
            Precondition: multiplier is an int or float not equal to 0
        """
        assert (type(multiplier) == int or type(multiplier) == float)
        assert multiplier != 0
        self.setVX(self.getVX() * multiplier)


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE