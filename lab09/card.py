# card.py
#  L. Lee (LJL2), S. Marschner (SRM2), and W. White (WMW2)
# September 28, 2013
"""Module providing a type for playing cards

Implementation adapted from chapter 18 of the course text, 
_Think Python_, by Allen B. Downey.
"""

SUIT_NAMES = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
NUM_SUITS  = len(SUIT_NAMES)

# Starts at None so that we can treat RANK_NAMES as a translation table:
# RANK_NAME[1] is 'Ace', RANK_NAME[13] is 'King', etc.
RANK_NAMES = [None, 'Ace', '2', '3', '4', '5', '6', '7',
              '8', '9', '10', 'Jack', 'Queen', 'King']
NUM_RANKS  = 13


class Card(object):
    """Represents a standard playing card.
    
    Instance Attributes:
        suit: The suit of this particular card. 
              The name of this suit is given by SUIT_NAMES[suit]. 
              [int, in 0..NUM_SUITS-1]
        rank: The rank of this particular card.  
              The name of this rank is given by RANK_NAMES[rank].  
              [int, in 1..NUM_RANKS]
    
    For example, if we execute c = Card(0, 12), SUIT_NAMES[c.suit] is 'Clubs'
    and RANK_NAMES[c.rank] is '12', and so this card is the Queen of Clubs."""
    
    def __init__(self, s, r):
        """Initializer: A new card with suit encoding s and rank encoding r.
        
        Example: if we execute c = Card(0, 12), then this card is the Queen of
        Clubs, since SUIT_NAMES[c.suit] is 'Clubs' and RANK_NAMES[c.rank] is 12.
        
        Parameter s: The card suit
        Precondition: s in 0..NUM_SUITS-1 (inclusive)
        
        Parameter r: The card rank
        Precondition: r in 1..NUM_RANKS (inclusive)"""
        self.suit = s
        self.rank = r
    
    def __str__(self):
        """Returns a readable string representation of this card.
        Example: '2 of Hearts'"""
        return RANK_NAMES[self.rank] + ' of ' + SUIT_NAMES[self.suit]
    
    def __repr__(self):
        """Returns the unambiguous string representation of this card.
        Example: 'Card(2 of Hearts)'"""
        return 'Card('+str(self)+')'
    
    def __eq__(self, other):
        """Returns true if other is equal to this card
        
        Equality is determined by equality of attributes
        
        Parameter other: The value to compare"""
        return (isinstance(other,Card) and
                (self.suit, self.rank) == (other.suit, other.rank))
    
    def __ne__(self, other):
        """Returns true if other is not equal to this card
        
        Equality is determined by equality of attributes
        
        Parameter other: The value to compare"""
        return not self.__eq__(other)


def full_deck():
    """Returns a list of the standard 52 cards"""
    output = []  # list of cards so far to be returned
    for suit in range(NUM_SUITS):
        for rank in range(1,NUM_RANKS+1):  # skip the None value
            output.append(Card(suit,rank))
    return output


def print_cards(clist):
    """Print cards in list clist.
    
    Parameter clist: The card hand
    Precondition: clist is a list of Cards, possibly empty."""
    for c in clist:
        print str(c)


