#!/usr/bin/env python

"""
PyFuck is a simple brainfuck interpreter
"""

import sys

class SyntaxError(Exception):
    pass

class RuntimeError(Exception):
    pass

class Interpreter(object):
    
    __reserved = '+|-|<|>|.|,|[|]'.split('|')
    __spacechars = ['\t', '\n', ' ']

    def __init__(self, debug=False, eof=0):
        """Initialize the interpreter"""
        self.stack = [0] * 30000
        self.__bstack = []      # Bracket stack
        self.__pointer = 0      # pointer initially at position 0
        self.__debug = debug    # Debug Flag
    
    def interpret(self, code):
        """Interpret a given string of code"""
        
        # Make sure brackets are correctly counted.
        if code.count('[') != code.count(']'):
            raise SyntaxError("Invalid Bracket Count")

        # Check for the brackets, then interpret each character individually.  
        x = 0
        while x < len(code):
            #print "\nStack: ", self.stack
            # if code[x] not in self.__reserved and code[x] not in self.__spacechars:
            #     print "<Brainfuck Traceback> %s - %s" %(code[x], ord(code[x]))
            #     raise SyntaxError("Invalid Syntax")
            if code[x] == '[':
                # If the byte at the data pointer is zero, then instead of
                # moving the instruction pointer forward to the next command,
                # jump it forward to the command after the matching ']'
                if self.stack[self.__pointer] != 0:
                    self.__bstack.append(x)                 # keep track of the last bracket position
                    x += 1                                  # and do nothing else
                else:
                    # Look ahead to find the matching ]
                    # since we've already checked that the bracket count is
                    # correct, we can safely assume that the first ] we
                    # encounter will match the [ we just scanned.
                    found = False
                    x += 1              # start looking forward 
                    nested = 0
                    while nested != -1:
                        if code[x] == '[':
                            nested += 1
                        if code[x] == ']':
                            nested -= 1
                        x += 1

            elif code[x] == ']':
                if self.__bstack != []:
                    x = self.__bstack.pop(0)
                else:
                    raise SyntaxError("'[' must come before ']'")
            else:
                # interpret other single chars
                self.__interpretChar(code[x])
                x += 1

    def __interpretChar(self, char):
        """Interpret other brainfuck characters"""
        # TODO: Error checking and handling edge-cases.
        if char == '+' and self.stack[self.__pointer] < 255:
            self.stack[self.__pointer] += 1
        elif char == '-' and self.stack[self.__pointer] > 0:
            self.stack[self.__pointer] -= 1
        elif char == '>':
            #self.stack.append(0)
            self.__pointer += 1
        elif char == '<':
            self.__pointer -= 1
        elif char == ',':
            # Input byte
            self.stack[self.__pointer] = ord(sys.stdin.read())
        elif char == '.':
            # Output byte
            sys.stdout.write(chr(self.stack[self.__pointer]))
            
    def __repr__(self):
        return "Stack: (%s) Pointer at: %d\n" %(self.stack, self.__pointer)        

if __name__ == "__main__":
    bf = Interpreter()
    fsock = open(sys.argv[1])
    code = fsock.read() 
    bf.interpret(code) 
         
