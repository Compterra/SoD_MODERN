# -*- coding: cp1254 -*-

from src.constants.module_constants import *
from src.constants.center_modifier_registry import (
    CENTER_MODIFIER_BY_KEY,
    BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER,
    BUILDING_FIELD_TO_CENTER_MODIFIER,
    derive_building_center_modifiers,
    normalize_center_modifier_entries,
)

try:
    integer_types = (int, long)
except NameError:
    integer_types = (int,)


SUPPORTED_BUILDING_SPECIALIZATIONS = (
    "economic",
    "military",
    "religious",
    "civic",
    "defensive",
    "population_health",
)

BUILDING_SPECIALIZATION_LABELS = {
    "economic": "Economic",
    "military": "Military",
    "religious": "Religious",
    "civic": "Civic",
    "defensive": "Defensive",
    "population_health": "Population Health",
}

SUPPORTED_BUILDING_ROLES = (
    "food_security",
    "trade_liquidity",
    "production",
    "population_capacity",
    "population_growth",
    "health_recovery",
    "raid_recovery",
    "security",
    "military_training",
    "construction_efficiency",
    "faith_support",
    "unrest_control",
    "administration",
    "noble_recruitment",
    "prisoner_control",
    "communications",
    "renown",
)

BUILDING_ROLE_LABELS = {
    "food_security": "Food Security",
    "trade_liquidity": "Trade Liquidity",
    "production": "Production",
    "population_capacity": "Population Capacity",
    "population_growth": "Population Growth",
    "health_recovery": "Health Recovery",
    "raid_recovery": "Raid Recovery",
    "security": "Security",
    "military_training": "Military Training",
    "construction_efficiency": "Construction Efficiency",
    "faith_support": "Faith Support",
    "unrest_control": "Unrest Control",
    "administration": "Administration",
    "noble_recruitment": "Noble Recruitment",
    "prisoner_control": "Prisoner Control",
    "communications": "Communications",
    "renown": "Renown",
}

LEGACY_BUILDING_SCRIPT_EFFECT_EXCEPTIONS = (
    "badboy_decay",
    "faith_world_drift",
    "noble_gathering",
    "player_message_text",
)


def _string_types():
    try:
        return (basestring,)
    except NameError:
        return (str,)


def _is_string(value):
    return isinstance(value, _string_types())


def _is_integer(value):
    return isinstance(value, integer_types)


def _normalize_tuple(value):
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if value == "":
        return ()
    return (value,)


def _merge_center_modifier_entries(entries):
    totals = {}
    sources = {}
    order = []
    for entry in entries:
        if len(entry) < 2:
            continue
        modifier_key = entry[0]
        value = entry[1]
        source = entry[2] if len(entry) > 2 else "building"
        if modifier_key not in totals:
            totals[modifier_key] = 0
            sources[modifier_key] = []
            order.append(modifier_key)
        totals[modifier_key] += value
        if source not in sources[modifier_key]:
            sources[modifier_key].append(source)
    return tuple((modifier_key, totals[modifier_key], "+".join(sources[modifier_key])) for modifier_key in order)


def _normalize_text(value, fallback=""):
    if value is None:
        return fallback
    return value


def _normalize_display_text(value, fallback=""):
    normalized_value = _normalize_text(value, fallback)
    if _is_string(normalized_value) and normalized_value.startswith("@"):
        return normalized_value[1:]
    return normalized_value


def _build_slot_label(slot_name):
    if slot_name is None:
        return ""
    return slot_name.replace("_", " ").title()


