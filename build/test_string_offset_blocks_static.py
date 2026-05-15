from __future__ import annotations

import ast
from pathlib import Path
import importlib
import sys


ROOT = Path(__file__).resolve().parents[1]
for path in (
    ROOT / "compile",
    ROOT / "compile" / "process",
):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from process_common import convert_to_identifier  # type: ignore  # noqa: E402


ARITHMETIC_OPS = {"store_add", "store_sub", "val_add"}

RELATION_BLOCK = [
    *(f"str_relation_mnus_{value}" for value in range(100, 0, -10)),
    *(f"str_relation_plus_{value}" for value in range(0, 100, 10)),
]

CENTER_RELATION_BLOCK = [
    *(f"str_center_relation_mnus_{value}" for value in range(100, 0, -10)),
    *(f"str_center_relation_plus_{value}" for value in range(0, 100, 10)),
]

PROSPERITY_BLOCK = [f"str_prosperity_{value}" for value in range(0, 101, 10)]
TOWN_PROSPERITY_BLOCK = [f"str_town_prosperity_{value}" for value in range(0, 101, 10)]
VILLAGE_PROSPERITY_BLOCK = [f"str_village_prosperity_{value}" for value in range(0, 101, 10)]

SOD_FAITH_NUMERIC_SUFFIXES = tuple(range(0, 6))
SOD_FAITH_BLOCKS = {
    f"str_sod_{name}_0": [f"str_sod_{name}_{value}" for value in SOD_FAITH_NUMERIC_SUFFIXES]
    for name in (
        "chapel",
        "chapter",
        "faith_level",
        "faith_suffix",
        "homeland",
        "monastery_improve",
        "monastery_summary",
    )
}

STRING_OFFSET_BLOCKS = {
    **SOD_FAITH_BLOCKS,
    "str_center_relation_mnus_100": CENTER_RELATION_BLOCK,
    "str_describe_faith_violent": [
        "str_describe_faith_violent",
        "str_describe_faith_hated",
        "str_describe_faith_swear",
        "str_describe_faith_poor",
        "str_describe_faith_indifferent",
        "str_describe_faith_tolerated",
        "str_describe_faith_accepted",
        "str_describe_faith_dominant",
        "str_describe_faith_inspiration",
    ],
    "str_describe_health_abysmal": [
        "str_describe_health_abysmal",
        "str_describe_health_terrible",
        "str_describe_health_unhealthy",
        "str_describe_health_poor",
        "str_describe_health_average",
        "str_describe_health_good",
        "str_describe_health_excellent",
        "str_describe_health_exceptional",
        "str_describe_health_fantastic",
    ],
    "str_faith_violent": [
        "str_faith_violent",
        "str_faith_hated",
        "str_faith_swear",
        "str_faith_poor",
        "str_faith_indifferent",
        "str_faith_tolerated",
        "str_faith_accepted",
        "str_faith_dominant",
        "str_faith_inspiration",
    ],
    "str_health_abysmal": [
        "str_health_abysmal",
        "str_health_terrible",
        "str_health_unhealthy",
        "str_health_poor",
        "str_health_average",
        "str_health_good",
        "str_health_excellent",
        "str_health_exceptional",
        "str_health_fantastic",
    ],
    "str_hero_not_upgrading_armor": [
        "str_hero_not_upgrading_armor",
        "str_hero_upgrading_armor",
    ],
    "str_hero_not_upgrading_horse": [
        "str_hero_not_upgrading_horse",
        "str_hero_upgrading_horse",
    ],
    "str_hero_wpn_slot_none": [
        "str_hero_wpn_slot_none",
        "str_hero_wpn_slot_horse",
        "str_hero_wpn_slot_one_handed",
        "str_hero_wpn_slot_two_handed",
        "str_hero_wpn_slot_polearm_all",
        "str_hero_wpn_slot_arrows",
        "str_hero_wpn_slot_bolts",
        "str_hero_wpn_slot_shield",
        "str_hero_wpn_slot_bow",
        "str_hero_wpn_slot_crossbow",
        "str_hero_wpn_slot_throwing",
    ],
    "str_imod_0": [f"str_imod_{value}" for value in range(0, 43)],
    "str_land_quality_barren": [
        "str_land_quality_barren",
        "str_land_quality_poor",
        "str_land_quality_average",
        "str_land_quality_arable",
        "str_land_quality_lush",
        "str_land_quality_rich",
    ],
    "str_prosperity_0": PROSPERITY_BLOCK,
    "str_relation_mnus_100": RELATION_BLOCK,
    "str_secret_sign_1": [f"str_secret_sign_{value}" for value in range(1, 5)],
    "str_sod_merc_commander_1_intro": [
        f"str_sod_merc_commander_{value}_intro"
        for value in range(1, 7)
    ],
    "str_swadian_rebellion_monarch_response_1": [
        f"str_{kingdom}_rebellion_monarch_response_1"
        for kingdom in ("swadian", "vaegir", "khergit", "nord", "rhodok")
    ],
    "str_swadian_rebellion_monarch_response_2": [
        f"str_{kingdom}_rebellion_monarch_response_2"
        for kingdom in ("swadian", "vaegir", "khergit", "nord", "rhodok")
    ],
    "str_swadian_rebellion_pretender_intro": [
        f"str_{kingdom}_rebellion_pretender_intro"
        for kingdom in ("swadian", "vaegir", "khergit", "nord", "rhodok")
    ],
    "str_swadian_rebellion_pretender_story_1": [
        f"str_{kingdom}_rebellion_pretender_story_1"
        for kingdom in ("swadian", "vaegir", "khergit", "nord", "rhodok")
    ],
    "str_swadian_rebellion_pretender_story_2": [
        f"str_{kingdom}_rebellion_pretender_story_2"
        for kingdom in ("swadian", "vaegir", "khergit", "nord", "rhodok")
    ],
    "str_swadian_rebellion_pretender_story_3": [
        f"str_{kingdom}_rebellion_pretender_story_3"
        for kingdom in ("swadian", "vaegir", "khergit", "nord", "rhodok")
    ],
    "str_town_prosperity_0": TOWN_PROSPERITY_BLOCK,
    "str_village_prosperity_0": VILLAGE_PROSPERITY_BLOCK,
    "str_war_report_minus_4": [
        "str_war_report_minus_4",
        "str_war_report_minus_3",
        "str_war_report_minus_2",
        "str_war_report_minus_1",
        "str_war_report_0",
        "str_war_report_plus_1",
        "str_war_report_plus_2",
        "str_war_report_plus_3",
        "str_war_report_plus_4",
    ],
}

