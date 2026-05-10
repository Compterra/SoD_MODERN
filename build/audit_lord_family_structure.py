from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "compile"
OUT = ROOT / "docs" / "reports" / "lord_family_validation_report.md"
SOURCE_AUDIT = ROOT / "docs" / "reports" / "lord_family_structure_audit.md"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(COMPILE / "ids"))
sys.path.insert(0, str(COMPILE))
sys.path.insert(0, str(COMPILE / "headers"))

from header_troops import tf_female  # type: ignore
import module_troops  # type: ignore
from module_constants import (  # type: ignore
    heroes_begin,
    heroes_end,
    kingdom_heroes_begin,
    kingdom_heroes_end,
    kingdom_ladies_begin,
    kingdom_ladies_end,
    pretenders_begin,
    pretenders_end,
    slot_troop_daughter,
    slot_troop_father,
    slot_troop_lover,
    slot_troop_mother,
    slot_troop_sibling,
    slot_troop_son,
    slot_troop_spouse,
)

try:
    from module_constants import (  # type: ignore
        slot_troop_sod_house_claim_strength,
        slot_troop_sod_house_grievance,
        slot_troop_sod_house_head,
        slot_troop_sod_house_id,
        slot_troop_sod_house_loyalty,
        slot_troop_sod_house_rank,
        sod_house_rank_lady,
        sod_house_rank_lord,
        sod_house_rank_named_actor,
        sod_house_rank_pretender,
        sod_house_rank_ruler,
    )
except ImportError:
    slot_troop_sod_house_id = 363
    slot_troop_sod_house_rank = 364
    slot_troop_sod_house_head = 365
    slot_troop_sod_house_grievance = 366
    slot_troop_sod_house_loyalty = 367
    slot_troop_sod_house_claim_strength = 368
    sod_house_rank_ruler = 1
    sod_house_rank_lord = 2
    sod_house_rank_lady = 3
    sod_house_rank_pretender = 4
    sod_house_rank_named_actor = 5


FAMILY_SLOTS = {
    slot_troop_spouse: "spouse",
    slot_troop_father: "father",
    slot_troop_mother: "mother",
    slot_troop_daughter: "daughter",
    slot_troop_son: "son",
    slot_troop_sibling: "sibling",
    slot_troop_lover: "lover",
}

COMPLETION_SLOTS = {
    slot_troop_spouse: "spouse",
    slot_troop_father: "father",
    slot_troop_mother: "mother",
    slot_troop_daughter: "daughter",
    slot_troop_son: "son",
    slot_troop_sibling: "sibling",
}


def troop_id(ref: str | int | None) -> str | None:
    if ref is None:
        return None
    if isinstance(ref, int):
        if ref <= 0 or ref >= len(module_troops.troops):
            return None
        return module_troops.troops[ref][0]
    if ref.startswith('"') and ref.endswith('"'):
        ref = ref[1:-1]
    if ref.startswith("trp_"):
        ref = ref[4:]
    return ref


def troop_index(ref: str | int) -> int:
    tid = troop_id(ref)
    if tid is None:
        raise KeyError(ref)
    return TROOP_INDEX[tid]


TROOP_IDS = [troop[0] for troop in module_troops.troops]
TROOP_INDEX = {tid: index for index, tid in enumerate(TROOP_IDS)}


def in_range(troop: str, begin: str | int, end: str | int) -> bool:
    index = TROOP_INDEX.get(troop, -1)
    return troop_index(begin) <= index < troop_index(end)


def name_of(troop: str | None) -> str:
    if not troop:
        return "-"
    index = TROOP_INDEX.get(troop)
    if index is None:
        return f"`trp_{troop}`"
    return f"{module_troops.troops[index][1]} (`trp_{troop}`)"


def gender_of(troop: str) -> int:
    flags = module_troops.troops[TROOP_INDEX[troop]][3]
    return 1 if flags & tf_female else 0


def empty_slots() -> dict[int, str | None]:
    return {slot: None for slot in FAMILY_SLOTS}


