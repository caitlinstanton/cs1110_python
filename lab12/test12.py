# test12.py
# Lillian Lee (LJL2) and Walker White (wmw2)
# November 10, 2016
"""Test cases for lab12.py"""

import cornelltest
import lab12

def test_num_runs():
    """Test the function num_space_runs"""
    print '  Testing num_space_runs'
    cornelltest.assert_equals(4, lab12.num_space_runs('  a  f   g    '))
    cornelltest.assert_equals(2, lab12.num_space_runs('a  f   g'))
    cornelltest.assert_equals(3, lab12.num_space_runs('  a  bc   d'))
    cornelltest.assert_equals(1, lab12.num_space_runs('  a'))
    cornelltest.assert_equals(0, lab12.num_space_runs('ab'))
    print '  num_space_runs looks okay'


def test_split():
    """Test the function split"""
    print '  Testing split'
    cornelltest.assert_equals(['a','b','c','d'], lab12.split('a b c d '))
    cornelltest.assert_equals(['ab','cd'],       lab12.split('ab cd '))
    cornelltest.assert_equals(['ab','c','de'],   lab12.split('ab c de '))
    cornelltest.assert_equals(['a'],             lab12.split('a '))
    print '  split looks okay'


# Script Code
if __name__ == '__main__':
    print 'Testing while loops with invariants'
    test_num_runs()
    test_split()
    print "Module lab12.py is working correctly"