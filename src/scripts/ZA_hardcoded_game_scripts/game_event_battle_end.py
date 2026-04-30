"""Compatibility forwarding for the engine battle-end hook."""

from typing import Any

SCRIPTS = [
    ("game_event_battle_end", []),
]

from src.scripts.ZG_quests.sod_quest_battle_advance_action import (
    _dispatch_battle_event,
    resolve_battle_objective,
)


def _extract_context(args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    runtime = kwargs.get("runtime")
    quest_id = kwargs.get("quest_id")
    stage_id = kwargs.get("stage_id")
    event = kwargs.get("event")
    objective = kwargs.get("objective")

    positional = list(args)
    if runtime is None and positional:
        runtime = positional.pop(0)
    if quest_id is None and positional:
        quest_id = positional.pop(0)
    if stage_id is None and positional:
        stage_id = positional.pop(0)
    if event is None and positional:
        event = positional.pop(0)
    if objective is None and positional:
        objective = positional.pop(0)

    return {
        "runtime": runtime,
        "quest_id": quest_id,
        "stage_id": stage_id,
        "event": event,
        "objective": objective,
    }


def script_game_event_battle_end(*args: Any, **kwargs: Any) -> None:
    context = _extract_context(args, kwargs)
    event = context["event"]
    if event is None:
        event = _dispatch_battle_event(
            context["runtime"],
            "battle_ended",
            quest_id=context["quest_id"],
            stage_id=context["stage_id"],
            payload={},
        )
    resolve_battle_objective(
        runtime=context["runtime"],
        quest_id=context["quest_id"],
        stage_id=context["stage_id"],
        event=event,
        objective=context["objective"],
    )


def game_event_battle_end(*args: Any, **kwargs: Any) -> None:
    script_game_event_battle_end(*args, **kwargs)


__all__ = [
    "game_event_battle_end",
    "script_game_event_battle_end",
]
