# lab05.py
# Walker M. White (wmw2)
# September 21, 2014
"""Module for implementing Lab 05 functions.

This module is broken up into to parts.  The first part contains two functions: 
first_vowel and pigify. The first is a helper function of the second (which is the 
primary function). The second function, pigify, convert English words to Pig-Latin. 
You are to IMPLEMENT the second function.

The second part uses the Time class provided by the module time.  It contains a single 
function: add_time.  You are to implement this function as well.

While you are encouraged to test your answers, you do not need to write  a unit test.  
Simply demonstrate your functions to you instructor to get get credit"""
import timeclass


# PART 1: Pig Latin

def first_vowel(w):
    """Returns: position of the first vowel; -1 if no vowels.
    
    There is a better way to do this function with for-loops, 
    but we have not covered that topic yet.
    
    Parameter w: the word to search
    Precondition: w is a nonempty string with only lowercase letters"""
    minpos = len(w) # invalid position; currently no vowels found
    
    # search for a
    pos = w.find('a')
    if pos != -1 and pos < minpos: # a found and is closest
        minpos = pos
    
    # search for e
    pos = w.find('e')
    if pos != -1 and pos < minpos: # e found and is closest
        minpos = pos
    
    # search for i
    pos = w.find('i')
    if pos != -1 and pos < minpos: # i found and is closest
        minpos = pos
    
    # search for o
    pos = w.find('o')
    if pos != -1 and pos < minpos: # o found and is closest
        minpos = pos
    
    # search for u
    pos = w.find('u')
    if pos != -1 and pos < minpos: # u found and is closest
        minpos = pos
    
    # search for y not at front
    backpos = w[1:].find('y')
    if backpos != -1: # y found in "back part"
        pos = backpos + 1; # position of y in w
        if pos < minpos: # y found in w and is closest
            minpos = pos
    
    # found something if minpos moved from first assignment
    return minpos if minpos != len(w) else -1


def pigify(w):
    """Returns: copy of w converted to Pig Latin
    
    See the lab handout for the complete rules on Pig Latin.
    
    Parameter w: the word to change to Pig Latin
    Precondition: w is a nonempty string with only lowercase letters"""
    if first_vowel(w) != 0:
    	first = w[0]
    	temp = w[1:]
    	return temp+first+'ay'
    else:
    	return w+'hay'



# PART 2: Time

def add_time(time1, time2):
    """Returns: The sum of time1 and time2 as a new Time object
    
    Example: Sum of 1hr 59min and 1hr 2min is 3hr 1min 
    DO NOT ALTER time1 or time2, even though they are mutable
    
    Parameter time1: the starting time
    Precondition: time1 is a Time object
    
    Parameter time2: the time to add
    Precondition: time2 is a Time object"""
    minutes=time1.minutes + time2.minutes
    hours=time1.hours + time2.hours

    hrs_fromminutes=minutes/60
    mins_fromminutes=minutes%60

    temp=timeclass.Time(hours+hrs_fromminutes,mins_fromminutes)
    return temp