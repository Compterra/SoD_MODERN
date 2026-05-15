from __future__ import annotations

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


COMPANION_COUNT = 16
COMPANION_STRING_SUFFIXES = (
    "intro",
    "intro_response_1",
    "intro_response_2",
    "backstory_a",
    "backstory_b",
    "backstory_c",
    "backstory_later",
    "backstory_response_1",
    "backstory_response_2",
    "signup",
    "signup_2",
    "signup_response_1",
    "signup_response_2",
    "payment",
    "payment_response",
    "morality_speech",
    "2ary_morality_speech",
    "personalityclash_speech",
    "personalityclash_speech_b",
    "personalityclash2_speech",
    "personalityclash2_speech_b",
    "personalitymatch_speech",
    "personalitymatch_speech_b",
    "retirement_speech",
    "rehire_speech",
    "home_intro",
    "home_description",
    "home_description_2",
    "home_recap",
    "honorific",
)


def _generated_string_ids() -> list[str]:
    sys.modules.pop("module_strings", None)
    module_strings = importlib.import_module("module_strings")
    return [
        f"str_{convert_to_identifier(entry[0])}"
        for entry in module_strings.strings
    ]


def test_companion_slot_string_table_matches_initializer_stride() -> None:
    ids = _generated_string_ids()
    start = ids.index("str_npc1_intro")
    expected = [
        f"str_npc{npc_no}_{suffix}"
        for suffix in COMPANION_STRING_SUFFIXES
        for npc_no in range(1, COMPANION_COUNT + 1)
    ]
    actual = ids[start : start + len(expected)]

    assert actual == expected
