import os
import sys


class ConsoleTestReporter:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"

    def __init__(self, use_color: bool = True, stream=None):
        self.stream = stream if stream is not None else sys.stdout
        self.use_color = use_color and self._supports_color(self.stream)

    def _supports_color(self, stream) -> bool:
        if os.getenv("NO_COLOR"):
            return False

        has_tty = hasattr(stream, "isatty") and stream.isatty()
        term = os.getenv("TERM", "")
        return has_tty and term != "dumb"

    def _style(self, text: str, color: str = "", bold: bool = False) -> str:
        if not self.use_color:
            return text

        start = ""
        if bold:
            start += self.BOLD
        if color:
            start += color
        return f"{start}{text}{self.RESET}"

    def print_header(self) -> None:
        print(self._style("Case File Result", self.CYAN, bold=True), file=self.stream)

    def print_case(self, case_number: int, file_path: str, is_pass: bool) -> None:
        status_text = "PASS" if is_pass else "FAIL"
        status_color = self.GREEN if is_pass else self.RED
        status = self._style(status_text, status_color, bold=True)
        print(f"{case_number:02d} {file_path} {status}", file=self.stream)

    def print_debug(
        self,
        case_number: int,
        expected_pass: bool,
        actual_pass: bool,
        cursor_position: int,
        input_length: int,
        token_types: list[str],
    ) -> None:
        expected_text = "PASS" if expected_pass else "FAIL"
        actual_text = "PASS" if actual_pass else "FAIL"
        expected_colored = self._style(expected_text, self.GREEN if expected_pass else self.RED, bold=True)
        actual_colored = self._style(actual_text, self.GREEN if actual_pass else self.RED, bold=True)
        cursor_text = self._style(f"{cursor_position}/{input_length}", self.CYAN)
        tokens_text = ", ".join(token_types) if token_types else "<none>"

        print(self._style(f"  debug case {case_number:02d}", self.YELLOW, bold=True), file=self.stream)
        print(f"  expected: {expected_colored}", file=self.stream)
        print(f"  actual:   {actual_colored}", file=self.stream)
        print(f"  cursor:   {cursor_text}", file=self.stream)
        print(f"  tokens:   {tokens_text}", file=self.stream)
        print(file=self.stream)

    def print_summary(self, total: int, passed: int, elapsed_seconds: float) -> None:
        failed = total - passed
        pass_rate = 0.0 if total == 0 else (passed / total) * 100
        elapsed_ms = elapsed_seconds * 1000

        summary_color = self.GREEN if failed == 0 else self.YELLOW
        passed_text = self._style(str(passed), self.GREEN, bold=True)
        failed_text = self._style(str(failed), self.RED, bold=True)
        pass_rate_text = self._style(f"{pass_rate:.1f}", summary_color, bold=True)
        elapsed_text = self._style(f"{elapsed_ms:.2f} ms ({elapsed_seconds:.4f} s)", self.CYAN)

        print(file=self.stream)
        print(self._style("Summary", self.CYAN, bold=True), file=self.stream)
        print(f"Total:  {total}", file=self.stream)
        print(f"Passed: {passed_text}", file=self.stream)
        print(f"Failed: {failed_text}", file=self.stream)
        print(f"Pass %: {pass_rate_text}", file=self.stream)
        print(f"Time:   {elapsed_text}", file=self.stream)