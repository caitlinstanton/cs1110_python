# play.py
# Caitlin Stanton (cs968), Andrew Denkewicz (ajd248)
# 12/06/2016
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _num_lives  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        _points     [int, greater than 0]
                    number of points player earns by breaking bricks
        _latest_powerup
                    [string]
                    message to be displayed to explain what powerup player unlocked
                    by breaking that Brick
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getBricks(self):
        """Function to return the list of Bricks left (_bricks)
        """
        return self._bricks

    def setBricks(self, thelist):
        """Function to update the list of Bricks left

            thelist: new list to set _bricks equal to
            Precondition: thelist is a list of Brick objects
        """
        assert len(thelist) >= 0
        for i in thelist:
            assert isinstance(i,Brick)
        self._bricks = thelist

    def getPaddle(self):
        """Function to return _paddle
        """
        return self._paddle

    def setPaddle(self,paddle):
        """Function to update _paddle

            paddle: new Paddle to set _paddle equal to
            Precondition: paddle is a Paddle object
        """
        assert isinstance(paddle,Paddle)
        self._paddle = paddle

    def getBall(self):
        """Function to return _ball
        """
        return self._ball

    def setBall(self,ball):
        """Function to update _ball

            ball: new Ball to set _ball equal to
            Precondition: ball is a Ball object
        """
        assert isinstance(ball, Ball)
        self._ball = ball

    def getPoints(self):
        """Function to return _points earned by the player
        """
        return self._points

    def setPoints(self,value):
        """Function to update _points and add a value to them

            value: number of points to update the _points attribute to
            Precondition: value is an int
        """
        assert type(value) == int
        self._points = value

    def getLives(self):
        """Function to return the number of turns a player has left (_num_lives)
        """
        return self._num_lives

    def setLives(self,value):
        """Function to update the number of lives left (_num_lives)

            value: number of lives that the player now has
            Precondition: value is an int
        """
        assert type(value) == int
        self._num_lives = value

    def getLatestPowerup(self):
        """Function to return the string in the _latest_powerup attribute
        """
        return self._latest_powerup

    def setLatestPowerup(self,value):
        """Function to set _latest_powerup to a new message

            value: new message based on latest powerup unlocked from breaking
                    a new Brick
            Precondition: value is a string or an empty string
        """
        assert len(value) >= 0
        self._latest_powerup = value

    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS

    def __init__(self):
        """Constructor for the game

            Create the paddle and bricks for the game with all relevant factors,
            and adds them to the _paddle and _bricks attributes

            Sets _num_lives and _points for a new game (at NUMBER_TURNS and
            0, respectively)
        """
        self._ball = None
        self._num_lives = NUMBER_TURNS
        self._points = 0
        self._latest_powerup = "No powerups used"
        thelist = []
        row_height = BRICK_HEIGHT + BRICK_SEP_V
        row_width = BRICK_WIDTH + BRICK_SEP_H
        color_block = BRICK_ROWS / 5
        color_block_height = row_height * color_block
        for y in range(BRICK_ROWS):
            bottom = GAME_HEIGHT - BRICK_Y_OFFSET - row_height * (y+1)
            if bottom >= GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 1:
                color = colormodel.RED
            elif (bottom < GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 1 
                and bottom >= GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 2):
                color = colormodel.ORANGE
            elif (bottom < GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 2 
                and bottom >= GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 3):
                color = colormodel.YELLOW
            elif (bottom < GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 3
                and bottom >= GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 4):
                color = colormodel.GREEN
            elif (bottom < GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 4 
                and bottom >= GAME_HEIGHT - BRICK_Y_OFFSET - color_block_height * 5):
                color = colormodel.CYAN
            else:
                color = colormodel.MAGENTA
            for x in range(BRICKS_IN_ROW):
                xval = (2*x+1)*(row_width/2)
                new_brick = Brick(xval,bottom,color)
                thelist.append(new_brick)
        self.setBricks(thelist)
        paddle = Paddle()
        self.setPaddle(paddle)

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    
    def updatePaddle(self,inputval):
        """Function to update the position of the Paddle

            Checks what key was pressed and moves the paddle accordingly, 
            within the boundaries of the screen

            inputval: user input (keys pressed)
            Precondition: instance of GInput
        """
        assert isinstance(inputval,GInput)
        x_step = 0
        if inputval.is_key_down('left'):
            x_step = x_step - 3
        if inputval.is_key_down('right'):
            x_step = x_step + 3
        new_paddle_x = self._paddle.x + x_step
        if new_paddle_x >= (self._paddle.getWidth()/2) and new_paddle_x <= GAME_WIDTH - (self._paddle.getWidth()/2):
            self._paddle.x = new_paddle_x

    def serveBall(self,view,vxVal):
        """Function to create a Ball object, set it to the _ball attribute
            and draw the Ball

            view: game view
            Precondition: instance of GView

            vxVal: value for the x velocity of the Ball
            Precondition: vxVal is an int or float
        """
        assert isinstance(view,GView)
        assert type(vxVal) == int or type(vxVal) == float
        ball = Ball(BALL_X_START,BALL_Y_START,vxVal)
        self.setBall(ball)
        self.getBall().draw(view)

    def updateBall(self,view):
        """Function to handle the bouncing of the ball off the walls of the game

            Check to see where the ball's position is in relation to the walls
            of the game and, based on that, negates the x or y velocity of the 
            ball to simulate a bounce

            view: game view
            Precondition: instance of GView
        """
        assert isinstance(view,GView)
        self.getBall().updateBall()
        if self.getBall().getYPosition() >= GAME_HEIGHT and self.getBall().getVY() > 0:
            self.getBall().setVY(self.getBall().getVY() * -1)
        if self.getBall().getXPosition() <= 0 and self.getBall().getVX() < 0:
            self.getBall().setVX(self.getBall().getVX() * -1)
        if self.getBall().getXPosition() >= GAME_WIDTH and self.getBall().getVX() > 0:
            self.getBall().setVX(self.getBall().getVX() * -1)
        self.getBall().draw(view)

    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS

    def draw(self,view,inputval):
        """Function to draw the bricks and paddle for the game

            Runs through all of the items in _bricks and _paddle, checks for any
            collisions, updates the item accordingly, and draws the item
        
            view: game view
            Precondition: instance of GView

            inputval: user input (keys pressed)
            Precondition: instance of GInput
        """
        assert isinstance(inputval,GInput)
        assert isinstance(view,GView)
        for b in self.getBricks():
            self.handle_collisions(b)
            b.draw(view)
        if self.getPaddle() != None:
            self.handle_collisions(self.getPaddle())
            self.updatePaddle(inputval)
            self.getPaddle().draw(view)

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    def handle_collisions(self,object_used):
        """Function to update a Brick or Paddle in the case of collision with
            the ball

            Checks to see if the object in question collided with the Ball

            If it did and the object is a Brick, it removes it from _bricks, 
            adds points to the player's score, checks for any powerups in the 
            Brick, and negates the Ball's y velocity

            If it did and the object is a Paddle, it will only negate the Ball's
            y velocity if the Ball already has a negative y velocity (is moving 
            down)

            object_used: item to check to see if the Ball collided with it and
                            to update the item's attributes
            Precondition: object_used is an instance of Brick or Paddle
        """
        assert isinstance(object_used,Brick) or isinstance(object_used,Paddle)
        if self.getBall() != None:
            if object_used.collides(self.getBall()):
                if isinstance(object_used,Brick):
                    self._bricks.remove(object_used)
                    self.getBall().setVY(self.getBall().getVY()*-1)
                    self.add_points()
                    self.checkPowerups(object_used)
                if isinstance(object_used,Paddle):
                    if self.getBall().getVY() < 0:
                        self.getBall().setVY(self.getBall().getVY()*-1)
        

    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE

    def checkPowerups(self,object_used):
        """Function to check powerup unlocked for a Brick

            Looks at _powerups attribute for the Brick and calls the functions
            accordingly
            - 1 --> Paddle length is doubled [changeLength() called]
            - 2 --> Paddle length is cut in half [changeLength() called]
            - 3 --> Ball x-velocity is doubled [changeVelocity() called]
            - 4 --> Ball x-velocity is cut in half [changeVelocity() called]
            - 5 --> Topmost row of Bricks is removed [remove_row() called]

            Updates _latest_powerup message with appropriate message
        """
        if object_used.getPowerups() == 1:
            self.getPaddle().changeLength(2)
            self.setLatestPowerup("Paddle length multipled by 2")
        elif object_used.getPowerups() == 2:
            self.getPaddle().changeLength(0.5)
            self.setLatestPowerup("Paddle length multipled by 0.5")
        elif object_used.getPowerups() == 3:
            self.getBall().changeVelocity(2)
            self.setLatestPowerup("Ball velocity multipled by 2")
        elif object_used.getPowerups() == 4:
            self.getBall().changeVelocity(0.5)
            self.setLatestPowerup("Ball velocity multipled by 0.5")
        elif object_used.getPowerups() == 5:
            self.remove_row()
            self.setLatestPowerup("Row of bricks removed")
        else:
            self.setLatestPowerup("No powerups used")

    def remove_row(self):
        """Function to remove row of bricks

            Iterates through _bricks and removes the first amount of BRICKS_IN_ROW

            Adds points to _points based on the number of bricks removed
        """
        self._bricks = self._bricks[BRICKS_IN_ROW:]
        for i in range(BRICKS_IN_ROW):
            self.add_points()

    def clearScreen(self):
        """Function to clear the screen of all _bricks, _paddle, and _ball
        """
        self._bricks = []
        self._paddle = None
        self._ball = None

    def lostLife(self):
        """Function to check if player lost a life

            Checks y position and y velocity of the Ball

            Returns if the y position is equal to or less than 0 and the 
            y velocity is negative (ball is moving down)
        """
        return self.getBall().getYPosition() <= 0 and self.getBall().getVY() <= 0
    
    def decreaseLives(self):
        """Function to decrease _num_lives by 1
        """
        self.setLives(self.getLives()-1)

    def bricksLeft(self):
        """Function to check if there are items left in _bricks

            Returns boolean of whether or not _bricks is empty
        """
        return len(self.getBricks()) == 0

    def add_points(self):
        """Function to add more points to _points

            Adds 5 per brick broken
        """
        self.setPoints(self.getPoints()+5)
