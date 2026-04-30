# -*- coding: cp1254 -*-

"""Generated building-effect aggregation.

This keeps runtime center calculations pointed at the registry while preserving
the old slot_center_has_* save format.
"""

from src.constants.module_constants import *
from src.constants.building_registry import BUILDING_REGISTRY


def _as_int(value):
    if isinstance(value, int):
        return value
    return 0


def _build_effect_total_ops():
    ops = [
        (store_script_param, ":center_no", 1),
        (assign, ":weekly_relations", 0),
        (assign, ":weekly_prosperity", 0),
        (assign, ":weekly_local_faith", 0),
        (assign, ":weekly_global_faith", 0),
        (assign, ":weekly_renown", 0),
        (assign, ":weekly_income_percent", 0),
        (assign, ":center_health_bonus", 0),
        (assign, ":prosperity_cap_bonus", 0),
        (assign, ":demesne_cost", 0),
        (assign, ":weekly_upkeep", 0),
        (assign, ":prosperity_multiplier_percent", 0),
    ]

    for definition in BUILDING_REGISTRY:
        building_slot = definition.get("building_slot")
        if not building_slot:
            continue

        ops.extend([
            (try_begin,),
            (party_slot_eq, ":center_no", building_slot, 1),
        ])

        weekly_upkeep = _as_int(definition.get("weekly_upkeep"))
        center_health_bonus = _as_int(definition.get("center_health_bonus"))
        prosperity_cap_bonus = _as_int(definition.get("prosperity_cap_bonus"))
        prosperity_multiplier = _as_int(definition.get("prosperity_multiplier_bonus_percent"))
        demesne_cost = _as_int(definition.get("demesne_cost"))
        weekly_renown = _as_int(definition.get("weekly_renown_bonus"))
        weekly_prosperity = _as_int(definition.get("weekly_prosperity_bonus"))
        weekly_income_percent = _as_int(definition.get("weekly_income_bonus_percent"))

        if weekly_upkeep:
            ops.append((val_add, ":weekly_upkeep", weekly_upkeep))
        if center_health_bonus:
            ops.append((val_add, ":center_health_bonus", center_health_bonus))
        if prosperity_cap_bonus:
            ops.append((val_add, ":prosperity_cap_bonus", prosperity_cap_bonus))
        if prosperity_multiplier:
            ops.append((val_add, ":prosperity_multiplier_percent", prosperity_multiplier))
        if demesne_cost:
            ops.append((val_add, ":demesne_cost", demesne_cost))
        if weekly_renown:
            ops.append((val_add, ":weekly_renown", weekly_renown))
        if weekly_prosperity:
            ops.append((val_add, ":weekly_prosperity", weekly_prosperity))
        if weekly_income_percent:
            ops.append((val_add, ":weekly_income_percent", weekly_income_percent))

        effect_tags = tuple(definition.get("effect_tags", ()))
        effect_numbers = tuple(definition.get("effect_numbers", ()))
        for index, tag in enumerate(effect_tags):
            value = effect_numbers[index] if index < len(effect_numbers) else 0
            if not isinstance(value, int) or not value:
                continue
            if tag == "weekly_relations":
                ops.append((val_add, ":weekly_relations", value))
            elif tag == "weekly_local_faith":
                ops.append((val_add, ":weekly_local_faith", value))
            elif tag == "weekly_global_faith":
                ops.append((val_add, ":weekly_global_faith", value))

        ops.append((try_end,))

    ops.extend([
        (assign, reg0, ":weekly_relations"),
        (assign, reg1, ":weekly_prosperity"),
        (assign, reg2, ":weekly_local_faith"),
        (assign, reg3, ":weekly_global_faith"),
        (assign, reg4, ":weekly_renown"),
        (assign, reg5, ":weekly_income_percent"),
        (assign, reg6, ":center_health_bonus"),
        (assign, reg7, ":prosperity_cap_bonus"),
        (assign, reg8, ":demesne_cost"),
        (assign, reg9, ":weekly_upkeep"),
        (assign, reg10, ":prosperity_multiplier_percent"),
    ])
    return ops


SCRIPTS = [
    ("get_center_building_effect_totals", _build_effect_total_ops()),
]
