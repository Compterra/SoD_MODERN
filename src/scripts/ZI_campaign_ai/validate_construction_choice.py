# -*- coding: cp1254 -*-

from src.constants.module_constants import *
from src.constants.building_registry import BUILDING_REGISTRY, get_building_display_name_text


BUILDING_VALIDATION_OK = 0
BUILDING_VALIDATION_UNKNOWN = 1
BUILDING_VALIDATION_WRONG_CENTER = 2
BUILDING_VALIDATION_ALREADY_BUILT = 3
BUILDING_VALIDATION_MISSING_PREREQUISITE = 4
BUILDING_VALIDATION_CONFLICT = 5
BUILDING_VALIDATION_UPGRADE_AVAILABLE = 6
BUILDING_VALIDATION_FACTION_LOCK = 7
BUILDING_VALIDATION_SPECIALIZATION_MISMATCH = 8

# Backward-compatible aliases for older callers and reports.
BUILDING_CAN_BUILD_OK = BUILDING_VALIDATION_OK
BUILDING_CAN_BUILD_UNKNOWN = BUILDING_VALIDATION_UNKNOWN
BUILDING_CAN_BUILD_WRONG_CENTER = BUILDING_VALIDATION_WRONG_CENTER
BUILDING_CAN_BUILD_ALREADY_BUILT = BUILDING_VALIDATION_ALREADY_BUILT
BUILDING_CAN_BUILD_MISSING_PREREQUISITE = BUILDING_VALIDATION_MISSING_PREREQUISITE
BUILDING_CAN_BUILD_CONFLICT = BUILDING_VALIDATION_CONFLICT
BUILDING_CAN_BUILD_UPGRADE_AVAILABLE = BUILDING_VALIDATION_UPGRADE_AVAILABLE
BUILDING_CAN_BUILD_FACTION_LOCK = BUILDING_VALIDATION_FACTION_LOCK
BUILDING_CAN_BUILD_SPECIALIZATION_MISMATCH = BUILDING_VALIDATION_SPECIALIZATION_MISMATCH

BUILDING_VALIDATION_REQUIRES_UPGRADE = BUILDING_VALIDATION_UPGRADE_AVAILABLE
BUILDING_VALIDATION_FACTION_REQUIREMENT = BUILDING_VALIDATION_FACTION_LOCK

CENTER_TYPE_CONSTANTS = {
    "village": spt_village,
    "town": spt_town,
    "castle": spt_castle,
}

BUILDING_VALIDATION_LABELS = {
    BUILDING_VALIDATION_OK: "Available",
    BUILDING_VALIDATION_UNKNOWN: "Unknown improvement",
    BUILDING_VALIDATION_WRONG_CENTER: "Wrong center type",
    BUILDING_VALIDATION_ALREADY_BUILT: "Already built",
    BUILDING_VALIDATION_MISSING_PREREQUISITE: "Missing prerequisite",
    BUILDING_VALIDATION_CONFLICT: "Conflicts with existing improvement",
    BUILDING_VALIDATION_UPGRADE_AVAILABLE: "Upgrade available",
    BUILDING_VALIDATION_FACTION_LOCK: "Faction locked",
    BUILDING_VALIDATION_SPECIALIZATION_MISMATCH: "Specialization mismatch",
}


def describe_validation_result(validation_code, blocking_slot=None):
    label = BUILDING_VALIDATION_LABELS.get(validation_code, "Unknown validation result")
    if not blocking_slot:
        return label

    blocking_name = get_building_display_name_text(blocking_slot) or str(blocking_slot)

    if validation_code == BUILDING_VALIDATION_MISSING_PREREQUISITE:
        return "%s: requires %s" % (label, blocking_name)
    if validation_code == BUILDING_VALIDATION_CONFLICT:
        return "%s: conflicts with %s" % (label, blocking_name)
    if validation_code == BUILDING_VALIDATION_ALREADY_BUILT:
        return "%s: already built (%s)" % (label, blocking_name)
    if validation_code == BUILDING_VALIDATION_UPGRADE_AVAILABLE:
        return "%s: upgrade available from %s" % (label, blocking_name)
    if validation_code == BUILDING_VALIDATION_FACTION_LOCK:
        return "%s: requires %s" % (label, blocking_name)
    if validation_code == BUILDING_VALIDATION_SPECIALIZATION_MISMATCH:
        return "%s: specialization mismatch (%s)" % (label, blocking_name)
    return "%s: %s" % (label, blocking_name)