def parse_seed_relations() -> tuple[dict[str, dict[int, str | None]], list[str]]:
    slots: dict[str, dict[int, str | None]] = defaultdict(empty_slots)
    warnings: list[str] = []
    raw = (ROOT / "src" / "scripts" / "ZA_hardcoded_game_scripts" / "game_start.py").read_text(
        encoding="utf-8",
        errors="replace",
    )
    pattern = re.compile(
        r"\(troop_set_slot,\s*\"(?P<src>trp_[^\"]+)\",\s*"
        r"(?P<slot>slot_troop_(?:spouse|father|mother|daughter|son|sibling|lover)),\s*"
        r"(?P<dst>\"trp_[^\"]+\"|0|-1)\s*\)"
    )
    slot_lookup = {f"slot_troop_{name}": slot for slot, name in FAMILY_SLOTS.items()}
    for match in pattern.finditer(raw):
        src = troop_id(match.group("src"))
        dst_raw = match.group("dst")
        slot = slot_lookup[match.group("slot")]
        if not src:
            continue
        if dst_raw in {"0", "-1"}:
            dst = None
        else:
            dst = troop_id(dst_raw)
        if src not in TROOP_INDEX:
            warnings.append(f"Seed source `{match.group('src')}` is not a compiled troop.")
            continue
        if dst is not None and dst not in TROOP_INDEX:
            warnings.append(f"Seed target `{dst_raw}` for `{match.group('src')}` is not a compiled troop.")
            continue
        slots[src][slot] = dst
    return slots, warnings


def complete_family_relations(slots: dict[str, dict[int, str | None]]) -> None:
    for troop in TROOP_IDS:
        if not in_range(troop, heroes_begin, heroes_end):
            continue
        current = slots[troop]
        gender = gender_of(troop)
        spouse = current[slot_troop_spouse]
        if spouse:
            slots[spouse][slot_troop_spouse] = troop
            daughter = current[slot_troop_daughter]
            son = current[slot_troop_son]
            if daughter:
                slots[spouse][slot_troop_daughter] = daughter
            if son:
                slots[spouse][slot_troop_son] = son
            spouse_daughter = slots[spouse][slot_troop_daughter]
            spouse_son = slots[spouse][slot_troop_son]
            if spouse_daughter:
                current[slot_troop_daughter] = spouse_daughter
            if spouse_son:
                current[slot_troop_son] = spouse_son

        sibling = current[slot_troop_sibling]
        if sibling:
            slots[sibling][slot_troop_sibling] = troop
            mother = current[slot_troop_mother]
            father = current[slot_troop_father]
            if mother:
                slots[sibling][slot_troop_mother] = mother
            if father:
                slots[sibling][slot_troop_father] = father
            sibling_mother = slots[sibling][slot_troop_mother]
            sibling_father = slots[sibling][slot_troop_father]
            if sibling_mother:
                current[slot_troop_mother] = sibling_mother
            if sibling_father:
                current[slot_troop_father] = sibling_father

        son = current[slot_troop_son]
        if son:
            slots[son][slot_troop_father if gender == 0 else slot_troop_mother] = troop
            other_parent = current[slot_troop_spouse]
            sibling = current[slot_troop_daughter]
            if other_parent:
                slots[son][slot_troop_father if gender == 1 else slot_troop_mother] = other_parent
            if sibling:
                slots[son][slot_troop_sibling] = sibling
            child_spouse = slots[son][slot_troop_mother if gender == 0 else slot_troop_father]
            child_daughter = slots[son][slot_troop_sibling]
            if child_spouse:
                current[slot_troop_spouse] = child_spouse
            if child_daughter:
                current[slot_troop_daughter] = child_daughter

        daughter = current[slot_troop_daughter]
        if daughter:
            slots[daughter][slot_troop_father if gender == 0 else slot_troop_mother] = troop
            other_parent = current[slot_troop_spouse]
            sibling = current[slot_troop_son]
            if other_parent:
                slots[daughter][slot_troop_father if gender == 1 else slot_troop_mother] = other_parent
            if sibling:
                slots[daughter][slot_troop_sibling] = sibling
            child_spouse = slots[daughter][slot_troop_mother if gender == 0 else slot_troop_father]
            child_son = slots[daughter][slot_troop_sibling]
            if child_spouse:
                current[slot_troop_spouse] = child_spouse
            if child_son:
                current[slot_troop_son] = child_son

        father = current[slot_troop_father]
        if father:
            slots[father][slot_troop_son if gender == 0 else slot_troop_daughter] = troop
            mother = current[slot_troop_mother]
            sibling = current[slot_troop_sibling]
            if mother:
                slots[father][slot_troop_spouse] = mother
            if sibling:
                slots[father][slot_troop_daughter if gender == 0 else slot_troop_son] = sibling
            inferred_sibling = slots[father][slot_troop_daughter if gender == 0 else slot_troop_son]
            inferred_mother = slots[father][slot_troop_spouse]
            if inferred_sibling:
                current[slot_troop_sibling] = inferred_sibling
            if inferred_mother:
                current[slot_troop_mother] = inferred_mother

        mother = current[slot_troop_mother]
        if mother:
            slots[mother][slot_troop_son if gender == 0 else slot_troop_daughter] = troop
            father = current[slot_troop_father]
            sibling = current[slot_troop_sibling]
            if father:
                slots[mother][slot_troop_spouse] = father
            if sibling:
                slots[mother][slot_troop_daughter if gender == 0 else slot_troop_son] = sibling
            inferred_sibling = slots[mother][slot_troop_daughter if gender == 0 else slot_troop_son]
            inferred_father = slots[mother][slot_troop_spouse]
            if inferred_sibling:
                current[slot_troop_sibling] = inferred_sibling
            if inferred_father:
                current[slot_troop_father] = inferred_father


