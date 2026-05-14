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
    dispatch_event_payload,
    emit_dialogue_memory,
    first_source,
    get_value,
    normalise_payload,
    set_value,
)


def sod_quest_dispatch_active_event(*args: Any, **kwargs: Any) -> dict[str, Any]:
    source = first_source(args, kwargs)
    event_kind = get_value(source, "event_kind", "event", default=None)
    if event_kind is None and kwargs:
        event_kind = kwargs.get("event_kind") or kwargs.get("event")

    if source is not None:
        set_value(source, "event_kind", event_kind)
        set_value(source, "event", event_kind)

    payload = normalise_payload(
        event_kind if event_kind is not None else build_constant("sod_quest_event_active", "sod_quest_event_active"),
        args,
        kwargs,
        state=get_value(source, "state", default=None) if source is not None else None,
        outcome=get_value(source, "outcome", default=None) if source is not None else None,
    )

    dispatched = dispatch_event_payload(payload)
    if dispatched is None and payload.get("quest_id") is not None:
        emit_dialogue_memory(payload.get("event_kind"), args, kwargs)

    return payload


def script_sod_quest_dispatch_active_event(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return sod_quest_dispatch_active_event(*args, **kwargs)


SCRIPT = script_sod_quest_dispatch_active_event
SCRIPTS = [
    (
        "sod_quest_dispatch_active_event",
        [
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "sod_quest_dispatch_active_event",
    "script_sod_quest_dispatch_active_event",
    "SCRIPT",
    "SCRIPTS",
]
