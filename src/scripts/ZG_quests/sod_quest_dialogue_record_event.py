# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
except Exception:
    str_store_string = "str_store_string"
    assign = "assign"
    reg0 = "reg0"
    s4 = "s4"

from typing import Any, Dict, Mapping, Tuple

from src.constants import module_constants as mc
from src.scripts.ZG_quests.sod_quest_dialogue_read_memory import (
    QuestMemorySnapshot,
    _apply_registers,
    _build_snapshot,
    _coerce_int,
    _detect_target,
    _extract_source,
    _merge_args_with_kwargs,
    _normalize_event_kind,
    _normalize_state_label,
    _normalize_text,
    _resolve_current_day,
    _resolve_slot,
    _summary_text,
    _write_slots,
)

__all__ = [
    "script_sod_quest_dialogue_record_event",
    "SCRIPT",
    "SCRIPTS",
]


def _resolve_record_event_kind(snapshot: QuestMemorySnapshot, kwargs: Mapping[str, Any]) -> str:
    explicit = kwargs.get("event_kind", kwargs.get("event", kwargs.get("kind")))
    event_kind = _normalize_event_kind(explicit)
    if event_kind:
        return event_kind

    outcome = _normalize_text(kwargs.get("outcome", snapshot.outcome), "").lower()
    quest_state = _normalize_text(kwargs.get("quest_state", kwargs.get("state", snapshot.quest_state)), "").lower()

    if outcome in {"complete", "completed", "success"} or "complete" in quest_state:
        return "complete"
    if outcome in {"fail", "failed", "failure"} or "fail" in quest_state:
        return "fail"
    if outcome in {"abort", "aborted", "expired"} or "abort" in quest_state:
        return "abort"
    if outcome == "abandoned" or "abandon" in quest_state:
        return "abandon"
    if outcome in {"accept", "active", "ongoing", "pending"} or "accept" in quest_state:
        return "accept"
    if "stage" in quest_state or quest_state in {"update", "updating"}:
        return "update"
    return "update"


def _determine_next_count(snapshot: QuestMemorySnapshot, kwargs: Mapping[str, Any]) -> int:
    previous_count = _coerce_int(snapshot.interaction_count, 0)
    provided_count = None
    for name in ("interaction_count", "interactions", "count", "memory_count"):
        if name in kwargs and kwargs[name] is not None:
            provided_count = _coerce_int(kwargs[name], 0)
            break

    if provided_count is None:
        return previous_count + 1

    return max(previous_count + 1, provided_count)


def _resolve_outcome(event_kind: str, snapshot: QuestMemorySnapshot, kwargs: Mapping[str, Any]) -> str:
    explicit = kwargs.get("outcome", kwargs.get("result", snapshot.outcome))
    if explicit is not None:
        text = _normalize_text(explicit, "")
        if text:
            return text

    if event_kind == "complete":
        return "completed"
    if event_kind == "fail":
        return "failed"
    if event_kind == "abort":
        return "aborted"
    if event_kind == "abandon":
        return "abandoned"
    if event_kind == "accept":
        return "active"
    return snapshot.classification or "active"


def _state_constant(label: str, default: int = 0) -> int:
    value = getattr(mc, f"sod_quest_state_{label}", default)
    return value if isinstance(value, int) else default


def _resolve_state(event_kind: str, snapshot: QuestMemorySnapshot, kwargs: Mapping[str, Any]) -> int:
    explicit_state = kwargs.get("quest_state", kwargs.get("state", None))
    if explicit_state is not None:
        normalized_label = _normalize_state_label(explicit_state)
        if normalized_label:
            return _state_constant(normalized_label, _coerce_int(snapshot.quest_state, 0))
        return _coerce_int(explicit_state, _coerce_int(snapshot.quest_state, 0))

    state_hint = _coerce_int(snapshot.quest_state, 0)
    if state_hint:
        return state_hint

    normalized_event = _normalize_event_kind(event_kind)
    if normalized_event == "complete":
        return _state_constant("completed", state_hint)
    if normalized_event == "fail":
        return _state_constant("failed", state_hint)
    if normalized_event == "abort":
        return _state_constant("aborted", state_hint)
    if normalized_event == "abandon":
        return _state_constant("expired", state_hint)
    if normalized_event in {"accept", "update", "repeat"}:
        return _state_constant("active", state_hint)
    return state_hint


def _build_record_snapshot(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> QuestMemorySnapshot:
    snapshot = _build_snapshot(args, kwargs)
    event_kind = _resolve_record_event_kind(snapshot, kwargs)
    interaction_count = _determine_next_count(snapshot, kwargs)

    source = _extract_source(args, kwargs)
    merged = _merge_args_with_kwargs(args, kwargs)

    day = snapshot.day
    current_day = _resolve_current_day(source, merged)
    if not day and current_day is not None:
        day = current_day

    outcome = _resolve_outcome(event_kind, snapshot, kwargs)
    quest_state = _resolve_state(event_kind, snapshot, kwargs)

    updated = QuestMemorySnapshot(
        quest_state=quest_state,
        stage_id=snapshot.stage_id,
        chain_id=snapshot.chain_id,
        event_kind=event_kind,
        actor_no=snapshot.actor_no,
        battle_action=snapshot.battle_action,
        quest_id=kwargs.get("quest_id", kwargs.get("quest", kwargs.get("quest_no", snapshot.quest_id))),
        outcome=outcome,
        day=day,
        interaction_count=interaction_count,
        memory_age=snapshot.memory_age,
    )
    if current_day is not None and day:
        updated.memory_age = max(current_day - day, 0)
    return updated


def script_sod_quest_dialogue_record_event(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    target = _detect_target(args, kwargs)
    snapshot = _build_record_snapshot(args, kwargs)
    text = _summary_text(snapshot)

    register_values = {
        "reg0": snapshot.quest_state,
        "reg1": snapshot.stage_id,
        "reg2": snapshot.chain_id,
        "reg3": _normalize_event_kind(snapshot.event_kind) or snapshot.event_kind,
        "reg4": snapshot.actor_no,
        "reg5": snapshot.battle_action,
        "reg6": snapshot.quest_id,
        "reg7": _normalize_state_label(snapshot.outcome) or snapshot.outcome or snapshot.classification,
        "reg8": snapshot.day,
        "reg9": snapshot.memory_age if snapshot.memory_age is not None else snapshot.interaction_count,
        "s4": text,
    }

    _apply_registers(target, register_values)
    if hasattr(target, "s4"):
        try:
            setattr(target, "s4", text)
        except Exception:
            pass

    _write_slots(target, snapshot)

    result = snapshot.to_dict()
    result["s4"] = text
    result.update(register_values)
    return result


SCRIPT = script_sod_quest_dialogue_record_event
SCRIPTS = [
    (
        "sod_quest_dialogue_record_event",
        [
            (str_store_string, s4, "@The quest memory has been updated."),
            (assign, reg0, 1),
        ],
    )
]
