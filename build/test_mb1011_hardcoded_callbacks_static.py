from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def test_warband_presentations_are_absent_for_mb1011() -> None:
    ids = read("compile/ids/ID_presentations.py")
    exported = read("_export/presentations.txt")
    order = read("src/presentations/_order_presentations.txt")
    assert_contains(ids, "prsnt_game_credits = 0")
    assert_contains(ids, "prsnt_banner_selection = 1")
    assert "0000_game_hardcoded_callbacks" not in order
    assert "9999_mb1011_game_presentation_stubs" not in order
    assert "prsnt_game_start" not in ids
    assert "prsnt_game_escape" not in ids
    assert "game_start " not in exported
    assert "game_escape " not in exported


def test_hardcoded_scripts_export_for_mb1011() -> None:
    ids = read("compile/ids/ID_scripts.py")
    exported = read("_export/scripts.txt")
    assert_contains(ids, "script_game_check_party_sees_party")
    assert_contains(ids, "script_game_get_party_speed_multiplier")
    assert_contains(exported, "game_check_party_sees_party -1")
    assert_contains(exported, "game_get_party_speed_multiplier -1")


def test_hardcoded_callback_sources_registered() -> None:
    presentations_order = read("src/presentations/_order_presentations.txt")
    presentation_raw = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in (ROOT / "src" / "presentations").rglob("*.py")
    )
    scripts_order = read("src/scripts/ZA_hardcoded_game_scripts/_order_za_scripts.txt")
    assert_contains(presentations_order, "0001_game_credits/game_credits.py")
    assert "game_hardcoded_callbacks" not in presentations_order
    assert '"game_start"' not in presentation_raw
    assert '"game_escape"' not in presentation_raw
    assert_contains(scripts_order, "ZA_hardcoded_game_scripts/game_check_party_sees_party.py")
    assert_contains(scripts_order, "ZA_hardcoded_game_scripts/game_get_party_speed_multiplier.py")
