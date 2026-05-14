# -*- coding: cp1254 -*-

"""Shared menu helpers for building UI.

This module keeps the building option generation logic data-driven so the menu
layer can surface richer design choices such as upgrades, replacements,
specialization, exclusivity, upkeep, and build timing.
"""

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *

from src.constants.building_registry import (
    BUILDING_REGISTRY,
    get_building_build_duration,
    get_building_category_label as registry_get_building_category_label,
    get_building_design_summary as registry_get_building_design_summary,
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

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


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


def _get_building_entry(building_slot):
    return BUILDING_REGISTRY.get(building_slot, {})


def get_building_display_name(building_slot):
    display_name = get_building_display_name_text(building_slot)
    if display_name:
        return display_name
    return building_slot.replace("_", " ").title()


def get_building_description(building_slot):
    entry = _get_building_entry(building_slot)
    return entry.get("description") or registry_get_building_design_summary(building_slot) or ""


def get_building_category_label(building_slot):
    label = registry_get_building_category_label(building_slot)
    if label:
        return label
    return None


def get_building_specialization(building_slot):
    entry = _get_building_entry(building_slot)
    specialization = entry.get("specialization")
    if specialization:
        return specialization
    return None


def get_building_specialization_label(building_slot):
    label = registry_get_building_specialization_label(building_slot)
    if label:
        return label
    return None


def get_building_tier(building_slot):
    tier = registry_get_building_tier(building_slot)
    if isinstance(tier, int) and tier >= 0:
        return tier
    return None


def get_building_upgrade_sources(building_slot):
    return _coerce_tuple(registry_get_building_upgrade_sources(building_slot))


def get_building_upgrade_targets(building_slot):
    return _coerce_tuple(registry_get_building_upgrade_targets(building_slot))


def get_building_exclusive_group(building_slot):
    exclusive_group = registry_get_building_exclusive_group(building_slot)
    if isinstance(exclusive_group, string_types):
        return exclusive_group
    return None


def get_building_weekly_upkeep(building_slot):
    weekly_upkeep = registry_get_building_weekly_upkeep(building_slot)
    if isinstance(weekly_upkeep, int):
        return weekly_upkeep
    return None


def get_building_build_time(building_slot):
    return get_building_build_duration(building_slot)


def get_building_design_summary(building_slot):
    return registry_get_building_design_summary(building_slot)


def get_building_faction_requirements(building_slot):
    return _coerce_tuple(registry_get_building_faction_requirements(building_slot))


def get_building_faction_flavor(building_slot):
    return registry_get_building_faction_flavor(building_slot)


def _format_slot_summary(slot_list):
    slot_list = _coerce_tuple(slot_list)
    if not slot_list:
        return ""
    return ", ".join(get_building_display_name(slot) for slot in slot_list)


def _format_faction_summary(faction_list):
    faction_list = _coerce_tuple(faction_list)
    if not faction_list:
        return ""
    return ", ".join(str(faction) for faction in faction_list)


def _build_label_suffix(entry):
    specialization = entry.get("specialization")
    tier = entry.get("tier")
    pieces = []

    specialization_label = get_building_specialization_label(entry.get("building_slot"))
    if specialization_label:
        pieces.append(specialization_label)
    elif specialization and isinstance(specialization, string_types):
        pieces.append(specialization.replace("_", " ").title())

    if isinstance(tier, int):
        pieces.append("T%s" % tier)

    if not pieces:
        return ""

    return " [%s]" % " ".join(pieces)


def _choose_option_label(building_slot, current_buildings=None):
    entry = _get_building_entry(building_slot)
    current_buildings = _coerce_building_set(current_buildings)

    upgrade_sources = get_building_upgrade_sources(building_slot)
    exclusive_group = get_building_exclusive_group(building_slot)
    label_suffix = _build_label_suffix(entry)

    source_owned = False
    if upgrade_sources and current_buildings:
        for source_slot in upgrade_sources:
            if source_slot in current_buildings:
                source_owned = True
                break

    if source_owned:
        return "Upgrade %s%s" % (get_building_display_name(building_slot), label_suffix)

    if exclusive_group and current_buildings:
        for other_slot in current_buildings:
            if other_slot == building_slot:
                continue
            other_entry = _get_building_entry(other_slot)
            if other_entry.get("exclusive_group") == exclusive_group:
                return "Replace %s with %s%s" % (
                    get_building_display_name(other_slot),
                    get_building_display_name(building_slot),
                    label_suffix,
                )

    return "Build %s%s" % (get_building_display_name(building_slot), label_suffix)


def _build_conditions(building_slot, current_buildings=None, center_type=None, owning_faction=None):
    entry = _get_building_entry(building_slot)
    current_buildings = _coerce_building_set(current_buildings)

    conditions = []

    allowed_center_types = _coerce_tuple(entry.get("allowed_center_types"))
    if center_type is not None and allowed_center_types:
        conditions.append(("allowed_center_types", allowed_center_types, center_type))

    upgrade_sources = get_building_upgrade_sources(building_slot)
    if upgrade_sources:
        conditions.append(("upgrade_sources", upgrade_sources, tuple(sorted(current_buildings))))

    exclusive_group = get_building_exclusive_group(building_slot)
    if exclusive_group:
        conflicting_slots = []
        for other_slot in current_buildings:
            if other_slot == building_slot:
                continue
            other_entry = _get_building_entry(other_slot)
            if other_entry.get("exclusive_group") == exclusive_group:
                conflicting_slots.append(other_slot)
        if conflicting_slots:
            conditions.append(("exclusive_group", exclusive_group, tuple(sorted(conflicting_slots))))

    faction_requirements = get_building_faction_requirements(building_slot)
    if owning_faction is not None and faction_requirements:
        conditions.append(("faction_requirements", faction_requirements, owning_faction))

    return tuple(conditions)


def generate_building_options(*args, **kwargs):
    """Return menu option tuples for the building UI.

    Tuple shape:
        (building_slot, label, conditions, metadata)

    The tuple remains compact so the menu layer can consume it directly while
    still exposing richer metadata for preview/confirmation panels.
    """
    current_buildings = kwargs.pop("current_buildings", None)
    center_type = kwargs.pop("center_type", None)
    owning_faction = kwargs.pop("owning_faction", None)
    available_slots = kwargs.pop("available_slots", None)

    if args:
        if current_buildings is None and len(args) > 0:
            current_buildings = args[0]
        if center_type is None and len(args) > 1:
            center_type = args[1]
        if owning_faction is None and len(args) > 2:
            owning_faction = args[2]
        if available_slots is None and len(args) > 3:
            available_slots = args[3]

    current_buildings = _coerce_building_set(current_buildings)
    available_slots = None if available_slots is None else set(_coerce_tuple(available_slots))

    options = []
    for building_slot in sorted(BUILDING_REGISTRY.keys()):
        if available_slots is not None and building_slot not in available_slots:
            continue

        entry = _get_building_entry(building_slot)
        if center_type is not None:
            allowed_center_types = _coerce_tuple(entry.get("allowed_center_types"))
            if allowed_center_types and center_type not in allowed_center_types:
                continue

        upgrade_sources = get_building_upgrade_sources(building_slot)
        if upgrade_sources:
            has_source = False
            for source_slot in upgrade_sources:
                if source_slot in current_buildings:
                    has_source = True
                    break
            if not has_source:
                continue

        faction_requirements = get_building_faction_requirements(building_slot)
        if owning_faction is not None and faction_requirements and owning_faction not in faction_requirements:
            continue

        label = _choose_option_label(building_slot, current_buildings=current_buildings)
        if label.startswith("Upgrade "):
            menu_variant = "upgrade"
        elif label.startswith("Replace "):
            menu_variant = "replace"
        else:
            menu_variant = "build"

        metadata = {
            "building_slot": building_slot,
            "display_name": get_building_display_name(building_slot),
            "description": get_building_description(building_slot),
            "category_label": get_building_category_label(building_slot),
            "specialization": get_building_specialization(building_slot),
            "specialization_label": get_building_specialization_label(building_slot),
            "tier": get_building_tier(building_slot),
            "build_time": get_building_build_time(building_slot),
            "upgrade_from": get_building_upgrade_sources(building_slot),
            "upgrade_to": get_building_upgrade_targets(building_slot),
            "exclusive_group": get_building_exclusive_group(building_slot),
            "weekly_upkeep": get_building_weekly_upkeep(building_slot),
            "faction_requirements": get_building_faction_requirements(building_slot),
            "faction_flavor": get_building_faction_flavor(building_slot),
            "design_summary": get_building_design_summary(building_slot),
            "menu_variant": menu_variant,
        }

        conditions = _build_conditions(
            building_slot,
            current_buildings=current_buildings,
            center_type=center_type,
            owning_faction=owning_faction,
        )

        options.append((building_slot, label, conditions, metadata))

    return options


def build_upgrade_troop_selection_option(troop_no):
    return (
        "troop%d" % troop_no,
        [
            (assign, ":upgrade_center", "$g_sod_upgrade_center"),
            (party_count_companions_of_type, ":troop_count", "p_main_party", troop_no),
            (gt, ":troop_count", 0),
            (assign, ":can_up1", 0),
            (assign, ":can_up2", 0),
            (troop_get_slot, ":upgrade1", troop_no, slot_troop_sod_upgrade1),
            (try_begin),
                (is_between, ":upgrade1", 0, "trp_last_troop"),
                (call_script, "script_sod_can_upgrade_troops_here", ":upgrade1", ":upgrade_center"),
                (assign, ":can_up1", reg0),
            (try_end),
            (troop_get_slot, ":upgrade2", troop_no, slot_troop_sod_upgrade2),
            (try_begin),
                (is_between, ":upgrade2", 0, "trp_last_troop"),
                (call_script, "script_sod_can_upgrade_troops_here", ":upgrade2", ":upgrade_center"),
                (assign, ":can_up2", reg0),
            (try_end),
            (this_or_next | eq, ":can_up1", 1),
            (eq, ":can_up2", 1),
            (str_store_troop_name_by_count, s3, troop_no, ":troop_count"),
        ],
        "Upgrade {s3}.",
        [
            (assign, "$g_sod_town_upgrade_selected_troop", troop_no),
            (jump_to_menu, "mnu_sod_upgrade_continue"),
        ],
    )


def generate_upgrade_options():
    result = [build_upgrade_troop_selection_option(troop_no) for troop_no in range(0, trp_last_troop)]
    result.append(("return", [], "Nevermind.", [(jump_to_menu, "$jump_menu")]))
    return result


def build_sod_battle_commander_change_option(option_id, return_menu, extra_conditions=None):
    conditions = list(extra_conditions or [])
    conditions.extend([
        (call_script, "script_cf_sod_battle_commander_party_has_available_commander"),
        (call_script, "script_sod_battle_commander_store_current_name_to_s7"),
    ])
    return (
        option_id,
        conditions,
        "Choose acting commander ({s7}).",
        [
            (assign, "$g_sod_battle_commander_return_menu", return_menu),
            (jump_to_menu, "mnu_sod_battle_commander_select"),
        ],
    )


def build_sod_battle_commander_select_option(troop_no):
    return (
        "sod_battle_commander_%s" % troop_no,
        [
            (call_script, "script_cf_sod_battle_commander_troop_available", troop_no),
            (str_store_troop_name, s3, troop_no),
        ],
        "Let {s3} lead.",
        [
            (call_script, "script_sod_battle_commander_select", troop_no),
            (jump_to_menu, "mnu_sod_battle_commander_select"),
        ],
    )


def generate_sod_battle_commander_select_options():
    result = [
        (
            "sod_battle_commander_player",
            [(call_script, "script_cf_sod_battle_commander_troop_available", "trp_player")],
            "Lead personally.",
            [
                (call_script, "script_sod_battle_commander_select", "trp_player"),
                (jump_to_menu, "mnu_sod_battle_commander_select"),
            ],
        )
    ]
    result.extend(
        build_sod_battle_commander_select_option("trp_npc%d" % npc_no)
        for npc_no in range(1, 17)
    )
    result.append(
        (
            "sod_battle_commander_done",
            [],
            "Done.",
            [(jump_to_menu, "$g_sod_battle_commander_return_menu")],
        )
    )
    return result


__all__ = [
    "BUILDING_REGISTRY",
    "build_sod_battle_commander_change_option",
    "generate_sod_battle_commander_select_options",
    "game_menus",
    "generate_building_options",
    "get_building_build_time",
    "get_building_category_label",
    "get_building_description",
    "get_building_design_summary",
    "get_building_display_name",
    "get_building_exclusive_group",
    "get_building_faction_flavor",
    "get_building_faction_requirements",
    "get_building_specialization",
    "get_building_specialization_label",
    "get_building_tier",
    "get_building_upgrade_sources",
    "get_building_upgrade_targets",
    "get_building_weekly_upkeep",
]
