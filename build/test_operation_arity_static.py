from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

ONE_ARG_COMPARISON = re.compile(
    r"\((?:eq|neq|gt|ge|lt|le),\s*(?:\"[^\"]+\"|:[A-Za-z_]\w*|\$[A-Za-z_]\w*)\s*\)"
)
ONE_ARG_ASSIGN = re.compile(
    r"\(assign,\s*(?:\"[^\"]+\"|:[A-Za-z_]\w*|\$[A-Za-z_]\w*|reg\d+)\s*\)"
)
ASSIGN_WITH_EXTRA_DEBUG_COLOR = re.compile(
    r"\(assign,\s*[^,\n]+,\s*[^,\n]+,\s*debug_color\s*\)"
)


def _line_no(text, pos):
    return text.count("\n", 0, pos) + 1


def main():
    offenders = []

    for path in sorted(SRC.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)

        for match in ONE_ARG_COMPARISON.finditer(text):
            offenders.append(f"{rel}:{_line_no(text, match.start())}: one-argument comparison {match.group(0)}")

        for match in ONE_ARG_ASSIGN.finditer(text):
            offenders.append(f"{rel}:{_line_no(text, match.start())}: one-argument assign {match.group(0)}")

        for match in ASSIGN_WITH_EXTRA_DEBUG_COLOR.finditer(text):
            offenders.append(f"{rel}:{_line_no(text, match.start())}: assign has stray debug_color argument")

    assert not offenders, "Malformed operation tuples found:\n" + "\n".join(offenders)


if __name__ == "__main__":
    main()
