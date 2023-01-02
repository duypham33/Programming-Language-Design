import sys
from psParser import read
from psOperators import Operators
from psItems import ArrayValue, Literal, Name, Array,Block
from colors import *

testinput1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """

testinput2 = """
    /x 40 def
    [1 2 3 4] dup 3 [x] putinterval /x exch def
    /g { x stack } def
    /f { /x [10 20 30 40] def g } def
    f
    """

testinput3 = """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n} def
    /chic
    	{ /n 1 def
	      /egg2 { n stack} def
	      n m
	      egg1
          m
	      egg2
	    } def
    n
    chic
        """

testinput4 = """
    /x 10 def
    /A { x } def
    /C { /x 40 def A stack } def
    /B { /x 30 def /A { x 2 mul } def C } def
    B
    """

testinput5 = """
    /x 2 def
    /n 5  def
    /A { 1  n {x mul} repeat} def
    /C { /n 3 def /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def
    B
    """

testinput6 = """
    /myfalse {1 2 eq} def
    /out true def 
    /xand { true eq {pop myfalse} {pop true} ifelse dup /x exch def stack} def 
    /myput { out dup /x exch def xand } def 
    /f { /out myfalse def myput } def 
    myfalse  f
    """

testinput7 = """
    /x [1 2 3 4] def
    /A { 0  x {add} forall } def
    /C { /x [10 20 30 40 50] def A stack } def
    /B { /x [6 7 8 9] def /A { x } def C } def
    B
    """

testinput8 = """
    /x [2 3 4 5] def
    /a 10 def  
    /A { x } def
    /C { /x [a 2 mul a 3 mul dup a 4 mul] def A  a x stack } def
    /B { /x [6 7 8 9] def /A { x } def /a 5 def C } def
    B
    """

"""
 ***** ADD YOUR TESTS HERE  *****
"""
testinput9 = """
    /x 1 def /y 1 def
    /f { 5 {y 1 add /y exch} repeat stack } def
    /g { /y 100 def f 100 y eq } def
    g y x add
"""

"""
-- TEST 9 --

STATIC
===**opstack**===
2
/y
2
/y
2
/y
2
/y
2
/y
===**dictstack**===
----2----0----
----1----0----
/y    100
----0----0----
/x    1
/y    1
/f    <function [Literal(5), Block([Name('y'), Literal(1), Name('add'), Name('/y'), Name('exch')]), Name('repeat'), Name('stack')]>
/g    <function [Name('/y'), Literal(100), Name('def'), Name('f'), Literal(100), Name('y'), Name('eq')]>
=================

DYNAMIC
===**opstack**===
101
/y
101
/y
101
/y
101
/y
101
/y
===**dictstack**===
----2----0----
----1----0----
/y    100
----0----0----
/x    1
/y    1
/f    <function [Literal(5), Block([Name('y'), Literal(1), Name('add'), Name('/y'), Name('exch')]), Name('repeat'), Name('stack')]>
/g    <function [Name('/y'), Literal(100), Name('def'), Name('f'), Literal(100), Name('y'), Name('eq')]>
=================
"""



testinput10 = """
    1 2 3 4 5
    /dfs { pop count 0 eq {stack} {g} ifelse } def
    /g {dfs} def
    dfs
"""

"""
-- TEST 10 --

STATIC
===**opstack**===
===**dictstack**===
----14----13----
----13----0----
----12----0----
----11----10----
----10----0----
----9----0----
----8----7----
----7----0----
----6----0----
----5----4----
----4----0----
----3----0----
----2----1----
----1----0----
----0----0----
/dfs    <function [Name('pop'), Name('count'), Literal(0), Name('eq'), Block([Name('stack')]), Block([Name('g')]), Name('ifelse')]>
/g    <function [Name('dfs')]>
=================

DYNAMIC
===**opstack**===
===**dictstack**===
----14----13----
----13----0----
----12----0----
----11----10----
----10----0----
----9----0----
----8----7----
----7----0----
----6----0----
----5----4----
----4----0----
----3----0----
----2----1----
----1----0----
----0----0----
/dfs    <function [Name('pop'), Name('count'), Literal(0), Name('eq'), Block([Name('stack')]), Block([Name('g')]), Name('ifelse')]>
/g    <function [Name('dfs')]>
=================
"""

testinput11 = """
    /x 5 def
    /A { /x 6 def /C { /B {D} def } def } def
    /B {/x x 5 add def A} def
    /C { /A {D} def B } def
    /D {x stack} def
    C
"""
"""
-- TEST 11 --

STATIC    (Because it has not reached stack() function)

DYNAMIC
===**opstack**===
10
===**dictstack**===
----4----0----
----3----1----
----2----0----
/x    10
----1----0----
/A    <function [Name('D')]>
----0----0----
/x    5
/A    <function [Name('/x'), Literal(6), Name('def'), Name('/C'), Block([Name('/B'), Block([Name('D')]), Name('def')]), Name('def')]>
/B    <function [Name('/x'), Name('x'), Literal(5), Name('add'), Name('def'), Name('A')]>
/C    <function [Name('/A'), Block([Name('D')]), Name('def'), Name('B')]>
/D    <function [Name('x'), Name('stack')]>
=================
"""


""" Make sure to add your test inputs to the below list as well!"""
tests = [testinput1,testinput2,testinput3,testinput4,testinput5,
testinput6,testinput7,testinput8,testinput9,testinput10,testinput11]

# program start
if __name__ == '__main__':
    
    psstacks_s = Operators("static")  
    psstacks_d = Operators("dynamic")  
    testnum = 1
    for testcase in tests:
        try:
            print("\n-- TEST {} --".format(testnum))
            expr_list = read(testcase)
            print("\nSTATIC")
            # interpret using static scoping rule
            for expr in expr_list:
                expr.evaluate(psstacks_s)
            print("\nDYNAMIC")
            # interpret using dynamic scoping rule
            for expr in expr_list:
                expr.evaluate(psstacks_d)    
            # clear the Stack objects 
            psstacks_s.clearBoth()
            psstacks_d.clearBoth()
        except (SyntaxError, NameError, TypeError, Exception) as err:
            print(type(err).__name__ + ':', err)
        testnum += 1
        # clear the Stack objects 
        psstacks_s.clearBoth()
        psstacks_d.clearBoth()