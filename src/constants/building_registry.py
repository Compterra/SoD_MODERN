# -*- coding: cp1254 -*-

from src.constants.module_constants import *

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
):
    effect_tags = tuple(effect_tags)
    effect_numbers = tuple(effect_numbers)
    if effect_summary is None:
        effect_summary = short_description_text if short_description_text is not None else (description_text if description_text is not None else description_string_id)
    if short_description_text is None:
        short_description_text = effect_summary if effect_summary is not None else description_text
    if design_summary is None:
        design_summary = short_description_text if short_description_text is not None else (effect_summary if effect_summary is not None else description_text)
    if build_days is None and build_hours is not None:
        build_days = build_hours

    return {
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
    }


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
    _text_building(slot_center_has_manor, "manor", "village_economy", ("village",), 2000, "@Manor", "@A village manor improves hospitality and logistics. Weekly Renown +3, Fief's Demesne Cost -2.", effect_tags=("weekly_renown", "demesne_cost"), effect_numbers=(3, -2), affects_village=True, specialization="civic", tier=1, weekly_upkeep=5, short_description_text="Village hospitality and logistics.", design_summary="Village hospitality and logistics.", center_health_bonus=5, prosperity_multiplier_bonus_percent=10, weekly_renown_bonus=3, demesne_cost=2),
    _text_building(slot_center_has_mill, "mill", "village_economy", ("village",), 2500, "@Mill", "@A mill improves village income and long-term prosperity. Weekly Prosperity +1, Prosperity Cap +20, Weekly Taxes +10%.", effect_tags=("weekly_prosperity", "prosperity_cap", "weekly_taxes_percent"), effect_numbers=(1, 20, 10), affects_village=True, specialization="economic", tier=1, weekly_upkeep=10, short_description_text="Village production and prosperity.", design_summary="Village production and prosperity.", center_health_bonus=5, prosperity_multiplier_bonus_percent=20, prosperity_cap_bonus=20, weekly_prosperity_bonus=1, weekly_income_bonus_percent=10),
    _text_building(slot_center_has_watch_tower, "watch_tower", "village_defense", ("village",), 1200, "@Watch Tower", "@A watch tower lets the villagers raise alarm earlier. The time it takes for enemies to loot the village increases by 25%. Village's Demesne Cost -1.", effect_tags=("loot_time_bonus_percent", "demesne_cost"), effect_numbers=(25, -1), affects_village=True, specialization="defensive", tier=1, weekly_upkeep=5, design_summary="Early warning and local defense.", demesne_cost=1),
    _text_building(slot_center_has_inn, "inn", "village_civic", ("village",), 2000, "@Inn", "@An inn increases the loyalty of the villagers to you by +2 every week.", effect_tags=("weekly_loyalty",), effect_numbers=(2,), affects_village=True, specialization="civic", tier=1, weekly_upkeep=10, design_summary="A social hub for travelers and locals."),
    _string_id_building(slot_center_has_shrine, "shrine", "faith", ("village",), 1000, "str_sod_shrine_0", "str_sod_temple_0_description", description_text="@Weekly Relations +1, Weekly Local Faith +3, Weekly Global Faith +2.", effect_tags=("weekly_relations", "weekly_local_faith", "weekly_global_faith"), effect_numbers=(1, 3, 2), affects_village=True, specialization="religious", tier=1, upgrade_to=(slot_center_has_monastery,), exclusive_group="village_religious_progression", weekly_upkeep=5, faction_flavor="Village shrine and pilgrim stop.", design_summary="A small village shrine that can later be replaced by a monastery."),
    _string_id_building(slot_center_has_monastery, "monastery", "faith", ("village",), 2000, "str_sod_monastery_0", "str_sod_temple_0_description", description_text="@Weekly Taxes +5%, Weekly Local Faith +2, Weekly Global Faith +2.", effect_tags=("weekly_taxes_percent", "weekly_local_faith", "weekly_global_faith"), effect_numbers=(5, 2, 2), affects_village=True, specialization="religious", tier=2, prerequisite_buildings=(slot_center_has_shrine,), upgrade_from=(slot_center_has_shrine,), exclusive_group="village_religious_progression", weekly_upkeep=20, faction_flavor="Village monastic estate and spiritual center.", center_health_bonus=5, design_summary="An expanded monastic complex that supersedes a shrine."),
    _string_id_building(slot_center_has_temple, "temple", "faith", ("town",), 2000, "str_sod_temple_0", "str_sod_temple_0_description", description_text="@Weekly Relations +1, Weekly Local Faith +5, Weekly Global Faith +4.", effect_tags=("weekly_relations", "weekly_local_faith", "weekly_global_faith"), effect_numbers=(1, 5, 4), affects_town=True, specialization="religious", tier=1, weekly_upkeep=10, design_summary="A civic religious center for a town."),
    _string_id_building(slot_center_has_chapel, "chapel", "faith", ("castle",), 500, "str_sod_chapel_0", "str_sod_temple_0_description", description_text="@Allows upgrade of Zealots into Faith Troops, Weekly Global Faith +1.", effect_tags=("faith_troop_upgrade", "weekly_global_faith"), effect_numbers=(1, 1), affects_castle=True, specialization="religious", tier=1, weekly_upkeep=5, design_summary="A castle chapel for military faith support."),
    _text_building(slot_center_has_barracks, "barracks", "military", ("town", "castle"), 2000, "@Barracks", "@Build it to train existing troops and recruit new infantry units. Fief's Demesne Cost -1.", effect_tags=("infantry_training", "demesne_cost"), effect_numbers=(1, -1), affects_town=True, affects_castle=True, specialization="military", tier=1, weekly_upkeep=10, short_description_text="Infantry training quarters.", design_summary="Infantry training quarters."),
    _text_building(slot_center_has_range, "practice_range", "military", ("town", "castle"), 2000, "@Practice Range", "@Build it to train existing troops and recruit new ranged units. Fief's Demesne Cost -1.", effect_tags=("ranged_training", "demesne_cost"), effect_numbers=(1, -1), affects_town=True, affects_castle=True, specialization="military", tier=1, weekly_upkeep=10, short_description_text="Ranged training grounds.", design_summary="Ranged training grounds."),
    _text_building(slot_center_has_stables, "stables", "military", ("town", "castle"), 2000, "@Stables", "@Build it to train cavalry. +4 Weekly Renown, Fief's Demesne Cost -1.", effect_tags=("cavalry_training", "weekly_renown", "demesne_cost"), effect_numbers=(1, 4, -1), affects_town=True, affects_castle=True, specialization="military", tier=1, weekly_upkeep=15, design_summary="Mounted troop support and horses."),
    _string_id_building(slot_center_has_chapter, "chapter", "military", ("castle",), 4000, "str_sod_chapter_0", "str_sod_temple_0_description", description_text="@Build it to assemble nobility from your fallen motherland. Weekly Renown +5, Fief's Demesne Cost -1.", effect_summary="@Weekly Renown +5, Fief's Demesne Cost -1.", effect_tags=("weekly_renown", "noble_assembly", "demesne_cost"), effect_numbers=(5, 1, -1), affects_castle=True, specialization="military", tier=2, weekly_upkeep=20, design_summary="A noble chapterhouse for elite recruitment."),
    _text_building(slot_center_has_blacksmith, "blacksmith", "military", ("town", "castle"), 1000, "@Blacksmith", "@Build it to reduce troop upgrade cost by 50% in this fief, and reduce garrison upkeep in castles (and towns).", effect_tags=("troop_upgrade_cost_multiplier", "garrison_upkeep_reduction"), effect_numbers=(50, 1), affects_town=True, affects_castle=True, specialization="economic", tier=1, weekly_upkeep=10, design_summary="A production building that supports war supply."),
    _text_building(slot_center_has_messenger_post, "messenger_post", "security", ("village", "town", "castle"), 1200, "@Messenger Post", "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here. Fief's Demesne Cost -1.", effect_tags=("enemy_warning_messages", "demesne_cost"), effect_numbers=(1, -1), affects_village=True, affects_town=True, affects_castle=True, specialization="civic", tier=1, weekly_upkeep=5, design_summary="Communication hub for center coordination."),
    _text_building(slot_center_has_prisoner_tower, "prisoner_tower", "security", ("town", "castle"), 1000, "@Prison Tower", "@A prison tower reduces the chance of captives escaping. Weekly Relations +1 (Towns only).", effect_tags=("captives_escape_chance", "weekly_relations"), effect_numbers=(1, 1), affects_town=True, affects_castle=True, specialization="defensive", tier=1, weekly_upkeep=10, design_summary="Security building for prisoners and control."),
    _text_building(slot_center_has_guild, "merchant_guild_hall", "town_economy", ("town",), 9000, "@Merchant's Guild Hall", "@Build it to please the merchant community and engage in trade enterprises. Weekly Relations +1, Weekly Prosperity +2, Fief's Demesne Cost -2, Weekly Taxes +10%.", effect_tags=("weekly_relations", "weekly_prosperity", "demesne_cost", "weekly_taxes_percent"), effect_numbers=(1, 2, -2, 10), affects_town=True, specialization="economic", tier=2, weekly_upkeep=30, design_summary="Major guild infrastructure for town commerce."),
    _text_building(slot_center_has_university, "university", "town_civic", ("town",), 4000, "@University", "@Erect it to improve your renown, as well as people's appreciation for you. Weekly Relations +1, Weekly Renown +15.", effect_tags=("weekly_relations", "weekly_renown"), effect_numbers=(1, 15), affects_town=True, specialization="civic", tier=2, weekly_upkeep=20, center_health_bonus=10, design_summary="A scholarly civic institution."),
    _text_building(slot_center_has_hospital, "hospital", "town_health", ("town",), 2500, "@Hospital", "@Build it to keep your people healthy. Health Cap +20 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap",), effect_numbers=(20,), affects_town=True, specialization="population_health", tier=3, prerequisite_buildings=(slot_center_has_canalization,), upgrade_from=(slot_center_has_canalization,), exclusive_group="town_health_progression", weekly_upkeep=35, faction_flavor="Advanced town medicine and treatment.", center_health_bonus=20, design_summary="A higher-tier hospital that supersedes canalization."),
    _text_building(slot_center_has_canalization, "canalization", "town_health", ("town",), 1200, "@Canalization", "@Build it to improve sanitation. Health Cap +10 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap",), effect_numbers=(10,), affects_town=True, specialization="population_health", tier=2, upgrade_to=(slot_center_has_hospital,), exclusive_group="town_health_progression", weekly_upkeep=15, faction_flavor="Town sanitation, drains, and waste management.", center_health_bonus=10, design_summary="Sanitation works that can become a hospital."),
    _text_building(slot_center_has_manufacture, "manufacture", "town_economy", ("town",), 2500, "@Manufacture", "@Build it to support long-term prosperity. Prosperity Cap +20 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap",), effect_numbers=(20,), affects_town=True, specialization="economic", tier=3, prerequisite_buildings=(slot_center_has_bank,), upgrade_from=(slot_center_has_bank,), exclusive_group="town_economic_progression", weekly_upkeep=45, faction_flavor="Large-scale town industry and investment.", design_summary="A major industrial building that supersedes the town bank."),
    _text_building(slot_center_has_bank, "bank", "town_economy", ("town",), 1200, "@Bank", "@Build it to support long-term prosperity. Prosperity Cap +10 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap",), effect_numbers=(10,), affects_town=True, specialization="economic", tier=2, upgrade_to=(slot_center_has_manufacture,), exclusive_group="town_economic_progression", weekly_upkeep=15, faction_flavor="Town finance and merchant credit.", design_summary="A civic bank that can later be replaced by a manufacture."),
    _text_building(slot_center_has_ambulatory, "ambulatory", "village_health", ("village",), 2500, "@Ambulatory", "@Build it to keep your people healthy. Health Cap +20 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap",), effect_numbers=(20,), affects_village=True, specialization="population_health", tier=2, prerequisite_buildings=(slot_center_has_water_supply,), upgrade_from=(slot_center_has_water_supply,), exclusive_group="village_health_progression", weekly_upkeep=15, faction_flavor="Basic village treatment and care.", center_health_bonus=20, design_summary="A local care facility replacing the water supply improvement."),
    _text_building(slot_center_has_water_supply, "water_supply", "village_health", ("village",), 1200, "@Water Supply", "@Build it to improve sanitation. Health Cap +10 (improves long-term health recovery and reduces health decline).", effect_tags=("health_cap",), effect_numbers=(10,), affects_village=True, specialization="population_health", tier=1, upgrade_to=(slot_center_has_ambulatory,), exclusive_group="village_health_progression", weekly_upkeep=5, faction_flavor="Clean water and basic sanitation.", center_health_bonus=10, design_summary="Village waterworks that can later become an ambulatory."),
    _text_building(slot_center_has_clayworks, "clayworks", "village_economy", ("village",), 2500, "@Clayworks", "@Build it to support long-term prosperity. Prosperity Cap +20 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap",), effect_numbers=(20,), affects_village=True, specialization="economic", tier=1, weekly_upkeep=10, design_summary="Village production and craft output."),
    _text_building(slot_center_has_rustic_blacksmith, "rustic_blacksmith", "village_economy", ("village",), 1200, "@Rustic Blacksmith", "@Build it to support long-term prosperity. Prosperity Cap +10 (improves long-term prosperity growth and reduces decline).", effect_tags=("prosperity_cap",), effect_numbers=(10,), affects_village=True, specialization="economic", tier=1, weekly_upkeep=5, design_summary="A small village smithy for local production."),
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

        _check_reference_slot_exists(issues, slot_name, "prerequisite_buildings", definition.get("prerequisite_buildings"))
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