def _center_type_guard_ops(definition):
    allowed_center_types = tuple(definition.get("allowed_center_types", ()))
    if len(allowed_center_types) == 3:
        return [(assign, ":center_type_ok", 1)]

    ops = [
        (assign, ":center_type_ok", 0),
        (try_begin,),
    ]

    for index, center_type in enumerate(allowed_center_types):
        if index > 0:
            ops.append((else_try,))
        ops.append((eq, ":center_type", CENTER_TYPE_CONSTANTS[center_type]))
        ops.append((assign, ":center_type_ok", 1))

    ops.append((try_end,))
    return ops


def _upgrade_source_guard_ops(definition):
    upgrade_sources = tuple(definition.get("upgrade_from", ()))
    ops = [
        (assign, ":upgrade_source_found", 0),
        (assign, ":upgrade_source_slot", 0),
    ]
    if not upgrade_sources:
        return ops

    ops.append((try_begin,))
    for index, source_slot in enumerate(upgrade_sources):
        if index > 0:
            ops.append((else_try,))
        ops.extend([
            (eq, ":validation_ok", 1),
            (eq, ":upgrade_source_found", 0),
            (party_slot_ge, ":center_no", source_slot, 1),
            (assign, ":upgrade_source_found", 1),
            (assign, ":upgrade_source_slot", source_slot),
        ])
    ops.append((try_end,))
    return ops


def _faction_requirement_guard_ops(definition):
    faction_requirements = tuple(definition.get("faction_requirements", ()))
    if not faction_requirements:
        return []

    ops = [
        (assign, ":faction_ok", 0),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (try_begin,),
    ]

    for index, faction_no in enumerate(faction_requirements):
        if index > 0:
            ops.append((else_try,))
        ops.extend([
            (eq, ":center_faction", faction_no),
            (assign, ":faction_ok", 1),
        ])

    ops.extend([
        (try_end,),
        (try_begin,),
        (eq, ":validation_ok", 1),
        (eq, ":faction_ok", 0),
        (assign, ":validation_ok", 0),
        (assign, reg0, 0),
        (assign, reg1, BUILDING_VALIDATION_FACTION_LOCK),
        (assign, reg2, 0),
        (try_end,),
    ])
    return ops


def _prerequisite_guard_ops(definition):
    prerequisite_buildings = tuple(definition.get("prerequisite_buildings", ()))
    prerequisite_any_buildings = tuple(definition.get("prerequisite_any_buildings", ()))
    if not prerequisite_buildings and not prerequisite_any_buildings:
        return []

    ops = []
    for prereq_slot in prerequisite_buildings:
        ops.extend([
            (try_begin,),
            (eq, ":validation_ok", 1),
            (eq, ":prereq_ok", 1),
            (party_slot_ge, ":center_no", prereq_slot, 1),
            (else_try,),
            (eq, ":validation_ok", 1),
            (eq, ":prereq_ok", 1),
            (assign, ":prereq_ok", 0),
            (assign, ":validation_ok", 0),
            (assign, reg0, 0),
            (assign, reg1, BUILDING_VALIDATION_MISSING_PREREQUISITE),
            (assign, reg2, prereq_slot),
            (try_end,),
        ])
    if prerequisite_any_buildings:
        ops.extend([
            (assign, ":any_prereq_ok", 0),
            (try_begin,),
        ])
        for index, prereq_slot in enumerate(prerequisite_any_buildings):
            if index > 0:
                ops.append((else_try,))
            ops.extend([
                (party_slot_ge, ":center_no", prereq_slot, 1),
                (assign, ":any_prereq_ok", 1),
            ])
        ops.extend([
            (try_end,),
            (try_begin,),
            (eq, ":validation_ok", 1),
            (eq, ":prereq_ok", 1),
            (eq, ":any_prereq_ok", 0),
            (assign, ":prereq_ok", 0),
            (assign, ":validation_ok", 0),
            (assign, reg0, 0),
            (assign, reg1, BUILDING_VALIDATION_MISSING_PREREQUISITE),
            (assign, reg2, prerequisite_any_buildings[0]),
            (try_end,),
        ])
    return ops


def _exclusive_group_conflict_slots(definition):
    conflict_slots = []
    seen = set()

    for slot_name in tuple(definition.get("conflicts_with", ())):
        if slot_name not in seen:
            seen.add(slot_name)
            conflict_slots.append(slot_name)

    exclusive_group = definition.get("exclusive_group")
    if exclusive_group:
        for other_definition in BUILDING_REGISTRY:
            if other_definition is definition:
                continue
            if other_definition.get("exclusive_group") != exclusive_group:
                continue
            other_slot = other_definition.get("building_slot")
            if other_slot and other_slot not in seen:
                seen.add(other_slot)
                conflict_slots.append(other_slot)

    return conflict_slots


