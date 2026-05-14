# -*- coding: utf-8 -*-
"""Shared adapter glue between authored quest specs and MB script fragments.

The quest framework has both Python-side authoring/runtime tests and generated
Mount & Blade script stubs. This module keeps the Python adapter behavior in
one place so accept/update/complete/fail/event wrappers do not each carry their
own payload normalizer and dialogue-memory dispatch copy.
"""
from __future__ import annotations

import inspect
from collections.abc import Mapping, MutableMapping
from typing import Any

from src.constants import module_constants as mc


CONTEXT_KEYS = (
    "quest_id",
    "stage_id",
    "chain_id",
    "event_kind",
    "event",
    "actor_no",
    "party_no",
    "center_no",
    "battle_action",
    "battle_objective",
    "objective_kind",
    "objective_type",
    "objective_state",
    "outcome",
    "state",
    "quest_state",
    "day",
    "interaction_count",
    "progress",
    "memory_age",
    "freshness",
    "result",
    "previous_stage_id",
    "old_stage_id",
    "from_stage_id",
    "previous_progress",
    "old_progress",
    "from_progress",
    "phase",
    "battle_phase",
    "pre_battle",
    "mid_battle",
    "post_battle",
    "objective_result",
)

RUNTIME_DEFAULTS = {
    "quest_id": None,
    "stage_id": None,
    "chain_id": None,
    "event_kind": None,
    "event": None,
    "actor_no": None,
    "party_no": None,
    "center_no": None,
    "battle_action": None,
    "outcome": None,
    "state": "inactive",
    "day": 0,
    "interaction_count": 0,
    "progress": 0,
    "memory_age": 0,
    "freshness": "fresh",
}


def build_constant(name: str, default: Any) -> Any:
    return getattr(mc, name, default)


def get_value(source: Any, *names: str, default: Any = None) -> Any:
    if source is None:
        return default

    if isinstance(source, Mapping):
        for name in names:
            if name in source:
                return source[name]

    for name in names:
        if hasattr(source, name):
            return getattr(source, name)

    metadata = getattr(source, "metadata", None)
    if isinstance(metadata, Mapping):
        for name in names:
            if name in metadata:
                return metadata[name]

    return default


def set_value(target: Any, name: str, value: Any) -> None:
    if target is None:
        return

    if isinstance(target, MutableMapping):
        target[name] = value
        return

    try:
        setattr(target, name, value)
        return
    except Exception:
        pass

    metadata = getattr(target, "metadata", None)
    if isinstance(metadata, MutableMapping):
        metadata[name] = value


def set_default(target: Any, name: str, value: Any) -> None:
    if target is None:
        return

    if isinstance(target, MutableMapping):
        target.setdefault(name, value)
        return

    if getattr(target, name, None) is None:
        set_value(target, name, value)


def initialise_runtime_defaults(target: Any) -> None:
    if target is None:
        return

    for key, value in RUNTIME_DEFAULTS.items():
        set_default(target, key, value)

    metadata = getattr(target, "metadata", None)
    if isinstance(metadata, MutableMapping):
        metadata.setdefault("narrative.initialised", True)
        metadata.setdefault("narrative.memory_age", 0)
        metadata.setdefault("narrative.freshness", "fresh")


