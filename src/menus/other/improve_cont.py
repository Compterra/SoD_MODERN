# -*- coding: cp1254 -*-

"""Confirmation panel for building improvements.

The menu layer can use the returned payload to render richer building details
before the player commits to construction.
"""

from src.constants.building_registry import (
    BUILDING_REGISTRY,
    get_building_build_duration,
    get_building_category_label as registry_get_building_category_label,
    get_building_display_name_text,
    get_building_exclusive_group as registry_get_building_exclusive_group,
    get_building_faction_flavor as registry_get_building_faction_flavor,
    get_building_faction_requirements as registry_get_building_faction_requirements,
    get_building_specialization_label as registry_get_building_specialization_label,
    get_building_tier as registry_get_building_tier,
    get_building_upgrade_sources as registry_get_building_upgrade_sources,
    get_building_upgrade_targets as registry_get_building_upgrade_targets,
    get_building_weekly_upkeep as registry_get_building_weekly_upkeep,
)
from src.scripts.ZI_campaign_ai.validate_construction_choice import (
    BUILDING_VALIDATION_ALREADY_BUILT,
    BUILDING_VALIDATION_CONFLICT,
    BUILDING_VALIDATION_FACTION_LOCK,
    BUILDING_VALIDATION_MISSING_PREREQUISITE,
    BUILDING_VALIDATION_OK,
    BUILDING_VALIDATION_UNKNOWN,
    BUILDING_VALIDATION_UPGRADE_AVAILABLE,
    BUILDING_VALIDATION_WRONG_CENTER,
    describe_validation_result,
)

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)

try:
    integer_types = (int, long)
except NameError:
    integer_types = (int,)


def _is_integer(value):
    return isinstance(value, integer_types)


def _is_string(value):
    return isinstance(value, string_types)


def _coerce_tuple(value):
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    return (value,)


def _coerce_building_set(current_buildings):
    if current_buildings is None:
        return set()
    if isinstance(current_buildings, set):
        return set(current_buildings)
    return set(_coerce_tuple(current_buildings))


def _get_entry(building_slot):
    return BUILDING_REGISTRY.get(building_slot, {})


def _get_display_name(building_slot):
    display_name = get_building_display_name_text(building_slot)
    if display_name:
        return display_name
    return building_slot.replace("_", " ").title()


def _get_description(building_slot):
    entry = _get_entry(building_slot)
    return entry.get("description") or entry.get("design_summary") or ""


def _get_category_label(building_slot):
    label = registry_get_building_category_label(building_slot)
    if label:
        return label
    return None


def _get_specialization_label(building_slot):
    label = registry_get_building_specialization_label(building_slot)
    if label:
        return label
    return None


def _format_slot_summary(slot_list):
    slot_list = _coerce_tuple(slot_list)
    if not slot_list:
        return ""
    names = []
    for slot in slot_list:
        names.append(_get_display_name(slot))
    return ", ".join(names)


def _format_faction_summary(faction_list):
    faction_list = _coerce_tuple(faction_list)
    if not faction_list:
        return ""
    return ", ".join(str(faction) for faction in faction_list)


def _format_validation_summary(validation_reason, validation_blocking_slot=None):
    if _is_integer(validation_reason):
        return describe_validation_result(validation_reason, validation_blocking_slot)
    if validation_reason in (None, ""):
        return ""
    return str(validation_reason)


def _validation_is_allowed(validation_reason):
    if not _is_integer(validation_reason):
        return None
    return validation_reason in (BUILDING_VALIDATION_OK, BUILDING_VALIDATION_UPGRADE_AVAILABLE)


def _center_type_matches_allowed(center_type, allowed_center_types):
    allowed_center_types = tuple(allowed_center_types or ())
    if not allowed_center_types or len(allowed_center_types) == 3:
        return True
    if center_type in CENTER_TYPE_CONSTANTS.values():
        allowed_center_values = [CENTER_TYPE_CONSTANTS.get(center_name) for center_name in allowed_center_types]
        return center_type in allowed_center_values
    if _is_string(center_type):
        return center_type in allowed_center_types
    return False


