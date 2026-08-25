from TokenType import TokenType
from Token import Token
from Nodes import NodeFactory


class Parser:
    def __init__(self):
        self.tokens: list[Token] = []
        self.index = 0
        self.root = None

    def parse(self, tokens: list[Token]) -> bool:
        self.tokens = tokens
        self.index = 0

        try:
            self.root = self.parse_value()
            if self.current().type != TokenType.EOF.name:
                raise ValueError("Unexpected trailing tokens")
            return True
        except ValueError:
            return False

    def current(self) -> Token:
        if self.index >= len(self.tokens):
            raise ValueError("Unexpected end of input")
        return self.tokens[self.index]

    def consume(self, expected_type: str) -> Token:
        token = self.current()
        if token.type != expected_type:
            raise ValueError(f"Expected {expected_type}, found {token.type}")
        self.index += 1
        return token

    def match(self, expected_type: str) -> bool:
        if self.index < len(self.tokens) and self.tokens[self.index].type == expected_type:
            self.index += 1
            return True
        return False

    def parse_value(self):
        token = self.current()

        if token.type == TokenType.LEFT_BRACE.name:
            return self.parse_object()
        if token.type == TokenType.LEFT_BRACKET.name:
            return self.parse_array()
        if token.type in [
            TokenType.STRING.name,
            TokenType.INTEGER.name,
            TokenType.FLOAT.name,
            TokenType.BOOLEAN.name,
            TokenType.NULL.name,
        ]:
            self.index += 1
            return NodeFactory.create_literal(token.value)

        raise ValueError(f"Unexpected token: {token.type}")

    def parse_object(self):
        obj = NodeFactory.create_object()
        self.consume(TokenType.LEFT_BRACE.name)

        if self.match(TokenType.RIGHT_BRACE.name):
            return obj

        while True:
            key_token = self.consume(TokenType.STRING.name)
            self.consume(TokenType.COLON.name)
            obj.children[key_token.value] = self.parse_value()

            if self.match(TokenType.COMMA.name):
                if self.current().type == TokenType.RIGHT_BRACE.name:
                    raise ValueError("Trailing comma in object")
                continue

            self.consume(TokenType.RIGHT_BRACE.name)
            return obj

    def parse_array(self):
        arr = NodeFactory.create_array()
        self.consume(TokenType.LEFT_BRACKET.name)

        if self.match(TokenType.RIGHT_BRACKET.name):
            return arr

        while True:
            arr.items.append(self.parse_value())

            if self.match(TokenType.COMMA.name):
                if self.current().type == TokenType.RIGHT_BRACKET.name:
                    raise ValueError("Trailing comma in array")
                continue

            self.consume(TokenType.RIGHT_BRACKET.name)
            return arr

