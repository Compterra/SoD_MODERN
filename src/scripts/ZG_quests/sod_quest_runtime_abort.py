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

import inspect
from collections.abc import Mapping, MutableMapping
from typing import Any

from src.constants import module_constants as mc


_CONTEXT_KEYS = (
    "quest_id",
    "stage_id",
    "chain_id",
    "event_kind",
    "event",
    "actor_no",
    "party_no",
    "center_no",
    "battle_action",
    "outcome",
    "state",
    "day",
    "interaction_count",
    "progress",
    "memory_age",
    "freshness",
    "result",
)


def _build_constant(name: str, default: Any) -> Any:
    return getattr(mc, name, default)


def _get_value(source: Any, *names: str, default: Any = None) -> Any:
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


def _set_value(target: Any, name: str, value: Any) -> None:
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


def _set_default(target: Any, name: str, value: Any) -> None:
    if target is None:
        return

    if isinstance(target, MutableMapping):
        target.setdefault(name, value)
        return

    if getattr(target, name, None) is None:
        _set_value(target, name, value)


def _first_source(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    for candidate in args:
        if candidate is not None:
            return candidate

    for key in ("context", "payload", "quest", "state", "data"):
        candidate = kwargs.get(key)
        if candidate is not None:
            return candidate

    return None


def _normalise_payload(
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

        for name in _CONTEXT_KEYS:
            value = _get_value(source, name, default=None)
            if value is not None and name not in payload:
                payload[name] = value

        nested = _get_value(source, "payload", default=None)
        if isinstance(nested, Mapping):
            payload.update(nested)

    payload.setdefault("event_kind", event_kind)
    payload.setdefault("event", payload.get("event_kind"))
    if state is not None:
        payload.setdefault("state", state)
    if outcome is not None:
        payload.setdefault("outcome", outcome)

    if payload.get("quest_id") is None:
        payload["quest_id"] = _get_value(payload, "quest_id", "quest", default=None)
    if payload.get("stage_id") is None:
        payload["stage_id"] = _get_value(payload, "stage_id", "stage", default=None)
    if payload.get("actor_no") is None:
        payload["actor_no"] = _get_value(payload, "actor_no", "actor", default=None)
    if payload.get("party_no") is None:
        payload["party_no"] = _get_value(payload, "party_no", "party", default=None)
    if payload.get("center_no") is None:
        payload["center_no"] = _get_value(payload, "center_no", "center", default=None)
    if payload.get("battle_action") is None:
        payload["battle_action"] = _get_value(payload, "battle_action", "action", default=None)
    if payload.get("day") is None:
        payload["day"] = _get_value(payload, "day", "event_day", default=None)
    if payload.get("interaction_count") is None:
        payload["interaction_count"] = _get_value(payload, "interaction_count", "count", default=None)
    if payload.get("progress") is None:
        payload["progress"] = _get_value(payload, "progress", "stage_progress", default=None)

    return payload


def _call_best_effort(func: Any, payload: Mapping[str, Any]) -> Any:
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
            parameter.kind in (
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


def _emit_dialogue_memory(
    event_kind: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    state: Any = None,
    outcome: Any = None,
) -> dict[str, Any]:
    payload = _normalise_payload(event_kind, args, kwargs, state=state, outcome=outcome)

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
        _call_best_effort(record_event, payload)

    return payload


def sod_quest_runtime_abort(*args: Any, **kwargs: Any) -> dict[str, Any]:
    source = _first_source(args, kwargs)
    event_kind = _build_constant("sod_quest_event_abort", "sod_quest_event_abort")
    if source is not None:
        _set_value(source, "event_kind", event_kind)
        _set_value(source, "event", event_kind)
        _set_value(source, "state", "aborted")
        _set_value(source, "quest_state", "aborted")
        _set_value(source, "outcome", "aborted")
        _set_default(source, "interaction_count", _get_value(source, "interaction_count", default=0) or 0)

    payload = _emit_dialogue_memory(
        event_kind,
        args,
        kwargs,
        state="aborted",
        outcome="aborted",
    )
    return payload


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
