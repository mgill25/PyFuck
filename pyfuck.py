#!/usr/bin/env python

"""
PyFuck is a simple brainfuck interpreter
"""

class SyntaxError(Exception):
    pass

class RuntimeError(Exception):
    pass


class Interpreter(object):
    
    __reserved = '+|-|<|>|.|,|[|]'.split('|')

    def __init__(self, debug=False, eof=0):
        """Initialize the interpreter"""
        self.stack = []
        self.__bstack = []      # Bracket stack
        self.__pointer = 1      # pointer initially at position 1
        self.__debug = debug    # Debug Flag
    
    def Interpret(self, code):
        """Interpret a given string of code"""
        
        # Make sure brackets are correctly counted.
        if code.count('[') != code.count(']'):
            raise SyntaxError("Invalid Bracket Count")

        # Check for the brackets, then interpret each character individually.  
        x = 0
        while x < len(code):
            if code[x] not in __reserved:
                raise SyntaxError("Invalid Syntax")
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
                    x += 1  # start looking forward 
                    while not found:
                        # What happens in case of nested brackets? :S
                        if code[x] == ']':
                            found = True
                        x += 1

            else if code[x] == ']':
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
        if char == '+':
            self.stack[self.__pointer] += 1
        elif char == '-':
            self.stack[self.__pointer] -= 1
        elif char == '>':
            self.__pointer += 1
        elif char == '<':
            self.__pointer -= 1
        elif char == ',':
            # input byte
            pass
        elif char == '.':
            # output byte
            pass
            
                                        

