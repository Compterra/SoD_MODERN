# -*- coding: cp1254 -*-

"""Canonical center modifier registry.

The modifier layer gives buildings, laws, investments, raids, and mobile
presence systems a shared vocabulary. Runtime scripts can ask for one modifier
without knowing which systems contributed to it.
"""

from src.constants.module_constants import *

try:
    integer_types = (int, long)
except NameError:
    integer_types = (int,)


CENTER_MODIFIER_FLAT = "flat"
CENTER_MODIFIER_PERCENT = "percent"
CENTER_MODIFIER_REDUCTION_PERCENT = "reduction_percent"


def _modifier(
    key,
    constant,
    category,
    label,
    value_type=CENTER_MODIFIER_FLAT,
    default=0,
    minimum=-1000000,
    maximum=1000000,
):
    return {
        "key": key,
        "id": constant,
        "constant_name": "sod_center_modifier_%s" % key,
        "category": category,
        "label": label,
        "value_type": value_type,
        "default": default,
        "min": minimum,
        "max": maximum,
    }


CENTER_MODIFIER_REGISTRY = (
    _modifier("trade_liquidity_flat", sod_center_modifier_trade_liquidity_flat, "economy_trade", "Trade Liquidity", CENTER_MODIFIER_FLAT, 0, -100, 500),
    _modifier("trade_volume_pct", sod_center_modifier_trade_volume_pct, "economy_trade", "Trade Volume %", CENTER_MODIFIER_PERCENT, 100, 25, 200),
    _modifier("tariff_income_pct", sod_center_modifier_tariff_income_pct, "economy_trade", "Tariff Income %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("market_wealth_flat", sod_center_modifier_market_wealth_flat, "economy_trade", "Market Wealth", CENTER_MODIFIER_FLAT, 0, -50000, 50000),
    _modifier("market_wealth_pct", sod_center_modifier_market_wealth_pct, "economy_trade", "Market Wealth %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("prosperity_cap_flat", sod_center_modifier_prosperity_cap_flat, "economy_trade", "Prosperity Cap", CENTER_MODIFIER_FLAT, 0, -100, 200),
    _modifier("prosperity_growth_flat", sod_center_modifier_prosperity_growth_flat, "economy_trade", "Prosperity Growth", CENTER_MODIFIER_FLAT, 0, -50, 50),
    _modifier("prosperity_growth_pct", sod_center_modifier_prosperity_growth_pct, "economy_trade", "Prosperity Growth %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("production_output_pct", sod_center_modifier_production_output_pct, "economy_trade", "Production Output %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("goods_import_demand_pct", sod_center_modifier_goods_import_demand_pct, "economy_trade", "Goods Import Demand %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("goods_export_supply_pct", sod_center_modifier_goods_export_supply_pct, "economy_trade", "Goods Export Supply %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("merchant_happiness_flat", sod_center_modifier_merchant_happiness_flat, "economy_trade", "Merchant Happiness", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("tax_efficiency_pct", sod_center_modifier_tax_efficiency_pct, "economy_trade", "Tax Efficiency %", CENTER_MODIFIER_PERCENT, 100, 0, 300),

    _modifier("population_capacity_flat", sod_center_modifier_population_capacity_flat, "population_health_food", "Population Capacity", CENTER_MODIFIER_FLAT, 0, -10000, 20000),
    _modifier("population_growth_flat", sod_center_modifier_population_growth_flat, "population_health_food", "Population Growth", CENTER_MODIFIER_FLAT, 0, -25, 50),
    _modifier("population_growth_pct", sod_center_modifier_population_growth_pct, "population_health_food", "Population Growth %", CENTER_MODIFIER_PERCENT, 100, 20, 300),
    _modifier("population_recovery_flat", sod_center_modifier_population_recovery_flat, "population_health_food", "Population Recovery", CENTER_MODIFIER_FLAT, 0, -25, 100),
    _modifier("migration_attraction_flat", sod_center_modifier_migration_attraction_flat, "population_health_food", "Migration Attraction", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("migration_retention_flat", sod_center_modifier_migration_retention_flat, "population_health_food", "Migration Retention", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("health_cap_flat", sod_center_modifier_health_cap_flat, "population_health_food", "Health Cap", CENTER_MODIFIER_FLAT, 0, -100, 200),
    _modifier("health_recovery_flat", sod_center_modifier_health_recovery_flat, "population_health_food", "Health Recovery", CENTER_MODIFIER_FLAT, 0, -25, 50),
    _modifier("disease_resistance_pct", sod_center_modifier_disease_resistance_pct, "population_health_food", "Disease Resistance %", CENTER_MODIFIER_REDUCTION_PERCENT, 0, 0, 95),
    _modifier("food_consumption_pct", sod_center_modifier_food_consumption_pct, "population_health_food", "Food Consumption %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("food_store_capacity_flat", sod_center_modifier_food_store_capacity_flat, "population_health_food", "Food Store Capacity", CENTER_MODIFIER_FLAT, 0, -1000, 5000),
    _modifier("food_security_flat", sod_center_modifier_food_security_flat, "population_health_food", "Food Security", CENTER_MODIFIER_FLAT, 0, -500, 500),
    _modifier("cattle_growth_flat", sod_center_modifier_cattle_growth_flat, "population_health_food", "Cattle Growth", CENTER_MODIFIER_FLAT, 0, -50, 100),
    _modifier("cattle_output_pct", sod_center_modifier_cattle_output_pct, "population_health_food", "Cattle Output %", CENTER_MODIFIER_PERCENT, 100, 25, 250),

    _modifier("security_flat", sod_center_modifier_security_flat, "security_recovery", "Security", CENTER_MODIFIER_FLAT, 0, -100, 200),
    _modifier("raid_resistance_pct", sod_center_modifier_raid_resistance_pct, "security_recovery", "Raid Resistance %", CENTER_MODIFIER_REDUCTION_PERCENT, 0, 0, 95),
    _modifier("raid_recovery_flat", sod_center_modifier_raid_recovery_flat, "security_recovery", "Raid Recovery", CENTER_MODIFIER_FLAT, 0, -25, 100),
    _modifier("threat_reduction_flat", sod_center_modifier_threat_reduction_flat, "security_recovery", "Threat Reduction", CENTER_MODIFIER_FLAT, 0, -200, 500),
    _modifier("bandit_spawn_reduction_pct", sod_center_modifier_bandit_spawn_reduction_pct, "security_recovery", "Bandit Spawn Reduction %", CENTER_MODIFIER_REDUCTION_PERCENT, 0, 0, 95),
    _modifier("desperation_bandit_reduction_pct", sod_center_modifier_desperation_bandit_reduction_pct, "security_recovery", "Desperation Bandit Reduction %", CENTER_MODIFIER_REDUCTION_PERCENT, 0, 0, 95),
    _modifier("unrest_flat", sod_center_modifier_unrest_flat, "security_recovery", "Unrest", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("unrest_reduction_flat", sod_center_modifier_unrest_reduction_flat, "security_recovery", "Unrest Reduction", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("prisoner_escape_reduction_pct", sod_center_modifier_prisoner_escape_reduction_pct, "security_recovery", "Prisoner Escape Reduction %", CENTER_MODIFIER_REDUCTION_PERCENT, 0, 0, 95),
    _modifier("warning_range_flat", sod_center_modifier_warning_range_flat, "security_recovery", "Warning Range", CENTER_MODIFIER_FLAT, 0, 0, 10),
    _modifier("patrol_response_pct", sod_center_modifier_patrol_response_pct, "security_recovery", "Patrol Response %", CENTER_MODIFIER_PERCENT, 100, 25, 250),

    _modifier("infantry_training_flat", sod_center_modifier_infantry_training_flat, "military_recruitment", "Infantry Training", CENTER_MODIFIER_FLAT, 0, 0, 10),
    _modifier("ranged_training_flat", sod_center_modifier_ranged_training_flat, "military_recruitment", "Ranged Training", CENTER_MODIFIER_FLAT, 0, 0, 10),
    _modifier("cavalry_training_flat", sod_center_modifier_cavalry_training_flat, "military_recruitment", "Cavalry Training", CENTER_MODIFIER_FLAT, 0, 0, 10),
    _modifier("garrison_recovery_flat", sod_center_modifier_garrison_recovery_flat, "military_recruitment", "Garrison Recovery", CENTER_MODIFIER_FLAT, 0, 0, 100),
    _modifier("garrison_upkeep_pct", sod_center_modifier_garrison_upkeep_pct, "military_recruitment", "Garrison Upkeep %", CENTER_MODIFIER_PERCENT, 100, 0, 250),
    _modifier("troop_upgrade_cost_pct", sod_center_modifier_troop_upgrade_cost_pct, "military_recruitment", "Troop Upgrade Cost %", CENTER_MODIFIER_PERCENT, 100, 0, 250),
    _modifier("recruit_count_flat", sod_center_modifier_recruit_count_flat, "military_recruitment", "Recruit Count", CENTER_MODIFIER_FLAT, 0, -25, 50),
    _modifier("recruit_tier_bonus_flat", sod_center_modifier_recruit_tier_bonus_flat, "military_recruitment", "Recruit Tier Bonus", CENTER_MODIFIER_FLAT, 0, -5, 5),
    _modifier("noble_recruitment_flat", sod_center_modifier_noble_recruitment_flat, "military_recruitment", "Noble Recruitment", CENTER_MODIFIER_FLAT, 0, 0, 20),
    _modifier("faith_troop_access_flat", sod_center_modifier_faith_troop_access_flat, "military_recruitment", "Faith Troop Access", CENTER_MODIFIER_FLAT, 0, 0, 5),
    _modifier("faith_ascension_bonus_flat", sod_center_modifier_faith_ascension_bonus_flat, "military_recruitment", "Faith Ascension Bonus", CENTER_MODIFIER_FLAT, 0, 0, 100),

    _modifier("construction_speed_pct", sod_center_modifier_construction_speed_pct, "construction_admin_prestige", "Construction Speed %", CENTER_MODIFIER_PERCENT, 100, 25, 250),
    _modifier("construction_cost_pct", sod_center_modifier_construction_cost_pct, "construction_admin_prestige", "Construction Cost %", CENTER_MODIFIER_PERCENT, 100, 0, 250),
    _modifier("weekly_upkeep_flat", sod_center_modifier_weekly_upkeep_flat, "construction_admin_prestige", "Weekly Upkeep", CENTER_MODIFIER_FLAT, 0, 0, 100000),
    _modifier("demesne_cost_flat", sod_center_modifier_demesne_cost_flat, "construction_admin_prestige", "Demesne Cost", CENTER_MODIFIER_FLAT, 0, -50, 50),
    _modifier("renown_weekly_flat", sod_center_modifier_renown_weekly_flat, "construction_admin_prestige", "Weekly Renown", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("relations_weekly_flat", sod_center_modifier_relations_weekly_flat, "construction_admin_prestige", "Weekly Relations", CENTER_MODIFIER_FLAT, 0, -20, 20),
    _modifier("administration_flat", sod_center_modifier_administration_flat, "construction_admin_prestige", "Administration", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("law_compliance_flat", sod_center_modifier_law_compliance_flat, "construction_admin_prestige", "Law Compliance", CENTER_MODIFIER_FLAT, 0, -100, 100),

    _modifier("local_faith_growth_flat", sod_center_modifier_local_faith_growth_flat, "faith_culture", "Local Faith Growth", CENTER_MODIFIER_FLAT, 0, -50, 100),
    _modifier("global_faith_growth_flat", sod_center_modifier_global_faith_growth_flat, "faith_culture", "Global Faith Growth", CENTER_MODIFIER_FLAT, 0, -50, 100),
    _modifier("faith_stability_flat", sod_center_modifier_faith_stability_flat, "faith_culture", "Faith Stability", CENTER_MODIFIER_FLAT, 0, -100, 100),
    _modifier("cultural_assimilation_flat", sod_center_modifier_cultural_assimilation_flat, "faith_culture", "Cultural Assimilation", CENTER_MODIFIER_FLAT, 0, -50, 100),
)


CENTER_MODIFIER_BY_KEY = dict((definition["key"], definition) for definition in CENTER_MODIFIER_REGISTRY)
CENTER_MODIFIER_BY_ID = dict((definition["id"], definition) for definition in CENTER_MODIFIER_REGISTRY)
CENTER_MODIFIER_KEYS = tuple(definition["key"] for definition in CENTER_MODIFIER_REGISTRY)
CENTER_MODIFIER_IDS = dict((definition["key"], definition["id"]) for definition in CENTER_MODIFIER_REGISTRY)
SUPPORTED_CENTER_MODIFIERS = CENTER_MODIFIER_KEYS


BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER = {
    "weekly_relations": "relations_weekly_flat",
    "weekly_loyalty": "relations_weekly_flat",
    "weekly_prosperity": "prosperity_growth_flat",
    "weekly_local_faith": "local_faith_growth_flat",
    "weekly_global_faith": "global_faith_growth_flat",
    "weekly_renown": "renown_weekly_flat",
    "weekly_taxes_percent": "tax_efficiency_pct",
    "demesne_cost": "demesne_cost_flat",
    "health_cap": "health_cap_flat",
    "prosperity_cap": "prosperity_cap_flat",
    "population_capacity": "population_capacity_flat",
    "weekly_population_growth": "population_growth_flat",
    "raid_recovery": "raid_recovery_flat",
    "loot_time_bonus_percent": "raid_resistance_pct",
    "enemy_warning_messages": "warning_range_flat",
    "captives_escape_chance": "prisoner_escape_reduction_pct",
    "infantry_training": "infantry_training_flat",
    "ranged_training": "ranged_training_flat",
    "cavalry_training": "cavalry_training_flat",
    "noble_assembly": "noble_recruitment_flat",
    "faith_troop_upgrade": "faith_troop_access_flat",
    "troop_upgrade_cost_multiplier": "troop_upgrade_cost_pct",
    "garrison_upkeep_reduction": "garrison_upkeep_pct",
}


BUILDING_FIELD_TO_CENTER_MODIFIER = (
    ("center_health_bonus", "health_cap_flat"),
    ("prosperity_cap_bonus", "prosperity_cap_flat"),
    ("prosperity_multiplier_bonus_percent", "prosperity_growth_pct"),
    ("demesne_cost", "demesne_cost_flat"),
    ("weekly_renown_bonus", "renown_weekly_flat"),
    ("weekly_prosperity_bonus", "prosperity_growth_flat"),
    ("weekly_income_bonus_percent", "tax_efficiency_pct"),
    ("population_capacity_bonus", "population_capacity_flat"),
    ("weekly_population_growth_bonus", "population_growth_flat"),
    ("raid_recovery_bonus", "raid_recovery_flat"),
    ("weekly_upkeep", "weekly_upkeep_flat"),
)


def get_center_modifier_definition(modifier):
    if modifier in CENTER_MODIFIER_BY_KEY:
        return CENTER_MODIFIER_BY_KEY.get(modifier)
    return CENTER_MODIFIER_BY_ID.get(modifier)


def get_center_modifier_id(modifier):
    definition = get_center_modifier_definition(modifier)
    if definition is None:
        return sod_center_modifier_none
    return definition["id"]


def get_center_modifier_key(modifier):
    definition = get_center_modifier_definition(modifier)
    if definition is None:
        return None
    return definition["key"]


def get_center_modifier_default(modifier):
    definition = get_center_modifier_definition(modifier)
    if definition is None:
        return 0
    return definition["default"]


def clamp_center_modifier_value(modifier, value):
    definition = get_center_modifier_definition(modifier)
    if definition is None:
        return value
    if value < definition["min"]:
        return definition["min"]
    if value > definition["max"]:
        return definition["max"]
    return value


def normalize_center_modifier_entries(entries):
    normalized = []
    if entries is None:
        return ()
    for entry in entries:
        if len(entry) < 2:
            continue
        modifier_key = get_center_modifier_key(entry[0])
        value = entry[1]
        source_key = entry[2] if len(entry) > 2 else "manual"
        if modifier_key is None or not isinstance(value, integer_types):
            continue
        normalized.append((modifier_key, value, source_key))
    return tuple(normalized)


def derive_building_center_modifiers(definition):
    modifiers = []
    seen = {}
    for field_name, modifier_key in BUILDING_FIELD_TO_CENTER_MODIFIER:
        value = definition.get(field_name, 0)
        if isinstance(value, integer_types) and value:
            if modifier_key == "prosperity_growth_pct":
                value = int(value)
            seen[modifier_key] = seen.get(modifier_key, 0) + int(value)

    effect_tags = tuple(definition.get("effect_tags", ()))
    effect_numbers = tuple(definition.get("effect_numbers", ()))
    for index, tag in enumerate(effect_tags):
        if index >= len(effect_numbers):
            continue
        value = effect_numbers[index]
        if not isinstance(value, integer_types) or not value:
            continue
        modifier_key = BUILDING_EFFECT_TAG_TO_CENTER_MODIFIER.get(tag)
        if modifier_key is None:
            continue

        if modifier_key == "troop_upgrade_cost_pct":
            # Legacy tag stores the resulting cost percent, while the modifier
            # source stores a delta around the neutral 100%.
            value = int(value) - 100
        elif modifier_key == "garrison_upkeep_pct":
            value = -50 if value > 0 else 0
        elif modifier_key == "demesne_cost_flat":
            value = abs(int(value))
        if modifier_key in seen:
            continue
        seen[modifier_key] = seen.get(modifier_key, 0) + int(value)

    for modifier_key, value in sorted(seen.items()):
        modifiers.append((modifier_key, value, "building"))
    return tuple(modifiers)


def validate_center_modifier_registry():
    issues = []
    seen_keys = {}
    seen_ids = {}
    for definition in CENTER_MODIFIER_REGISTRY:
        key = definition.get("key")
        modifier_id = definition.get("id")
        seen_keys[key] = seen_keys.get(key, 0) + 1
        seen_ids[modifier_id] = seen_ids.get(modifier_id, 0) + 1
        if not key:
            issues.append("center modifier has no key")
        if not isinstance(modifier_id, integer_types) or modifier_id <= 0:
            issues.append("%s: invalid modifier id %s" % (key, modifier_id))
        if definition.get("value_type") not in (CENTER_MODIFIER_FLAT, CENTER_MODIFIER_PERCENT, CENTER_MODIFIER_REDUCTION_PERCENT):
            issues.append("%s: unsupported value_type %s" % (key, definition.get("value_type")))
        if definition.get("min") > definition.get("max"):
            issues.append("%s: min is greater than max" % key)
        if definition.get("default") < definition.get("min") or definition.get("default") > definition.get("max"):
            issues.append("%s: default %s is outside bounds %s..%s" % (key, definition.get("default"), definition.get("min"), definition.get("max")))
        if definition.get("value_type") == CENTER_MODIFIER_PERCENT and definition.get("default") != 100:
            issues.append("%s: percent modifiers should default to 100" % key)
        if definition.get("value_type") == CENTER_MODIFIER_REDUCTION_PERCENT and definition.get("default") != 0:
            issues.append("%s: reduction percent modifiers should default to 0" % key)
        if definition.get("min") <= -1000000 or definition.get("max") >= 1000000:
            issues.append("%s: modifier bounds are too broad for safe runtime use" % key)
    duplicates = [key for key, count in seen_keys.items() if count > 1]
    if duplicates:
        issues.append("duplicate center modifier keys: %s" % ", ".join(map(str, duplicates)))
    duplicate_ids = [modifier_id for modifier_id, count in seen_ids.items() if count > 1]
    if duplicate_ids:
        issues.append("duplicate center modifier ids: %s" % ", ".join(map(str, duplicate_ids)))
    return issues
