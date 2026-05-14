# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
except Exception:
    assign = "assign"
    reg0 = "reg0"

from typing import Any

from src.quests.quest_runtime_bridge import first_source, initialise_runtime_defaults


def sod_quest_runtime_init_metadata(*args: Any, **kwargs: Any) -> Any:
    source = first_source(args, kwargs)
    initialise_runtime_defaults(source)
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
