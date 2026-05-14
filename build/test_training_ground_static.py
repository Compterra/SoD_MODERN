from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_SCRIPT = ROOT / "src" / "scripts" / "ZI_campaign_ai" / "cf_training_ground_sub_routine_for_training_result.py"
START_SCRIPT = ROOT / "src" / "scripts" / "ZI_campaign_ai" / "start_training_at_training_ground.py"
RESULT_MENU = ROOT / "src" / "menus" / "training" / "training_ground_training_result.py"


def main() -> None:
    result_source = RESULT_SCRIPT.read_text(encoding="utf-8")
    start_source = START_SCRIPT.read_text(encoding="utf-8")
    result_menu = RESULT_MENU.read_text(encoding="utf-8")

    assert '("cf_training_ground_sub_routine_for_training_result",' in result_source
    assert '(store_mul, ":xp_ratio_to_add_for_stack", ":xp_ratio_to_add", ":hardness_dif")' in result_source
    assert '(val_div, ":xp_ratio_to_add_for_stack", 1000)' in result_source
    assert '(assign, reg0, ":random_xp_to_add")' in result_source

    assert '("start_training_at_training_ground",' in start_source
    assert '(assign, "$scene_num_total_gourds_destroyed", 0)' in start_source
    assert '(set_visitor, 0, "trp_player")' in start_source
    assert '(jump_to_menu, "mnu_training_ground_description")' in start_source

    assert '("training_ground_training_result", mnf_disable_all_keys,' in result_menu
    assert '(store_mul, ":xp_ratio_to_add", "$g_training_ground_training_success_ratio", "$g_training_ground_training_success_ratio")' in result_menu
    assert '(store_mul, ":xp_ratio_to_add_with_trainer_skill", ":xp_ratio_to_add", ":trainer_skill_multiplier")' in result_menu
    assert '(call_script, "script_cf_training_ground_sub_routine_for_training_result", "trp_player", -1, 1, ":xp_ratio_to_add")' in result_menu

    stale_needles = [
        "Hardness difference:",
        '##     (assign, reg0, ":hardness_dif")',
        '##       (assign, reg0, ":xp_ratio_to_add")',
        "xp earn ratio:",
        "$g_training_ground_training_troop_stack_index",
    ]
    combined = result_source + "\n" + start_source + "\n" + result_menu
    for needle in stale_needles:
        assert needle not in combined, needle

    print("test_training_ground_static: OK")


if __name__ == "__main__":
    main()
