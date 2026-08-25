from Token import Token


class Node:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value
        self.children = {}
        self.items = []


class ObjectNode(Node):
    def __init__(self):
        super().__init__('object')


class ArrayNode(Node):
    def __init__(self):
        super().__init__('array')


class LiteralNode(Node):
    def __init__(self, value):
        super().__init__('literal', value)


class NodeFactory:
    @staticmethod
    def create_object():
        return ObjectNode()

    @staticmethod
    def create_array():
        return ArrayNode()

    @staticmethod
    def create_literal(value):
        return LiteralNode(value)

    @staticmethod
    def create_node(token: Token, kind: str = 'literal') -> Node:
        if kind == 'object':
            return ObjectNode()
        if kind == 'array':
            return ArrayNode()
        return LiteralNode(token.value)