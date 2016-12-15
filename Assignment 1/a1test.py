# Test a1
# Caitlin Stanton (cs968), Andrew Denkewicz(ajd248)
# 09/10/2016

"""Unit test for module a1

When run as a script, this module invokes several procedures that 
test the various functions in the module a1."""

import cornelltest
import a1

def testA():
	s="125 dollars"
	assert_equals("125", before_space(s))

def testB():
	pass

def testC():
	pass

def testD():
	pass

testA()
testB()
testC()
testD()
print "Module a1 passed all tests"