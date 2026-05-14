from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_guarded_before(raw: str, message_token: str, guard_token: str, window: int = 260) -> None:
    idx = raw.find(message_token)
    assert idx >= 0, f"missing message token: {message_token}"
    before = raw[max(0, idx - window):idx]
    assert guard_token in before, f"{message_token!r} is not guarded by {guard_token!r}"


def test_looter_village_victory_companion_lines_use_correct_party_membership() -> None:
    raw = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    assert_guarded_before(raw, "Ymira watches the village road", '(main_party_has_troop, "trp_npc3")')
    assert_guarded_before(raw, "Bunduk counts the scattered looters", '(main_party_has_troop, "trp_npc10")')
    assert_guarded_before(raw, "Deshavi looks toward the tree line", '(main_party_has_troop, "trp_npc7")')


def test_looter_raid_aftermath_companion_lines_use_correct_party_membership() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    assert_guarded_before(raw, "Bunduk nods toward the smoke", '(main_party_has_troop, "trp_npc10")')
    assert_guarded_before(raw, "Ymira looks at the wounded villagers", '(main_party_has_troop, "trp_npc3")')
