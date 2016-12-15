# lab03.py
# Caitlin Stanton, cs968
# September 6, 2016

def first_inside_quotes(s):
    """Returns: The first substring of s between two (double) quote characters
    A quote character is one that is inside a string, not one that delimits it.
    We typically use single quotes (') to delimit a string if want to use a double
    quote character (") inside of it.
       
    Example:  If s is 'A "B C" D', this function returns 'B C'
    Example:  If s is 'A "B C" D "E F" G', this function still returns 'B C'
    because it only picks the first such substring.
       
    Parameter s: a string to search
    Precondition: s a string with at least two (double) quote characters."""
    
    #Find the starting double quotes
    start = s.index('"')

    #Store the substring after the quotes
    temp = s[start + 1:]

    #Find the ending double quotes
    end = temp.index('"')

    #Return the substring before the ending quotes
    return temp[:end]