def _collect_conflict_slots(definition):
    conflict_slots = []
    seen_slots = set()

    for slot_name in tuple(definition.get("conflicts_with", ())):
        if slot_name not in seen_slots:
            seen_slots.add(slot_name)
            conflict_slots.append(slot_name)

    exclusive_group = definition.get("exclusive_group")
    if exclusive_group:
        for other_definition in BUILDING_REGISTRY:
            if other_definition is definition:
                continue
            if other_definition.get("exclusive_group") != exclusive_group:
                continue
            other_slot = other_definition.get("building_slot")
            if other_slot and other_slot not in seen_slots:
                seen_slots.add(other_slot)
                conflict_slots.append(other_slot)

    return conflict_slots


def _validate_building_choice(building_slot, current_buildings=None, center_type=None, owning_faction=None):
    entry = _get_entry(building_slot)
    current_buildings = _coerce_building_set(current_buildings)

    if not building_slot or not entry:
        return BUILDING_VALIDATION_UNKNOWN, 0

    allowed_center_types = tuple(entry.get("allowed_center_types", ()))
    if center_type is not None and not _center_type_matches_allowed(center_type, allowed_center_types):
        return BUILDING_VALIDATION_WRONG_CENTER, 0

    if building_slot in current_buildings:
        return BUILDING_VALIDATION_ALREADY_BUILT, building_slot

    if owning_faction is not None:
        faction_requirements = _coerce_tuple(entry.get("faction_requirements"))
        if faction_requirements and owning_faction not in faction_requirements:
            return BUILDING_VALIDATION_FACTION_LOCK, 0

    upgrade_sources = _coerce_tuple(entry.get("upgrade_from"))
    upgrade_source_slot = 0
    for source_slot in upgrade_sources:
        if source_slot in current_buildings:
            upgrade_source_slot = source_slot
            break

    prerequisite_buildings = _coerce_tuple(entry.get("prerequisite_buildings"))
    for prereq_slot in prerequisite_buildings:
        if prereq_slot not in current_buildings:
            return BUILDING_VALIDATION_MISSING_PREREQUISITE, prereq_slot

    for conflict_slot in _collect_conflict_slots(entry):
        if conflict_slot in current_buildings and conflict_slot != upgrade_source_slot:
            return BUILDING_VALIDATION_CONFLICT, conflict_slot

    if upgrade_source_slot:
        return BUILDING_VALIDATION_UPGRADE_AVAILABLE, upgrade_source_slot

    return BUILDING_VALIDATION_OK, 0


def validate_center_improve_choice(building_slot, current_buildings=None, center_type=None, owning_faction=None):
    validation_code, validation_blocking_slot = _validate_building_choice(
        building_slot,
        current_buildings=current_buildings,
        center_type=center_type,
        owning_faction=owning_faction,
    )
    validation_summary = _format_validation_summary(validation_code, validation_blocking_slot)
    validation_blocking_name = _get_display_name(validation_blocking_slot) if validation_blocking_slot else ""
    return {
        "validation_code": validation_code,
        "validation_summary": validation_summary,
        "validation_blocking_slot": validation_blocking_slot,
        "validation_blocking_name": validation_blocking_name,
        "validation_is_allowed": _validation_is_allowed(validation_code),
    }


