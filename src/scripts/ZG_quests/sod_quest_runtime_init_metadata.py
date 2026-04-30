# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
except Exception:
    assign = "assign"
    reg0 = "reg0"

from collections.abc import Mapping, MutableMapping
from typing import Any

from src.constants import module_constants as mc


_RUNTIME_DEFAULTS = {
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


def _initialise_runtime_defaults(target: Any) -> None:
    if target is None:
        return

    for key, value in _RUNTIME_DEFAULTS.items():
        _set_default(target, key, value)

    metadata = getattr(target, "metadata", None)
    if isinstance(metadata, MutableMapping):
        metadata.setdefault("narrative.initialised", True)
        metadata.setdefault("narrative.memory_age", 0)
        metadata.setdefault("narrative.freshness", "fresh")


def sod_quest_runtime_init_metadata(*args: Any, **kwargs: Any) -> Any:
    source = _first_source(args, kwargs)
    _initialise_runtime_defaults(source)
    return source


def script_sod_quest_runtime_init_metadata(*args: Any, **kwargs: Any) -> Any:
    return sod_quest_runtime_init_metadata(*args, **kwargs)


SCRIPT = script_sod_quest_runtime_init_metadata
SCRIPTS = [
    (
        "sod_quest_runtime_init_metadata",
        [
            (assign, reg0, 1),
        ],
    )
]

__all__ = [
    "sod_quest_runtime_init_metadata",
    "script_sod_quest_runtime_init_metadata",
    "SCRIPT",
    "SCRIPTS",
]
