import argparse
import sys
import time
from Lexer import Lexer
from pathlib import Path
from test_reporter import ConsoleTestReporter
from Parser import Parser


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run JSON lexer test cases"
    )
    parser.add_argument(
        "step",
        nargs="?",
        default=0,
        type=int,
        help="Step to run: 0 for all steps, or 1-5 for a single step",
    )
    parser.add_argument(
        "--case",
        dest="case_number",
        type=int,
        default=None,
        help="Run only one test case by its displayed case number",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print detailed per-test debug information",
    )
    return parser.parse_args()


def expected_to_pass(test_file: Path) -> bool:
    stem = test_file.stem.lower()
    if stem.startswith("valid"):
        return True
    if stem.startswith("invalid"):
        return False
    return True


def run_test(test_file: Path) -> tuple[bool, bool, dict]:
    context = test_file.read_text()
    lexer = Lexer(context)
    lexed_successfully = lexer.process_InputString()
    # add parsing here
    parser = Parser()
    parsed_successfully = parser.parse(lexer.getLexedTokens())
    actual_pass = lexed_successfully and parsed_successfully


    expected_pass = expected_to_pass(test_file)

    debug_info = {
        "input_length": len(context),
        "cursor_position": lexer.position,
        "tokens": lexer.getLexed(),
    }
    return actual_pass, expected_pass, debug_info


def main() -> int:
    start_time = time.perf_counter()
    args = parse_args()
    reporter = ConsoleTestReporter(use_color=not args.no_color)

    if args.step < 0 or args.step > 5:
        print("Error: step must be 0 or between 1 and 5.")
        return 1

    files = getAllTestsInAllSteps() if args.step == 0 else getAllTestsForAStep(args.step)

    if not files:
        print("No test files found.")
        return 1

    selected_cases = list(enumerate(files, start=1))
    if args.case_number is not None:
        if args.case_number < 1 or args.case_number > len(files):
            print(f"Error: case must be between 1 and {len(files)}.")
            return 1
        selected_cases = [(args.case_number, files[args.case_number - 1])]

    passed = 0
    reporter.print_header()
    for case_number, test_file in selected_cases:
        actual, expected, debug_info = run_test(test_file)
        is_pass = actual == expected
        if is_pass:
            passed += 1

        relative_path = test_file.as_posix()
        reporter.print_case(case_number, relative_path, is_pass)
        if args.debug:
            reporter.print_debug(
                case_number=case_number,
                expected_pass=expected,
                actual_pass=actual,
                cursor_position=debug_info["cursor_position"],
                input_length=debug_info["input_length"],
                token_types=debug_info["tokens"],
            )

    elapsed_seconds = time.perf_counter() - start_time
    reporter.print_summary(len(selected_cases), passed, elapsed_seconds)
    return 0 if passed == len(selected_cases) else 1

def getAllTestsForAStep(stepNumber):
    files = [f for f in Path(f"tests/step{stepNumber}").iterdir() if f.is_file()]
    return sorted(files, key=lambda path: path.name)

def getAllTestsInAllSteps():
    all_files = []
    for step in range(1, 6):
        all_files.extend(getAllTestsForAStep(step))
    return all_files


if __name__ == "__main__":
    sys.exit(main())