# a simple lexer to identify known things in simple english

from TokenType import TokenType
from Token import Token, TokenManager

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.position = 0
        self.tokenManager = TokenManager()

    def handleIntegerOrFloat(self) -> tuple[bool, int]:
        start_position = self.position
        while start_position < len(self.input_string):
            current_char = self.input_string[start_position]
            if current_char.isdigit():
                start_position += 1
            elif current_char == ".":
                start_position += 1
            else:
                break
        number_value = self.input_string[self.position:start_position]
        if "." in number_value:
            self.addToken(TokenType.FLOAT.name, number_value, self.position)
        else:
            self.addToken(TokenType.INTEGER.name, number_value, self.position)
        increment = start_position - self.position
        return True, increment

    def handleBooleanAndNull(self) -> tuple[bool, int]:
        start_position = self.position
        while start_position < len(self.input_string):
            current_char = self.input_string[start_position]
            if current_char.isalpha():
                start_position += 1
            else:
                break
        value = self.input_string[self.position:start_position]
        if value == "true" or value == "false":
            self.addToken(TokenType.BOOLEAN.name, value, self.position)
        elif value == "null":
            self.addToken(TokenType.NULL.name, value, self.position)
        else:
            return False, start_position - self.position
        increment = start_position - self.position
        return True, increment

    def handleString(self) -> tuple[bool, int]:
        start_position = self.position + 1
        string_value = ""
        while start_position < len(self.input_string):
            current_char = self.input_string[start_position]
            if current_char == '"':
                self.addToken(TokenType.STRING.name, string_value, start_position)
                increment = start_position - self.position + 1
                return True, increment
            else:
                string_value += current_char
                start_position += 1
        # If we reach here, the string was not closed
        return False, start_position

    def handleIdentifier(self) -> tuple[bool, int]:
        start_position = self.position
        while start_position < len(self.input_string):
            current_char = self.input_string[start_position]
            if current_char in ["{", "}", ":", "[", "]", ",", " ", "\n", "\r", "\t"]:
                break
            start_position += 1
        value = self.input_string[self.position:start_position]
        self.addToken(TokenType.IDENTIFIER.name, value, self.position)
        increment = start_position - self.position
        return True, increment

    def process_InputString(self):
        while self.position < len(self.input_string):
            current_char = self.input_string[self.position]
            increment = 0
            success = False
            if current_char in ["{", "}", ":", "[", "]", ","]:
                self.addToken(TokenType(current_char).name, current_char, self.position)                
                increment = 1
                success = True
            elif current_char in ['\n', '\r', '\t', ' ']:
                increment = 1
                success = True
            elif current_char in ['t', 'f', 'n']:
                success, increment = self.handleBooleanAndNull()
            elif current_char == '"':
                success, increment = self.handleString()
            elif current_char.isdigit():
                success, increment = self.handleIntegerOrFloat()
            elif current_char == "'":
                return False
            else:
                success, increment = self.handleIdentifier()

            if not success:
                return False
            
            self.position += increment
            
        self.addToken(TokenType.EOF.name, "", self.position)
        return True

    def addToken(self, token_type, token_value, token_position):
        self.tokenManager.addToken(Token(token_type, token_value, token_position))

    def getLexed(self):
        return [token.type for token in self.tokenManager.getTokens()]
