# -*- coding: cp1254 -*-

from src.constants.module_constants import *
from src.constants.building_registry import BUILDING_REGISTRY


def _build_grouped_construction_count_ops(center_param_name):
    grouped_slots = []
    grouped_lookup = {}
    standalone_slots = []

    for definition in BUILDING_REGISTRY:
        if not isinstance(definition, dict):
            continue
        group = definition.get("exclusive_group")
        slot_name = definition.get("building_slot")
        if not slot_name:
            continue
        if group:
            if group not in grouped_lookup:
                grouped_lookup[group] = []
                grouped_slots.append(group)
            grouped_lookup[group].append(slot_name)
        else:
            standalone_slots.append(slot_name)

    ops = [
        (assign, ":num_improvements", 0),
    ]

    for slot_name in standalone_slots:
        ops.extend([
            (try_begin,),
            (call_script, "script_validate_construction_choice", center_param_name, slot_name, 1),
            (eq, reg0, 1),
            (val_add, ":num_improvements", 1),
            (try_end,),
        ])

    for group in grouped_slots:
        slots = grouped_lookup[group]
        ops.extend([
            (assign, ":group_available", 0),
            (try_begin,),
        ])
        for index, slot_name in enumerate(slots):
            if index > 0:
                ops.append((else_try,))
            ops.extend([
                (eq, ":group_available", 0),
                (call_script, "script_validate_construction_choice", center_param_name, slot_name, 1),
                (eq, reg0, 1),
                (assign, ":group_available", 1),
            ])
        ops.extend([
            (try_end,),
            (try_begin,),
            (eq, ":group_available", 1),
            (val_add, ":num_improvements", 1),
            (try_end,),
        ])

    ops.append((assign, reg0, ":num_improvements"))
    return ops


SCRIPTS = [
    (
        "center_has_more_construction_opportunities",
        [
            (store_script_param, ":center", 1),
        ] + _build_grouped_construction_count_ops(":center"),
    ),
]