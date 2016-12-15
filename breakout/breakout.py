# breakout.py
# Caitlin Stanton (cs968), Andrew Denkewicz (ajd248)
# 12/06/2016
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

        _num_turns  [int, initially set to NUMBER_TURNS, between 0 and NUMBER_TURNS]
                    number of turns (balls) left for the game
        _frames     [int, greater than 0]
                    number of times game updates, increases by one every time update() is completed
        _was_key_pressed    
                    [boolean]
                    True if key was pressed and added to _input in last frame, False otherwise
        _level      [int, between 1 and 3]
                    represents the level of the game (1-EASY, 2-MEDIUM, 3-HARD)
    """
    
    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME
        self._state = STATE_INACTIVE
        self._game = None
        self._frames = 0
        self._was_key_pressed = False
        if self._state == STATE_INACTIVE:
            message = "Welcome to Breakout!\nThis is an updated version,\nwhere black bricks are powerups\n\nUse the left and right arrows\nto control the paddle\n\nTo select a level, press:\n1 for EASY\n2 for MEDIUM\n3 for HARD\nor 0 to select a random level"
        self._mssg = GLabel(x=240, y=310, text=message, font_size=18, font_name="ArialBold",halign='center', valign='middle')
        self._mssg.draw(self.view)
        
    
    #Written with guidance from Shivansh Gupta and Professor White's sample code
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        curr_keys = self.input.key_count
        
        # Only change if we have just pressed the keys this animation frame
        self._was_key_pressed = curr_keys > 0
        temp = self._state
        if temp == STATE_INACTIVE:
            self._state_inactive()
        elif temp == STATE_NEWGAME:
            self._state_newgame()
        elif temp == STATE_COUNTDOWN:
            self._state_countdown()
        elif temp == STATE_PAUSED:
            self._state_paused()
        elif temp == STATE_ACTIVE:
            self._state_active()
        elif temp == STATE_GAMEOVER:
            self._state_gameover()
        elif temp == STATE_WON:
            self._state_won()

    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        # IMPLEMENT ME
        if self._mssg != None:
            self._mssg.draw(self.view)
        if self._game != None:
            self._game.draw(self.view,self.input)
    
    
    # HELPER METHODS FOR THE STATES GO HERE

    #Written with guidance from Shivansh Gupta
    def _state_newgame(self):
        """Function to change _state to STATE_COUNTDOWN
            Occurs once key is pressed after game is first started
            and _state is STATE_NEWGAME
        """
        self._state = STATE_COUNTDOWN
        self._game = Play()

    #Written with guidance from Shivansh Gupta
    def _state_inactive(self):
        """Function to change _state to STATE_NEWGAME
            Occurs if no key was pressed in the last frame (STATE_INACTIVE)
            but player pressed a key to start game

            Checks key pressed to select specific level for the game
        """
        curr_keys = self.input.key_count
        if curr_keys > 0 and self._was_key_pressed:
            if self.input.is_key_down('1'):
                self._level = 1
                self._state = STATE_NEWGAME
                self._mssg = None
                self._was_key_pressed = False 
            elif self.input.is_key_down('2'):
                self._level = 2
                self._state = STATE_NEWGAME
                self._mssg = None
                self._was_key_pressed = False 
            elif self.input.is_key_down('3'):
                self._level = 3
                self._state = STATE_NEWGAME
                self._mssg = None
                self._was_key_pressed = False 
            elif self.input.is_key_down('0'):
                self._level = random.randint(1,3)
                self._state = STATE_NEWGAME
                self._mssg = None
                self._was_key_pressed = False 

    #Written with guidance from Shivansh Gupta
    def _state_countdown(self):
        """Function to change _state to STATE_ACTIVE
            Occurs after spending 3 seconds in STATE_COUNTDOWN
            Equal to 180 frames of update(), since it runs 60 times/sec
        """
        self._game.getPaddle().setX(GAME_WIDTH/2)
        self._frames += 1
        count = "Game starts in \n " + str((self._frames/60)+1)
        self._mssg = GLabel(x=240, y=300, text=count, font_size=16, font_name="Zapfino",halign='center', valign='middle')
        if self._frames >= 179:
            self._game.serveBall(self.view,self._level*3.0)
            self._state = STATE_ACTIVE
            self._frames = 0

    #Written with guidance from Shivansh Gupta
    def _state_active(self):
        """Function to change _state to STATE_PAUSED
            Occurs if _state was STATE_ACTIVE but ball went past paddle
            and there are still turns left

           OR

           Function to change _state to STATE_GAMEOVER
            Occurs if _state was STATE_ACTIVE but ball went past paddle
            and there are no turns left

           OR

           Function to set _state to STATE_WON
            Occurs when _state was STATE_ACTIVE and there are no bricks left
        """
        lives_left = str(self._game.getLives())
        points_won = str(self._game.getPoints())
        powerups = str(self._game.getLatestPowerup())
        message = "Lives Left: " + lives_left + "\nPoints Scored: " + points_won + "\n" + powerups
        self._mssg = GLabel(x=100, y=575, text=message, font_size=14, font_name="Arial",halign='left')
        self._game.updatePaddle(self.input)
        self._game.updateBall(self.view)
        self._was_key_pressed = True
        if self._game.bricksLeft():
            self._state = STATE_WON
        if self._game.lostLife():
            if self._game.getLives() > 0 and self._game.getLives() <= 3:
                self._state = STATE_PAUSED
                self._game.decreaseLives()
            if self._game.getLives() <= 0:
                self._state = STATE_GAMEOVER
                self._num_lives = 3

    #Written with guidance from Shivansh Gupta
    def _state_paused(self):
        """Function to set _state to STATE_COUNTDOWN
            Occurs when _state was STATE_NEWGAME in the last frame
        """
        self._mssg = GLabel(x=240, y=310, text="Press 0 to use your next turn", font_size=20, font_name="TimesBoldItalic",halign='center', valign='middle')
        if self.input.key_count > 0 and self._was_key_pressed and self.input.is_key_down('0'):
            self._frames = 0
            self._state =STATE_COUNTDOWN
            self._mssg = None
            self._game.getPaddle().setWidth(PADDLE_WIDTH)
            self._was_key_pressed = False

    def _state_gameover(self):
        """Function to set _state to STATE_NEWGAME
            Occurs when _state was STATE_GAMEOVER and key was
            pressed to start another game

            Calls _state_inactive() function so that, if player wants to play
            new game, it can check the input accordingly
        """
        self._game.clearScreen()
        message = "Whoops! \n You've lost \n Your score was: " + str(self._game.getPoints()) + " \n\nTo play again and select a level, press:\n1 for EASY\n2 for MEDIUM\n3 for HARD\nor 0 to select a random level"
        self._mssg = GLabel(x=240, y=310, text=message, font_size=24, font_name="ArialBold",halign='center', valign='middle')
        self._was_key_pressed = True
        self._state_inactive()


    def _state_won(self):
        """Function to set _state to STATE_NEWGAME
            Occurs when _state was STATE_WON and key was
            pressed to start another game

            Calls _state_inactive() function so that, if player wants to play
            new game, it can check the input accordingly
        """
        self._game.clearScreen()
        message = "Congratulations!\nYou've won!\nYour score was: " + str(self._game.getPoints()) + " \n\nTo play again and select a level, press:\n1 for EASY\n2 for MEDIUM\n3 for HARD\nor 0 to select a random level"
        self._mssg = GLabel(x=240, y=310, text=message, font_size=24, font_name="ArialBold",halign='center', valign='middle')
        curr_keys = self.input.key_count
        self._state_inactive()