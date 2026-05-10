from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read_export_tokens() -> list[str]:
    raw = (ROOT / "_export" / "menus.txt").read_text(encoding="utf-8", errors="replace")
    return raw.split()


def _read_int(tokens: list[str], index: int, context: str) -> tuple[int, int]:
    assert index < len(tokens), f"EOF while reading {context} at token {index}"
    token = tokens[index]
    try:
        return int(token), index + 1
    except ValueError as exc:
        raise AssertionError(
            f"expected integer for {context} at token {index}, got {token!r}"
        ) from exc


def _skip_ops(tokens: list[str], index: int, count: int, context: str) -> int:
    for op_index in range(count):
        _, index = _read_int(tokens, index, f"{context} op-code #{op_index}")
        argc, index = _read_int(tokens, index, f"{context} op-argc #{op_index}")
        assert 0 <= argc <= 1000, f"suspicious argc {argc} in {context} op #{op_index}"
        index += argc
        assert index <= len(tokens), f"EOF while reading {context} op #{op_index} args"
    return index


def test_exported_menus_txt_is_token_parseable() -> None:
    tokens = _read_export_tokens()
    assert tokens[:3] == ["menusfile", "version", "1"]
    index = 3
    declared_count, index = _read_int(tokens, index, "menu count")
    menu_ids: list[str] = []

    for menu_index in range(declared_count):
        assert index < len(tokens), f"EOF before menu #{menu_index}"
        menu_id = tokens[index]
        assert menu_id.startswith("menu_"), (
            f"expected menu id at token {index} after {menu_index} menus, got {menu_id!r}"
        )
        menu_ids.append(menu_id)
        index += 1
        _, index = _read_int(tokens, index, f"{menu_id} flags")
        index += 2  # text, mesh
        menu_ops, index = _read_int(tokens, index, f"{menu_id} operation count")
        index = _skip_ops(tokens, index, menu_ops, f"{menu_id} menu ops")
        option_count, index = _read_int(tokens, index, f"{menu_id} option count")

        for option_index in range(option_count):
            assert index < len(tokens), f"EOF before {menu_id} option #{option_index}"
            option_id = tokens[index]
            assert option_id.startswith("mno_"), (
                f"expected option id for {menu_id} option #{option_index} at token "
                f"{index}, got {option_id!r}"
            )
            index += 1
            condition_ops, index = _read_int(
                tokens, index, f"{menu_id}/{option_id} condition count"
            )
            index = _skip_ops(
                tokens, index, condition_ops, f"{menu_id}/{option_id} conditions"
            )
            index += 1  # option text
            consequence_ops, index = _read_int(
                tokens, index, f"{menu_id}/{option_id} consequence count"
            )
            index = _skip_ops(
                tokens, index, consequence_ops, f"{menu_id}/{option_id} consequences"
            )
            index += 1  # door text

    assert index == len(tokens), f"unparsed trailing menu tokens: {len(tokens) - index}"
    duplicates = sorted({menu_id for menu_id in menu_ids if menu_ids.count(menu_id) > 1})
    assert not duplicates, f"duplicate exported menu id(s): {duplicates}"


def test_mb1011_hardcoded_start_menus_keep_native_indices() -> None:
    ids = (ROOT / "compile" / "ids" / "ID_menus.py").read_text(
        encoding="utf-8", errors="replace"
    )
    expected = {
        "menu_start_game_1": 0,
        "menu_start_phase_2": 1,
    }
    for menu_id, expected_index in expected.items():
        token = f"{menu_id} = {expected_index}"
        assert token in ids

    lines = (ROOT / "_export" / "menus.txt").read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()
    assert lines[2].startswith("menu_start_game_1 ")
    assert lines[4].startswith("menu_start_phase_2 ")


def test_quest_journal_report_uses_caret_breaks_not_literal_newlines() -> None:
    raw = (ROOT / "src" / "menus" / "camp" / "quest_journal_report.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert "Quest Journal^^[Active Log and Companion Arcs]" in raw
    assert "\\n" not in raw
