# lab09.py
# YOUR NAME(S) AND NETID(S) HERE
# initial skeleton by L. Lee (LJL2), S. Marschner (SRM2), and W. White (WMW2)
# September 28, 2013

"""Module for a very simple approximation of the game Blackjack"""
import card
import random


class Blackjack(object):
    """Represents the state of a game of blackjack with one player.
    
    Instance Attributes:
        playerHand: list of the Cards held by the player       [list of Cards]
        dealerHand: list of the Cards held by the dealer       [list of Cards]
        deck:       list of the remaining Cards to draw from   [list of Cards]
        
    The deck attribute is assumed to hold enough Cards for the game 
    to be able to run to completion (i.e. the deck wil not run out 
    of cards for the player or dealer to draw)."""
    
    def __init__(self,deck):
        """Initializer: a new blackjack game with the two hands initialized.
        
        The player's hand playerHand will be the first two cards in deck.
        The dealer's hand dealerHand will be the third card in deck.  
        These three cards are removed from deck.
        
        Deck is a parameter because we allow the caller, such as a casino, 
        to "stack the deck" (choose the arrangement of the cards, insert 
        extra cards,etc.) to its advantage!
        
        Parameter deck: The deck of cards to play wiht
        Precondition: deck is a list of Card.  It contains at least
        three Cards (more is preferable)."""
        # ASSERT THE PRECONDITIONS (BEST YOU CAN)
        self.playerHand = deck[0:2]
        self.dealerHand = deck[2]
        self.deck = deck[3:]
    
    def __str__(self):
        """Returns: the string <player's score>, <dealer's score>
    
        Here, we are assuming that all that matters is the score 
        (which is True if aces are always 11).
    
        Example output:
            player: 12; dealer: 20
        """
        pass  # TODO: implement me, according to my spec
    
    def dealerScore(self):
        """Returns: score for the dealer."""
        s = 0  # score to return
        for c in self.dealerHand:
            if c.rank >= 11:  # c is a face card
                s = s + 10
            elif c.rank == 1:  # c is an ace
                s = s + 11
            else:
                s = s + c.rank
        return s
    
    def playerScore(self):
        """Returns: score for the player."""
        pass  # TODO: implement me, according to my spec
    
    def playerBust(self):
        """Returns: True if player has gone bust (score is over 21),
        and False otherwise"""
        pass  # TODO: implement me, according to my spec
    
    def dealerBust(self):
        """Returns: True if dealer has gone bust (score is over 21),
        and False otherwise"""
        pass  # TODO: implement me, according to my spec
    
    # HELPER METHOD (DO NOT MODIFY)
    def _score(self, clist):
        """Returns: simplified-blackjack score for clist
        
        Helper method for computing the score of a given hand. 
        In our version of blackjack, aces always count as 11 points.  
        Face cards count as 10 points and Suits do not matter.
        
        Example: input: [2 of Hearts, Ace of spades], output: 13
        Example: input: [King of Diamonds, 3 of Clubs], output 13
        
        Parameter clist: The current hand
        Precondition: clist is a list of Cards"""
        s = 0  # score to return
        for c in clist:
            if c.rank >= 11:  # c is a face card
                s = s + 10
            elif c.rank == 1:  # c is an ace
                s = s + 11
            else:
                s = s + c.rank
        return s        


# DO NOT MODIFY BELOW THIS LINE

def play_a_game():
    """Create and play a new blackjack game.
    
    This function provides a text based interface for blackjack.
    It will continue to run until the end of the game."""
    
    # Create a new shuffled full deck
    deck = card.full_deck()
    random.shuffle(deck)
    
    # Start a new game. Player gets two cards; dealer gets one
    game = Blackjack(deck)
    
    # Tell player the scoring rules
    print 'Welcome to CS 1110 Blackjack.'
    print 'Rules: Face cards are 10 points. Aces are 11 points.'
    print '       All other cards are at face value.'
    print # Blank line
    
    # Show initial deal
    print 'Your hand: '
    card.print_cards(game.playerHand)
    print # Blank line
    print 'Dealer\'s hand: '
    card.print_cards(game.dealerHand)
    print # Blank line
    
    # While player has not bust, ask if player wants to draw
    player_halted = False  # True player wants to halt, False otherwise
    while not game.playerBust() and not player_halted:
        # ri: input received from player
        ri = _prompt_player('Type h for new card, s to stop: ',['h', 's'])
        
        player_halted = (ri == 's')
        if (not player_halted):
            game.playerHand.append(game.deck.pop(0))
            print "You drew the " + str(game.playerHand[-1])
            print
    
    if game.playerBust():
        print "You went bust, dealer wins."
    else:
        _dealer_turn(game)
    
    print
    print "The final scores were " + str(game)


def _prompt_player(prompt,valid):
    """Returns: the choice of a player from a given prompt.
    
    This is a a helper function for play_a_game().  It asks
    the user a question, and waits for a response.  It checks
    if the response is valid against a list of acceptable 
    answers.  If it is not valid, it asks the question again.
    Otherwise, it returns the player's answer.
    
    This function has been factored out of play_a_game() to
    show good design.  Otherwise, play_a_game() is a long
    and unreadable function.
    
    Parameter prompt: The prompt to ask for a response
    Precondition: prompt is a string
    
    Parameter valid: The valid inputs
    Precondition: valid is a list of strings"""
    # Ask the question for the first time.
    # ri: input received from player
    ri = raw_input(prompt)
    
    # Continue to ask while the response is not valid.
    while not (ri in valid):
        print 'Invalid response.  Answer must be one of '+str(valid)
        print # Blank line
        ri = raw_input(prompt)
    
    return ri


def _dealer_turn(game):
    """Performs the dealer's turn, printing out the result.
    
    The function uses standard BlackJack rules: the dealer
    stands above 17, but hits otherwise.
    
    This function has been factored out of play_a_game() to
    show good design.  Otherwise, play_a_game() is a long
    and unreadable function.
    
    Parameter game: The black jack game
    Precondition: game is a Blackjack object
    """
    # Dealer draws until at 17 or above or goes bust
    while game.dealerScore() < 17 and not game.dealerBust():
        game.dealerHand.append(game.deck.pop(0))
        print "Dealer drew the " + str(game.dealerHand[-1])
     
    print # Blank line
    if (game.dealerBust()):
        print "Dealer went bust, you win!"
    elif (game.dealerScore() > game.playerScore()):
        print "Dealer outscored you, dealer wins."
    elif (game.dealerScore() < game.playerScore()):
        print "You outscored dealer, you win!"
    else:
        print "The game was a tie."


# Script code
if __name__ == '__main__':
    play_a_game()


