# Build Your Own JSON Parser

This project is a complete Python implementation of the "Build Your Own JSON Parser" challenge. It includes both a lexer and a recursive-descent parser that validate and parse JSON data structures from raw input.

## Challenge goals
- Tokenize valid JSON syntax
- Parse objects, arrays, strings, numbers, booleans, and null
- Reject malformed JSON and trailing tokens
- Validate the implementation against the provided challenge test cases
- Provide a compact CLI for running and debugging tests

## What is implemented
The solution now supports:
- Objects and arrays: `{}`, `[]`
- Key-value pairs with `:`
- Comma-separated elements and members
- Double-quoted strings
- Integer and float numeric literals
- Boolean values: `true` and `false`
- Null values: `null`
- Whitespace skipping and EOF handling
- Parser validation for complete JSON documents

The parser is built around a simple recursive-descent approach:
- `parse_value()` handles any valid JSON value
- `parse_object()` parses object members
- `parse_array()` parses array elements
- `current()`, `consume()`, and `match()` manage token progression and validation

## Project files
- [main.py](main.py) - CLI entry point and test runner
- [Lexer.py](Lexer.py) - tokenizes raw JSON input
- [Parser.py](Parser.py) - recursive-descent JSON parser
- [Nodes.py](Nodes.py) - in-memory representation for parsed values
- [Token.py](Token.py) - token container and token manager
- [TokenType.py](TokenType.py) - token definitions
- [test_reporter.py](test_reporter.py) - report formatting and summary output
- [tests/](tests/) - challenge fixtures for each step

## Running the tests
From the project directory, run all test cases:

```bash
python3 main.py 0
```

Run a single step:

```bash
python3 main.py 1
python3 main.py 2
python3 main.py 3
python3 main.py 4
python3 main.py 5
```

Run one specific test case from the selected scope:

```bash
python3 main.py 0 --case 10
python3 main.py 2 --case 3
```

Disable colors:

```bash
python3 main.py 0 --no-color
```

Enable detailed debug output:

```bash
python3 main.py 0 --debug
python3 main.py 2 --case 3 --debug
```

## Current status
The implementation passes all provided tests in the challenge suite:
- 12 total cases
- 12 passed
- 0 failed
- 100% pass rate

## Useful references
- [JSON specification on json.org](https://www.json.org/json-en.html)
- [JSON RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259)

## Notes
This solution completes the parser challenge by converting the lexer output into a working JSON parser that validates both valid and invalid JSON inputs in the supplied test set.

