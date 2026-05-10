from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dialogue_sources_do_not_use_literal_newline_escapes() -> None:
    offenders: list[str] = []
    for path in (ROOT / "src" / "dialogs").rglob("*.py"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "\\n" in raw:
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, "dialogue source files contain literal newline escapes: " + ", ".join(offenders)


def test_exported_conversation_record_count_matches_header() -> None:
    lines = (ROOT / "_export" / "conversation.txt").read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()
    assert lines[0] == "dialogsfile version 1"
    declared_count = int(lines[1])
    records = [line for line in lines[2:] if line.strip()]
    assert len(records) == declared_count


def test_exported_conversation_records_stay_on_single_physical_lines() -> None:
    lines = (ROOT / "_export" / "conversation.txt").read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()
    bad_records = [
        (index + 3, line[:120])
        for index, line in enumerate(lines[2:])
        if line.strip() and not line.startswith("dlga_")
    ]
    assert not bad_records, f"malformed conversation records: {bad_records[:5]}"
