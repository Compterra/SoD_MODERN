# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
except Exception:
    assign = "assign"
    reg0 = "reg0"

from typing import Any

from src.quests.quest_runtime_bridge import (
    build_constant,
    debug_print,
    emit_dialogue_memory,
    get_value,
    normalise_payload,
    set_value,
)


def sod_quest_event_dispatch(*args: Any, **kwargs: Any) -> dict[str, Any]:
    event_kind = kwargs.get("event_kind") or kwargs.get("event")
    if event_kind is None and args:
        event_kind = get_value(args[0], "event_kind", "event", default=None)

    payload = normalise_payload(
        event_kind if event_kind is not None else build_constant("sod_quest_event_update", "sod_quest_event_update"),
        args,
        kwargs,
    )

    source = args[0] if args else get_value(kwargs, "context", "payload", default=None)
    if source is not None:
        set_value(source, "event_kind", payload.get("event_kind"))
        set_value(source, "event", payload.get("event_kind"))
        set_value(source, "state", payload.get("state"))
        set_value(source, "outcome", payload.get("outcome"))

    debug_print(payload)
    if payload.get("quest_id") is not None:
        emit_dialogue_memory(payload.get("event_kind"), args, kwargs)
    return payload


def script_sod_quest_event_dispatch(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return sod_quest_event_dispatch(*args, **kwargs)


SCRIPT = script_sod_quest_event_dispatch
SCRIPTS = [
    (
        "sod_quest_event_dispatch",
        [
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "sod_quest_event_dispatch",
    "script_sod_quest_event_dispatch",
    "SCRIPT",
    "SCRIPTS",
]
