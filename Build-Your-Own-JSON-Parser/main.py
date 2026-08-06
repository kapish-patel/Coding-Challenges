import sys
from lexer import Lexer
from pathlib import Path


def main():
    testCaseStepNumber = int(sys.argv[1])
    if testCaseStepNumber <= 0 or testCaseStepNumber >= 5:
        return False

    # read all the files in a directory
    files = [f for f in Path(f"tests/step{testCaseStepNumber}").iterdir() if f.is_file()]

    index = 1
    for fl in files:
        print(f"{index} - Running TestCase in: {fl.name}")
        index += 1

        context = fl.read_text();

        lexer = Lexer(context)
        if not lexer.process_InputString():
            print(f"Failed to lex string \n {lexer.getLexed()}", end='\n\n')
            continue;

        print(lexer.getLexed(), end='\n\n')

    


if __name__ == "__main__":
    main()