def get_building_display_name_text(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return _build_slot_label(building_slot)

    display_name = building.get("display_name")
    if not display_name:
        return _build_slot_label(building.get("building_key") or building_slot)
    if _is_string(display_name) and display_name.startswith("str_"):
        return _build_slot_label(building.get("building_key") or display_name)

    return _normalize_display_text(display_name)


def get_building_category_label(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ""

    category = building.get("ui_category") or building.get("category")
    if not category:
        return ""

    if _is_string(category):
        return category.replace("_", " ").title()

    return str(category)


def get_building_specialization_label(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ""

    specialization = building.get("specialization")
    if not specialization:
        return ""

    return BUILDING_SPECIALIZATION_LABELS.get(specialization, _build_slot_label(specialization))


def get_building_roles(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ()
    return _normalize_tuple(building.get("building_roles"))


def get_building_role_labels(building_slot):
    return tuple(BUILDING_ROLE_LABELS.get(role, _build_slot_label(role)) for role in get_building_roles(building_slot))


def building_has_role(building_slot, role):
    return role in get_building_roles(building_slot)


def get_building_build_duration(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return 0

    if building.get("build_days") is not None:
        return building.get("build_days")
    if building.get("build_hours") is not None:
        return building.get("build_hours")
    return 0


def _build_registry_entry(
    building_slot,
    building_key,
    name_string_id=None,
    name_text=None,
    description_string_id=None,
    description_text=None,
    cost=0,
    build_hours=None,
    build_days=None,
    allowed_center_types=(),
    prerequisite_buildings=(),
    prerequisite_any_buildings=(),
    conflicts_with=(),
    effect_tags=(),
    effect_numbers=(),
    ui_category="",
    effect_summary=None,
    is_unique=True,
    is_upgradable=False,
    affects_village=False,
    affects_town=False,
    affects_castle=False,
    specialization=None,
    tier=0,
    upgrade_from=(),
    upgrade_to=(),
    exclusive_group=None,
    weekly_upkeep=0,
    faction_requirements=(),
    faction_flavor="",
    design_summary=None,
    short_description_text=None,
    failure_reason_text=None,
    center_health_bonus=0,
    prosperity_multiplier_bonus_percent=0,
    prosperity_cap_bonus=0,
    demesne_cost=0,
    weekly_renown_bonus=0,
    weekly_prosperity_bonus=0,
    weekly_income_bonus_percent=0,
    population_capacity_bonus=0,
    weekly_population_growth_bonus=0,
    raid_recovery_bonus=0,
    building_roles=(),
    center_modifiers=None,
):
    effect_tags = tuple(effect_tags)
    effect_numbers = tuple(effect_numbers)
    building_roles = _normalize_tuple(building_roles)
    if effect_summary is None:
        effect_summary = short_description_text if short_description_text is not None else (description_text if description_text is not None else description_string_id)
    if short_description_text is None:
        short_description_text = effect_summary if effect_summary is not None else description_text
    if design_summary is None:
        design_summary = short_description_text if short_description_text is not None else (effect_summary if effect_summary is not None else description_text)
    if build_days is None and build_hours is not None:
        build_days = build_hours

    entry = {
        "building_slot": building_slot,
        "slot": building_slot,
        "building_key": building_key,
        "key": building_key,
        "name_string_id": name_string_id,
        "name_text": name_text,
        "description_string_id": description_string_id,
        "description_text": description_text,
        "cost": cost,
        "build_hours": build_hours,
        "build_days": build_days,
        "allowed_center_types": tuple(allowed_center_types),
        "prerequisite_buildings": tuple(prerequisite_buildings),
        "prerequisite_any_buildings": tuple(prerequisite_any_buildings),
        "conflicts_with": tuple(conflicts_with),
        "effect_tags": effect_tags,
        "effect_numbers": effect_numbers,
        "ui_category": ui_category,
        "category": ui_category,
        "display_name_kind": "string_id" if name_string_id is not None else "text",
        "display_name": name_string_id if name_string_id is not None else name_text,
        "description_kind": "string_id" if description_string_id is not None else "text",
        "description": description_string_id if description_string_id is not None else description_text,
        "effect_summary": effect_summary,
        "short_description_text": short_description_text,
        "short_description": short_description_text if short_description_text is not None else description_text,
        "failure_reason_text": failure_reason_text,
        "failure_reason": failure_reason_text if failure_reason_text is not None else "",
        "is_unique": is_unique,
        "is_upgradable": is_upgradable,
        "runtime_effects": tuple((effect_tags[i], effect_numbers[i]) for i in range(len(effect_tags))),
        "affects_village": affects_village,
        "affects_town": affects_town,
        "affects_castle": affects_castle,
        "specialization": specialization,
        "tier": tier,
        "upgrade_from": tuple(upgrade_from),
        "upgrade_to": tuple(upgrade_to),
        "exclusive_group": exclusive_group,
        "weekly_upkeep": weekly_upkeep,
        "faction_requirements": tuple(faction_requirements),
        "faction_flavor": faction_flavor,
        "design_summary": design_summary,
        "center_health_bonus": center_health_bonus,
        "prosperity_multiplier_bonus_percent": prosperity_multiplier_bonus_percent,
        "prosperity_cap_bonus": prosperity_cap_bonus,
        "demesne_cost": demesne_cost,
        "weekly_renown_bonus": weekly_renown_bonus,
        "weekly_prosperity_bonus": weekly_prosperity_bonus,
        "weekly_income_bonus_percent": weekly_income_bonus_percent,
        "population_capacity_bonus": population_capacity_bonus,
        "weekly_population_growth_bonus": weekly_population_growth_bonus,
        "raid_recovery_bonus": raid_recovery_bonus,
        "building_roles": building_roles,
        "roles": building_roles,
    }
    if center_modifiers is None:
        center_modifiers = derive_building_center_modifiers(entry)
    else:
        center_modifiers = derive_building_center_modifiers(entry) + normalize_center_modifier_entries(center_modifiers)
    center_modifiers = _merge_center_modifier_entries(center_modifiers)
    entry["center_modifiers"] = center_modifiers
    entry["modifiers"] = center_modifiers
    return entry


def _text_building(
    building_slot,
    building_key,
    ui_category,
    allowed_center_types,
    cost,
    display_name,
    description_text,
    effect_summary=None,
    build_hours=None,
    build_days=None,
    prerequisite_buildings=(),
    conflicts_with=(),
    effect_tags=(),
    effect_numbers=(),
    is_unique=True,
    is_upgradable=False,
    affects_village=False,
    affects_town=False,
    affects_castle=False,
    specialization=None,
    tier=0,
    upgrade_from=(),
    upgrade_to=(),
    exclusive_group=None,
    weekly_upkeep=0,
    faction_requirements=(),
    faction_flavor="",
    design_summary=None,
    **kwargs
):
    return _build_registry_entry(
        building_slot,
        building_key,
        name_text=display_name,
        description_text=description_text,
        cost=cost,
        build_hours=build_hours,
        build_days=build_days,
        allowed_center_types=allowed_center_types,
        prerequisite_buildings=prerequisite_buildings,
        conflicts_with=conflicts_with,
        effect_tags=effect_tags,
        effect_numbers=effect_numbers,
        ui_category=ui_category,
        effect_summary=effect_summary if effect_summary is not None else description_text,
        is_unique=is_unique,
        is_upgradable=is_upgradable,
        affects_village=affects_village,
        affects_town=affects_town,
        affects_castle=affects_castle,
        specialization=specialization,
        tier=tier,
        upgrade_from=upgrade_from,
        upgrade_to=upgrade_to,
        exclusive_group=exclusive_group,
        weekly_upkeep=weekly_upkeep,
        faction_requirements=faction_requirements,
        faction_flavor=faction_flavor,
        design_summary=design_summary,
        **kwargs
    )


def _string_id_building(
    building_slot,
    building_key,
    ui_category,
    allowed_center_types,
    cost,
    name_string_id,
    description_string_id,
    description_text=None,
    effect_summary=None,
    build_hours=None,
    build_days=None,
    prerequisite_buildings=(),
    conflicts_with=(),
    effect_tags=(),
    effect_numbers=(),
    is_unique=True,
    is_upgradable=False,
    affects_village=False,
    affects_town=False,
    affects_castle=False,
    specialization=None,
    tier=0,
    upgrade_from=(),
    upgrade_to=(),
    exclusive_group=None,
    weekly_upkeep=0,
    faction_requirements=(),
    faction_flavor="",
    design_summary=None,
    **kwargs
):
    return _build_registry_entry(
        building_slot,
        building_key,
        name_string_id=name_string_id,
        description_string_id=description_string_id,
        description_text=description_text,
        cost=cost,
        build_hours=build_hours,
        build_days=build_days,
        allowed_center_types=allowed_center_types,
        prerequisite_buildings=prerequisite_buildings,
        conflicts_with=conflicts_with,
        effect_tags=effect_tags,
        effect_numbers=effect_numbers,
        ui_category=ui_category,
        effect_summary=effect_summary if effect_summary is not None else description_text,
        is_unique=is_unique,
        is_upgradable=is_upgradable,
        affects_village=affects_village,
        affects_town=affects_town,
        affects_castle=affects_castle,
        specialization=specialization,
        tier=tier,
        upgrade_from=upgrade_from,
        upgrade_to=upgrade_to,
        exclusive_group=exclusive_group,
        weekly_upkeep=weekly_upkeep,
        faction_requirements=faction_requirements,
        faction_flavor=faction_flavor,
        design_summary=design_summary,
        **kwargs
    )


BUILDING_REGISTRY = [
    _text_building(slot_center_has_manor, "manor", "village_economy", ("village",), 2000, "@Manor", "@A village manor improves hospitality, legal order, and work coordination. Weekly Renown +3, Fief's Demesne Cost -2.", effect_tags=("weekly_renown", "demesne_cost", "population_capacity", "weekly_population_growth"), effect_numbers=(3, -2, 100, 1), affects_village=True, specialization="civic", tier=1, weekly_upkeep=5, short_description_text="Village administration, hospitality, and household stability.", design_summary="Village administration, hospitality, work coordination, and household stability.", center_health_bonus=5, prosperity_multiplier_bonus_percent=10, weekly_renown_bonus=3, demesne_cost=2, population_capacity_bonus=100, weekly_population_growth_bonus=1, building_roles=("administration", "population_capacity", "population_growth", "renown", "construction_efficiency"), center_modifiers=(("administration_flat", 8, "manor_local_administration"), ("construction_speed_pct", 10, "manor_work_coordination"), ("migration_retention_flat", 6, "manor_household_stability"))),
    _text_building(slot_center_has_mill, "mill", "village_economy", ("village",), 2500, "@Mill", "@A mill improves village food processing, income, and long-term prosperity. Weekly Prosperity +1, Prosperity Cap +20, Weekly Taxes +10%.", effect_tags=("weekly_prosperity", "prosperity_cap", "weekly_taxes_percent", "population_capacity"), effect_numbers=(1, 20, 10, 80), affects_village=True, specialization="economic", tier=1, weekly_upkeep=10, short_description_text="Village grain processing, food security, and prosperity.", design_summary="Village grain processing, food security, production, and prosperity.", center_health_bonus=5, prosperity_multiplier_bonus_percent=20, prosperity_cap_bonus=20, weekly_prosperity_bonus=1, weekly_income_bonus_percent=10, population_capacity_bonus=80, building_roles=("food_security", "production", "population_capacity", "trade_liquidity"), center_modifiers=(("food_security_flat", 30, "mill_food_processing"), ("food_store_capacity_flat", 120, "mill_storage"), ("goods_export_supply_pct", 10, "mill_surplus_grain"), ("trade_liquidity_flat", 20, "mill_market_flow"))),
    _text_building(slot_center_has_watch_tower, "watch_tower", "village_defense", ("village",), 1200, "@Watch Tower", "@A watch tower lets villagers raise alarms earlier and organize raid recovery. The time it takes for enemies to loot the village increases by 25%. Village's Demesne Cost -1.", effect_tags=("loot_time_bonus_percent", "demesne_cost", "raid_recovery"), effect_numbers=(25, -1, 1), affects_village=True, specialization="defensive", tier=1, weekly_upkeep=5, design_summary="Early warning, local defense, patrol response, and faster post-raid regrouping.", demesne_cost=1, raid_recovery_bonus=1, building_roles=("security", "raid_recovery", "communications"), center_modifiers=(("security_flat", 15, "watch_tower_alarm_network"), ("threat_reduction_flat", 20, "watch_tower_scouting"), ("bandit_spawn_reduction_pct", 8, "watch_tower_visibility"), ("warning_range_flat", 1, "watch_tower_lookouts"), ("patrol_response_pct", 10, "watch_tower_signals"))),
    _text_building(slot_center_has_inn, "inn", "village_civic", ("village",), 2000, "@Inn", "@An inn increases local loyalty, travel, migration, and market exchange. Weekly Relations +2.", effect_tags=("weekly_loyalty", "weekly_population_growth"), effect_numbers=(2, 1), affects_village=True, specialization="civic", tier=1, weekly_upkeep=10, design_summary="A social hub for travelers, locals, returning families, and small traders.", weekly_population_growth_bonus=1, building_roles=("population_growth", "trade_liquidity", "unrest_control"), center_modifiers=(("trade_liquidity_flat", 25, "inn_travel_trade"), ("migration_attraction_flat", 8, "inn_returning_families"), ("migration_retention_flat", 4, "inn_local_ties"), ("unrest_reduction_flat", 4, "inn_social_pressure"))),
    _string_id_building(slot_center_has_shrine, "shrine", "faith", ("village",), 1000, "str_sod_shrine_0", "str_sod_temple_0_description", description_text="@Weekly Relations +1, Weekly Local Faith +3, Weekly Global Faith +2.", effect_tags=("weekly_relations", "weekly_local_faith", "weekly_global_faith"), effect_numbers=(1, 3, 2), affects_village=True, specialization="religious", tier=1, upgrade_to=(slot_center_has_monastery,), exclusive_group="village_religious_progression", weekly_upkeep=5, faction_flavor="Village shrine and pilgrim stop.", design_summary="A small village shrine that steadies faith, local order, and post-crisis morale before it can become a monastery.", building_roles=("faith_support", "unrest_control"), center_modifiers=(("faith_stability_flat", 8, "shrine_local_rites"), ("unrest_reduction_flat", 3, "shrine_moral_order"), ("migration_retention_flat", 3, "shrine_community_identity"))),
    _string_id_building(slot_center_has_monastery, "monastery", "faith", ("village",), 2000, "str_sod_monastery_0", "str_sod_temple_0_description", description_text="@Weekly Taxes +5%, Weekly Local Faith +2, Weekly Global Faith +2.", effect_tags=("weekly_taxes_percent", "weekly_local_faith", "weekly_global_faith", "population_capacity"), effect_numbers=(5, 2, 2, 60), affects_village=True, specialization="religious", tier=2, prerequisite_buildings=(slot_center_has_shrine,), upgrade_from=(slot_center_has_shrine,), exclusive_group="village_religious_progression", weekly_upkeep=20, faction_flavor="Village monastic estate and spiritual center.", center_health_bonus=5, design_summary="An expanded monastic complex that supersedes a shrine with charity, schooling, records, and stable farm households.", population_capacity_bonus=60, building_roles=("faith_support", "population_capacity", "unrest_control", "administration"), center_modifiers=(("faith_stability_flat", 14, "monastery_spiritual_anchor"), ("health_recovery_flat", 2, "monastery_charity"), ("population_recovery_flat", 2, "monastery_refuge"), ("administration_flat", 6, "monastery_records"), ("unrest_reduction_flat", 6, "monastery_mediation"))),
    _string_id_building(slot_center_has_temple, "temple", "faith", ("town",), 2000, "str_sod_temple_0", "str_sod_temple_0_description", description_text="@Weekly Relations +1, Weekly Local Faith +5, Weekly Global Faith +4.", effect_tags=("weekly_relations", "weekly_local_faith", "weekly_global_faith"), effect_numbers=(1, 5, 4), affects_town=True, specialization="religious", tier=1, weekly_upkeep=10, design_summary="A civic religious center for town legitimacy, mediation, charity, and faith identity.", building_roles=("faith_support", "unrest_control", "administration"), center_modifiers=(("faith_stability_flat", 12, "temple_civic_rites"), ("unrest_reduction_flat", 6, "temple_mediation"), ("migration_retention_flat", 5, "temple_community_identity"), ("law_compliance_flat", 5, "temple_public_morality"))),
    _string_id_building(slot_center_has_chapel, "chapel", "faith", ("castle",), 500, "str_sod_chapel_0", "str_sod_temple_0_description", description_text="@Allows upgrade of Zealots into Faith Troops, Weekly Global Faith +1.", effect_tags=("faith_troop_upgrade", "weekly_global_faith"), effect_numbers=(1, 1), affects_castle=True, specialization="religious", tier=1, weekly_upkeep=5, design_summary="A castle chapel for garrison morale, faith discipline, wounded soldiers, and elite faith troop access.", building_roles=("faith_support", "military_training", "health_recovery", "unrest_control"), center_modifiers=(("faith_stability_flat", 10, "chapel_garrison_rites"), ("faith_ascension_bonus_flat", 8, "chapel_military_vows"), ("garrison_recovery_flat", 4, "chapel_morale"), ("health_recovery_flat", 2, "chapel_infirmary"), ("unrest_reduction_flat", 3, "chapel_order"))),
    _text_building(slot_center_has_barracks, "barracks", "military", ("town", "castle"), 2000, "@Barracks", "@Build it to train existing troops and recruit new infantry units. Fief's Demesne Cost -1.", effect_tags=("infantry_training", "demesne_cost", "population_capacity"), effect_numbers=(1, -1, 70), affects_town=True, affects_castle=True, specialization="military", tier=1, weekly_upkeep=10, short_description_text="Infantry training quarters.", design_summary="Infantry training quarters, disciplined lodging, watch rotations, reserve labor, and fortress work gangs.", population_capacity_bonus=70, building_roles=("military_training", "population_capacity", "security", "construction_efficiency"), center_modifiers=(("security_flat", 12, "barracks_watch_rotations"), ("garrison_recovery_flat", 10, "barracks_mustering"), ("recruit_count_flat", 2, "barracks_drill_yard"), ("construction_speed_pct", 8, "barracks_work_crews"), ("garrison_upkeep_pct", -5, "barracks_orderly_lodging"))),
    _text_building(slot_center_has_range, "practice_range", "military", ("town", "castle"), 2000, "@Practice Range", "@Build it to train existing troops and recruit new ranged units. Fief's Demesne Cost -1.", effect_tags=("ranged_training", "demesne_cost"), effect_numbers=(1, -1), affects_town=True, affects_castle=True, specialization="military", tier=1, weekly_upkeep=10, short_description_text="Ranged training grounds.", design_summary="Ranged training grounds, wall practice, militia confidence, and fortress missile discipline.", building_roles=("military_training", "security"), center_modifiers=(("security_flat", 10, "practice_range_watch_drill"), ("threat_reduction_flat", 14, "practice_range_visible_militia"), ("recruit_tier_bonus_flat", 1, "practice_range_basic_drill"), ("desperation_bandit_reduction_pct", 6, "practice_range_local_confidence"), ("raid_resistance_pct", 5, "practice_range_wall_coverage"))),
    _text_building(slot_center_has_stables, "stables", "military", ("town", "castle"), 2000, "@Stables", "@Build it to train cavalry. +4 Weekly Renown, Fief's Demesne Cost -1.", effect_tags=("cavalry_training", "weekly_renown", "demesne_cost", "population_capacity"), effect_numbers=(1, 4, -1, 50), affects_town=True, affects_castle=True, specialization="military", tier=1, weekly_upkeep=15, design_summary="Mounted troop support, horses, courier movement, patrol reach, and service households.", population_capacity_bonus=50, building_roles=("military_training", "population_capacity", "renown", "communications"), center_modifiers=(("patrol_response_pct", 15, "stables_mounted_patrols"), ("warning_range_flat", 1, "stables_couriers"), ("trade_volume_pct", 5, "stables_pack_animals"), ("cattle_output_pct", 8, "stables_animal_husbandry"), ("threat_reduction_flat", 10, "stables_route_screens"))),
    _string_id_building(slot_center_has_chapter, "chapter", "military", ("castle",), 4000, "str_sod_chapter_0", "str_sod_temple_0_description", description_text="@Build it to assemble nobility from your fallen motherland. Weekly Renown +5, Fief's Demesne Cost -1.", effect_summary="@Weekly Renown +5, Fief's Demesne Cost -1.", effect_tags=("weekly_renown", "noble_assembly", "demesne_cost"), effect_numbers=(5, 1, -1), affects_castle=True, specialization="military", tier=2, weekly_upkeep=20, design_summary="A noble chapterhouse for homeland nobles, elite recruitment, household officers, and fortress prestige.", building_roles=("noble_recruitment", "renown", "military_training", "administration"), center_modifiers=(("noble_recruitment_flat", 3, "chapter_homeland_nobles"), ("recruit_tier_bonus_flat", 1, "chapter_elite_drill"), ("administration_flat", 8, "chapter_household_officers"), ("law_compliance_flat", 6, "chapter_noble_authority"), ("garrison_recovery_flat", 6, "chapter_retinue_mustering"))),
    _text_building(slot_center_has_blacksmith, "blacksmith", "military", ("town", "castle"), 1000, "@Blacksmith", "@Build it to reduce troop upgrade cost by 50% in this fief, and reduce garrison upkeep in castles (and towns).", effect_tags=("troop_upgrade_cost_multiplier", "garrison_upkeep_reduction"), effect_numbers=(50, 1), affects_town=True, affects_castle=True, specialization="economic", tier=1, weekly_upkeep=10, design_summary="A production building that supports war supply, tools, repairs, and construction crews.", building_roles=("production", "construction_efficiency", "military_training"), center_modifiers=(("construction_speed_pct", 14, "blacksmith_tools"), ("production_output_pct", 10, "blacksmith_repairs"), ("market_wealth_flat", 250, "blacksmith_local_sales"), ("security_flat", 5, "blacksmith_arms_maintenance"))),
    _text_building(slot_center_has_messenger_post, "messenger_post", "security", ("village", "town", "castle"), 1200, "@Messenger Post", "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here. Fief's Demesne Cost -1.", effect_tags=("enemy_warning_messages", "demesne_cost"), effect_numbers=(1, -1), affects_village=True, affects_town=True, affects_castle=True, specialization="civic", tier=1, weekly_upkeep=5, design_summary="Communication hub for alarms, labor coordination, and center-to-market messaging.", building_roles=("communications", "security", "construction_efficiency"), center_modifiers=(("security_flat", 6, "messenger_post_fast_warnings"), ("construction_speed_pct", 6, "messenger_post_work_orders"), ("trade_liquidity_flat", 8, "messenger_post_market_news"), ("patrol_response_pct", 8, "messenger_post_dispatch"))),
    _text_building(slot_center_has_prisoner_tower, "prisoner_tower", "security", ("town", "castle"), 1000, "@Prison Tower", "@A prison tower reduces the chance of captives escaping. Weekly Relations +1 (Towns only).", effect_tags=("captives_escape_chance", "weekly_relations"), effect_numbers=(1, 1), affects_town=True, affects_castle=True, specialization="defensive", tier=1, weekly_upkeep=10, design_summary="Security building for prisoners, court authority, and visible order.", building_roles=("prisoner_control", "security", "unrest_control"), center_modifiers=(("security_flat", 12, "prisoner_tower_order"), ("unrest_reduction_flat", 5, "prisoner_tower_deterrence"), ("law_compliance_flat", 8, "prisoner_tower_courts"), ("desperation_bandit_reduction_pct", 5, "prisoner_tower_detention"))),
    _text_building(slot_center_has_guild, "merchant_guild_hall", "town_economy", ("town",), 9000, "@Merchant's Guild Hall", "@Build it to please the merchant community and engage in trade enterprises. Weekly Relations +1, Weekly Prosperity +2, Fief's Demesne Cost -2, Weekly Taxes +10%.", effect_tags=("weekly_relations", "weekly_prosperity", "demesne_cost", "weekly_taxes_percent", "weekly_population_growth"), effect_numbers=(1, 2, -2, 10, 1), affects_town=True, specialization="economic", tier=2, weekly_upkeep=30, design_summary="Major guild infrastructure for town commerce, credit, merchant politics, and labor demand.", weekly_population_growth_bonus=1, building_roles=("trade_liquidity", "population_growth", "administration", "production"), center_modifiers=(("trade_liquidity_flat", 80, "guild_market_network"), ("trade_volume_pct", 15, "guild_trade_contracts"), ("merchant_happiness_flat", 12, "guild_representation"), ("goods_import_demand_pct", 10, "guild_warehouses"), ("goods_export_supply_pct", 10, "guild_factors"), ("market_wealth_pct", 10, "guild_credit"))),
    _text_building(slot_center_has_university, "university", "town_civic", ("town",), 4000, "@University", "@Erect it to improve your renown, as well as people's appreciation for you. Weekly Relations +1, Weekly Renown +15.", effect_tags=("weekly_relations", "weekly_renown", "population_capacity"), effect_numbers=(1, 15, 100), affects_town=True, specialization="civic", tier=2, weekly_upkeep=20, center_health_bonus=10, design_summary="A scholarly civic institution that supports skilled urban households, administration, engineering, and law.", population_capacity_bonus=100, building_roles=("administration", "population_capacity", "renown", "construction_efficiency"), center_modifiers=(("administration_flat", 12, "university_bureaucrats"), ("construction_speed_pct", 10, "university_engineers"), ("law_compliance_flat", 8, "university_legal_training"), ("cultural_assimilation_flat", 5, "university_schools"))),
    _text_building(slot_center_has_hospital, "hospital", "town_health", ("town",), 2500, "@Hospital", "@Build it to keep your people healthy. Health Cap +20 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap", "population_capacity", "weekly_population_growth", "raid_recovery"), effect_numbers=(20, 340, 2, 2), affects_town=True, specialization="population_health", tier=3, prerequisite_buildings=(slot_center_has_canalization,), upgrade_from=(slot_center_has_canalization,), exclusive_group="town_health_progression", weekly_upkeep=35, faction_flavor="Advanced town medicine and treatment.", center_health_bonus=20, design_summary="A higher-tier hospital that supersedes canalization with physicians, wards, quarantine, and post-raid care.", population_capacity_bonus=340, weekly_population_growth_bonus=2, raid_recovery_bonus=2, building_roles=("health_recovery", "population_capacity", "population_growth", "raid_recovery"), center_modifiers=(("health_recovery_flat", 8, "hospital_physicians"), ("disease_resistance_pct", 18, "hospital_quarantine"), ("population_recovery_flat", 6, "hospital_wards"), ("migration_retention_flat", 8, "hospital_family_security"))),
    _text_building(slot_center_has_canalization, "canalization", "town_health", ("town",), 1200, "@Canalization", "@Build it to improve sanitation. Health Cap +10 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap", "population_capacity", "raid_recovery"), effect_numbers=(10, 180, 1), affects_town=True, specialization="population_health", tier=2, upgrade_to=(slot_center_has_hospital,), exclusive_group="town_health_progression", weekly_upkeep=15, faction_flavor="Town sanitation, drains, and waste management.", center_health_bonus=10, design_summary="Sanitation works that can become a hospital, reducing disease, crowding pressure, and food spoilage.", population_capacity_bonus=180, raid_recovery_bonus=1, building_roles=("health_recovery", "population_capacity", "raid_recovery", "food_security"), center_modifiers=(("health_recovery_flat", 4, "canalization_sanitation"), ("disease_resistance_pct", 10, "canalization_waste_control"), ("food_security_flat", 20, "canalization_clean_storage"), ("food_consumption_pct", -5, "canalization_less_spoilage"))),
    _text_building(slot_center_has_manufacture, "manufacture", "town_economy", ("town",), 2500, "@Manufacture", "@Build it to support long-term prosperity. Prosperity Cap +20 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap", "population_capacity", "weekly_population_growth"), effect_numbers=(20, 240, 1), affects_town=True, specialization="economic", tier=3, prerequisite_buildings=(slot_center_has_bank,), upgrade_from=(slot_center_has_bank,), exclusive_group="town_economic_progression", weekly_upkeep=45, faction_flavor="Large-scale town industry and investment.", design_summary="A major industrial building that supersedes the town bank with workshops, wage labor, exports, and construction capacity.", population_capacity_bonus=240, weekly_population_growth_bonus=1, building_roles=("production", "population_capacity", "population_growth", "construction_efficiency"), center_modifiers=(("production_output_pct", 25, "manufacture_workshops"), ("goods_export_supply_pct", 18, "manufacture_finished_goods"), ("market_wealth_flat", 1500, "manufacture_wages"), ("construction_speed_pct", 12, "manufacture_material_supply"), ("tax_efficiency_pct", 8, "manufacture_assessed_output"))),
    _text_building(slot_center_has_bank, "bank", "town_economy", ("town",), 1200, "@Bank", "@Build it to support long-term prosperity. Prosperity Cap +10 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap", "population_capacity"), effect_numbers=(10, 120), affects_town=True, specialization="economic", tier=2, upgrade_to=(slot_center_has_manufacture,), exclusive_group="town_economic_progression", weekly_upkeep=15, faction_flavor="Town finance and merchant credit.", design_summary="A civic bank that can later be replaced by a manufacture, improving credit, liquidity, and recovery financing.", population_capacity_bonus=120, building_roles=("trade_liquidity", "population_capacity", "administration"), center_modifiers=(("trade_liquidity_flat", 45, "bank_credit"), ("market_wealth_pct", 8, "bank_deposits"), ("merchant_happiness_flat", 6, "bank_letters_of_credit"), ("construction_cost_pct", -5, "bank_project_financing"), ("raid_recovery_flat", 2, "bank_reconstruction_loans"))),
    _text_building(slot_center_has_ambulatory, "ambulatory", "village_health", ("village",), 2500, "@Ambulatory", "@Build it to keep your people healthy. Health Cap +20 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap", "population_capacity", "weekly_population_growth", "raid_recovery"), effect_numbers=(20, 180, 2, 2), affects_village=True, specialization="population_health", tier=2, prerequisite_buildings=(slot_center_has_water_supply,), upgrade_from=(slot_center_has_water_supply,), exclusive_group="village_health_progression", weekly_upkeep=15, faction_flavor="Basic village treatment and care.", center_health_bonus=20, design_summary="A local care facility replacing the water supply improvement with treatment, midwives, recovery beds, and raid aftercare.", population_capacity_bonus=180, weekly_population_growth_bonus=2, raid_recovery_bonus=2, building_roles=("health_recovery", "population_capacity", "population_growth", "raid_recovery"), center_modifiers=(("health_recovery_flat", 6, "ambulatory_treatment"), ("disease_resistance_pct", 12, "ambulatory_prevention"), ("population_recovery_flat", 4, "ambulatory_aftercare"), ("migration_retention_flat", 5, "ambulatory_family_security"))),
    _text_building(slot_center_has_water_supply, "water_supply", "village_health", ("village",), 1200, "@Water Supply", "@Build it to improve sanitation. Health Cap +10 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap", "population_capacity", "weekly_population_growth", "raid_recovery"), effect_numbers=(10, 90, 1, 1), affects_village=True, specialization="population_health", tier=1, upgrade_to=(slot_center_has_ambulatory,), exclusive_group="village_health_progression", weekly_upkeep=5, faction_flavor="Clean water and basic sanitation.", center_health_bonus=10, design_summary="Village waterworks that can later become an ambulatory, improving sanitation, food preparation, and recovery.", population_capacity_bonus=90, weekly_population_growth_bonus=1, raid_recovery_bonus=1, building_roles=("health_recovery", "population_capacity", "population_growth", "raid_recovery", "food_security"), center_modifiers=(("health_recovery_flat", 3, "water_supply_sanitation"), ("disease_resistance_pct", 8, "water_supply_clean_water"), ("food_security_flat", 12, "water_supply_food_prep"), ("population_recovery_flat", 1, "water_supply_survival"))),
    _text_building(slot_center_has_clayworks, "clayworks", "village_economy", ("village",), 2500, "@Clayworks", "@Build it to support construction materials, craft output, and long-term prosperity. Prosperity Cap +20 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap", "population_capacity"), effect_numbers=(20, 80), affects_village=True, specialization="economic", tier=1, weekly_upkeep=10, design_summary="Village bricks, pottery, construction materials, craft output, and seasonal labor.", population_capacity_bonus=80, building_roles=("production", "population_capacity", "construction_efficiency", "trade_liquidity"), center_modifiers=(("construction_speed_pct", 18, "clayworks_local_materials"), ("production_output_pct", 12, "clayworks_crafts"), ("goods_export_supply_pct", 8, "clayworks_trade_goods"), ("market_wealth_flat", 300, "clayworks_local_sales"))),
    _text_building(slot_center_has_rustic_blacksmith, "rustic_blacksmith", "village_economy", ("village",), 1200, "@Rustic Blacksmith", "@Build it to support tools, repairs, construction work, and long-term prosperity. Prosperity Cap +10 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap", "population_capacity"), effect_numbers=(10, 45), affects_village=True, specialization="economic", tier=1, weekly_upkeep=5, design_summary="A small village smithy for tool repair, ploughshares, local production, and construction labor.", population_capacity_bonus=45, building_roles=("production", "construction_efficiency", "security"), center_modifiers=(("construction_speed_pct", 12, "rustic_blacksmith_tools"), ("production_output_pct", 8, "rustic_blacksmith_repairs"), ("security_flat", 5, "rustic_blacksmith_arms_repair"), ("troop_upgrade_cost_pct", -5, "rustic_blacksmith_local_arms"))),
    _text_building(slot_center_has_militia_yard, "militia_yard", "village_defense", ("village",), 1800, "@Militia Yard", "@A militia yard gives villagers a proper muster ground, weapon racks, and drill routine. It improves local defense, recruit quality, and garrison recovery.", effect_tags=("raid_recovery", "population_capacity"), effect_numbers=(1, 60), affects_village=True, specialization="military", tier=1, weekly_upkeep=10, design_summary="A village muster yard with drills, racks, levy rolls, and enough discipline to make raiders pay for every lane.", population_capacity_bonus=60, raid_recovery_bonus=1, building_roles=("security", "military_training", "raid_recovery", "population_capacity"), center_modifiers=(("garrison_recovery_flat", 10, "militia_yard_muster_rolls"), ("recruit_count_flat", 1, "militia_yard_drill_call"), ("recruit_tier_bonus_flat", 1, "militia_yard_basic_drill"), ("security_flat", 8, "militia_yard_watch_rotations"), ("raid_resistance_pct", 8, "militia_yard_local_defense"))),
    _text_building(slot_center_has_beacon_hill, "beacon_hill", "village_defense", ("village",), 1400, "@Beacon Hill", "@A beacon hill gives the village a prepared signal site and scout watch. It improves warning range, patrol response, and local threat reduction.", effect_tags=("enemy_warning_messages", "raid_recovery"), effect_numbers=(1, 1), affects_village=True, specialization="defensive", tier=1, weekly_upkeep=5, design_summary="A maintained signal hill, lookout post, and runner path that makes raids harder to hide and easier to answer.", raid_recovery_bonus=1, building_roles=("security", "communications", "raid_recovery"), center_modifiers=(("warning_range_flat", 1, "beacon_hill_signal_fire"), ("patrol_response_pct", 12, "beacon_hill_runner_paths"), ("security_flat", 4, "beacon_hill_watch"), ("threat_reduction_flat", 8, "beacon_hill_scouting"), ("bandit_spawn_reduction_pct", 4, "beacon_hill_visibility"))),
    _text_building(slot_center_has_granary, "granary", "village_economy", ("village",), 2200, "@Granary", "@A granary stores reserve grain, reduces famine pressure, and helps the village recover after raids or poor harvests.", effect_tags=("population_capacity", "raid_recovery", "weekly_population_growth"), effect_numbers=(120, 1, 1), affects_village=True, specialization="economic", tier=1, weekly_upkeep=10, design_summary="A defended village grain store for lean months, seed reserves, food distribution, and recovery after raids.", population_capacity_bonus=120, weekly_population_growth_bonus=1, raid_recovery_bonus=1, building_roles=("food_security", "population_capacity", "population_growth", "raid_recovery"), center_modifiers=(("food_store_capacity_flat", 180, "granary_reserve_bins"), ("food_security_flat", 25, "granary_seed_reserve"), ("raid_recovery_flat", 1, "granary_emergency_stores"), ("population_recovery_flat", 1, "granary_lean_months"), ("migration_retention_flat", 4, "granary_winter_confidence"))),
    _text_building(slot_center_has_militia_armory, "militia_armory", "village_defense", ("village",), 1600, "@Militia Armory", "@A militia armory stores spears, shields, bows, repair tools, and levy gear. It slightly improves militia quality, but raiders may steal arms if they break the village.", effect_tags=("raid_recovery", "population_capacity"), effect_numbers=(1, 40), affects_village=True, specialization="military", tier=1, weekly_upkeep=8, prerequisite_any_buildings=(slot_center_has_rustic_blacksmith, slot_center_has_manor), design_summary="A local arms store for levy gear and repair tools. It gives defenders better equipment, but a clean raider victory can arm bandits for a short time.", population_capacity_bonus=40, raid_recovery_bonus=1, building_roles=("security", "military_training", "raid_recovery", "population_capacity"), center_modifiers=(("recruit_tier_bonus_flat", 1, "militia_armory_levy_gear"), ("garrison_recovery_flat", 4, "militia_armory_repair_tools"), ("security_flat", 5, "militia_armory_stored_arms"), ("raid_resistance_pct", 4, "militia_armory_better_armed_watch"))),
]

