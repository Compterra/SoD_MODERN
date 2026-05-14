# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def assert_before(raw: str, first: str, second: str) -> None:
    assert first in raw, f"missing token: {first}"
    assert second in raw, f"missing token: {second}"
    assert raw.index(first) < raw.index(second), f"{first} should appear before {second}"


ENTRY_RE = re.compile(
    r"\[\s*([^,\]]+)\s*,\s*([\"'])([^\"']+)\2\s*,.*?,\s*([\"'])(.*?)\4\s*,\s*([\"'])([^\"']+)\6\s*,",
    re.DOTALL,
)


IMMERSION_FILES = [
    "src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_personality_greeting.py",
    "src/dialogs/ZC01_centers_and_economy/anyone_mayor_social_weather.py",
    "src/dialogs/ZC01_centers_and_economy/anyone_village_elder_social_weather.py",
    "src/dialogs/ZC01_centers_and_economy/anyone_goods_merchant_social_weather.py",
    "src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_social_weather.py",
    "src/dialogs/ZZ99_misc_dialogs/anyone_gm_pretalk_social_weather.py",
    "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_patrol_party_nonplayer_immersion_start.py",
    "src/dialogs/ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_05.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_merchant_caravan_world_about.py",
]


CRITICAL_ORDER_PAIRS = [
    (
        "ZA01_startup_and_dispatch/anyone_lord_start_personality_greeting.py",
        "ZA01_startup_and_dispatch/anyone_lord_start_30.py",
    ),
    (
        "ZC01_centers_and_economy/anyone_mayor_social_weather.py",
        "ZC01_centers_and_economy/anyone_mayor_pretalk.py",
    ),
    (
        "ZC01_centers_and_economy/anyone_village_elder_social_weather.py",
        "ZC01_centers_and_economy/anyone_village_elder_pretalk.py",
    ),
    (
        "ZC01_centers_and_economy/anyone_goods_merchant_social_weather.py",
        "ZC01_centers_and_economy/anyone_goods_merchant_pretalk.py",
    ),
    (
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_social_weather.py",
        "ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_pretalk.py",
    ),
    (
        "ZZ99_misc_dialogs/anyone_gm_pretalk_social_weather.py",
        "ZZ99_misc_dialogs/anyone_gm_pretalk.py",
    ),
    (
        "ZA01_startup_and_dispatch/party_tpl_pt_patrol_party_nonplayer_immersion_start.py",
        "ZA01_startup_and_dispatch/party_tpl_pt_patrol_party_start.py",
    ),
    (
        "ZA01_startup_and_dispatch/party_tpl_pt_merchant_caravan_start_05.py",
        "ZC01_centers_and_economy/anyone_plyr_escort_merchant_caravan_talk.py",
    ),
]


def extract_state_text_pairs(path: str) -> list[tuple[str, str]]:
    raw = read(path)
    pairs: list[tuple[str, str]] = []
    for _speaker, _state_quote, state, _text_quote, text, _next_quote, _next_state in ENTRY_RE.findall(raw):
        normalized_text = " ".join(text.split())
        pairs.append((state, normalized_text))
    return pairs


def test_ambient_entries_precede_known_generic_fallbacks() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    for first, second in CRITICAL_ORDER_PAIRS:
        assert_before(order, first, second)


def test_immersion_files_do_not_duplicate_state_text_pairs() -> None:
    seen: dict[tuple[str, str], list[str]] = defaultdict(list)
    for path in IMMERSION_FILES:
        for state, text in extract_state_text_pairs(path):
            if text and "Warning: This line" not in text:
                seen[(state, text)].append(path)

    duplicates = {
        key: paths
        for key, paths in seen.items()
        if len(paths) > 1
    }
    assert not duplicates, f"duplicate dialogue state/text pairs: {duplicates}"


def test_core_ambient_scripts_remain_o1_and_reg0_guarded() -> None:
    scripts = read("src/scripts/ZY_helper_scripts/sod_dialogue_immersion.py")
    for script_name in [
        "sod_store_lord_first_line_to_s12",
        "sod_store_mayor_social_weather_to_s12",
        "sod_store_village_elder_social_weather_to_s12",
        "sod_store_goods_merchant_social_weather_to_s12",
        "sod_store_tavernkeeper_social_weather_to_s12",
        "sod_store_guild_master_social_weather_to_s12",
        "sod_store_nonplayer_patrol_first_line_to_s12",
    ]:
        start = scripts.index(f'("{script_name}"')
        next_script = scripts.find('\n("', start + 1)
        body = scripts[start:] if next_script == -1 else scripts[start:next_script]
        assert "(assign, reg0, 0)" in body, f"{script_name} should default reg0 to 0"
        assert "(assign, reg0, 1)" in body, f"{script_name} should set reg0 only when a line is valid"
        assert "try_for_parties" not in body
        assert "try_for_agents" not in body
        assert "try_for_range" not in body


if __name__ == "__main__":
    test_ambient_entries_precede_known_generic_fallbacks()
    test_immersion_files_do_not_duplicate_state_text_pairs()
    test_core_ambient_scripts_remain_o1_and_reg0_guarded()
    print("test_dialogue_immersion_order_safety_static: OK")
