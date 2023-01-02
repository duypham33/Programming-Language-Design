# Duy Pham, ID: 011742984

from psItems import Value, ArrayValue, FunctionValue

class Operators:
    def __init__(self):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        
        #The builtin operators supported by our interpreter
        self.builtin_operators = {
             # include the key value pairs where the keys are the PostScrip operator names and the values are the function values that implement that operator. 
             # Make sure **not to call the functions**
             "def": self.psDef,
             "dict": self.psDict,
             "begin": self.begin,
             "end": self.end,
             "add": self.add,
             "sub": self.sub,
             "mul": self.mul,
             "mod": self.mod,
             "eq": self.eq,
             "lt": self.lt,
             "gt": self.gt,
             "length": self.length,
             "getinterval": self.getinterval,
             "putinterval": self.putinterval,
             "aload": self.aload,
             "astore": self.astore,
             "pop": self.pop,
             "stack": self.stack,
             "dup": self.dup,
             "exch": self.exch,
             "copy": self.copy,
             "count": self.count,
             "clear": self.clear,
             "roll": self.roll,
             "if": self.psIf,
             "ifelse": self.psIfelse,
             "repeat": self.repeat,
             "forall": self.forall
        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
          return self.opstack.pop()
        print('Warning: The operand stack is currently empty!')
        return None

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self, value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        if len(self.dictstack) > 0:
          return self.dictstack.pop()
        print('Warning: The dictionary stack is currently empty!')
        return None 

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self, d):
        self.dictstack.append(d)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    def define(self, name, value):
        if len(self.dictstack) == 0:
          self.dictstack.append({})
        self.dictstack[-1][name] = value

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self, name):
        name = '/' + name
        for d in self.dictstack[::-1]:
          if name in d:
            return d[name]
        print('Error: The variable hasn\'t been defined yet!')
        return None
    
    #------- Arithmetic Operators --------------
    
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """ 
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: mod expects 2 operands")


    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
          
            self.opPush(op1 == op2)      
        else:
            print("Error: eq expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
          
            self.opPush(op2 < op1)      
        else:
            print("Error: lt expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
          
            self.opPush(op2 > op1)      
        else:
            print("Error: gt expects 2 operands")

    # ------- Array Operators --------------
    """ 
       Pops an array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support ArrayValue values.
    """
    def length(self):
        if len(self.opstack) > 0:
            op = self.opPop()
            if isinstance(op, ArrayValue):
              self.opPush(len(op.value))  
            else:
              print("Error: length expects one array constant!")
              self.opPush(op)   
        else:
            print("Error: length expects one operand")

    """ 
        Pops the `count` (int), an (zero-based) start `index`, and an array constant (ArrayValue) from the operand stack.  
        Pushes the slice of the array of length `count` starting at `index` onto the opstack.(i.e., from `index` to `index`+`count`) 
        If the end index of the slice goes beyond the array length, will give an error. 
    """
    def getinterval(self):
        if len(self.opstack) > 2:
            op1 = self.opPop()
            op2 = self.opPop()
            op3 = self.opPop()
            valid = False
            if isinstance(op1, int) == False:
              print("Error: getinterval expects the third operand is an integer!")
            elif isinstance(op2, int) == False:
              print("Error: getinterval expects the second operand is an integer!")
            elif isinstance(op3, ArrayValue) == False:
              print("Error: getinterval expects the first operand is an array constant!")
            else:
              end = op2 + op1 - 1
              if end >= len(op3.value):
                print("Error: The interval goes beyond the array length!")
              else:
                valid = True
                op3.value = op3.value[op2:(end + 1)]
                self.opPush(op3)
            
            if valid == False:
              self.opPush(op3)
              self.opPush(op2)
              self.opPush(op1)  
                  
        else:
            print("Error: getinterval expects 3 operands")

    """ 
        Pops an array constant (ArrayValue), start `index` (int), and another array constant (ArrayValue) from the operand stack.  
        Replaces the slice in the bottom ArrayValue starting at `index` with the top ArrayValue (the one we popped first). 
        The result is not pushed onto the stack.
        The index is 0-based. If the end index of the slice goes beyond the array length, will give an error. 
    """
    def putinterval(self):
        if len(self.opstack) > 2:
            op1 = self.opPop()
            op2 = self.opPop()
            op3 = self.opPop()
            valid = False
            if isinstance(op3, ArrayValue) == False:
              print("Error: putinterval expects the first operand is an array constant!")
            elif isinstance(op2, int) == False:
              print("Error: putinterval expects the second operand is an integer!")
            elif isinstance(op1, ArrayValue) == False:
              print("Error: putinterval expects the third operand is an array constant!")
            else:
              end = op2 + len(op1.value) - 1
              if end >= len(op3.value):
                print("Error: The putinterval goes beyond the array length!")
              else:
                valid = True
                op3.value[op2:(end + 1)] = op1.value
            
            if valid == False:
              self.opPush(op3)
              self.opPush(op2)
              self.opPush(op1)  
                  
        else:
            print("Error: putinterval expects 3 operands")
            

    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pushes all values in the array constant to the opstack in order (the first value in the array should be pushed first). 
        Pushes the orginal array value back onto the stack. 
    """
    def aload(self):
        if len(self.opstack) > 0:
          op = self.opPop()
          if isinstance(op, ArrayValue) == True:
            for v in op.value:
              self.opPush(v)
          else:
            print("Error: aload expects an array constant!")
          
          self.opPush(op)

        else:
          print("Error: aload expects one operand!")
        
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pops as many elements as the length of the array from the operand stack and stores them in the array constant. 
        The value which was on the top of the opstack will be the last element in the array. 
        Pushes the array value back onto the operand stack. 
    """
    def astore(self):
        if len(self.opstack) > 0:
          op = self.opPop()
          if isinstance(op, ArrayValue) == True:
            if len(self.opstack) >= len(op.value):
              for i in range(len(op.value) - 1, -1, -1):
                v = self.opPop()
                if v:
                  op.value[i] = v
            else:
              print("Error: There are not enough elements in the stack for storing!")
          else:
            print("Error: astore expects an array constant!")
          
          self.opPush(op)

        else:
          print("Error: astore expects one operand!")

    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
      self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
    def stack(self):
      print(self.opstack[::-1])

    """
       Copies the top element in opstack.
    """
    def dup(self):
      if len(self.opstack) > 0:
        self.opPush(self.opstack[-1])
      else:
        print("Error: The operand stack is currently empty!")

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if len(self.opstack) > 0:
          op = self.opPop()
          if isinstance(op, int) == True:
            for v in self.opstack[-op:]:
              self.opPush(v)
          else:
            print("Error: copy expects an integer operand!")
            self.opPush(op)

        else:
          print("Error: copy expects one operand!")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
      self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
      self.opstack[:] = []
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
      if len(self.opstack) > 1:
        self.opstack[-2], self.opstack[-1] = self.opstack[-1], self.opstack[-2]
      else:
        print("Error: exch expects two operands!")

    """
        Implements roll operator.
        Pops two integer values (m, n) from opstack; 
        Rolls the top m values in opstack n times (if n is positive roll clockwise, otherwise roll counter-clockwise)
    """
    def roll(self):
      if len(self.opstack) > 1:
        if isinstance(self.opstack[-1], int) and isinstance(self.opstack[-2], int):
          n = self.opPop()
          m = self.opPop()
          if len(self.opstack) >= m:
            if n != 0:
              last_m = self.opstack[-m:]
              n = n % m
              
              if n != 0:
                last_m[:-n], last_m[-n:] = last_m[-n:], last_m[:-n]
                self.opstack[-m:] = last_m
          else:
            print("Error: There are not enough elements left to roll!")
            self.opPush(m)
            self.opPush(n)
        else:
          print("Error: roll expects two integer operands!")
      else:
        print("Error: roll expects two operands!")

    """
       Pops an integer from the opstack (size argument) and pushes an empty dictionary onto the opstack.
    """
    def psDict(self):
      if len(self.opstack) > 0:
        if isinstance(self.opstack[-1], int):
          self.opPop()
          self.opPush({})
        else:
          print("Error: dict expects an integer operand!")
      else:
        print("Error: dict expects one operand!")

    """
       Pops the dictionary at the top of the opstack; pushes it to the dictstack.
    """
    def begin(self):
      if len(self.opstack) > 0:
        if isinstance(self.opstack[-1], dict):
          op = self.opPop()
          self.dictPush(op)
        else:
          print("Error: begin expects a dictionary operand!")
      else:
        print("Error: begin expects one operand!")

    """
       Removes the top dictionary from dictstack.
    """
    def end(self):
      self.dictPop()
        
    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    def psDef(self):
      if len(self.opstack) > 1:
        if isinstance(self.opstack[-1], str):
          print('Error: def expects the second operand is any rather than a name constant!')
        elif isinstance(self.opstack[-2], str) == False:
          print('Error: def expects the first operand is a name constant!')
        else:
          value = self.opPop()
          name = self.opPop()
          self.define(name, value)
      else:
        print("Error: def expects two operands!")


    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
    def psIf(self):
        if len(self.opstack) > 1:
          if isinstance(self.opstack[-1], FunctionValue) == False:
            print('Error: if expects the second operand is a code array!')
          elif isinstance(self.opstack[-2], bool) == False:
            print('Error: if expects the first operand is a boolean constant!')
          else:
            code = self.opPop()
            condition = self.opPop()
            if condition == True:
              code.apply(self)
        else:
          print("Error: if expects two operands!")

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        if len(self.opstack) > 2:
          if isinstance(self.opstack[-1], FunctionValue) == False:
            print('Error: ifelse expects the third operand is a code array!')
          elif isinstance(self.opstack[-2], FunctionValue) == False:
            print('Error: ifelse expects the second operand is a code array!')
          elif isinstance(self.opstack[-3], bool) == False:
            print('Error: ifelse expects the first operand is a boolean constant!')
          else:
            code2 = self.opPop()
            code1 = self.opPop()
            condition = self.opPop()
            if condition == True:
              code1.apply(self)
            else:
              code2.apply(self)
        else:
          print("Error: ifelse expects three operands!")


    #------- Loop Operators --------------
    """
       Implements repeat operator.   
       Pops the `loop_body` (FunctionValue) and loop `count` (int) arguments from opstack; 
       Evaluates (applies) the `loopbody` `count` times. 
       Will be completed in part-2. 
    """  
    def repeat(self):
        if len(self.opstack) > 1:
          if isinstance(self.opstack[-1], FunctionValue) == False:
            print('Error: repeat expects the second operand is a code array!')
          elif isinstance(self.opstack[-2], int) == False:
            print('Error: repeat expects the first operand is an integer constant!')
          else:
            code = self.opPop()
            counter = self.opPop()
            if counter > 0:
              for i in range(counter):
                code.apply(self)
        else:
          print("Error: repeat expects two operands!")
        
    """
       Implements forall operator.   
       Pops a `codearray` (FunctionValue) and an `array` (ArrayValue) from opstack; 
       Evaluates (applies) the `codearray` on every value in the `array`.  
       Will be completed in part-2. 
    """ 
    def forall(self):
        if len(self.opstack) > 1:
          if isinstance(self.opstack[-1], FunctionValue) == False:
            print('Error: forall expects the second operand is a code array!')
          elif isinstance(self.opstack[-2], ArrayValue) == False:
            print('Error: forall expects the first operand is an array constant!')
          else:
            code = self.opPop()
            arr = self.opPop()
            for element in arr.value:
              self.opPush(element)
              code.apply(self)
        else:
          print("Error: forall expects two operands!")

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []


    def cleanTop(self): 
        if len(self.opstack)>1: 
            if self.opstack[-1] is None: 
                self.opstack.pop() 
