from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_village_defender_recovery_uses_modifier_profiles() -> None:
    defenders = read("src/scripts/ZD_centers/refresh_village_defenders.py")

    assert_contains(defenders, "script_sod_get_center_security_profile")
    assert_contains(defenders, "script_sod_get_center_garrison_policy")
    assert_contains(defenders, ":security_defense_bonus")
    assert_contains(defenders, ":garrison_policy_bonus")
    assert_contains(defenders, ":raid_resistance_bonus")
    assert_contains(defenders, ":recovery_relief")
    assert_contains(defenders, ":garrison_recovery")
    assert_not_contains(defenders, "slot_center_has_watch_tower")
    assert_not_contains(defenders, "slot_center_has_manor")
    assert_not_contains(defenders, "slot_center_has_ambulatory")


def test_looter_assault_building_math_uses_modifiers() -> None:
    raids = read("src/scripts/ZY_helper_scripts/sod_looter_village_raids.py")

    assert_contains(raids, "script_sod_get_center_security_profile")
    assert_contains(raids, "script_sod_get_center_garrison_policy")
    assert_contains(raids, "script_sod_get_center_food_profile")
    assert_contains(raids, "sod_center_modifier_health_recovery_flat")
    assert_contains(raids, ":garrison_recovery")
    assert_contains(raids, ":food_security")
    assert_contains(raids, ":health_recovery")
    assert_contains(raids, ":modifier_defense")
    assert_contains(raids, ":modifier_protection")

    assault_slice = raids[
        raids.index('"sod_looter_resolve_village_garrison_assault"') :
        raids.index('"sod_apply_village_garrison_assault_losses"')
    ]
    assert_not_contains(assault_slice, "slot_center_has_watch_tower")
    assert_not_contains(assault_slice, "slot_center_has_messenger_post")
    assert_not_contains(assault_slice, "slot_center_has_ambulatory")


def test_alarm_and_bandit_pressure_use_security_profile() -> None:
    alarms = read("src/scripts/ZY_helper_scripts/process_alarms.py")
    bandits = read("src/scripts/ZD_centers/update_villages_infested_by_bandits.py")
    buildings = read("src/constants/building_registry.py")

    assert_contains(alarms, "script_sod_get_center_security_profile")
    assert_contains(alarms, ":warning_range")
    assert_contains(alarms, "(val_add, \":spotting_range\", \":warning_range\")")
    assert_contains(alarms, "(ge, \":warning_range\", 1)")
    assert_not_contains(alarms, "slot_center_has_watch_tower")
    assert_not_contains(alarms, "slot_center_has_messenger_post")

    assert_contains(bandits, "script_sod_get_center_security_profile")
    assert_contains(bandits, ":bandit_reduction")
    assert_contains(bandits, ":bandit_infestation_chance")
    assert_contains(bandits, ":warning_range")
    assert_not_contains(bandits, "slot_center_has_watch_tower")
    assert_not_contains(bandits, "slot_center_has_messenger_post")
    assert_contains(buildings, "(\"warning_range_flat\", 1, \"watch_tower_lookouts\")")


def test_modifier_audit_doc_records_migration_rule() -> None:
    doc = read("docs/systems/CENTER_MODIFIER_SYSTEM_AUDIT.md")

    assert_contains(doc, "Use modifiers for math.")
    assert_contains(doc, "Use direct building slots for identity.")
    assert_contains(doc, "Village Defense Migration")
    assert_contains(doc, "Weekly building relation, prosperity, and renown effects now flow through")
    assert_contains(doc, "Palisade")


def test_weekly_building_cleanup_uses_modifier_totals() -> None:
    weekly_apply = read("src/scripts/ZI_campaign_ai/apply_weekly_building_effects.py")
    weekly_dispatch = read("src/triggers/ST04_weekly/entry_0018.py")
    university_inn = read("src/triggers/ST04_weekly/entry_0094.py")
    prisoner_tower = read("src/triggers/ST04_weekly/entry_0095.py")
    guild = read("src/triggers/ST04_weekly/entry_0096.py")
    mill = read("src/triggers/ST04_weekly/entry_0097.py")

    assert_contains(weekly_dispatch, "script_apply_weekly_building_effects")
    assert_contains(weekly_apply, "script_get_center_building_effect_totals")
    assert_contains(weekly_apply, ":weekly_relations")
    assert_contains(weekly_apply, ":weekly_prosperity")
    assert_contains(weekly_apply, ":weekly_renown")
    assert_contains(weekly_apply, "script_change_center_prosperity")
    assert_contains(weekly_apply, "script_change_troop_renown")
    assert_contains(weekly_apply, "slot_center_player_relation")

    assert_not_contains(university_inn, "$g_sod_building_university_renown")
    assert_not_contains(university_inn, "$g_sod_building_university_reputation")
    assert_not_contains(university_inn, "$g_sod_building_inn_reputation")
    assert_contains(university_inn, "script_change_center_health")
    assert_contains(university_inn, ":university_supply_roll")
    assert_contains(university_inn, ":inn_trade_surge_roll")

    assert_not_contains(prisoner_tower, "slot_center_player_relation")
    assert_contains(prisoner_tower, ":tower_order_roll")
    assert_contains(prisoner_tower, ":tower_confidence_roll")

    assert_not_contains(guild, "$g_sod_building_guild_prosperity")
    assert_not_contains(guild, "$g_sod_building_guild_reputation")
    assert_contains(guild, ":guild_food_boost")
    assert_contains(guild, ":guild_trade_surge_roll")

    assert_not_contains(mill, "$g_sod_building_mill_prosperity")
    assert_not_contains(mill, "slot_center_player_relation")
    assert_contains(mill, ":mill_food_boost")
    assert_contains(mill, ":mill_processing_roll")

    village_manor_inn = read("src/triggers/ST04_weekly/entry_0074.py")
    stables = read("src/triggers/ST04_weekly/entry_0092.py")
    chapter = read("src/triggers/ST04_weekly/entry_0093.py")

    assert_not_contains(village_manor_inn, "$g_sod_building_manor_renown")
    assert_not_contains(village_manor_inn, "$g_sod_building_inn_reputation")
    assert_contains(village_manor_inn, ":manor_stewardship_roll")
    assert_contains(village_manor_inn, ":inn_trade_roll")

    assert_not_contains(stables, "$g_sod_building_stables_renown")
    assert_contains(stables, ":stable_trade_roll")
    assert_contains(stables, ":stable_logistics_roll")

    assert_not_contains(chapter, "$g_sod_building_chapter_renown")
    assert_contains(chapter, ":chapter_stability_roll")


if __name__ == "__main__":
    test_village_defender_recovery_uses_modifier_profiles()
    test_looter_assault_building_math_uses_modifiers()
    test_alarm_and_bandit_pressure_use_security_profile()
    test_modifier_audit_doc_records_migration_rule()
    test_weekly_building_cleanup_uses_modifier_totals()
    print("test_center_modifier_migration_static: OK")
