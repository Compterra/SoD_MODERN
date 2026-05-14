from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    fief = read("src/presentations/0020_sod_fief_management/sod_fief_management.py")
    artifacts = read("src/presentations/0021_sod_royal_artifacts/sod_royal_artifacts.py")

    for token in [
        '(val_max, ":value", 1)',
        '(val_clamp, ":value", 1, "$pres_sod_fief_buildings")',
        '(val_clamp, ":value", 0, ":daily_garrisoning")',
        '(create_game_button_overlay, "$g_presentation_obj_4", "@>", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_5", "@<", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_8", "@>", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_9", "@<", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_14", "@<", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_15", "@>", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_17", "@<", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_18", "@>", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_20", "@<", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_21", "@>", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_27", "@>", tf_center_justify)',
        '(create_game_button_overlay, "$g_presentation_obj_28", "@<", tf_center_justify)',
        '(eq, ":object", "$g_presentation_obj_11")',
        '(display_message, "@Not enough funds.", dark_red)',
        'script_sod_get_center_construction_quote',
        "@Set the garrison limit.",
        "@Set how many recruits this center's trainers can add daily.",
        "@Set this center's trainer count.",
    ]:
        assert token in fief, f"missing fief presentation slider hardening: {token}"

    for token in [
        "slot_center_has_barracks1",
        "slot_center_has_barracks2",
        "slot_center_has_barracks3",
        "slot_center_has_barracks4",
        "slot_center_has_barracks5",
        "slot_center_has_range1",
        "slot_center_has_range2",
        "slot_center_has_range3",
        "slot_center_has_range4",
        "slot_center_has_range5",
        "Garrisoning impossible",
    ]:
        assert token not in fief, f"stale fief presentation garrison block remains: {token}"

    for token in [
        '(gt, ":mission_heroes", 0)',
        '(store_troop_gold, ":player_gold", "trp_player")',
        '(ge, ":player_gold", ":mission_gold")',
        '(party_count_members_of_type, ":available_heroes", "p_main_party", "$sod_royal_hero")',
        '(ge, ":available_heroes", ":mission_heroes")',
    ]:
        assert token in artifacts, f"missing royal artifact send validation: {token}"

    print("Presentation hardening static checks passed")


if __name__ == "__main__":
    main()
