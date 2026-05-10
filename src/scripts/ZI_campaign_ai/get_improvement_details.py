# -*- coding: cp1254 -*-

from src.constants.module_constants import *
from src.constants.building_registry import (
    BUILDING_REGISTRY,
    get_building_design_summary,
    get_building_exclusive_group,
    get_building_faction_flavor,
    get_building_faction_requirements,
    get_building_specialization,
    get_building_tier,
    get_building_upgrade_sources,
    get_building_upgrade_targets,
    get_building_weekly_upkeep,
)


BUILDING_CAN_BUILD_OK = 0
BUILDING_CAN_BUILD_UNKNOWN = 1
BUILDING_CAN_BUILD_WRONG_CENTER = 2
BUILDING_CAN_BUILD_MISSING_PREREQUISITE = 3
BUILDING_CAN_BUILD_CONFLICT = 4


CENTER_TYPE_CONSTANTS = {
    "village": spt_village,
    "town": spt_town,
    "castle": spt_castle,
}


def _string_types():
    try:
        return (basestring,)
    except NameError:
        return (str,)


def _is_string(value):
    return isinstance(value, _string_types())


def _normalize_label(value, fallback="General"):
    if not value:
        return fallback
    return value.replace("_", " ").title()


def _literal_string(value, fallback="@-"):
    if value is None or value == "":
        return fallback
    if _is_string(value) and value.startswith("@"):
        return value
    return "@%s" % value


def _is_faith_building(definition):
    return definition["ui_category"] == "faith"


def _building_duration(definition):
    if definition["build_days"] is not None:
        return definition["build_days"]
    if definition["build_hours"] is not None:
        return definition["build_hours"]
    return 0


def _store_display_name_ops(definition):
    if definition["name_string_id"] is not None:
        if _is_faith_building(definition):
            return [
                (assign, ":s0", definition["name_string_id"]),
                (val_add, ":s0", "$g_sod_faith"),
                (str_store_string, s0, ":s0"),
            ]
        return [(str_store_string, s0, definition["name_string_id"])]
    return [(str_store_string, s0, definition["name_text"])]


def _store_description_ops(definition):
    if definition["description_string_id"] is not None:
        if _is_faith_building(definition):
            return [
                (assign, ":s1", definition["description_string_id"]),
                (val_add, ":s1", "$g_sod_faith"),
                (str_store_string, s1, ":s1"),
                (str_store_string, s1, "@{s1} %s" % definition["effect_summary"].lstrip("@")),
            ]
        return [(str_store_string, s1, definition["description_string_id"])]
    return [(str_store_string, s1, definition["description_text"])]


def _store_cost_ops(definition):
    return [(assign, reg0, definition["cost"])]


def _store_definition_metadata_ops(definition):
    building_slot = definition["building_slot"]
    specialization = get_building_specialization(building_slot)
    specialization_label = _normalize_label(specialization or definition["ui_category"])
    upgrade_sources = tuple(get_building_upgrade_sources(building_slot))
    upgrade_targets = tuple(get_building_upgrade_targets(building_slot))
    exclusive_group = get_building_exclusive_group(building_slot)
    weekly_upkeep = get_building_weekly_upkeep(building_slot)
    faction_requirements = tuple(get_building_faction_requirements(building_slot))
    design_summary = get_building_design_summary(building_slot)
    faction_flavor = get_building_faction_flavor(building_slot)

    source_slot = upgrade_sources[0] if len(upgrade_sources) > 0 else None
    target_slot = upgrade_targets[0] if len(upgrade_targets) > 0 else None

    ops = [
        (str_store_string_reg, s8, s0),
        (str_store_string_reg, s9, s1),
        (assign, reg0, definition["cost"]),
        (assign, reg1, _building_duration(definition)),
        (assign, reg2, len(definition["prerequisite_buildings"])),
        (assign, reg3, len(definition["conflicts_with"])),
        (assign, reg4, 1 if definition["is_unique"] else 0),
        (assign, reg5, 1 if definition["is_upgradable"] else 0),
        (assign, reg6, len(definition["effect_tags"])),
        (assign, reg7, get_building_tier(building_slot)),
        (assign, reg8, weekly_upkeep),
        (assign, reg9, len(faction_requirements)),
    ]

    if source_slot is not None:
        ops.extend([
            (call_script, "script_get_building_display_name", source_slot),
            (str_store_string_reg, s3, s0),
        ])
    else:
        ops.append((str_store_string, s3, "@-"))

    if target_slot is not None:
        ops.extend([
            (call_script, "script_get_building_display_name", target_slot),
            (str_store_string_reg, s4, s0),
        ])
    else:
        ops.append((str_store_string, s4, "@-"))

    ops.extend([
        (str_store_string_reg, s0, s8),
        (str_store_string_reg, s1, s9),
        (str_store_string, s2, _literal_string(specialization_label)),
    ])

    if exclusive_group:
        ops.append((str_store_string, s5, _literal_string(_normalize_label(exclusive_group))))
    else:
        ops.append((str_store_string, s5, "@-"))

    ops.append((str_store_string, s6, _literal_string(design_summary)))
    ops.append((str_store_string, s7, _literal_string("Weekly upkeep: %d denars/week" % weekly_upkeep)))
    ops.append((str_store_string, s8, _literal_string(faction_flavor)))
    if faction_requirements:
        ops.append((str_store_string, s9, _literal_string("Faction requirements: %d" % len(faction_requirements))))
    else:
        ops.append((str_store_string, s9, "@-"))

    return ops


