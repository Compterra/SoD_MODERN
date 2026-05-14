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
    slot_quest_giver_troop = "slot_quest_giver_troop"

from typing import Any

from src.quests.quest_runtime_bridge import apply_runtime_transition


def sod_quest_runtime_accept(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return apply_runtime_transition(
        "sod_quest_event_accept",
        "sod_quest_event_accept",
        args,
        kwargs,
        state="active",
        quest_state="active",
        outcome="accepted",
    )


def script_sod_quest_runtime_accept(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return sod_quest_runtime_accept(*args, **kwargs)


SCRIPT = script_sod_quest_runtime_accept
SCRIPTS = [
    (
        "sod_quest_runtime_accept",
        [
            (store_script_param, ":quest_no", 1),
            (store_script_param, ":giver_troop_no", 2),
            (quest_set_slot, ":quest_no", slot_quest_current_state, 1),
            (quest_set_slot, ":quest_no", slot_quest_giver_troop, ":giver_troop_no"),
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "sod_quest_runtime_accept",
    "script_sod_quest_runtime_accept",
    "SCRIPT",
    "SCRIPTS",
]
