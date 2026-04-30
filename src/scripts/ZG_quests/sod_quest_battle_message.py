"""Table-driven battle objective messaging helpers."""

from typing import Any

SCRIPTS = [
    ("sod_quest_battle_message", []),
]

from src.scripts.ZG_quests.sod_quest_battle_advance_action import (
    _maybe_write_note,
    load_battle_state,
    normalize_action_kind,
    format_battle_objective_message,
)


def _extract_context(args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
    runtime = kwargs.get("runtime")
    quest_id = kwargs.get("quest_id")
    stage_id = kwargs.get("stage_id")
    event = kwargs.get("event")
    objective = kwargs.get("objective")
    status = kwargs.get("status", "active")
    action_kind = kwargs.get("action_kind")

    positional = list(args)
    if runtime is None and positional:
        runtime = positional.pop(0)
    if quest_id is None and positional:
        quest_id = positional.pop(0)
    if stage_id is None and positional:
        stage_id = positional.pop(0)
    if action_kind is None and positional:
        action_kind = positional.pop(0)
    if event is None and positional:
        event = positional.pop(0)
    if objective is None and positional:
        objective = positional.pop(0)

    return {
        "runtime": runtime,
        "quest_id": quest_id,
        "stage_id": stage_id,
        "action_kind": action_kind,
        "event": event,
        "objective": objective,
        "status": status,
    }


def script_sod_quest_battle_message(*args: Any, **kwargs: Any) -> str:
    context = _extract_context(args, kwargs)
    state = load_battle_state(
        runtime=context["runtime"],
        quest_id=context["quest_id"],
        stage_id=context["stage_id"],
        objective=context["objective"],
        event=context["event"],
    )
    if context["action_kind"] is not None:
        state = state.__class__(
            quest_id=state.quest_id,
            stage_id=state.stage_id,
            action_kind=normalize_action_kind(context["action_kind"]),
            target_troop=state.target_troop,
            target_party=state.target_party,
            required=state.required,
            progress=state.progress,
            timer_start=state.timer_start,
            timer_duration=state.timer_duration,
            flags=state.flags,
            source=state.source,
            source_line=state.source_line,
            payload=state.payload,
        )

    message = format_battle_objective_message(state, status=context["status"])
    if context["runtime"] is not None and context["quest_id"] is not None:
        _maybe_write_note(context["runtime"], context["quest_id"], message)
    return message


__all__ = [
    "format_battle_objective_message",
    "script_sod_quest_battle_message",
]
