# test07.py
# Walker M. White (wmw2)
# October 7, 2015
"""Unit test for Lab 7"""
import cornelltest
import lab07

def test_lesser_than():
    """Test procedure for function unique"""
    print 'Testing function lesser_than'
    thelist = [5, 9, 5, 7, 3, 10, 4]
    cornelltest.assert_equals(2,lab07.lesser_than(thelist,5))
    cornelltest.assert_equals(1,lab07.lesser_than(thelist,4))
    cornelltest.assert_equals(0,lab07.lesser_than(thelist,3))
    cornelltest.assert_equals(4,lab07.lesser_than(thelist,6))
    cornelltest.assert_equals(6,lab07.lesser_than(thelist,10))
    cornelltest.assert_equals(7,lab07.lesser_than(thelist,20))


def test_uniques():
    """Test procedure for function uniques"""
    print 'Testing function uniques'
    thelist = [5, 9, 5, 7] 
    cornelltest.assert_equals(3,lab07.uniques(thelist))
    
    thelist = [5, 5, 1, 'a', 5, 'a']
    cornelltest.assert_equals(3,lab07.uniques(thelist))
    
    thelist = [1, 2, 3, 4, 5]
    cornelltest.assert_equals(5,lab07.uniques(thelist))

    thelist = []
    cornelltest.assert_equals(0,lab07.uniques(thelist))
    
    # Make sure the function does not modify the original
    thelist = [5, 9, 5, 7]
    result  = lab07.uniques(thelist)
    cornelltest.assert_equals([5, 9, 5, 7],thelist)


def test_clamp():
    """Test procedure for function clamp"""
    print 'Testing function clamp'
    
    thelist = [-1, 1, 3, 5]
    lab07.clamp(thelist,0,4)
    # You CAN use assert_equals to compare lists
    # Though we will see a better way in A4
    cornelltest.assert_equals([0,1,3,4],thelist)
    
    thelist = [1, 3]
    lab07.clamp(thelist,0,4)
    cornelltest.assert_equals([1,3],thelist)
    
    thelist = [-1, 1, 3, 5]
    lab07.clamp(thelist,1,1)
    cornelltest.assert_equals([1,1,1,1],thelist)
    
    thelist = []
    lab07.clamp(thelist,0,4)
    cornelltest.assert_equals([],thelist)


# Script code
if __name__ == '__main__':
    test_lesser_than()
    test_uniques()
    test_clamp()
    print 'Lab 7 is working correctly'