SPECIALIZED_STRING_OFFSET_BASES = {
    "str_battle_won_default",
    "str_battle_won_grudging_default",
    "str_battle_won_unfriendly_default",
    "str_comment_intro_common_liege",
    "str_comment_intro_famous_liege",
    "str_comment_intro_noble_liege",
    "str_enemy_meet_default",
    "str_gossip_about_character_default",
    "str_lord_challenged_default",
    "str_lord_follow_refusal_default",
    "str_lord_insult_default",
    "str_lord_mission_failed_default",
    "str_npc1_intro",
    "str_npc1_payment",
    "str_npc1_payment_response",
    "str_personality_archetypes",
    "str_prisoner_released_default",
    "str_rebellion_agree_default",
    "str_rebellion_dilemma_2_default",
    "str_rebellion_dilemma_default",
    "str_rebellion_refuse_default",
    "str_rebellion_rival_default",
    "str_surrender_demand_default",
    "str_surrender_offer_default",
    "str_talk_later_default",
    "str_troop_train_request_default",
    "str_unnecessary_attack_default",
    "str_unprovoked_attack_default",
}


def _generated_string_ids() -> list[str]:
    sys.modules.pop("module_strings", None)
    module_strings = importlib.import_module("module_strings")
    return [
        f"str_{convert_to_identifier(entry[0])}"
        for entry in module_strings.strings
    ]


def _operation_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    return None


def _string_arithmetic_bases_from_source() -> set[str]:
    bases: set[str] = set()
    for source in (ROOT / "src").rglob("*.py"):
        if "__pycache__" in source.parts:
            continue
        tree = ast.parse(source.read_text(encoding="utf-8", errors="replace"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Tuple, ast.List)) or not node.elts:
                continue
            if _operation_name(node.elts[0]) not in ARITHMETIC_OPS:
                continue
            for element in node.elts[1:]:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    if element.value.startswith("str_"):
                        bases.add(element.value)
    return bases


def test_string_arithmetic_bases_are_covered_by_static_guards() -> None:
    covered = set(STRING_OFFSET_BLOCKS) | SPECIALIZED_STRING_OFFSET_BASES
    discovered = _string_arithmetic_bases_from_source()
    unguarded = sorted(discovered - covered)
    assert not unguarded, (
        "string arithmetic base(s) need a static block order guard:\n"
        + "\n".join(unguarded)
    )


def test_string_arithmetic_blocks_are_contiguous() -> None:
    ids = _generated_string_ids()
    issues: list[str] = []
    for base_id, expected in sorted(STRING_OFFSET_BLOCKS.items()):
        if base_id not in ids:
            issues.append(f"{base_id}: missing from generated strings")
            continue
        start = ids.index(base_id)
        actual = ids[start : start + len(expected)]
        if actual != expected:
            issues.append(
                f"{base_id}: expected contiguous {expected}, got {actual}"
            )

    assert not issues, "string arithmetic block mismatch:\n" + "\n".join(issues)
