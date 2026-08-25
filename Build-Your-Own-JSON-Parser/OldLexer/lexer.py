# a simple lexetr which identify and label the input string.

from enum import Enum
from token import Token, TokenManager
from functools import wraps
from collections.abc import Callable
from typing import Any

class TokenType(Enum):
    LPARA = '{'
    RPARA = '}'
    BREAKER = ':'
    NRECORD = ','
    STRING = '"'
    LARR = '['
    RARR = ']'    
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    NULL = 'null'
    NEWLINE = '\n'
    SPACE = ' '
    QUOTE = '"'
    SINGLEQUOTE = "'"
    

type Data = dict[str, Any]
type ExportFn = Callable[[Data], None]

class Lexer:
    def __init__(self, input_string: str):
        self.input_string = input_string
        self.position = 0
        self.tm = TokenManager()
        self.registery = {
            TokenType.LPARA.value: self.handleOpenBrace,
            TokenType.RPARA.value: self.handleCloseBrace,
            TokenType.BREAKER.value: self.handleBreaker,
            TokenType.NRECORD.value: self.handleNRecord,
            TokenType.QUOTE.value: self.handleQuote,
            TokenType.LARR.value: self.handleArrayStart,
            TokenType.RARR.value: self.handleArrayEnd,
            TokenType.SPACE.value: self.handleSpaceAndNewLine,
            TokenType.NEWLINE.value: self.handleSpaceAndNewLine,
            TokenType.SINGLEQUOTE.value: self.handleQuote,
        }

    def handleOpenBrace(self):
        c = self.input_string[self.position]
        self.tm.add_token(Token(TokenType.LPARA, c, self.position))
        self.position += 1
        return True

    def handleCloseBrace(self):
        c = self.input_string[self.position]
        self.tm.add_token(Token(TokenType.RPARA, c, self.position))
        self.position += 1
        return True

    def handleBreaker(self):
        c = self.input_string[self.position]
        self.tm.add_token(Token(TokenType.BREAKER, c, self.position))
        self.position += 1
        return True

    def handleNRecord(self):
        c = self.input_string[self.position]
        self.tm.add_token(Token(TokenType.NRECORD, c, self.position))
        self.position += 1
        return True

    def handleQuote(self):
        c = self.input_string[self.position]
        if c == "'":
            return False
        self.tm.add_token(Token(TokenType.QUOTE, c, self.position))
        self.position += 1
        return True

    def handleValue(self):
        value, typ = self.getValueWithType(self.position)
        if value is None and typ is None:
            return False
        self.tm.add_token(Token(typ, value, self.position))
        self.position += len(str(value)) # move past the string including starting and ending quotes
        return True
    
    def handleArrayStart(self):
        c = self.input_string[self.position]
        self.tm.add_token(Token(TokenType.LARR, c, self.position))
        self.position += 1
        return True
    
    def handleArrayEnd(self):
        c = self.input_string[self.position]
        self.tm.add_token(Token(TokenType.RARR, c, self.position))
        self.position += 1
        return True

    def handleSpaceAndNewLine(self):
        self.position += 1
        return True
        
    def process_InputString(self):
        # we have to make a recursive solution so we call the handle object 
        if self.handleObject() and self.tm.tokens != []:
            return True
        return False

    def handleObject(self):

        # we need a base case which will be EOF
        if self.position >= len(self.input_string):
            return True

        c = self.input_string[self.position]

        if c in self.registery:
            if not self.registery[c]():
                return False
        else:
            if not self.handleValue():
                return False

        return self.handleObject()



    def getValueWithType(self, start_pos) -> tuple:
        # if starting value is " that means we have a string if not we potentially could have a number or boolean
        result = '' 
        # if the string start with " we can start with next pos
        if self.input_string[start_pos] == '"':
            start_pos += 1

        # we read continously until we hit a delimiter (comma, closing brace, or closing bracket)
        while start_pos < len(self.input_string):
            c = self.input_string[start_pos]
            if c in [',', '}', ']', '"', ':']:
                break
            result += c
            start_pos += 1
        # now we have a single value
        # we have to skip the space or any escape chars and increment the position
        
        if result.isdigit():
            return int(result), TokenType.INT
        try:
            return float(result), TokenType.FLOAT
        except ValueError:
            pass
        if result == 'true':
            return True, TokenType.BOOL
        if result == 'false':
            return False, TokenType.BOOL
        if result == 'null':
            return None, TokenType.NULL
        if result == 'True':
            return None, None
        if result == 'False':
            return None, None
        if result == 'Null':
            return None, None

        return result, TokenType.STRING


    def getLexed(self):
        # return an array with all the lexed tokens
        return [token.value for token in self.tm.tokens]