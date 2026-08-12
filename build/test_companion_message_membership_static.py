from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_guarded_before(raw: str, message_token: str, guard_token: str, window: int = 260) -> None:
    idx = raw.find(message_token)
    assert idx >= 0, f"missing message token: {message_token}"
    before = raw[max(0, idx - window):idx]
    assert guard_token in before, f"{message_token!r} is not guarded by {guard_token!r}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"unexpected token: {token}"


def script_body(raw: str, script_name: str, next_script_name: str | None = None) -> str:
    start = raw.find(f'("{script_name}"')
    assert start >= 0, f"missing script: {script_name}"
    if next_script_name:
        end = raw.find(f'("{next_script_name}"', start + 1)
    else:
        match = re.search(r'\n\("[^"]+",\n \[', raw[start + 1:])
        end = start + 1 + match.start() if match else len(raw)
    assert end > start, f"could not isolate script: {script_name}"
    return raw[start:end]


def test_companion_tavern_refresh_does_not_emit_debug_log_messages() -> None:
    raw = read("src/scripts/ZH_heroes/update_companion_candidates_in_taverns.py")
    assert_not_contains(raw, "Companion tavern debug")
    assert_not_contains(raw, "(display_message")
    assert_not_contains(raw, '"script_store_troop_name_link", 4')
    assert_not_contains(raw, "str_store_party_name_link, 5")


def test_auto_loot_does_not_ship_debug_log_messages() -> None:
    raw = read("src/scripts/ZZ_common_array_processing/auto_loot_all.py")
    assert_not_contains(raw, "Auto-loot debug")
    assert_not_contains(raw, "debug_color")


def test_looter_village_victory_companion_lines_use_correct_party_membership() -> None:
    raw = read("src/scripts/ZC_parties/event_player_defeated_enemy_party.py")
    assert_guarded_before(raw, "Ymira watches the village road", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc3")')
    assert_guarded_before(raw, "Bunduk counts the scattered looters", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")')
    assert_guarded_before(raw, "Deshavi looks toward the tree line", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc7")')


def test_looter_raid_aftermath_companion_lines_use_correct_party_membership() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")
    assert_guarded_before(raw, "Bunduk nods toward the smoke", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")')
    assert_guarded_before(raw, "Ymira looks at the wounded villagers", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc3")')


def test_mini_faction_companion_lines_use_correct_party_membership() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_mini_faction_incidents.py")
    assert_guarded_before(raw, "Bunduk says stretched hearth guards", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")')


def test_post_battle_companion_lines_use_shared_membership_helper() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_companion_post_battle_comment.py")
    assert_not_contains(raw, "main_party_has_troop")
    assert_guarded_before(raw, "Bunduk counts the missing voices", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")')
    assert_guarded_before(raw, "Bunduk keeps his voice low", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")')
    assert_guarded_before(raw, "Bunduk watches the ranks flinch", '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")')


def test_companion_presence_helper_requires_main_party_has_troop_and_count() -> None:
    raw = read("src/scripts/ZH_heroes/cf_sod_companion_in_main_party.py")
    assert "(main_party_has_troop, \":companion\")" in raw
    assert "(party_count_companions_of_type, \":companion_count\", \"p_main_party\", \":companion\")" in raw
    assert "(gt, \":companion_count\", 0)" in raw
    assert '"cf_sod_any_companion_in_main_party"' in raw
    assert "(eq, \":found\", 1)" in raw


def test_companion_depth_named_reactions_do_not_use_any_companion_gate() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    assert_not_contains(raw, "script_cf_sod_any_companion_in_main_party")


def test_triangle_quest_recording_requires_all_named_companions_present() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_companion_depth.py")
    body = script_body(raw, "sod_companion_record_triangle_quest_event", "sod_companion_assign_role")
    for companion in (":companion_a", ":companion_b", ":companion_c"):
        assert_guarded_before(body, f'script_sod_companion_sync_personal_quest_framework", "{companion}"', f'(call_script, "script_cf_sod_companion_in_main_party", "{companion}")', window=420)
    assert "(call_script, \"script_sod_quest_journal_update\")" in body


def test_company_and_prisoner_companion_hooks_use_shared_membership_helper() -> None:
    company = read("src/scripts/ZY_helper_scripts/sod_company_troop_dialogue.py")
    prisoner = read("src/scripts/ZY_helper_scripts/sod_prisoner_economy.py")
    assert_not_contains(company, "main_party_has_troop")
    assert_not_contains(prisoner, "main_party_has_troop")
    assert '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")' in company
    assert '(call_script, "script_cf_sod_companion_in_main_party", "trp_npc10")' in prisoner


if __name__ == "__main__":
    test_companion_tavern_refresh_does_not_emit_debug_log_messages()
    test_auto_loot_does_not_ship_debug_log_messages()
    test_looter_village_victory_companion_lines_use_correct_party_membership()
    test_looter_raid_aftermath_companion_lines_use_correct_party_membership()
    test_mini_faction_companion_lines_use_correct_party_membership()
    test_post_battle_companion_lines_use_shared_membership_helper()
    test_companion_presence_helper_requires_main_party_has_troop_and_count()
    test_companion_depth_named_reactions_do_not_use_any_companion_gate()
    test_triangle_quest_recording_requires_all_named_companions_present()
    test_company_and_prisoner_companion_hooks_use_shared_membership_helper()
    print("test_companion_message_membership_static: OK")
