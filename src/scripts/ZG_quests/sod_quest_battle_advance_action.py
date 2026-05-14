# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
except Exception:
    assign = "assign"
    reg0 = "reg0"

from collections.abc import Mapping
from typing import Any

from src.quests.quest_runtime_bridge import (
    build_constant,
    emit_dialogue_memory,
    first_source,
    get_value,
    normalise_payload,
    set_value,
)


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _classify_objective(payload: Mapping[str, Any]) -> dict[str, Any]:
    objective_kind = payload.get("objective_kind") or payload.get("objective_type") or payload.get("battle_objective")
    battle_action = payload.get("battle_action") or payload.get("action")
    if objective_kind is None:
        objective_kind = battle_action

    phase = payload.get("phase") or payload.get("battle_phase")
    if phase is None:
        if payload.get("pre_battle"):
            phase = "pre"
        elif payload.get("post_battle"):
            phase = "post"
        else:
            phase = "mid"

    state = payload.get("state") or payload.get("objective_state")
    outcome = payload.get("outcome") or payload.get("objective_result") or payload.get("result")

    if outcome is None:
        if state in ("completed", "complete", "success", "won", "victory"):
            outcome = "completed"
        elif state in ("failed", "fail", "defeat", "lost"):
            outcome = "failed"
        else:
            outcome = "progress"

    event_kind = payload.get("event_kind") or payload.get("event")
    if event_kind is None:
        if outcome == "completed":
            event_kind = build_constant("sod_quest_event_battle_complete", "sod_quest_event_battle_complete")
        elif outcome == "failed":
            event_kind = build_constant("sod_quest_event_battle_fail", "sod_quest_event_battle_fail")
        else:
            event_kind = build_constant("sod_quest_event_battle_progress", "sod_quest_event_battle_progress")

    return {
        "event_kind": event_kind,
        "objective_kind": _coerce_text(objective_kind),
        "battle_action": _coerce_text(battle_action or objective_kind),
        "phase": _coerce_text(phase),
        "state": _coerce_text(state or ("completed" if outcome == "completed" else "active")),
        "outcome": _coerce_text(outcome),
    }


def resolve_battle_objective(*args: Any, **kwargs: Any) -> dict[str, Any]:
    source = first_source(args, kwargs)
    payload = normalise_payload(
        kwargs.get("event_kind")
        or kwargs.get("event")
        or build_constant("sod_quest_event_battle_progress", "sod_quest_event_battle_progress"),
        args,
        kwargs,
    )
    if source is not None:
        payload.setdefault("objective_kind", get_value(source, "objective_kind", "objective_type", "battle_objective", default=None))
        payload.setdefault("battle_action", get_value(source, "battle_action", "action", default=None))
        payload.setdefault("objective_state", get_value(source, "objective_state", default=None))
        payload.setdefault("objective_result", get_value(source, "objective_result", default=None))
        payload.setdefault("phase", get_value(source, "phase", "battle_phase", default=None))
    classification = _classify_objective(payload)
    payload.update(classification)
    return payload


def script_sod_quest_battle_advance_action(*args: Any, **kwargs: Any) -> dict[str, Any]:
    payload = resolve_battle_objective(*args, **kwargs)
    source = first_source(args, kwargs)
    if source is not None:
        set_value(source, "event_kind", payload.get("event_kind"))
        set_value(source, "event", payload.get("event_kind"))
        set_value(source, "battle_action", payload.get("battle_action"))
        set_value(source, "state", payload.get("state"))
        set_value(source, "outcome", payload.get("outcome"))
    if payload.get("quest_id") is not None:
        emit_dialogue_memory(
            payload.get("event_kind"),
            args,
            {**kwargs, **payload},
            state=payload.get("state"),
            outcome=payload.get("outcome"),
        )
    return payload


def sod_quest_battle_advance_action(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return script_sod_quest_battle_advance_action(*args, **kwargs)


SCRIPT = script_sod_quest_battle_advance_action
SCRIPTS = [
    (
        "sod_quest_battle_advance_action",
        [
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "resolve_battle_objective",
    "script_sod_quest_battle_advance_action",
    "sod_quest_battle_advance_action",
    "SCRIPT",
    "SCRIPTS",
]
