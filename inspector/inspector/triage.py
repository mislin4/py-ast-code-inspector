import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class TracebackDiagnostic:
    error_type: str
    error_message: str
    failed_line_number: Optional[int]
    target_symbol: Optional[str]


class TracebackTriage:
    """
    Python traceback ve stderr metinlerini ayrıştırarak
    hatanın tipini, satır numarasını ve hedef sembolünü çıkaran teşhis motoru.
    """

    @staticmethod
    def parse(stderr_text: str) -> TracebackDiagnostic:
        lines = [line.strip() for line in stderr_text.splitlines() if line.strip()]
        if not lines:
            return TracebackDiagnostic("UnknownError", "", None, None)

        last_line = lines[-1]
        error_type = "RuntimeError"
        error_message = last_line

        if ":" in last_line:
            parts = last_line.split(":", 1)
            error_type = parts[0].strip()
            error_message = parts[1].strip()

        # Satır numarası tespiti
        line_no = None
        for line in reversed(lines):
            match = re.search(r"File\s+.*?,\s+line\s+(\d+)", line)
            if match:
                line_no = int(match.group(1))
                break

        # Hata tipine göre ilgili değişken veya anahtar tespiti
        target_symbol = None
        if error_type == "KeyError":
            key_match = re.search(r"['\"]([^'\"]+)['\"]", error_message)
            if key_match:
                target_symbol = key_match.group(1)
        elif error_type == "NameError":
            name_match = re.search(r"name\s+['\"]([^'\"]+)['\"]\s+is not defined", error_message)
            if name_match:
                target_symbol = name_match.group(1)

        return TracebackDiagnostic(
            error_type=error_type,
            error_message=error_message,
            failed_line_number=line_no,
            target_symbol=target_symbol,
        )
