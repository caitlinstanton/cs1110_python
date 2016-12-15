# lab06.py
# YOUR NAME AND NETID HERE
# Initial skeleton by Walker White (wmw2)
# THE DATE COMPLETED HERE
"""Module to demonstrate debugging and error handling.

This module contains several functions with bugs in it.  You are to
find and remove the bugs using the techniques that we talked about in
class.  

In addition, you will also add assert statements to this functions to
assert the (somewhat complex) precondition.  These assert statements
will be aided by the latter two functions in this module."""


# PART 1: DEBUGGING
def time_to_military(s):
    """ Returns: the time in 24-hour (military) format.
    
    24-hour format has the form '<hours>:<minutes>'. The hours are between 0 and 23, 
    and are always two digits (so there must be a leading zero).  The minutes are 
    between 0 and 59, and are always 2 digits.
    
    Examples:
        '2:45 PM' becomes '14:45'
        '9:05 AM' becomes '09:05'
        '12:00 AM' becomes '00:00'
    
    Parameter s: string representation of the time
    Precondition: s is a string in 12-format <hours>:<min> AM/PM"""
    # PART 2: Add assert statements here to enforce preconditions

    # Split up the string
    if is_time_format(s) == True:
        pos1 = s.index(':')
        pos2 = s.index(' ')
    
    # Extract hours and minutes
        hour = int(s[:pos1])
        mins = s[pos1+1:pos2]
        suff = s[pos2+1:]
    
    # Adjust hour to be correct.
        if (suff == 'PM') and (hour != 12):
            hour += 12
        elif (suff == "PM") and (hour == 12):
            hour = 12  
        elif (suff == "AM") and (hour == 12):
    	    hour = 0
        else:
            hour = '0'+str(hour)
    
    # Glue it back together
        return str(hour)+':'+mins
    else:
    	return "Invalid time format" 

def time_to_minutes(s):
    """Returns: number of minutes since midnight
    
    Examples:
       '2:45 PM' => 14*60+45 = 885
       '9:05 AM' => 9*60+5 = 545
      '12:00 AM' => 0
    
    Parameter s: string representation of the time
    Precondition: s is a string in 12-format <hours>:<min> AM/PM"""
    # PART 2: Add assert statements here to enforce preconditions
    
    # Find the separators
    pos1 = s.index(':')
    print "pos1 is " + str(pos1)
    pos2 = s.index(' ')
    print "pos2 is " + str(pos2)
    
    # Get hour and convert to int
    hour = s[:pos1]
    hour = int(hour)
    print "hour = " + str(hour)
    
    # Adjust hour to be correct.
    suff = s[pos2+1:]
    print "suff = " + suff
    print "entering if statement"
    if (suff == 'PM'):
    	print "suff == pm"
        hour = hour+12
        print "new hours " + str(hour)
    elif (suff == 'AM' and hour == 12):
        print "suff == am and hour == 12"
        hour = 0
    print "exiting if statement"
    # Get min and convert to int
    mins = s[pos1+1:pos2]
    mins = int(mins)
    print "mins = " + str(mins)

    return hour*60+mins

# PART 2: ASSERT HELPER
def is_time_format(s):
    """Returns: True if s is a string in 12-format <hours>:<min> AM/PM
    
    Example: 
        is_time_format('2:45 PM') returns True
        is_time_format('2:45PM') returns False
        is_time_format('14:45') returns False
        is_time_format('14:45 AM') returns False
        is_time_format(245) returns False
    
    Parameter s: the candidate time to format
    Precondition: NONE (s can be any value)"""
    # HINT: Your function must be prepared to do something if s is a string.
    # Even if s is a string, the first number before the colon may be one
    # or two digits.  You must be prepared for either.
    # You might find the method s.isdigit() to be useful.
    pos1 = s.find(':')
    pos2 = s.find(' ')
    hours = s[:pos1]
    mins = s[pos1+1:pos2]
    suff = s[pos2+1:]
    if s:
    	if (pos1 == 1) or (pos1 == 2):
    		if (pos2 == 4) or (pos2 == 5):
        		if (hours.isdigit()) and (mins.isdigit()) and (suff.isalpha()):
    				if (int(hours) <= 12) and (int(mins) <= 59) and ((suff == 'AM') or (suff == 'PM')):
    					return True
    				else:
    					return False
    			else:
    				return False
    		else:
    			return False
    	else:
    		return False
    else:
    	return False

# PART 3: TRY-EXCEPT
def something_to_military(s):
    """Returns: the time in 24-hour (military) format if appropriate.
    
    The function is the same as time_to_military if s satisfies the
    precondition for that function.  If s does not satisfy the precondition
    then this function returns 'Invalid time format'
    
    Examples: 
        something_to_military('2:45 PM') returns '14:45'
        something_to_military('9:05 AM') returns '09:05'
        something_to_military('12:00 AM') returns '00:00'
        something_to_military(905) returns 'Invalid time format'
        something_to_military('abc') returns 'Invalid time format'
        something_to_military('9:05') returns 'Invalid time format'
    
    Parameter s: the candidate time to format
    Precondition: NONE (s can be any value)"""
    # You are not allowed to use 'if' in this definition. Use try-except instead.
    # Hint: You have to complete PART 2 before you complete this part.
    try:
    	result = time_to_military(s)
    	return result
    except:
    	return "Invalid time format"