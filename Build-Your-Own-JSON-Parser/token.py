class Token:
    def __init__(self, typ, value, position):
        self.type = typ
        self.value = value
        self.position = position


class TokenManager:
    def __init__(self):
        self.tokens = []

    def add_token(self, token: Token):
        self.tokens.append(token)

    def get_tokens(self) -> list[Token]:
        return self.tokens