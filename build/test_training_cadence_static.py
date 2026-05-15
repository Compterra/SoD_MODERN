from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def main() -> None:
    center_training = read("src/triggers/ST03_daily/entry_0134.py")
    center_training_helper = read("src/scripts/ZD_centers/sod_center_training_maintenance.py")
    party_training = read("src/triggers/ST03_daily/entry_0021.py")
    party_training_helper = read("src/scripts/ZC_parties/sod_party_training_maintenance.py")
    retinues = read("src/scripts/ZC_parties/sod_companion_retinues.py")
    doc = read("docs/company/TRAINING_CADENCE_DESIGN.md")
    skills = read("compile/module_skills.py")

    assert_contains(center_training, "(6,")
    assert_contains(center_training, 'script_sod_center_process_trainer_xp_pulse')
    assert_not_contains(center_training, "try_for_range")
    assert_contains(center_training_helper, '"sod_center_process_trainer_xp_pulse"')
    assert_contains(center_training_helper, '(party_slot_eq, ":cur_center", slot_town_lord, "trp_player")')
    assert_contains(center_training_helper, '(party_get_slot, ":trainers", ":cur_center", slot_center_trainers)')
    assert_contains(center_training_helper, '(store_mul, ":exp", ":trainers", ":stack_size")')
    assert_contains(center_training_helper, "slot_center_has_barracks")
    assert_contains(center_training_helper, "slot_center_has_range")
    assert_contains(center_training_helper, "slot_center_has_stables")
    assert_contains(center_training_helper, '(party_upgrade_with_xp, ":cur_center", 1, 1)')
    assert_not_contains(center_training, '(val_mul, ":trainers", 4)')
    assert_not_contains(center_training_helper, '(val_mul, ":trainers", 4)')
    assert_contains(party_training, "(48,")
    assert_contains(party_training, "script_sod_party_process_hero_and_garrison_training_xp")
    assert_not_contains(party_training, "try_for_range")
    for token in [
        '"sod_party_process_hero_and_garrison_training_xp"',
        "chance_hero_party_gain_extra_xp",
        "chance_garrison_gain_extra_xp",
        "store_character_level, \":player_level\", \"trp_player\"",
        "store_skill_level, \":trainer_level\", skl_trainer",
        "(val_add, \":trainer_level\", 2)",
        "(val_div, \":player_level\", 4)",
        "(store_mul, \":xp_gain\", \":trainer_level\", 500)",
        "script_cf_party_upgrade_with_xp",
        "walled_centers_begin, walled_centers_end",
        "(neq, \":center_lord\", \"trp_player\")",
        '":center_no", 3000',
    ]:
        assert_contains(party_training_helper, token)

    training = retinues[
        retinues.index('"sod_companion_retinue_apply_training"') :
        retinues.index('"sod_companion_retinue_get_account_totals_to_regs"')
    ]
    assert_contains(training, '(ge, ":hours_since_training", 6)')
    assert_contains(training, '(val_div, ":stack_xp", 4)')
    assert_contains(training, '(val_max, ":stack_xp", 1)')
    assert_contains(training, 'party_add_xp_to_stack, ":retinue_party", ":stack_no", ":stack_xp"')

    assert_contains(retinues, "last drill {reg29} xp")
    assert_not_contains(retinues, "training last day {reg29} xp")
    assert_contains(doc, "native player-party Trainer pulse does not appear as editable module-source logic")
    assert_contains(doc, "Fire every 6 hours.")
    assert_contains(doc, "Apply roughly one quarter of the old daily training XP each pulse.")
    assert_contains(skills, "Every day, each hero with this skill adds some experience")
    assert_contains(skills, "{0,4,10,16,23,30,38,46,55,65,80}")
    assert_not_contains(retinues, "sod_apply_player_party_training_interval")
    assert_not_contains(center_training, "sod_apply_player_party_training_interval")
    assert_not_contains(center_training_helper, "sod_apply_player_party_training_interval")
    assert_not_contains(party_training_helper, "sod_apply_player_party_training_interval")

    print("test_training_cadence_static: OK")


if __name__ == "__main__":
    main()
