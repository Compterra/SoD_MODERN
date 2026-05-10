# -*- coding: cp1254 -*-

"""Generated center modifier aggregation.

The runtime selector keeps center systems from depending on one-off building
math. Buildings are the first source; law, investment, raid, diplomacy, and
mobile-presence sources can be layered into this same script later.
"""

from src.constants.module_constants import *
from src.constants.building_registry import BUILDING_REGISTRY
from src.constants.center_modifier_registry import CENTER_MODIFIER_REGISTRY


def _as_int(value):
    if isinstance(value, int):
        return value
    return 0


def _modifier_default(definition):
    return _as_int(definition.get("default"))


def _modifier_bounds(definition):
    minimum = _as_int(definition.get("min"))
    maximum = _as_int(definition.get("max"))
    return minimum, maximum + 1


def _building_modifier_value(building_definition, modifier_key):
    total = 0
    for entry in building_definition.get("center_modifiers", ()):
        if len(entry) < 2:
            continue
        if entry[0] == modifier_key:
            total += _as_int(entry[1])
    return total


def _build_get_center_modifier_ops():
    ops = [
        (store_script_param, ":center_no", 1),
        (store_script_param, ":modifier_id", 2),
        (assign, ":modifier_value", 0),
    ]

    for modifier_definition in CENTER_MODIFIER_REGISTRY:
        modifier_id = _as_int(modifier_definition.get("id"))
        modifier_key = modifier_definition.get("key")
        minimum, maximum = _modifier_bounds(modifier_definition)
        ops.extend([
            (try_begin,),
            (eq, ":modifier_id", modifier_id),
            (assign, ":modifier_value", _modifier_default(modifier_definition)),
        ])

        for building_definition in BUILDING_REGISTRY:
            value = _building_modifier_value(building_definition, modifier_key)
            if not value:
                continue
            building_slot = building_definition.get("building_slot")
            ops.extend([
                (try_begin,),
                (gt, ":center_no", 0),
                (party_slot_eq, ":center_no", building_slot, 1),
                (val_add, ":modifier_value", value),
                (try_end,),
            ])

        ops.extend([
            (val_clamp, ":modifier_value", minimum, maximum),
            (try_end,),
        ])

    ops.append((assign, reg0, ":modifier_value"))
    return ops


def _call_modifier_ops(local_name, modifier_constant):
    return [
        (call_script, "script_sod_get_center_modifier", ":center_no", modifier_constant),
        (assign, local_name, reg0),
    ]


def _build_get_center_modifier_totals_ops():
    ops = [
        (store_script_param, ":center_no", 1),
    ]
    hot_modifiers = (
        (":population_capacity_flat", sod_center_modifier_population_capacity_flat),
        (":population_growth_flat", sod_center_modifier_population_growth_flat),
        (":population_growth_pct", sod_center_modifier_population_growth_pct),
        (":population_recovery_flat", sod_center_modifier_population_recovery_flat),
        (":health_cap_flat", sod_center_modifier_health_cap_flat),
        (":health_recovery_flat", sod_center_modifier_health_recovery_flat),
        (":food_consumption_pct", sod_center_modifier_food_consumption_pct),
        (":food_store_capacity_flat", sod_center_modifier_food_store_capacity_flat),
        (":food_security_flat", sod_center_modifier_food_security_flat),
        (":prosperity_cap_flat", sod_center_modifier_prosperity_cap_flat),
        (":prosperity_growth_flat", sod_center_modifier_prosperity_growth_flat),
        (":prosperity_growth_pct", sod_center_modifier_prosperity_growth_pct),
        (":trade_liquidity_flat", sod_center_modifier_trade_liquidity_flat),
        (":trade_volume_pct", sod_center_modifier_trade_volume_pct),
        (":tariff_income_pct", sod_center_modifier_tariff_income_pct),
        (":raid_resistance_pct", sod_center_modifier_raid_resistance_pct),
        (":raid_recovery_flat", sod_center_modifier_raid_recovery_flat),
        (":security_flat", sod_center_modifier_security_flat),
        (":construction_speed_pct", sod_center_modifier_construction_speed_pct),
        (":construction_cost_pct", sod_center_modifier_construction_cost_pct),
        (":weekly_upkeep_flat", sod_center_modifier_weekly_upkeep_flat),
    )
    for local_name, modifier_constant in hot_modifiers:
        ops.extend(_call_modifier_ops(local_name, modifier_constant))

    ops.extend([
        (assign, reg0, ":population_capacity_flat"),
        (assign, reg1, ":population_growth_flat"),
        (assign, reg2, ":population_growth_pct"),
        (assign, reg3, ":population_recovery_flat"),
        (assign, reg4, ":health_cap_flat"),
        (assign, reg5, ":health_recovery_flat"),
        (assign, reg6, ":food_consumption_pct"),
        (assign, reg7, ":food_store_capacity_flat"),
        (assign, reg8, ":food_security_flat"),
        (assign, reg9, ":prosperity_cap_flat"),
        (assign, reg10, ":prosperity_growth_flat"),
        (assign, reg11, ":prosperity_growth_pct"),
        (assign, reg12, ":trade_liquidity_flat"),
        (assign, reg13, ":trade_volume_pct"),
        (assign, reg14, ":tariff_income_pct"),
        (assign, reg15, ":raid_resistance_pct"),
        (assign, reg16, ":raid_recovery_flat"),
        (assign, reg17, ":security_flat"),
        (assign, reg18, ":construction_speed_pct"),
        (assign, reg19, ":construction_cost_pct"),
        (assign, reg20, ":weekly_upkeep_flat"),
    ])
    return ops


SCRIPTS = [
    ("sod_get_center_modifier", _build_get_center_modifier_ops()),
    ("sod_get_center_modifier_totals", _build_get_center_modifier_totals_ops()),
]
