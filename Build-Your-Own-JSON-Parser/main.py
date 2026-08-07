from modulefinder import test
import sys
from Lexer import Lexer
from pathlib import Path


def main():
    testCaseStepNumber = int(sys.argv[1])
    if testCaseStepNumber <= -1 or testCaseStepNumber >= 6:
        return False

    # we have to make a mechanism from which we can run single or multiple files
    if testCaseStepNumber == 0:
        files = getAllTestsInAllSteps()
    else:
        files = getAllTestsForAStep(testCaseStepNumber)

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

def getAllTestsForAStep(stepNumber):
    return [f for f in Path(f"tests/step{stepNumber}").iterdir() if f.is_file()]

def getAllTestsInAllSteps():
    all_files = []
    for step in range(1, 6):
        all_files.extend(getAllTestsForAStep(step))
    return all_files


if __name__ == "__main__":
    main()