def _store_prerequisites_ops(definition):
    prereqs = tuple(definition["prerequisite_buildings"]) + tuple(definition.get("prerequisite_any_buildings", ()))
    ops = [
        (assign, reg0, len(prereqs)),
        (assign, reg1, 0),
        (assign, reg2, 0),
        (assign, reg3, 0),
        (assign, reg4, 0),
        (assign, reg5, 0),
        (assign, reg6, 0),
    ]
    for index, prereq in enumerate(prereqs[:6]):
        ops.append((assign, reg(index + 1), prereq))
    return ops


def _store_center_type_ok_ops(definition):
    allowed_center_types = definition["allowed_center_types"]
    if len(allowed_center_types) == 3:
        return [(assign, ":center_type_ok", 1)]

    ops = [(assign, ":center_type_ok", 0)]
    ops.append((try_begin,))
    for index, center_type in enumerate(allowed_center_types):
        if index > 0:
            ops.append((else_try,))
        ops.append((eq, ":center_type", CENTER_TYPE_CONSTANTS[center_type]))
        ops.append((assign, ":center_type_ok", 1))
    ops.append((try_end,))
    return ops


def _store_prereq_ok_ops(definition):
    prereqs = definition["prerequisite_buildings"]
    any_prereqs = tuple(definition.get("prerequisite_any_buildings", ()))
    ops = [
        (assign, ":prereq_ok", 1),
        (assign, ":blocked_slot", 0),
        (assign, ":any_prereq_ok", 0),
    ]
    for prereq in prereqs:
        ops.extend([
            (try_begin,),
            (eq, ":prereq_ok", 1),
            (party_slot_ge, ":center_no", prereq, 1),
            (else_try,),
            (eq, ":prereq_ok", 1),
            (assign, ":prereq_ok", 0),
            (assign, ":blocked_slot", prereq),
            (try_end,),
        ])
    if any_prereqs:
        ops.append((try_begin,))
        for index, prereq in enumerate(any_prereqs):
            if index > 0:
                ops.append((else_try,))
            ops.extend([
                (party_slot_ge, ":center_no", prereq, 1),
                (assign, ":any_prereq_ok", 1),
            ])
        ops.extend([
            (try_end,),
            (try_begin,),
            (eq, ":prereq_ok", 1),
            (eq, ":any_prereq_ok", 0),
            (assign, ":prereq_ok", 0),
            (assign, ":blocked_slot", any_prereqs[0]),
            (try_end,),
        ])
    return ops


def _store_conflict_ok_ops(definition):
    conflicts = definition["conflicts_with"]
    ops = [
        (assign, ":conflict_ok", 1),
        (assign, ":blocked_slot", 0),
    ]
    for conflict in conflicts:
        ops.extend([
            (try_begin,),
            (eq, ":conflict_ok", 1),
            (party_slot_ge, ":center_no", conflict, 1),
            (assign, ":conflict_ok", 0),
            (assign, ":blocked_slot", conflict),
            (try_end,),
        ])
    return ops


