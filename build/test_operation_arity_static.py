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
STR_STORE_STRING_WITH_EXTRA_ZERO = re.compile(
    r"\(str_store_string,\s*[^,\n]+,\s*\"[^\"]*\",\s*0\s*\)"
)
TWO_ARG_STORE_ARITHMETIC = re.compile(
    r"\((?:store_add|store_sub|store_mul|store_div|store_mod|min|max),\s*[^,\n]+,\s*[^,\n]+\s*\)"
)
MISSING_GET_SLOT_SLOT_ID = re.compile(
    r"\((?:party_get_slot|troop_get_slot|faction_get_slot|quest_get_slot),\s*"
    r"(?:\"[^\"]+\"|:[A-Za-z_]\w*|\$[A-Za-z_]\w*|reg\d+),\s*"
    r"(?:\"[^\"]+\"|:[A-Za-z_]\w*|\$[A-Za-z_]\w*)\s*\)"
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

        for match in STR_STORE_STRING_WITH_EXTRA_ZERO.finditer(text):
            offenders.append(f"{rel}:{_line_no(text, match.start())}: str_store_string has stray zero argument")

        for match in TWO_ARG_STORE_ARITHMETIC.finditer(text):
            offenders.append(f"{rel}:{_line_no(text, match.start())}: store arithmetic op has too few operands")

        for match in MISSING_GET_SLOT_SLOT_ID.finditer(text):
            offenders.append(f"{rel}:{_line_no(text, match.start())}: slot getter is missing a slot id")

    assert not offenders, "Malformed operation tuples found:\n" + "\n".join(offenders)


if __name__ == "__main__":
    main()