def first_source(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    for candidate in args:
        if candidate is not None:
            return candidate

    for key in ("context", "payload", "quest", "state", "data"):
        candidate = kwargs.get(key)
        if candidate is not None:
            return candidate

    return None


def normalise_payload(
    event_kind: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    state: Any = None,
    outcome: Any = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {}

    for source in args + (kwargs,):
        if source is None:
            continue

        if isinstance(source, Mapping):
            payload.update(source)
            nested = source.get("payload")
            if isinstance(nested, Mapping):
                payload.update(nested)
            continue

        for name in CONTEXT_KEYS:
            value = get_value(source, name, default=None)
            if value is not None and name not in payload:
                payload[name] = value

        nested = get_value(source, "payload", default=None)
        if isinstance(nested, Mapping):
            payload.update(nested)

    payload.setdefault("event_kind", event_kind)
    payload.setdefault("event", payload.get("event_kind"))
    if state is not None:
        payload.setdefault("state", state)
    if outcome is not None:
        payload.setdefault("outcome", outcome)

    aliases = (
        ("quest_id", ("quest",)),
        ("stage_id", ("stage",)),
        ("actor_no", ("actor",)),
        ("party_no", ("party",)),
        ("center_no", ("center",)),
        ("battle_action", ("action",)),
        ("day", ("event_day",)),
        ("interaction_count", ("count",)),
        ("progress", ("stage_progress",)),
        ("phase", ("battle_phase",)),
        ("objective_kind", ("objective_type", "battle_objective")),
        ("objective_result", ("result",)),
    )
    for canonical, alternates in aliases:
        if payload.get(canonical) is None:
            payload[canonical] = get_value(payload, canonical, *alternates, default=None)

    return payload


# American spelling alias for new code that naturally asks for "normalize".
normalize_payload = normalise_payload


def call_best_effort(func: Any, payload: Mapping[str, Any]) -> Any:
    attempts = []
    try:
        signature = inspect.signature(func)
    except (TypeError, ValueError):
        signature = None

    accepts_kwargs = True
    accepts_positional = True
    if signature is not None:
        parameters = tuple(signature.parameters.values())
        accepts_kwargs = any(parameter.kind == inspect.Parameter.VAR_KEYWORD for parameter in parameters)
        accepts_positional = any(
            parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.VAR_POSITIONAL,
            )
            for parameter in parameters
        )

    if accepts_kwargs:
        attempts.append(lambda: func(**payload))
    if accepts_positional:
        attempts.append(lambda: func(dict(payload)))
        attempts.append(lambda: func(dict(payload), **payload))
    attempts.append(lambda: func())

    for attempt in attempts:
        try:
            return attempt()
        except TypeError:
            continue

    return None


def emit_dialogue_memory(
    event_kind: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    state: Any = None,
    outcome: Any = None,
) -> dict[str, Any]:
    payload = normalise_payload(event_kind, args, kwargs, state=state, outcome=outcome)

    try:
        from src.scripts.ZG_quests.sod_quest_dialogue_record_event import (
            sod_quest_dialogue_record_event as record_event,
        )
    except Exception:
        try:
            from src.scripts.ZG_quests.sod_quest_dialogue_record_event import (
                script_sod_quest_dialogue_record_event as record_event,
            )
        except Exception:
            record_event = None

    if record_event is not None:
        call_best_effort(record_event, payload)

    return payload


def has_stage_or_progress_changed(source: Any) -> bool:
    current_stage = get_value(source, "stage_id", "stage", default=None)
    previous_stage = get_value(source, "previous_stage_id", "old_stage_id", "from_stage_id", default=None)
    current_progress = get_value(source, "progress", "stage_progress", default=None)
    previous_progress = get_value(source, "previous_progress", "old_progress", "from_progress", default=None)

    stage_changed = previous_stage is not None and current_stage is not None and previous_stage != current_stage
    progress_changed = previous_progress is not None and current_progress is not None and previous_progress != current_progress
    return stage_changed or progress_changed


def apply_runtime_transition(
    event_constant_name: str,
    default_event_kind: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    state: Any,
    outcome: Any,
    quest_state: Any | None = None,
    emit_memory: bool = True,
) -> dict[str, Any]:
    source = first_source(args, kwargs)
    event_kind = build_constant(event_constant_name, default_event_kind)
    if source is not None:
        set_value(source, "event_kind", event_kind)
        set_value(source, "event", event_kind)
        set_value(source, "state", state)
        set_value(source, "quest_state", quest_state if quest_state is not None else state)
        set_value(source, "outcome", outcome)
        set_default(source, "interaction_count", get_value(source, "interaction_count", default=0) or 0)

    if emit_memory:
        return emit_dialogue_memory(event_kind, args, kwargs, state=state, outcome=outcome)
    return normalise_payload(event_kind, args, kwargs, state=state, outcome=outcome)


def debug_print(payload: Mapping[str, Any]) -> None:
    if not (
        payload.get("debug")
        or payload.get("show_debug")
        or payload.get("verbose")
        or payload.get("debug_display")
        or payload.get("display_debug")
    ):
        return

    summary = {
        "quest_id": payload.get("quest_id"),
        "stage_id": payload.get("stage_id"),
        "event_kind": payload.get("event_kind"),
        "state": payload.get("state"),
        "outcome": payload.get("outcome"),
    }
    print(f"[quest-event] {summary}")


def dispatch_event_payload(payload: Mapping[str, Any]) -> Any:
    try:
        from src.scripts.ZG_quests.sod_quest_event_dispatch import (
            sod_quest_event_dispatch as event_dispatch,
        )
    except Exception:
        try:
            from src.scripts.ZG_quests.sod_quest_event_dispatch import (
                script_sod_quest_event_dispatch as event_dispatch,
            )
        except Exception:
            event_dispatch = None

    if event_dispatch is None:
        return None

    try:
        return event_dispatch(dict(payload))
    except TypeError:
        try:
            return event_dispatch(**dict(payload))
        except TypeError:
            return event_dispatch()


__all__ = [
    "CONTEXT_KEYS",
    "apply_runtime_transition",
    "build_constant",
    "call_best_effort",
    "debug_print",
    "dispatch_event_payload",
    "emit_dialogue_memory",
    "first_source",
    "get_value",
    "has_stage_or_progress_changed",
    "initialise_runtime_defaults",
    "normalise_payload",
    "normalize_payload",
    "set_default",
    "set_value",
]