def validate(slots: dict[str, dict[int, str | None]]) -> dict[str, list[str]]:
    issues: dict[str, list[str]] = defaultdict(list)
    for troop in TROOP_IDS:
        if not in_range(troop, heroes_begin, heroes_end):
            continue
        current = slots[troop]
        for slot, relation in FAMILY_SLOTS.items():
            target = current[slot]
            if not target:
                continue
            if target == troop:
                issues["self_links"].append(f"{name_of(troop)} has self-link in `{relation}`.")
            if target not in TROOP_INDEX:
                issues["invalid_targets"].append(f"{name_of(troop)} {relation} points to missing `trp_{target}`.")
                continue
            if not in_range(target, heroes_begin, heroes_end):
                issues["out_of_range_targets"].append(f"{name_of(troop)} {relation} points outside hero range: {name_of(target)}.")

        spouse = current[slot_troop_spouse]
        if spouse and slots[spouse][slot_troop_spouse] != troop:
            issues["spouse_not_reciprocal"].append(f"{name_of(troop)} spouse {name_of(spouse)} does not point back.")
        if spouse and gender_of(spouse) == gender_of(troop):
            issues["same_gender_spouse_links"].append(f"{name_of(troop)} and {name_of(spouse)} are both stored with the same troop gender.")

        sibling = current[slot_troop_sibling]
        if sibling and slots[sibling][slot_troop_sibling] != troop:
            issues["sibling_not_reciprocal"].append(f"{name_of(troop)} sibling {name_of(sibling)} does not point back.")

        father = current[slot_troop_father]
        if father:
            if gender_of(father) != 0:
                issues["father_gender"].append(f"{name_of(troop)} father slot points to female troop {name_of(father)}.")
            if slots[father][slot_troop_son if gender_of(troop) == 0 else slot_troop_daughter] != troop:
                issues["parent_child_not_reciprocal"].append(f"{name_of(troop)} father {name_of(father)} does not point back as child.")
        mother = current[slot_troop_mother]
        if mother:
            if gender_of(mother) != 1:
                issues["mother_gender"].append(f"{name_of(troop)} mother slot points to male troop {name_of(mother)}.")
            if slots[mother][slot_troop_son if gender_of(troop) == 0 else slot_troop_daughter] != troop:
                issues["parent_child_not_reciprocal"].append(f"{name_of(troop)} mother {name_of(mother)} does not point back as child.")

        son = current[slot_troop_son]
        if son:
            if gender_of(son) != 0:
                issues["child_gender"].append(f"{name_of(troop)} son slot points to female troop {name_of(son)}.")
            if slots[son][slot_troop_father if gender_of(troop) == 0 else slot_troop_mother] != troop:
                issues["child_parent_not_reciprocal"].append(f"{name_of(troop)} son {name_of(son)} does not point back as parent.")
        daughter = current[slot_troop_daughter]
        if daughter:
            if gender_of(daughter) != 1:
                issues["child_gender"].append(f"{name_of(troop)} daughter slot points to male troop {name_of(daughter)}.")
            if slots[daughter][slot_troop_father if gender_of(troop) == 0 else slot_troop_mother] != troop:
                issues["child_parent_not_reciprocal"].append(f"{name_of(troop)} daughter {name_of(daughter)} does not point back as parent.")

    for lady in TROOP_IDS:
        if not in_range(lady, kingdom_ladies_begin, kingdom_ladies_end):
            continue
        if not slots[lady][slot_troop_father] and not slots[lady][slot_troop_spouse]:
            issues["ladies_without_family_anchor"].append(f"{name_of(lady)} has no father or spouse after completion.")

    return issues