def _build_detail_lines(
    building_slot,
    current_buildings=None,
    center_type=None,
    owning_faction=None,
    cost=None,
    build_time=None,
):
    entry = _get_entry(building_slot)
    current_buildings = _coerce_building_set(current_buildings)

    lines = []
    display_name = _get_display_name(building_slot)
    description = _get_description(building_slot)

    lines.append(display_name)

    category_label = _get_category_label(building_slot)
    if category_label:
        lines.append("Category: %s" % category_label)

    specialization_label = _get_specialization_label(building_slot)
    tier = registry_get_building_tier(building_slot)
    upgrade_from = registry_get_building_upgrade_sources(building_slot)
    upgrade_to = registry_get_building_upgrade_targets(building_slot)
    exclusive_group = registry_get_building_exclusive_group(building_slot)
    weekly_upkeep = registry_get_building_weekly_upkeep(building_slot)
    faction_requirements = registry_get_building_faction_requirements(building_slot)
    faction_flavor = registry_get_building_faction_flavor(building_slot)
    design_summary = entry.get("design_summary") or ""

    if specialization_label:
        lines.append("Specialization: %s" % specialization_label)

    if isinstance(tier, int):
        lines.append("Tier: %s" % tier)

    if upgrade_from:
        lines.append("Upgrades from: %s" % _format_slot_summary(upgrade_from))

    if upgrade_to:
        lines.append("Can upgrade into: %s" % _format_slot_summary(upgrade_to))

    if exclusive_group:
        lines.append("Exclusive group: %s" % exclusive_group)

    if weekly_upkeep is not None and isinstance(weekly_upkeep, int) and weekly_upkeep > 0:
        lines.append("Weekly upkeep: -%s denars" % weekly_upkeep)

    if faction_requirements:
        lines.append("Faction requirement: %s" % _format_faction_summary(faction_requirements))

    if faction_flavor:
        lines.append(faction_flavor)

    if design_summary and design_summary != description:
        lines.append(design_summary)

    if description:
        lines.append(description)

    if cost is not None:
        lines.append("Cost: %s denars" % cost)

    if build_time is None:
        build_time = get_building_build_duration(building_slot)
    if build_time is not None:
        lines.append("Build time: %s days" % build_time)

    if current_buildings and upgrade_from:
        owned_sources = []
        for source_slot in upgrade_from:
            if source_slot in current_buildings:
                owned_sources.append(_get_display_name(source_slot))
        if owned_sources:
            lines.append("Upgrade source present: %s" % ", ".join(owned_sources))

    if current_buildings and exclusive_group:
        conflicts = []
        for other_slot in current_buildings:
            if other_slot == building_slot:
                continue
            other_entry = _get_entry(other_slot)
            if other_entry.get("exclusive_group") == exclusive_group:
                conflicts.append(_get_display_name(other_slot))
        if conflicts:
            lines.append("Conflicts with: %s" % ", ".join(conflicts))

    if owning_faction is not None and faction_requirements:
        lines.append("Owned by: %s" % str(owning_faction))

    return lines


