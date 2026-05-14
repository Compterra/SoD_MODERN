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
    emit_dialogue_memory,
    first_source,
    get_value,
    has_stage_or_progress_changed,
    normalise_payload,
    set_default,
    set_value,
)


def sod_quest_runtime_update(*args: Any, **kwargs: Any) -> dict[str, Any]:
    source = first_source(args, kwargs)
    event_kind = build_constant("sod_quest_event_update", "sod_quest_event_update")
    if source is not None:
        set_value(source, "event_kind", event_kind)
        set_value(source, "event", event_kind)
        set_default(source, "interaction_count", get_value(source, "interaction_count", default=0) or 0)
        set_value(source, "state", get_value(source, "state", default="active") or "active")
        set_value(source, "quest_state", get_value(source, "quest_state", default="active") or "active")

    should_refresh = source is not None and has_stage_or_progress_changed(source)
    force_refresh = bool(kwargs.get("force_refresh") or kwargs.get("refresh_memory"))
    if should_refresh or force_refresh:
        set_value(source, "outcome", "updated")
        return emit_dialogue_memory(
            event_kind,
            args,
            kwargs,
            state=get_value(source, "state", default="active") if source is not None else "active",
            outcome="updated",
        )

    return normalise_payload(
        event_kind,
        args,
        kwargs,
        state=get_value(source, "state", default="active") if source is not None else "active",
        outcome=get_value(source, "outcome", default="updated"),
    )


def script_sod_quest_runtime_update(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return sod_quest_runtime_update(*args, **kwargs)


SCRIPT = script_sod_quest_runtime_update
SCRIPTS = [
    (
        "sod_quest_runtime_update",
        [
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "sod_quest_runtime_update",
    "script_sod_quest_runtime_update",
    "SCRIPT",
    "SCRIPTS",
]
