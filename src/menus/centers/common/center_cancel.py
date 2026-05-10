# -*- coding: cp1254 -*-

"""Current-project and cancellation panel for center construction."""

from src.constants.building_registry import BUILDING_REGISTRY

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)

SUPPORTED_SPECIALIZATIONS = (
    "economic",
    "military",
    "religious",
    "civic",
    "defensive",
    "population_health",
)

SPECIALIZATION_LABELS = {
    "economic": "Economic",
    "military": "Military",
    "religious": "Religious",
    "civic": "Civic",
    "defensive": "Defensive",
    "population_health": "Population Health",
}


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
    entry = _get_entry(building_slot)
    display_name = entry.get("display_name") or entry.get("name")
    if display_name:
        return display_name
    return building_slot.replace("_", " ").title()


def _get_category_label(building_slot):
    entry = _get_entry(building_slot)
    category = entry.get("ui_category") or entry.get("category")
    if not category:
        return None
    if isinstance(category, string_types):
        return category.replace("_", " ").title()
    return str(category)


def _format_slot_summary(slot_list):
    slot_list = _coerce_tuple(slot_list)
    if not slot_list:
        return ""
    return ", ".join(_get_display_name(slot) for slot in slot_list)


def _format_faction_summary(faction_list):
    faction_list = _coerce_tuple(faction_list)
    if not faction_list:
        return ""
    return ", ".join(str(faction) for faction in faction_list)