def _conflict_guard_ops(definition):
    conflict_slots = _exclusive_group_conflict_slots(definition)
    if not conflict_slots:
        return []

    ops = [
        (assign, ":conflict_ok", 1),
        (assign, ":blocked_slot", 0),
    ]

    for conflict_slot in conflict_slots:
        ops.extend([
            (try_begin,),
            (eq, ":validation_ok", 1),
            (eq, ":conflict_ok", 1),
            (party_slot_ge, ":center_no", conflict_slot, 1),
            (assign, ":ignore_conflict", 0),
            (try_begin,),
            (eq, ":upgrade_source_found", 1),
            (eq, ":upgrade_source_slot", conflict_slot),
            (assign, ":ignore_conflict", 1),
            (try_end,),
            (try_begin,),
            (eq, ":ignore_conflict", 0),
            (assign, ":conflict_ok", 0),
            (assign, ":validation_ok", 0),
            (assign, reg0, 0),
            (assign, reg1, BUILDING_VALIDATION_CONFLICT),
            (assign, reg2, conflict_slot),
            (assign, ":blocked_slot", conflict_slot),
            (try_end,),
            (try_end,),
        ])

    return ops


def _success_ops():
    return [
        (try_begin,),
        (eq, ":validation_ok", 1),
        (eq, ":upgrade_source_found", 1),
        (assign, reg0, 1),
        (assign, reg1, BUILDING_VALIDATION_UPGRADE_AVAILABLE),
        (assign, reg2, ":upgrade_source_slot"),
        (else_try,),
        (eq, ":validation_ok", 1),
        (assign, reg0, 1),
        (assign, reg1, BUILDING_VALIDATION_OK),
        (assign, reg2, 0),
        (try_end,),
    ]


def _validation_ops_for_definition(definition):
    ops = [
        (assign, reg0, 0),
        (assign, reg1, BUILDING_VALIDATION_UNKNOWN),
        (assign, reg2, 0),
        (assign, ":validation_ok", 1),
        (assign, ":prereq_ok", 1),
        (assign, ":center_type_ok", 0),
        (assign, ":upgrade_source_found", 0),
        (assign, ":upgrade_source_slot", 0),
        (assign, ":faction_ok", 1),
        (assign, ":conflict_ok", 1),
        (assign, ":any_prereq_ok", 0),
        (assign, ":blocked_slot", 0),
        (assign, ":ignore_conflict", 0),
        (eq, ":any_prereq_ok", ":any_prereq_ok"),
        (eq, ":faction_ok", ":faction_ok"),
        (eq, ":blocked_slot", ":blocked_slot"),
        (party_get_slot, ":center_type", ":center_no", slot_party_type),
    ]
    ops.extend(_center_type_guard_ops(definition))
    ops.extend([
        (try_begin,),
        (eq, ":validation_ok", 1),
        (eq, ":center_type_ok", 0),
        (assign, ":validation_ok", 0),
        (assign, reg0, 0),
        (assign, reg1, BUILDING_VALIDATION_WRONG_CENTER),
        (assign, reg2, 0),
        (try_end,),
        (try_begin,),
        (eq, ":validation_ok", 1),
        (party_slot_ge, ":center_no", definition["building_slot"], 1),
        (assign, ":validation_ok", 0),
        (assign, reg0, 0),
        (assign, reg1, BUILDING_VALIDATION_ALREADY_BUILT),
        (assign, reg2, definition["building_slot"]),
        (try_end,),
    ])
    ops.extend(_upgrade_source_guard_ops(definition))
    ops.extend(_faction_requirement_guard_ops(definition))
    ops.extend(_prerequisite_guard_ops(definition))
    ops.extend(_conflict_guard_ops(definition))
    ops.extend(_success_ops())
    return ops


def _build_validate_construction_choice_ops():
    ops = [
        (store_script_param, ":center_no", 1),
        (store_script_param, ":building_no", 2),
        (assign, reg0, 0),
        (assign, reg1, BUILDING_VALIDATION_UNKNOWN),
        (assign, reg2, 0),
    ]

    for index, definition in enumerate(BUILDING_REGISTRY):
        if index == 0:
            ops.append((try_begin,))
        else:
            ops.append((else_try,))
        ops.append((eq, ":building_no", definition["building_slot"]))
        ops.extend(_validation_ops_for_definition(definition))

    ops.extend([
        (else_try,),
        (assign, reg0, 0),
        (assign, reg1, BUILDING_VALIDATION_UNKNOWN),
        (assign, reg2, 0),
        (try_end,),
    ])
    return ops


SCRIPTS = [
    ("validate_construction_choice", _build_validate_construction_choice_ops()),
]