def build_center_improve_payload(*args, **kwargs):
    building_slot = kwargs.pop("building_slot", None)
    current_buildings = kwargs.pop("current_buildings", None)
    center_type = kwargs.pop("center_type", None)
    owning_faction = kwargs.pop("owning_faction", None)
    cost = kwargs.pop("cost", None)
    build_time = kwargs.pop("build_time", None)
    validation_reason = kwargs.pop("validation_reason", None)
    validation_blocking_slot = kwargs.pop("validation_blocking_slot", None)
    validation_summary = kwargs.pop("validation_summary", None)
    validation_is_allowed = kwargs.pop("validation_is_allowed", None)
    validation_code = kwargs.pop("validation_code", None)
    validation_blocking_name = kwargs.pop("validation_blocking_name", None)

    if args:
        if building_slot is None and len(args) > 0:
            building_slot = args[0]
        if current_buildings is None and len(args) > 1:
            current_buildings = args[1]
        if center_type is None and len(args) > 2:
            center_type = args[2]
        if owning_faction is None and len(args) > 3:
            owning_faction = args[3]
        if cost is None and len(args) > 4:
            cost = args[4]
        if build_time is None and len(args) > 5:
            build_time = args[5]
        if validation_reason is None and len(args) > 6:
            validation_reason = args[6]
        if validation_blocking_slot is None and len(args) > 7:
            validation_blocking_slot = args[7]

    entry = _get_entry(building_slot)
    current_buildings_set = _coerce_building_set(current_buildings)
    detail_lines = _build_detail_lines(
        building_slot,
        current_buildings=current_buildings_set,
        center_type=center_type,
        owning_faction=owning_faction,
        cost=cost,
        build_time=build_time,
    )

    upgrade_from = registry_get_building_upgrade_sources(building_slot)
    upgrade_to = registry_get_building_upgrade_targets(building_slot)
    exclusive_group = registry_get_building_exclusive_group(building_slot)
    weekly_upkeep = registry_get_building_weekly_upkeep(building_slot)
    faction_requirements = registry_get_building_faction_requirements(building_slot)

    if validation_code is None and validation_summary is None and validation_reason in (None, ""):
        validation_code, validation_blocking_slot = _validate_building_choice(
            building_slot,
            current_buildings=current_buildings_set,
            center_type=center_type,
            owning_faction=owning_faction,
        )
        validation_summary = _format_validation_summary(validation_code, validation_blocking_slot)
        validation_blocking_name = _get_display_name(validation_blocking_slot) if validation_blocking_slot else ""
        validation_is_allowed = _validation_is_allowed(validation_code)

    if validation_code is None and _is_integer(validation_reason):
        validation_code = validation_reason

    if validation_summary is None:
        if validation_code is not None:
            validation_summary = _format_validation_summary(validation_code, validation_blocking_slot)
        elif validation_reason not in (None, ""):
            validation_summary = str(validation_reason)

    if validation_is_allowed is None and validation_code is not None:
        validation_is_allowed = _validation_is_allowed(validation_code)

    if validation_blocking_name is None and validation_blocking_slot:
        validation_blocking_name = _get_display_name(validation_blocking_slot)

    menu_variant = "build"
    if upgrade_from:
        for source_slot in upgrade_from:
            if source_slot in current_buildings_set:
                menu_variant = "upgrade"
                break
    if menu_variant == "build" and exclusive_group:
        for other_slot in current_buildings_set:
            if other_slot == building_slot:
                continue
            other_entry = _get_entry(other_slot)
            if other_entry.get("exclusive_group") == exclusive_group:
                menu_variant = "replace"
                break

    status_lines = []
    if validation_summary:
        status_lines.append("Validation: %s" % validation_summary)
    if validation_is_allowed is False:
        status_lines.append("This improvement is not currently available.")

    warnings = []
    if upgrade_from:
        warnings.append("This improvement is part of an upgrade chain.")
    if exclusive_group:
        warnings.append("This improvement belongs to an exclusive group.")
    if weekly_upkeep is not None and isinstance(weekly_upkeep, int) and weekly_upkeep > 0:
        warnings.append("This improvement has ongoing weekly upkeep.")
    if faction_requirements:
        warnings.append("This improvement may be restricted by faction ownership.")

    if build_time is None:
        build_time = get_building_build_duration(building_slot)

    confirmation_text = "\n".join(detail_lines + status_lines + warnings)

    return {
        "menu_id": "center_improve",
        "menu_title": "Improve the center",
        "validation_script": "validate_construction_choice",
        "menu_variant": menu_variant,
        "building_slot": building_slot,
        "display_name": _get_display_name(building_slot),
        "description": _get_description(building_slot),
        "detail_lines": tuple(detail_lines),
        "warning_lines": tuple(warnings),
        "confirmation_text": confirmation_text,
        "category_label": _get_category_label(building_slot),
        "specialization": entry.get("specialization"),
        "specialization_label": _get_specialization_label(building_slot),
        "tier": registry_get_building_tier(building_slot),
        "build_duration": build_time,
        "upgrade_from": upgrade_from,
        "upgrade_to": upgrade_to,
        "upgrade_source_summary": _format_slot_summary(upgrade_from),
        "upgrade_target_summary": _format_slot_summary(upgrade_to),
        "exclusive_group": exclusive_group,
        "exclusive_group_summary": exclusive_group or "",
        "weekly_upkeep": weekly_upkeep if isinstance(weekly_upkeep, int) else None,
        "weekly_upkeep_summary": ("Weekly upkeep: -%s denars" % weekly_upkeep) if isinstance(weekly_upkeep, int) and weekly_upkeep > 0 else "",
        "faction_requirements": faction_requirements,
        "faction_requirement_summary": _format_faction_summary(faction_requirements),
        "faction_flavor": registry_get_building_faction_flavor(building_slot),
        "design_summary": entry.get("design_summary") or "",
        "current_buildings": tuple(current_buildings_set),
        "center_type": center_type,
        "owning_faction": owning_faction,
        "cost": cost,
        "build_time": build_time,
        "validation_reason": validation_reason,
        "validation_code": validation_code,
        "validation_summary": validation_summary or "",
        "validation_is_allowed": validation_is_allowed,
        "validation_blocking_slot": validation_blocking_slot,
        "validation_blocking_name": validation_blocking_name or "",
        "can_build": validation_is_allowed,
    }


def center_improve(*args, **kwargs):
    """Compatibility wrapper for the confirmation menu payload."""
    return build_center_improve_payload(*args, **kwargs)


center_improve_menu = center_improve

MENUS = [
    (
        "center_improve",
        0,
        "Improve the center",
        "none",
        [],
        [
            ("continue", [], "Continue...", [(jump_to_menu, "mnu_fief_reports")]),
        ],
    ),
]

__all__ = [
    "build_center_improve_payload",
    "center_improve",
    "center_improve_menu",
    "validate_center_improve_choice",
]
