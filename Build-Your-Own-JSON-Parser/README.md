# Build Your Own JSON Parser

This project is a small implementation of a JSON lexer built as part of the "Build Your Own JSON Parser" challenge. The goal is to scan raw JSON-like input and convert it into a stream of tokens that can later be used by a parser.

## Challenge goals
- Implement lexing for JSON-like input
- Recognize structural characters such as braces, brackets, commas, and colons
- Tokenize values such as strings, numbers, booleans, and null
- Ignore whitespace and produce an end-of-file token
- Support running sample tests for different challenge steps

## Current implementation
The lexer now supports:
- Objects and arrays: `{`, `}`, `[`, `]`
- Separators: `,` and `:`
- Strings wrapped in double quotes
- Integers and floats
- Boolean values: `true` and `false`
- Null values: `null`
- Whitespace handling
- Token management through lightweight token and token-type classes

## Project files
- [main.py](main.py) - entry point for running the lexer against test files
- [Lexer.py](Lexer.py) - main lexer implementation
- [Token.py](Token.py) - token container and token manager
- [TokenType.py](TokenType.py) - token type definitions
- [test_reporter.py](test_reporter.py) - reusable console test reporter with colors and summary stats

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

Run one specific test case number from the selected scope:

```bash
python3 main.py 0 --case 10
python3 main.py 2 --case 3
```

Disable colors when needed:

```bash
python3 main.py 0 --no-color
```

Enable debug mode for clean per-test diagnostics:

```bash
python3 main.py 0 --debug
python3 main.py 2 --case 3 --debug
```

Output is compact and includes only:
- Case number
- Test file
- PASS or FAIL
- Final summary stats (total, passed, failed, pass percentage, execution time)

With debug mode enabled, each test also prints:
- Expected result (PASS/FAIL)
- Actual lexer result (PASS/FAIL)
- Lexer cursor position
- Token stream snapshot

## Useful references
- [JSON graphical representation](https://www.json.org/json-en.html)
- [JSON defined by IETF](https://www.rfc-editor.org/info/std90/)

## Notes
This is an early-stage lexer implementation, and the next step would be to turn these tokens into a full JSON parser.

