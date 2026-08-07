from enum import Enum

class TokenType(Enum):
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'

    COMMA = ','
    COLON = ':'

    STRING = "string"
    INTEGER = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"
    NULL = "null"

    EOF = "eof"
    IDENTIFIER = "identifier"