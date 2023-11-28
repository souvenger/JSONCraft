# types.py
from typing import Dict, Union, List

TokenType = Union[
    "BraceOpen",
    "BraceClose",
    "BracketOpen",
    "BracketClose",
    "String",
    "Number",
    "Comma",
    "Colon",
    "True",
    "False",
    "Null",
]

Token = Dict[str, Union[TokenType, str]]

ASTNode = Union[
    Dict[str, "ASTNode"],
    List["ASTNode"],
    Dict[str, Union[str, int, bool, None]],
    str,
    int,
    bool,
    None,
]


# utils.py
def is_boolean_true(value: str) -> bool:
    return value == "true"


def is_boolean_false(value: str) -> bool:
    return value == "false"


def is_null(value: str) -> bool:
    return value == "null"


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


# tokenizer.py
def tokenizer(input_string: str) -> List[Token]:
    length = len(input_string)
    current = 0
    tokens = []
    count_comma = 0

    while current < len(input_string):
        char = input_string[current]

        if char == "{":
            tokens.append({"type": "BraceOpen", "value": char})
            current += 1
            continue

        if char == "}":
            tokens.append({"type": "BraceClose", "value": char})
            current += 1
            continue

        if char == "[":
            tokens.append({"type": "BracketOpen", "value": char})
            current += 1
            continue

        if char == "]":
            tokens.append({"type": "BracketClose", "value": char})
            current += 1
            continue

        if char == ":":
            tokens.append({"type": "Colon", "value": char})
            current += 1
            continue

        if char == ",":
            tokens.append({"type": "Comma", "value": char})
            current += 1
            count_comma += 1
            continue

        if char == '"':
            value = ""
            char = input_string[current + 1]
            while char != '"':
                value += char
                current += 1
                if current + 1 >= length:
                    raise ValueError("Not a valid String")
                char = input_string[current + 1]
            current += 2  # Skip closing quote
            tokens.append({"type": "String", "value": value})
            continue

        # For number, boolean and null values
        if char.isdigit() or char.isalpha():
            value = ""
            while char.isdigit() or char.isalpha() or char == ".":
                value += char
                current += 1
                char = input_string[current]

            if is_number(value):
                tokens.append({"type": "Number", "value": value})
            elif is_boolean_true(value):
                tokens.append({"type": "True", "value": value})
            elif is_boolean_false(value):
                tokens.append({"type": "False", "value": value})
            elif is_null(value):
                tokens.append({"type": "Null", "value": value})
            else:
                raise ValueError("Unexpected value: " + value)

            continue

        # Skip whitespace
        if char.isspace():
            current += 1
            continue

        raise ValueError("Unexpected character: " + char)

    return tokens


# parser.py
def parser(tokens: List[Token]) -> ASTNode:
    if not tokens:
        raise ValueError("Nothing to parse. Exiting!")

    current = 0

    def advance():
        nonlocal current
        current += 1
        return tokens[current]

    def parse_value() -> ASTNode:
        token = tokens[current]
        if token["type"] == "String":
            return {"type": "String", "value": token["value"]}
        elif token["type"] == "Number":
            return {"type": "Number", "value": float(token["value"])}
        elif token["type"] == "True":
            return {"type": "Boolean", "value": True}
        elif token["type"] == "False":
            return {"type": "Boolean", "value": False}
        elif token["type"] == "Null":
            return {"type": "Null"}
        elif token["type"] == "BraceOpen":
            return parse_object()
        elif token["type"] == "BracketOpen":
            return parse_array()
        else:
            raise ValueError("Unexpected token type: " + token["type"])

    def parse_object() -> Dict[str, ASTNode]:
        node = {"type": "Object", "value": {}}
        token = advance()  # Eat '{'

        while token["type"] != "BraceClose":
            if token["type"] == "String":
                key = token["value"]
                token = advance()  # Eat key
                if token["type"] != "Colon":
                    raise ValueError("Expected : in key-value pair")
                token = advance()  # Eat ':'
                value = parse_value()  # Recursively parse the value
                node["value"][key] = value
            else:
                raise ValueError(
                    "Expected String key in object. Token type: " + token["type"]
                )
            token = advance()  # Eat value or ','
            # Check for a comma to handle multiple key-value pairs
            if token["type"] == "Comma":
                token = advance()  # Eat ',' if present

        return node

    def parse_array() -> List[ASTNode]:
        node = {"type": "Array", "value": []}
        token = advance()  # Eat '['

        while token["type"] != "BracketClose":
            value = parse_value()
            node["value"].append(value)

            token = advance()  # Eat value or ','
            if token["type"] == "Comma":
                token = advance()  # Eat ',' if present

        return node

    AST = parse_value()

    return AST


# main.py
# from parser import parser
# from tokenizer import tokenizer


def is_valid_json(input_string: str) -> bool:
    try:
        tokens = tokenizer(input_string)
        parser(tokens)
        return True
    except ValueError:
        return False


# tokens = tokenizer(
#     """
# {
#   "key": "value",
#   "key-n": 101,
#   "key-o": {
#     "inner key": "inner value"
#   },
#   "key-l": ["list value"]
# }
# """
# )
json = """
 {
  "name": "Justin Delacruz",
  "email": "erinvega@example.com",
  "address": {
    "city": "Port Scottside",
    "state": "Kansas",
    "zip_code": "04259"
  },
  "phone_number": "(209)508-3454",
  "is_student": "False",
  "grades": [
    "85",
    "95",
    "98",
    "81",
    "90"
  ]
}"""

print(is_valid_json(json))
