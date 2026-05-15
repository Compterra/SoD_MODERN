from __future__ import annotations

from pathlib import Path
import importlib
import re
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


CLASSIC_LORD_COMMENT_SUFFIXES = (
    "default",
    "martial",
    "quarrelsome",
    "pitiless",
    "cunning",
    "sadistic",
    "goodnatured",
    "upstanding",
)

INTRO_COMMENT_SUFFIXES = (
    "liege",
    "martial",
    "badtempered",
    "pitiless",
    "cunning",
    "sadistic",
    "goodnatured",
    "upstanding",
)

GOSSIP_COMMENT_SUFFIXES = (
    "default",
    "martial",
    "quarrelsome",
    "selfrighteous",
    "cunning",
    "sadistic",
    "goodnatured",
    "upstanding",
)

PERSONALITY_ARCHETYPE_IDS = (
    "str_personality_archetypes",
    "str_martial",
    "str_quarrelsome",
    "str_selfrighteous",
    "str_cunning",
    "str_debauched",
    "str_goodnatured",
    "str_upstanding",
)

REPUTATION_OFFSET_BLOCKS = {
    "str_battle_won_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_battle_won_grudging_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_battle_won_unfriendly_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_comment_intro_common_liege": INTRO_COMMENT_SUFFIXES,
    "str_comment_intro_famous_liege": INTRO_COMMENT_SUFFIXES,
    "str_comment_intro_noble_liege": INTRO_COMMENT_SUFFIXES,
    "str_enemy_meet_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_gossip_about_character_default": GOSSIP_COMMENT_SUFFIXES,
    "str_lord_challenged_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_lord_follow_refusal_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_lord_insult_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_lord_mission_failed_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_prisoner_released_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_rebellion_agree_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_rebellion_dilemma_2_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_rebellion_dilemma_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_rebellion_refuse_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_rebellion_rival_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_surrender_demand_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_surrender_offer_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_talk_later_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_troop_train_request_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_unnecessary_attack_default": CLASSIC_LORD_COMMENT_SUFFIXES,
    "str_unprovoked_attack_default": CLASSIC_LORD_COMMENT_SUFFIXES,
}


def _generated_string_ids() -> list[str]:
    sys.modules.pop("module_strings", None)
    module_strings = importlib.import_module("module_strings")
    return [
        f"str_{convert_to_identifier(entry[0])}"
        for entry in module_strings.strings
    ]


def _prefix_for(base_id: str, suffixes: tuple[str, ...]) -> str:
    prefix = f"str_"
    for suffix in suffixes:
        ending = f"_{suffix}"
        if base_id.endswith(ending):
            return base_id[: -len(ending)]
    raise AssertionError(f"{base_id} does not end in any expected suffix")


def _discover_lord_comment_offset_bases() -> set[str]:
    bases: set[str] = set()
    pattern = re.compile(r'"script_lord_comment_to_s43"\s*,[^)\n]*"(str_[A-Za-z0-9_]+)"')
    for source in (ROOT / "src" / "dialogs").rglob("*.py"):
        text = source.read_text(encoding="utf-8", errors="replace")
        bases.update(pattern.findall(text))
    return bases


def test_lord_comment_offset_bases_are_covered_by_static_guard() -> None:
    discovered = _discover_lord_comment_offset_bases()
    unguarded = sorted(discovered - set(REPUTATION_OFFSET_BLOCKS))
    assert not unguarded, (
        "lord_comment_to_s43 string offset base(s) need a static block order guard:\n"
        + "\n".join(unguarded)
    )


def test_reputation_string_offset_blocks_match_lrep_order() -> None:
    ids = _generated_string_ids()
    issues: list[str] = []

    for base_id, suffixes in sorted(REPUTATION_OFFSET_BLOCKS.items()):
        if base_id not in ids:
            issues.append(f"{base_id}: missing from generated strings")
            continue

        start = ids.index(base_id)
        prefix = _prefix_for(base_id, suffixes)
        expected = [f"{prefix}_{suffix}" for suffix in suffixes]
        actual = ids[start : start + len(expected)]
        if actual != expected:
            issues.append(
                f"{base_id}: expected contiguous {expected}, got {actual}"
            )

    assert not issues, "reputation string offset block mismatch:\n" + "\n".join(issues)


def test_personality_archetype_debug_strings_match_lrep_order() -> None:
    ids = _generated_string_ids()
    start = ids.index("str_personality_archetypes")
    actual = tuple(ids[start : start + len(PERSONALITY_ARCHETYPE_IDS)])
    assert actual == PERSONALITY_ARCHETYPE_IDS
