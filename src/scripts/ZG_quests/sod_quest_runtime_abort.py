# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
    from module_constants import *  # type: ignore
except Exception:
    store_script_param = "store_script_param"
    quest_set_slot = "quest_set_slot"
    assign = "assign"
    reg0 = "reg0"
    slot_quest_current_state = "slot_quest_current_state"

from typing import Any

from src.quests.quest_runtime_bridge import apply_runtime_transition


def sod_quest_runtime_abort(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return apply_runtime_transition(
        "sod_quest_event_abort",
        "sod_quest_event_abort",
        args,
        kwargs,
        state="aborted",
        quest_state="aborted",
        outcome="aborted",
    )


def script_sod_quest_runtime_abort(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return sod_quest_runtime_abort(*args, **kwargs)


SCRIPT = script_sod_quest_runtime_abort
SCRIPTS = [
    (
        "sod_quest_runtime_abort",
        [
            (store_script_param, ":quest_no", 1),
            (quest_set_slot, ":quest_no", slot_quest_current_state, 4),
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "sod_quest_runtime_abort",
    "script_sod_quest_runtime_abort",
    "SCRIPT",
    "SCRIPTS",
]
