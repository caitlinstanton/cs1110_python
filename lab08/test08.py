# test08.py
# Lillian Lee (LJL2) and Walker White (wmw2)
# October 15, 2014
"""Test cases for lab7.py"""

from cornelltest import *
from lab08 import *


def test_numberof():
    """Test function numberof"""
    mylist = [5, 3, 3455, 74, 74, 74, 3]
    assert_equals(0, numberof([],4))
    assert_equals(1, numberof([4],4))
    assert_equals(3, numberof(mylist,74))
    assert_equals(2, numberof(mylist,3))
    assert_equals(0, numberof(mylist,4))


def test_replace():
    """Test function replace"""
    mylist = [5, 3, 3455, 74, 74, 74, 3]
    assert_equals([],  replace([], 1, 2))
    assert_equals([4], replace([5],5,4))
    assert_equals([5, 20, 3455, 74, 74, 74, 20], replace(mylist,3, 20))
    assert_equals([5, 3, 3455, 74, 74, 74, 3],   replace(mylist, 1, 3))
    
    # test for whether the code is really returning a copy of the original list
    assert_equals([5, 3, 3455, 74, 74, 74, 3], mylist)
    assert_equals(False, mylist is replace(mylist, 1, 3))


def test_remove_dups():
    """Test function remove_dups"""
    mylist = [1,2,2,3,3,3,4,5,1,1,1]
    assert_equals([],  remove_dups([]))
    assert_equals([3], remove_dups([3,3]))
    assert_equals([4], remove_dups([4]))
    assert_equals([5], remove_dups([5, 5]))
    assert_equals([1,2,3,4,5,1], remove_dups(mylist))
    
    # test for whether the code is really returning a copy of the original list
    assert_equals([1,2,2,3,3,3,4,5,1,1,1], mylist)
    assert_equals(False, mylist is remove_dups(mylist))


def test_oddsevens():
    """Test function oddsevens"""
    mylist = [1,2,3,4,5,6]
    assert_equals([], oddsevens([]))
    assert_equals([3], oddsevens([3]))
    assert_equals([3,4], oddsevens([4,3]))
    assert_equals([-1,1,2,0], oddsevens([-1,0,1,2]))
    assert_equals([1,3,5,6,4,2], oddsevens(mylist))
    
    # test for whether the code is really returning a copy of the original list
    assert_equals([1,2,3,4,5,6], mylist)
    assert_equals(False, mylist is oddsevens(mylist))


### OPTIONAL EXERCISES ###

# Sequences Examples #

def test_number_not():
    """Test function number_not"""
    mylist = [5, 3, 3455, 74, 74, 74, 3]
    assert_equals(0, number_not([],4))
    assert_equals(0, number_not([4],4))
    assert_equals(4, number_not(mylist,74))
    assert_equals(5, number_not(mylist,3))
    assert_equals(7, number_not(mylist,4))


def test_remove_first():
    """Test function remove_first"""
    assert_equals([],remove_first([],3))
    assert_equals([],remove_first([3],3))
    assert_equals([3],remove_first([3],4))
    assert_equals([3, 4, 4, 5],remove_first([3, 4, 4, 4, 5],4))
    assert_equals([3, 5, 4, 4, 4],remove_first([3, 4, 5, 4, 4, 4],4))
 

def test_histogram():
    """Test function histogram"""
    assert_equals({}, histogram(''))
    assert_equals({'a':1}, histogram('a'))
    assert_equals({'a':1,'b':1,'c':1}, histogram('abc'))
    assert_equals({'a':3}, histogram('aaa'))
    assert_equals({'s':1, 'a':1, 'm':1, 'p':1, 'l':1, 'e':1}, histogram('sample'))
    assert_equals({'a':5, 'b':2, 'c':1, 'd':1, 'r':2}, histogram('abracadabra'))


def test_sum_list():
    """Test function sum_list"""
    assert_equals(0, sum_list([]))
    assert_equals(34, sum_list([34]))
    assert_equals(46, sum_list([7,34,1,2,2]))


def test_sum_to():
    """Test function sum_to"""
    assert_equals(1, sum_to(1))
    assert_equals(6, sum_to(3))
    assert_equals(15, sum_to(5))


def test_num_digits():
    """Test function num_digits"""
    assert_equals(1, num_digits(0))
    assert_equals(1, num_digits(3))
    assert_equals(2, num_digits(34))
    assert_equals(4, num_digits(1356))


def test_sum_digits():
    """Test function sum_digits"""
    assert_equals(0, sum_digits(0))
    assert_equals(3, sum_digits(3))
    assert_equals(7, sum_digits(34))
    assert_equals(12, sum_digits(345))


def test_number2():
    """Test function number2"""
    assert_equals(0, number2(0))
    assert_equals(1, number2(2))
    assert_equals(3, number2(234252))


def test_into():
    """Test function into"""
    assert_equals(0, into(5,3))
    assert_equals(1, into(6, 3))
    assert_equals(4, into(3*3*3*3*7,3))


# Script Code
if __name__ == '__main__':
    test_numberof()
    test_replace()
    test_remove_dups()
    
    # UNCOMMENT ANY OPTIONAL ONES YOU DO
    test_number_not()
    test_remove_first()
    test_sum_list()
    test_histogram()
    test_sum_to()
    test_num_digits()
    test_sum_digits()
    test_number2()
    test_into()
    print "Module lab08 is working correctly"