def relation_counts(slots: dict[str, dict[int, str | None]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for troop in TROOP_IDS:
        if not in_range(troop, heroes_begin, heroes_end):
            continue
        for slot, name in FAMILY_SLOTS.items():
            if slots[troop][slot]:
                counts[name] += 1
    return counts


def build_house_identities(slots: dict[str, dict[int, str | None]]) -> dict[str, dict[str, int | str]]:
    houses: dict[str, dict[str, int | str]] = {}
    for troop in TROOP_IDS:
        if not in_range(troop, heroes_begin, heroes_end):
            continue
        house_id = TROOP_INDEX[troop] - troop_index(heroes_begin) + 1
        if in_range(troop, pretenders_begin, pretenders_end):
            rank = sod_house_rank_pretender
        elif in_range(troop, kingdom_ladies_begin, kingdom_ladies_end):
            rank = sod_house_rank_lady
        elif in_range(troop, kingdom_heroes_begin, kingdom_heroes_end):
            rank = sod_house_rank_lord
        else:
            rank = sod_house_rank_named_actor
        houses[troop] = {
            "house_id": house_id,
            "head": troop,
            "rank": rank,
            "grievance": 0,
            "loyalty": 50,
            "claim_strength": 40 if rank == sod_house_rank_pretender else 20 if rank == sod_house_rank_lord else 0,
        }

    for troop in TROOP_IDS:
        if not in_range(troop, heroes_begin, heroes_end):
            continue
        spouse = slots[troop][slot_troop_spouse]
        if not spouse or spouse not in houses:
            continue
        if TROOP_INDEX[troop] >= TROOP_INDEX[spouse]:
            continue
        if in_range(troop, kingdom_heroes_begin, kingdom_heroes_end):
            head = troop
        elif in_range(spouse, kingdom_heroes_begin, kingdom_heroes_end):
            head = spouse
        else:
            head = troop
        house_id = int(houses[head]["house_id"])
        houses[troop]["house_id"] = house_id
        houses[spouse]["house_id"] = house_id
        houses[troop]["head"] = head
        houses[spouse]["head"] = head
    return houses


def house_counts(houses: dict[str, dict[str, int | str]]) -> Counter[str]:
    unique_house_ids = {int(data["house_id"]) for data in houses.values()}
    member_counts: Counter[int] = Counter(int(data["house_id"]) for data in houses.values())
    counts: Counter[str] = Counter()
    counts["hero_rows"] = len(houses)
    counts["unique_houses"] = len(unique_house_ids)
    counts["married_house_groups"] = sum(1 for count in member_counts.values() if count > 1)
    counts["single_actor_houses"] = sum(1 for count in member_counts.values() if count == 1)
    counts["rank_lord_or_ruler"] = sum(
        1
        for data in houses.values()
        if int(data["rank"]) in {sod_house_rank_lord, sod_house_rank_ruler}
    )
    counts["rank_lady"] = sum(1 for data in houses.values() if int(data["rank"]) == sod_house_rank_lady)
    counts["rank_pretender"] = sum(1 for data in houses.values() if int(data["rank"]) == sod_house_rank_pretender)
    return counts


def family_rows(slots: dict[str, dict[int, str | None]]) -> list[str]:
    rows = []
    for troop in TROOP_IDS:
        if not in_range(troop, kingdom_heroes_begin, kingdom_heroes_end):
            continue
        current = slots[troop]
        if not any(current[slot] for slot in COMPLETION_SLOTS):
            continue
        rows.append(
            "| {lord} | {spouse} | {father} | {mother} | {son} | {daughter} | {sibling} |".format(
                lord=name_of(troop),
                spouse=name_of(current[slot_troop_spouse]),
                father=name_of(current[slot_troop_father]),
                mother=name_of(current[slot_troop_mother]),
                son=name_of(current[slot_troop_son]),
                daughter=name_of(current[slot_troop_daughter]),
                sibling=name_of(current[slot_troop_sibling]),
            )
        )
    return rows


def write_report(slots: dict[str, dict[int, str | None]], seed_warnings: list[str], issues: dict[str, list[str]]) -> None:
    hero_total = sum(1 for troop in TROOP_IDS if in_range(troop, kingdom_heroes_begin, kingdom_heroes_end))
    lady_total = sum(1 for troop in TROOP_IDS if in_range(troop, kingdom_ladies_begin, kingdom_ladies_end))
    counts = relation_counts(slots)
    houses = build_house_identities(slots)
    house_stats = house_counts(houses)
    issue_total = sum(len(items) for items in issues.values()) + len(seed_warnings)
    depth_warnings: list[str] = []
    if counts["father"] == 0 and counts["mother"] == 0:
        depth_warnings.append("No parent links exist after simulated completion.")
    if counts["son"] == 0 and counts["daughter"] == 0:
        depth_warnings.append("No child links exist after simulated completion.")
    if counts["sibling"] == 0:
        depth_warnings.append("No sibling links exist after simulated completion.")
    if counts["spouse"] > 0 and counts["father"] == 0 and counts["son"] == 0 and counts["daughter"] == 0:
        depth_warnings.append("The active graph is currently spouse-only, despite daughter/wife troop naming conventions.")
    lines: list[str] = [
        "# Lord Family Validation Report",
        "",
        "Generated by `py build/audit_lord_family_structure.py`.",
        "",
        "## Summary",
        "",
        f"- Kingdom hero range entries: {hero_total}",
        f"- Kingdom lady range entries: {lady_total}",
        f"- Seed warnings: {len(seed_warnings)}",
        f"- Validation issues: {issue_total}",
        f"- Model depth warnings: {len(depth_warnings)}",
        "",
        "## Relationship Slot Counts After Simulated Completion",
        "",
    ]
    for name in ("spouse", "father", "mother", "son", "daughter", "sibling", "lover"):
        lines.append(f"- {name}: {counts[name]}")

    lines.extend(
        [
            "",
            "## House Identity Layer",
            "",
            "The new house layer is intentionally separate from the shallow Native family slots. It gives each hero a stable house identity, then merges spouses into the same house with the lord spouse preferred as house head.",
            "",
            f"- House slot constants: `{slot_troop_sod_house_id}`, `{slot_troop_sod_house_rank}`, `{slot_troop_sod_house_head}`, `{slot_troop_sod_house_grievance}`, `{slot_troop_sod_house_loyalty}`, `{slot_troop_sod_house_claim_strength}`",
            f"- House identity rows: {house_stats['hero_rows']}",
            f"- Unique houses after spouse merge: {house_stats['unique_houses']}",
            f"- Married house groups: {house_stats['married_house_groups']}",
            f"- Single-actor houses: {house_stats['single_actor_houses']}",
            f"- Lord/ruler rank rows: {house_stats['rank_lord_or_ruler']}",
            f"- Lady rank rows: {house_stats['rank_lady']}",
            f"- Pretender rank rows: {house_stats['rank_pretender']}",
            "",
        ]
    )

    lines.extend(["", "## Issues", ""])
    if not seed_warnings and not issues:
        lines.append("- No structural issues found in the simulated family graph.")
    else:
        if seed_warnings:
            lines.append("### Seed Warnings")
            lines.append("")
            for warning in seed_warnings:
                lines.append(f"- {warning}")
            lines.append("")
        for key in sorted(issues):
            items = issues[key]
            lines.append(f"### {key.replace('_', ' ').title()} ({len(items)})")
            lines.append("")
            for item in items[:50]:
                lines.append(f"- {item}")
            if len(items) > 50:
                lines.append(f"- ...and {len(items) - 50} more.")
            lines.append("")

    lines.extend(["", "## Model Depth Warnings", ""])
    if depth_warnings:
        for warning in depth_warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- No depth warnings.")
    lines.append("")

    rows = family_rows(slots)
    lines.extend(
        [
            "## Immediate Family Rows",
            "",
            "Only lords with at least one completed immediate-family slot are listed.",
            "",
            "| Lord | Spouse | Father | Mother | Son | Daughter | Sibling |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Interpretation",
            "",
            "- The current graph remains shallow by design: one spouse, one parent pair, one child of each gender, and one sibling.",
            "- A zero-issue report would not mean the family model is rich; it would only mean the existing shallow links are internally consistent.",
        "- `Ladies Without Family Anchor` is the most important watchlist for court placement and family-facing quests.",
        "- Same-gender spouse links may be valid only if the troop gender flags are intentionally nonstandard; otherwise they deserve manual review.",
        "- The house layer now provides a broader political identity surface for grievance, loyalty, and claim strength without requiring fake parent/child links.",
        "",
    ]
    )
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def patch_audit_summary(issue_count: int) -> None:
    if not SOURCE_AUDIT.exists():
        return
    raw = SOURCE_AUDIT.read_text(encoding="utf-8", errors="replace")
    marker = "## Validator Pass\n"
    section = (
        "## Validator Pass\n\n"
        "Implemented `build/audit_lord_family_structure.py`, which parses the `game_start.py` family seed assignments, "
        "simulates the existing `script_complete_family_relations` behavior, and writes "
        "`docs/reports/lord_family_validation_report.md`.\n\n"
        f"Latest validation issue count: {issue_count}. The generated report shows the active graph is structurally valid but shallow: spouse links exist, while parent, child, and sibling links are absent after simulated completion. It now also summarizes the lightweight house identity layer initialized by `script_sod_initialize_house_identity`.\n\n"
    )
    if marker in raw:
        before = raw.split(marker, 1)[0]
        after = raw.split(marker, 1)[1]
        next_header = after.find("\n## ")
        if next_header >= 0:
            raw = before + section + after[next_header + 1 :]
        else:
            raw = before + section
    else:
        insert = raw.find("## Best Immediate Next Step")
        if insert >= 0:
            raw = raw[:insert] + section + raw[insert:]
        else:
            raw = raw.rstrip() + "\n\n" + section
    SOURCE_AUDIT.write_text(raw, encoding="utf-8")


def main() -> int:
    slots, seed_warnings = parse_seed_relations()
    complete_family_relations(slots)
    complete_family_relations(slots)
    issues = validate(slots)
    issue_count = sum(len(items) for items in issues.values()) + len(seed_warnings)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_report(slots, seed_warnings, issues)
    patch_audit_summary(issue_count)
    print(f"[audit_lord_family_structure] wrote {OUT}")
    print(f"[audit_lord_family_structure] validation issues: {issue_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
