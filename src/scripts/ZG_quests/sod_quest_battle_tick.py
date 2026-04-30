"""Battle tick hook used to advance timed battle objectives."""

from typing import Any, Dict

SCRIPTS = [
    ("sod_quest_battle_tick", []),
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
    delta = kwargs.get("delta", kwargs.get("amount", 1))

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
    if positional and delta == 1:
        delta = positional.pop(0)

    return {
        "runtime": runtime,
        "quest_id": quest_id,
        "stage_id": stage_id,
        "event": event,
        "objective": objective,
        "delta": delta,
    }


def _runtime_time_payload(runtime: Any) -> Dict[str, Any]:
    for attr in (
        "battle_time",
        "mission_time",
        "time",
        "elapsed_time",
        "current_time",
        "mission_elapsed_time",
    ):
        if runtime is not None and hasattr(runtime, attr):
            value = getattr(runtime, attr)
            if value is not None:
                return {"elapsed": value}
    return {}


def script_sod_quest_battle_tick(*args: Any, **kwargs: Any) -> None:
    context = _extract_context(args, kwargs)
    event = context["event"]
    if event is None:
        event = _dispatch_battle_event(
            context["runtime"],
            "battle_tick",
            quest_id=context["quest_id"],
            stage_id=context["stage_id"],
            payload=_runtime_time_payload(context["runtime"]),
        )
    resolve_battle_objective(
        runtime=context["runtime"],
        quest_id=context["quest_id"],
        stage_id=context["stage_id"],
        event=event,
        objective=context["objective"],
        delta=context["delta"],
    )


__all__ = [
    "script_sod_quest_battle_tick",
]