def build_center_cancel_payload(*args, **kwargs):
    current_project = kwargs.pop("current_project", None)
    current_buildings = kwargs.pop("current_buildings", None)
    center_type = kwargs.pop("center_type", None)
    owning_faction = kwargs.pop("owning_faction", None)
    refund_allowed = kwargs.pop("refund_allowed", False)

    if args:
        if current_project is None and len(args) > 0:
            current_project = args[0]
        if current_buildings is None and len(args) > 1:
            current_buildings = args[1]
        if center_type is None and len(args) > 2:
            center_type = args[2]
        if owning_faction is None and len(args) > 3:
            owning_faction = args[3]
        if len(args) > 4 and "refund_allowed" not in kwargs:
            refund_allowed = args[4]

    entry = _get_entry(current_project) if current_project else {}
    current_buildings_set = _coerce_building_set(current_buildings)

    detail_lines = []
    if current_project:
        detail_lines.append("Current project: %s" % _get_display_name(current_project))

        category_label = _get_category_label(current_project)
        if category_label:
            detail_lines.append("Category: %s" % category_label)

        specialization = entry.get("specialization")
        if specialization in SUPPORTED_SPECIALIZATIONS:
            detail_lines.append("Specialization: %s" % SPECIALIZATION_LABELS.get(specialization, specialization.title()))

        tier = entry.get("tier")
        upgrade_from = _coerce_tuple(entry.get("upgrade_from"))
        upgrade_to = _coerce_tuple(entry.get("upgrade_to"))
        exclusive_group = entry.get("exclusive_group")
        weekly_upkeep = entry.get("weekly_upkeep")
        faction_requirements = _coerce_tuple(entry.get("faction_requirements"))
        faction_flavor = entry.get("faction_flavor") or ""
        design_summary = entry.get("design_summary") or ""

        if isinstance(tier, int):
            detail_lines.append("Tier: %s" % tier)
        if upgrade_from:
            detail_lines.append("Upgrade source: %s" % _format_slot_summary(upgrade_from))
        if upgrade_to:
            detail_lines.append("Upgrade target: %s" % _format_slot_summary(upgrade_to))
        if exclusive_group:
            detail_lines.append("Exclusive group: %s" % exclusive_group)
        if weekly_upkeep is not None and isinstance(weekly_upkeep, int) and weekly_upkeep > 0:
            detail_lines.append("Weekly upkeep: -%s denars" % weekly_upkeep)
        if faction_requirements:
            detail_lines.append("Faction requirement: %s" % _format_faction_summary(faction_requirements))
        if faction_flavor:
            detail_lines.append(faction_flavor)
        if design_summary:
            detail_lines.append(design_summary)

        if current_buildings and exclusive_group:
            conflicts = []
            for other_slot in current_buildings_set:
                if other_slot == current_project:
                    continue
                other_entry = _get_entry(other_slot)
                if other_entry.get("exclusive_group") == exclusive_group:
                    conflicts.append(_get_display_name(other_slot))
            if conflicts:
                detail_lines.append("Conflicts with: %s" % ", ".join(conflicts))

        if current_buildings and upgrade_from:
            owned_sources = []
            for source_slot in upgrade_from:
                if source_slot in current_buildings_set:
                    owned_sources.append(_get_display_name(source_slot))
            if owned_sources:
                detail_lines.append("Upgrade source present: %s" % ", ".join(owned_sources))

    if refund_allowed:
        detail_lines.append("Cancellation may return resources if the project has not started.")
    else:
        detail_lines.append("Cancellation does not refund invested resources.")

    menu_variant = "cancel"
    if current_project:
        upgrade_from = _coerce_tuple(entry.get("upgrade_from"))
        exclusive_group = entry.get("exclusive_group")
        if upgrade_from:
            for source_slot in upgrade_from:
                if source_slot in current_buildings_set:
                    menu_variant = "upgrade"
                    break
        if menu_variant == "cancel" and exclusive_group:
            for other_slot in current_buildings_set:
                if other_slot == current_project:
                    continue
                other_entry = _get_entry(other_slot)
                if other_entry.get("exclusive_group") == exclusive_group:
                    menu_variant = "replace"
                    break

    return {
        "menu_id": "center_cancel",
        "menu_title": "Cancel current project",
        "current_project": current_project,
        "display_name": _get_display_name(current_project) if current_project else "",
        "category_label": _get_category_label(current_project) if current_project else "",
        "specialization": entry.get("specialization"),
        "tier": entry.get("tier"),
        "upgrade_from": _coerce_tuple(entry.get("upgrade_from")),
        "upgrade_to": _coerce_tuple(entry.get("upgrade_to")),
        "upgrade_source_summary": _format_slot_summary(entry.get("upgrade_from")),
        "upgrade_target_summary": _format_slot_summary(entry.get("upgrade_to")),
        "exclusive_group": entry.get("exclusive_group"),
        "weekly_upkeep": entry.get("weekly_upkeep") if isinstance(entry.get("weekly_upkeep"), int) else None,
        "faction_requirements": _coerce_tuple(entry.get("faction_requirements")),
        "faction_requirement_summary": _format_faction_summary(entry.get("faction_requirements")),
        "faction_flavor": entry.get("faction_flavor") or "",
        "design_summary": entry.get("design_summary") or "",
        "detail_lines": tuple(detail_lines),
        "current_buildings": tuple(current_buildings_set),
        "center_type": center_type,
        "owning_faction": owning_faction,
        "refund_allowed": bool(refund_allowed),
        "menu_variant": menu_variant,
        "cancel_text": "^^".join(detail_lines),
    }


def center_cancel(*args, **kwargs):
    """Compatibility wrapper for the cancellation menu payload."""
    return build_center_cancel_payload(*args, **kwargs)


center_cancel_menu = center_cancel

MENUS = [
    ("center_cancel", 0,
        "{s1}",
        "none",
        [
            (set_background_mesh, "mesh_pic_report_screen"),
            (str_store_party_name, s2, "$current_town"),
            (party_get_slot, ":current_project", "$current_town", slot_center_current_improvement),
            (try_begin),
                (gt, ":current_project", 0),
                (str_store_string, s1, "@Cancel current project at {s2}:^^This project can be reviewed here before returning to the center management screen. Full cancellation/refund rules remain governed by the construction scripts."),
            (else_try),
                (str_store_string, s1, "@Cancel current project at {s2}:^^There is no active construction project here."),
            (try_end),
        ],
        [
            ("return", [], "Return to center management.",
                [
                    (jump_to_menu, "mnu_center_manage"),
                ]),
        ]
    ),
]

__all__ = [
    "build_center_cancel_payload",
    "center_cancel",
    "center_cancel_menu",
]