class BuildingRegistry(dict):
    def __iter__(self):
        return iter(self.values())


BUILDING_REGISTRY = BuildingRegistry((definition["building_slot"], definition) for definition in BUILDING_REGISTRY)

BUILDING_DEFINITIONS = BUILDING_REGISTRY
BUILDING_BY_SLOT = dict((definition["building_slot"], definition) for definition in BUILDING_REGISTRY)
BUILDING_BY_KEY = dict((definition["building_key"], definition) for definition in BUILDING_REGISTRY)
BUILDING_SLOTS = tuple(definition["building_slot"] for definition in BUILDING_REGISTRY)
BUILDING_KEYS = tuple(definition["building_key"] for definition in BUILDING_REGISTRY)


def get_building_registry():
    return BUILDING_REGISTRY


def get_building_definition(building_slot):
    return BUILDING_BY_SLOT.get(building_slot)


def get_building_definition_by_key(building_key):
    return BUILDING_BY_KEY.get(building_key)


def get_building_cost(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    return building["cost"]


def get_building_name_definition(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    if building["name_string_id"] is not None:
        return {"kind": "string_id", "string_id": building["name_string_id"]}
    return {"kind": "text", "text": building["display_name"]}


def get_building_description_definition(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    if building["description_string_id"] is not None:
        return {"kind": "string_id", "string_id": building["description_string_id"]}
    return {"kind": "text", "text": building["description"]}


def get_building_short_description_definition(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    short_description = building.get("short_description_text")
    if short_description is None:
        short_description = building.get("short_description")
    if short_description:
        return {"kind": "text", "text": _normalize_display_text(short_description)}
    return get_building_description_definition(building_slot)


def get_building_short_description_text(building_slot):
    definition = get_building_short_description_definition(building_slot)
    if definition is None:
        return ""
    return definition.get("text", definition.get("string_id", ""))


def get_building_failure_reason_definition(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    failure_reason = building.get("failure_reason_text")
    if failure_reason is None:
        failure_reason = building.get("failure_reason")
    if failure_reason:
        return {"kind": "text", "text": _normalize_display_text(failure_reason)}
    return None


def get_building_failure_reason_text(building_slot):
    definition = get_building_failure_reason_definition(building_slot)
    if definition is None:
        return ""
    return definition.get("text", definition.get("string_id", ""))


def get_building_effect_summary(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    return building["effect_summary"]


def get_building_specialization(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    return building.get("specialization")


def get_building_tier(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return 0
    return building.get("tier", 0)


def get_building_upgrade_sources(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ()
    return _normalize_tuple(building.get("upgrade_from"))


def get_building_upgrade_targets(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ()
    return _normalize_tuple(building.get("upgrade_to"))


def get_building_exclusive_group(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return None
    return building.get("exclusive_group")


def get_building_weekly_upkeep(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return 0
    return building.get("weekly_upkeep", 0)


def get_building_design_summary(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ""
    return _normalize_text(building.get("design_summary"), building.get("description", ""))


def get_building_balance_value(building_slot, field_name, default=0):
    building = get_building_definition(building_slot)
    if building is None:
        return default
    value = building.get(field_name, default)
    if value is None:
        return default
    return value


def get_building_center_modifiers(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ()
    return _normalize_tuple(building.get("center_modifiers"))


def get_building_center_modifier_value(building_slot, modifier_key):
    total = 0
    for entry in get_building_center_modifiers(building_slot):
        if len(entry) < 2:
            continue
        if entry[0] == modifier_key:
            total += entry[1]
    return total


def get_building_center_health_bonus(building_slot):
    return get_building_balance_value(building_slot, "center_health_bonus", 0)


def get_building_prosperity_multiplier_bonus_percent(building_slot):
    return get_building_balance_value(building_slot, "prosperity_multiplier_bonus_percent", 0)


def get_building_prosperity_cap_bonus(building_slot):
    return get_building_balance_value(building_slot, "prosperity_cap_bonus", 0)


def get_building_demesne_cost(building_slot):
    return get_building_balance_value(building_slot, "demesne_cost", 0)


def get_building_weekly_renown_bonus(building_slot):
    return get_building_balance_value(building_slot, "weekly_renown_bonus", 0)


def get_building_weekly_prosperity_bonus(building_slot):
    return get_building_balance_value(building_slot, "weekly_prosperity_bonus", 0)


def get_building_weekly_income_bonus_percent(building_slot):
    return get_building_balance_value(building_slot, "weekly_income_bonus_percent", 0)


def get_building_population_capacity_bonus(building_slot):
    return get_building_balance_value(building_slot, "population_capacity_bonus", 0)


def get_building_weekly_population_growth_bonus(building_slot):
    return get_building_balance_value(building_slot, "weekly_population_growth_bonus", 0)


def get_building_raid_recovery_bonus(building_slot):
    return get_building_balance_value(building_slot, "raid_recovery_bonus", 0)


def get_building_faction_requirements(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ()
    return _normalize_tuple(building.get("faction_requirements"))


def get_building_faction_flavor(building_slot):
    building = get_building_definition(building_slot)
    if building is None:
        return ""
    return _normalize_text(building.get("faction_flavor"), "")


def get_buildings_for_center_type(center_type):
    return [definition for definition in BUILDING_REGISTRY if center_type in definition["allowed_center_types"]]


def get_buildings_with_role(role, center_type=None):
    result = []
    for definition in BUILDING_REGISTRY:
        if role not in definition.get("building_roles", ()):
            continue
        if center_type is not None and center_type not in definition.get("allowed_center_types", ()):
            continue
        result.append(definition)
    return result


def get_building_slots_for_center_type(center_type):
    return [definition["building_slot"] for definition in get_buildings_for_center_type(center_type)]


def _check_reference_slot_exists(issues, slot_name, field_name, reference_value):
    if reference_value is None:
        return
    if not isinstance(reference_value, (tuple, list)):
        issues.append("%s: %s must be a tuple or list of slot names" % (slot_name, field_name))
        return
    for ref_slot in reference_value:
        if ref_slot not in BUILDING_BY_SLOT:
            issues.append("%s: %s references unknown slot %s" % (slot_name, field_name, ref_slot))


def validate_building_registry():
    issues = []
    seen_slots = {}
    seen_keys = {}
    for definition in BUILDING_REGISTRY:
        if not isinstance(definition, dict):
            issues.append("registry entry must be a dictionary: %s" % definition)
            continue

        slot_name = definition.get("building_slot")
        building_key = definition.get("building_key")
        if slot_name is None:
            issues.append("missing building_slot on %s" % building_key)
            continue
        if building_key is None:
            issues.append("%s: missing building_key" % slot_name)
        seen_slots[slot_name] = seen_slots.get(slot_name, 0) + 1
        seen_keys[building_key] = seen_keys.get(building_key, 0) + 1

        specialization = definition.get("specialization")
        if specialization is not None and specialization not in SUPPORTED_BUILDING_SPECIALIZATIONS:
            issues.append("%s: specialization %s is not supported" % (slot_name, specialization))

        allowed_center_types = definition.get("allowed_center_types", ())
        if allowed_center_types is None:
            allowed_center_types = ()
        if not isinstance(allowed_center_types, (tuple, list)):
            issues.append("%s: allowed_center_types must be a tuple or list" % slot_name)
        else:
            for center_type in allowed_center_types:
                if center_type not in ("village", "town", "castle"):
                    issues.append("%s: allowed_center_types references unknown center type %s" % (slot_name, center_type))
                    break

        build_hours = definition.get("build_hours")
        build_days = definition.get("build_days")
        for field_name, value in (("build_hours", build_hours), ("build_days", build_days)):
            if value is None:
                continue
            if not _is_integer(value):
                issues.append("%s: %s must be an integer" % (slot_name, field_name))
            elif value < 0:
                issues.append("%s: %s must be non-negative" % (slot_name, field_name))
        if build_hours is not None and build_days is not None and build_hours != build_days:
            issues.append("%s: build_hours and build_days disagree" % slot_name)

        effect_tags = definition.get("effect_tags", ())
        effect_numbers = definition.get("effect_numbers", ())
        if effect_tags is None:
            effect_tags = ()
        if effect_numbers is None:
            effect_numbers = ()
        if not isinstance(effect_tags, (tuple, list)):
            issues.append("%s: effect_tags must be a tuple or list" % slot_name)
        if not isinstance(effect_numbers, (tuple, list)):
            issues.append("%s: effect_numbers must be a tuple or list" % slot_name)
        if isinstance(effect_tags, (tuple, list)) and isinstance(effect_numbers, (tuple, list)) and len(effect_tags) != len(effect_numbers):
            issues.append("%s: effect_tags and effect_numbers must have the same length" % slot_name)
        if isinstance(effect_tags, (tuple, list)):
            for effect_tag in effect_tags:
                if effect_tag not in BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER:
                    issues.append("%s: effect tag %s must map to a center modifier before adding scripted behavior" % (slot_name, effect_tag))
        for field_name, _modifier_key in BUILDING_FIELD_TO_CENTER_MODIFIER:
            field_value = definition.get(field_name, 0)
            if field_value and not definition.get("center_modifiers"):
                issues.append("%s: field %s must derive or define center_modifiers" % (slot_name, field_name))

        tier = definition.get("tier", 0)
        if tier is None:
            tier = 0
        if not _is_integer(tier):
            issues.append("%s: tier must be an integer" % slot_name)
        elif tier < 0:
            issues.append("%s: tier must be non-negative" % slot_name)

        weekly_upkeep = definition.get("weekly_upkeep", 0)
        if weekly_upkeep is None:
            weekly_upkeep = 0
        if not _is_integer(weekly_upkeep):
            issues.append("%s: weekly_upkeep must be an integer" % slot_name)
        elif weekly_upkeep < 0:
            issues.append("%s: weekly_upkeep must be non-negative" % slot_name)

        exclusive_group = definition.get("exclusive_group")
        if exclusive_group is not None and not isinstance(exclusive_group, _string_types()):
            issues.append("%s: exclusive_group must be a string or None" % slot_name)

        faction_requirements = definition.get("faction_requirements", ())
        if faction_requirements is None:
            faction_requirements = ()
        if not isinstance(faction_requirements, (tuple, list)):
            issues.append("%s: faction_requirements must be a tuple or list" % slot_name)

        building_roles = definition.get("building_roles", ())
        if building_roles is None:
            building_roles = ()
        if not isinstance(building_roles, (tuple, list)):
            issues.append("%s: building_roles must be a tuple or list" % slot_name)
        else:
            for role in building_roles:
                if role not in SUPPORTED_BUILDING_ROLES:
                    issues.append("%s: building role %s is not supported" % (slot_name, role))

        center_modifiers = definition.get("center_modifiers", ())
        if center_modifiers is None:
            center_modifiers = ()
        if not isinstance(center_modifiers, (tuple, list)):
            issues.append("%s: center_modifiers must be a tuple or list" % slot_name)
        else:
            for modifier_entry in center_modifiers:
                if not isinstance(modifier_entry, (tuple, list)) or len(modifier_entry) < 2:
                    issues.append("%s: center modifier entry must be a tuple/list with at least key and value" % slot_name)
                    continue
                modifier_key = modifier_entry[0]
                modifier_value = modifier_entry[1]
                if modifier_key not in CENTER_MODIFIER_BY_KEY:
                    issues.append("%s: center modifier %s is not supported" % (slot_name, modifier_key))
                if not _is_integer(modifier_value):
                    issues.append("%s: center modifier %s value must be an integer" % (slot_name, modifier_key))

        _check_reference_slot_exists(issues, slot_name, "prerequisite_buildings", definition.get("prerequisite_buildings"))
        _check_reference_slot_exists(issues, slot_name, "prerequisite_any_buildings", definition.get("prerequisite_any_buildings"))
        _check_reference_slot_exists(issues, slot_name, "upgrade_from", definition.get("upgrade_from"))
        _check_reference_slot_exists(issues, slot_name, "upgrade_to", definition.get("upgrade_to"))
        _check_reference_slot_exists(issues, slot_name, "conflicts_with", definition.get("conflicts_with"))

    duplicate_slots = [slot for slot, count in seen_slots.items() if count > 1]
    duplicate_keys = [key for key, count in seen_keys.items() if count > 1]

    if duplicate_slots:
        issues.append("duplicate slots: %s" % ", ".join(map(str, duplicate_slots)))
    if duplicate_keys:
        issues.append("duplicate keys: %s" % ", ".join(map(str, duplicate_keys)))

    return issues
