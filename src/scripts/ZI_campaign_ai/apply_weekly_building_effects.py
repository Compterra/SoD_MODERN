# -*- coding: cp1254 -*-

"""Weekly building effect helpers.

This module keeps building effects data-driven and applies weekly upkeep in the
same pass so the player sees the full tradeoff of each improvement.
"""

from src.constants.building_registry import (
    BUILDING_REGISTRY,
    get_building_category_label as registry_get_building_category_label,
    get_building_design_summary as registry_get_building_design_summary,
    get_building_display_name_text,
    get_building_specialization_label as registry_get_building_specialization_label,
    get_building_tier as registry_get_building_tier,
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


def _get_entry(building_slot):
    return BUILDING_REGISTRY.get(building_slot, {})


def _get_buildings_for_center(center_state):
    if center_state is None:
        return ()
    if isinstance(center_state, dict):
        for key in ("buildings", "building_slots", "improvements", "improvement_slots"):
            if key in center_state:
                return _coerce_tuple(center_state.get(key))
        return ()
    return _coerce_tuple(center_state)


def _get_center_owner_key(center_state):
    if not isinstance(center_state, dict):
        return None
    for key in ("owner", "owner_key", "owning_faction", "owner_troop", "lord", "player"):
        owner_value = center_state.get(key)
        if owner_value is not None:
            return owner_value
    return None


def _format_category_label(building_slot):
    label = registry_get_building_category_label(building_slot)
    if label:
        return label
    return ""


def _format_specialization_label(building_slot):
    label = registry_get_building_specialization_label(building_slot)
    if label:
        return label
    return ""


def _is_player_owner(owner_key):
    if owner_key is None:
        return False
    if isinstance(owner_key, string_types):
        return owner_key in ("trp_player", "player")
    return False


def _apply_upkeep_delta(wealth_state, owner_key, upkeep):
    if upkeep <= 0 or owner_key is None:
        return 0

    if isinstance(wealth_state, dict):
        if owner_key not in wealth_state:
            wealth_state[owner_key] = 0
        wealth_state[owner_key] = int(wealth_state[owner_key]) - int(upkeep)
        return int(upkeep)

    if isinstance(owner_key, dict):
        for key in ("wealth", "gold", "money"):
            if key in owner_key:
                owner_key[key] = int(owner_key.get(key, 0)) - int(upkeep)
                return int(upkeep)

    return int(upkeep)


def _summarize_effects_for_building(building_slot):
    entry = _get_entry(building_slot)
    effect_tags = _coerce_tuple(entry.get("effect_tags"))
    effect_numbers = _coerce_tuple(entry.get("effect_numbers"))
    summary = []

    if effect_tags or effect_numbers:
        summary.append({
            "building_slot": building_slot,
            "display_name": get_building_display_name_text(building_slot),
            "category_label": _format_category_label(building_slot),
            "specialization_label": _format_specialization_label(building_slot),
            "tier": registry_get_building_tier(building_slot),
            "weekly_upkeep": registry_get_building_weekly_upkeep(building_slot),
            "design_summary": registry_get_building_design_summary(building_slot),
            "effect_tags": effect_tags,
            "effect_numbers": effect_numbers,
        })

    return summary


def calculate_weekly_building_effects(*args, **kwargs):
    """Calculate and apply upkeep for a set of centers.

    The function is intentionally generic so the caller can pass either a list of
    center dictionaries or a single center state. It returns a summary payload
    describing the upkeep that was applied and any metadata-based effect summary
    that downstream menu/report code can display.
    """
    centers = kwargs.pop("centers", None)
    wealth_state = kwargs.pop("wealth_state", None)

    if args:
        if centers is None and len(args) > 0:
            centers = args[0]
        if wealth_state is None and len(args) > 1:
            wealth_state = args[1]

    if centers is None:
        centers = []
    elif isinstance(centers, dict):
        centers = [centers]
    else:
        centers = list(centers)

    if wealth_state is None:
        wealth_state = {}

    result = {
        "upkeep_total": 0,
        "centers": [],
        "effect_summaries": [],
    }

    for center_state in centers:
        if center_state is None:
            continue

        building_slots = _get_buildings_for_center(center_state)
        if isinstance(center_state, dict):
            center_state["weekly_building_upkeep"] = 0
        if not building_slots:
            continue

        center_result = {
            "center": center_state,
            "buildings": [],
            "upkeep": 0,
        }

        owner_key = _get_center_owner_key(center_state)
        center_result["owner_key"] = owner_key
        center_result["owner_is_player"] = _is_player_owner(owner_key)

        for building_slot in building_slots:
            entry = _get_entry(building_slot)
            if not entry:
                continue

            display_name = get_building_display_name_text(building_slot) or building_slot.replace("_", " ").title()
            weekly_upkeep = registry_get_building_weekly_upkeep(building_slot)
            if not isinstance(weekly_upkeep, int) or weekly_upkeep < 0:
                weekly_upkeep = 0

            building_result = {
                "building_slot": building_slot,
                "display_name": display_name,
                "category_label": _format_category_label(building_slot),
                "specialization_label": _format_specialization_label(building_slot),
                "specialization": entry.get("specialization"),
                "tier": registry_get_building_tier(building_slot),
                "weekly_upkeep": weekly_upkeep,
                "effect_tags": _coerce_tuple(entry.get("effect_tags")),
                "effect_numbers": _coerce_tuple(entry.get("effect_numbers")),
                "design_summary": registry_get_building_design_summary(building_slot),
            }

            if weekly_upkeep > 0:
                center_result["upkeep"] += weekly_upkeep
                result["upkeep_total"] += weekly_upkeep
                _apply_upkeep_delta(wealth_state, owner_key, weekly_upkeep)

                if isinstance(center_state, dict):
                    center_state["wealth_delta"] = int(center_state.get("wealth_delta", 0)) - int(weekly_upkeep)
                    for wealth_key in ("wealth", "gold", "money"):
                        if wealth_key in center_state:
                            center_state[wealth_key] = int(center_state.get(wealth_key, 0)) - int(weekly_upkeep)
                            break

            building_result["effect_summary"] = _summarize_effects_for_building(building_slot)
            if building_result["effect_summary"]:
                result["effect_summaries"].extend(building_result["effect_summary"])

            center_result["buildings"].append(building_result)

        if isinstance(center_state, dict):
            center_state["weekly_building_upkeep"] = center_result["upkeep"]

        result["centers"].append(center_result)

    result["wealth_state"] = wealth_state
    return result


def apply_weekly_building_effects(*args, **kwargs):
    """Compatibility wrapper that keeps weekly effects and upkeep in one pass."""
    return calculate_weekly_building_effects(*args, **kwargs)


script_apply_weekly_building_effects = apply_weekly_building_effects


def _build_apply_weekly_building_effects_ops():
    return [
        (store_script_param, ":center_no", 1),
        (call_script, "script_get_center_building_effect_totals", ":center_no"),
        (assign, ":weekly_relations", reg0),
        (assign, ":weekly_prosperity", reg1),
        (assign, ":weekly_renown", reg4),

        (try_begin),
            (neq, ":weekly_prosperity", 0),
            (set_show_messages, 0),
            (call_script, "script_change_center_prosperity", ":center_no", ":weekly_prosperity"),
            (set_show_messages, 1),
        (try_end),

        (try_begin),
            (neq, ":weekly_renown", 0),
            (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
            (ge, ":center_lord", 0),
            (set_show_messages, 0),
            (call_script, "script_change_troop_renown", ":center_lord", ":weekly_renown"),
            (set_show_messages, 1),
        (try_end),

        (try_begin),
            (neq, ":weekly_relations", 0),
            (store_faction_of_party, ":center_faction", ":center_no"),
            (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
            (party_get_slot, ":cur_relation", ":center_no", slot_center_player_relation),
            (val_add, ":cur_relation", ":weekly_relations"),
            (val_clamp, ":cur_relation", -100, 101),
            (party_set_slot, ":center_no", slot_center_player_relation, ":cur_relation"),
        (try_end),
    ]


SCRIPTS = [
    ("apply_weekly_building_effects", _build_apply_weekly_building_effects_ops()),
]

__all__ = [
    "apply_weekly_building_effects",
    "calculate_weekly_building_effects",
    "script_apply_weekly_building_effects",
    "_build_apply_weekly_building_effects_ops",
]
