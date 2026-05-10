from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_kt0_constants_exist():
    text = read("src/constants/module_constants.py")
    for token in [
        "kt_slot_troop_o_val",
        "kt_slot_troop_d_val",
        "kt_slot_troop_h_val",
        "kt_slot_troop_type",
        "kt_troop_type_footsoldier",
        "kt_troop_type_cavalry",
        "kt_troop_type_archer",
        "kt_troop_type_mtdarcher",
    ]:
        assert token in text


def test_kt0_initializer_writes_compatible_slots():
    text = read("src/scripts/_preamble/00_imports.py")
    assert "kt_apply_doctrine_modifiers" in text
    assert "kt_slot_troop_o_val" in text
    assert "kt_slot_troop_d_val" in text
    assert "kt_slot_troop_h_val" in text
    assert "kt_slot_troop_type" in text
    assert "sod_faith" in text
    assert "imperial_" in text
    assert "slaver" in text


def test_kt0_battle_paths_use_siege_context():
    ai_battle = read("src/scripts/ZA_hardcoded_game_scripts/game_event_simulate_battle.py")
    order_attack = read("src/menus/encounter/order_attack_continue.py")
    castle_sim = read("src/menus/other/continue_15.py")

    assert '(assign, ":is_siege_atk", 2)' in ai_battle
    assert 'script_kt_party_calculate_strength", "p_collective_ally", 0, ":is_siege"' in ai_battle
    assert 'script_kt_party_calculate_strength", "p_collective_enemy", 0, ":is_siege_atk"' in ai_battle

    assert '(assign, ":is_siege_atk", 2)' in order_attack
    assert 'script_kt_party_calculate_strength", "p_main_party", 1, ":is_siege_atk"' in order_attack
    assert 'script_kt_party_calculate_strength", "p_collective_enemy", 0, ":is_siege_def"' in order_attack

    assert 'script_kt_party_calculate_strength_with_attachments", "p_main_party", 1, 2' in castle_sim
    assert 'script_kt_party_calculate_strength_with_attachments", "$g_encountered_party", 0, 1' in castle_sim
    assert "going to solver" not in castle_sim


def test_game_options_preserve_three_modes():
    text = read("src/menus/camp/game_options_2.py")
    assert "Kt0's Improved Autoresolve" in text
    assert "Blood Bath System" in text
    assert "Native System" in text
    assert '("game_options_autoresolve_1"' in text
    assert '("game_options_autoresolve_2"' in text
    assert '("game_options_autoresilve_3"' in text


def test_audit_exposes_kt0_report():
    text = read("build/audit_non_hero_troops.py")
    assert "KT0_OUT_PATH" in text
    assert "kt0_autoresolve_audit.md" in text
    assert "Autoresolve Balance Notes" in text
    assert "KT0 Top Pressure" in text
    assert "KT0 Watchlist" in text
    assert "write_kt0_report" in text
    assert "zero offense despite weapons" in text
    assert "horse/type mismatch" in text
    assert "extreme autoresolve outlier" in text


def test_generated_kt0_report_has_no_structural_failures():
    report = read("docs/reports/kt0_autoresolve_audit.md")
    assert "Combat rows with zero offense: 0" in report
    assert "Armored/shield rows with zero defense: 0" in report
    assert "Horse/type mismatches: 0" in report
    assert "KT0 Structural Issues" not in report


if __name__ == "__main__":
    test_kt0_constants_exist()
    test_kt0_initializer_writes_compatible_slots()
    test_kt0_battle_paths_use_siege_context()
    test_game_options_preserve_three_modes()
    test_audit_exposes_kt0_report()
    test_generated_kt0_report_has_no_structural_failures()
    print("KT0 autoresolve static checks passed")