def _build_lookup_ops(definition, output_mode):
    ops = []
    if output_mode == "display_name":
        ops.extend(_store_display_name_ops(definition))
    elif output_mode == "description":
        ops.extend(_store_description_ops(definition))
    elif output_mode == "cost":
        ops.extend(_store_cost_ops(definition))
    elif output_mode == "definition":
        ops.extend(_store_display_name_ops(definition))
        ops.extend(_store_description_ops(definition))
        ops.extend(_store_definition_metadata_ops(definition))
    elif output_mode == "prerequisites":
        ops.extend(_store_prerequisites_ops(definition))
    elif output_mode == "can_build":
        ops.extend([
            (assign, reg0, 1),
            (assign, reg1, BUILDING_CAN_BUILD_OK),
            (assign, reg2, 0),
            (party_get_slot, ":center_type", ":center_no", slot_party_type),
        ])
        ops.extend(_store_center_type_ok_ops(definition))
        ops.extend([
            (try_begin,),
            (eq, ":center_type_ok", 1),
        ])
        ops.extend(_store_prereq_ok_ops(definition))
        ops.extend([
            (try_begin,),
            (eq, ":prereq_ok", 1),
        ])
        ops.extend(_store_conflict_ok_ops(definition))
        ops.extend([
            (try_begin,),
            (eq, ":conflict_ok", 1),
            (assign, reg0, 1),
            (assign, reg1, BUILDING_CAN_BUILD_OK),
            (assign, reg2, 0),
            (else_try,),
            (assign, reg0, 0),
            (assign, reg1, BUILDING_CAN_BUILD_CONFLICT),
            (assign, reg2, ":blocked_slot"),
            (try_end,),
            (else_try,),
            (assign, reg0, 0),
            (assign, reg1, BUILDING_CAN_BUILD_MISSING_PREREQUISITE),
            (assign, reg2, ":blocked_slot"),
            (try_end,),
            (else_try,),
            (assign, reg0, 0),
            (assign, reg1, BUILDING_CAN_BUILD_WRONG_CENTER),
            (assign, reg2, 0),
            (try_end,),
        ])
    elif output_mode == "apply_effects":
        ops.extend([
            (call_script, "script_can_build_improvement", ":center_no", ":building_no"),
            (assign, reg2, reg0),
        ])
    return ops


def _build_branching_script(script_name, param_names, output_mode):
    ops = []
    for index, param_name in enumerate(param_names):
        ops.append((store_script_param, param_name, index + 1))

    for index, definition in enumerate(BUILDING_REGISTRY):
        ops.append((try_begin,) if index == 0 else (else_try,))
        ops.append((eq, ":building_no", definition["building_slot"]))
        ops.extend(_build_lookup_ops(definition, output_mode))

    ops.extend([
        (else_try,),
        (assign, reg0, 0),
        (assign, reg1, BUILDING_CAN_BUILD_UNKNOWN),
        (assign, reg2, 0),
        (str_store_string, s0, "@Error: Invalid improvement #{reg0}"),
        (str_store_string_reg, s1, s0),
        (try_end,),
    ])

    return ops


def _build_get_building_definition_ops():
    return _build_branching_script(
        "get_building_definition",
        [":building_no"],
        "definition",
    )


def _build_get_building_display_name_ops():
    return _build_branching_script(
        "get_building_display_name",
        [":building_no"],
        "display_name",
    )


def _build_get_building_description_ops():
    return _build_branching_script(
        "get_building_description",
        [":building_no"],
        "description",
    )


def _build_get_building_cost_ops():
    return _build_branching_script(
        "get_building_cost",
        [":building_no"],
        "cost",
    )


def _build_get_building_prerequisites_ops():
    return _build_branching_script(
        "get_building_prerequisites",
        [":building_no"],
        "prerequisites",
    )


def _build_can_build_improvement_ops():
    return [
        (store_script_param, ":center_no", 1),
        (store_script_param, ":building_no", 2),
        (call_script, "script_validate_construction_choice", ":center_no", ":building_no"),
    ]


def _build_apply_building_effects_ops():
    return _build_branching_script(
        "apply_building_effects",
        [":center_no", ":building_no"],
        "apply_effects",
    )


def _build_get_improvement_details_ops():
    return [
        (store_script_param, ":building_no", 1),
        (call_script, "script_get_building_definition", ":building_no"),
        (str_store_string_reg, s0, s0),
        (str_store_string_reg, s1, s1),
    ]


SCRIPTS = [
    ("get_building_definition", _build_get_building_definition_ops()),
    ("get_building_display_name", _build_get_building_display_name_ops()),
    ("get_building_description", _build_get_building_description_ops()),
    ("get_building_cost", _build_get_building_cost_ops()),
    ("get_building_prerequisites", _build_get_building_prerequisites_ops()),
    ("can_build_improvement", _build_can_build_improvement_ops()),
    ("apply_building_effects", _build_apply_building_effects_ops()),
    ("get_improvement_details", _build_get_improvement_details_ops()),
]
