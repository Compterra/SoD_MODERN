# -*- coding: utf-8 -*-
from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
    from module_constants import *  # type: ignore
except Exception:
    str_store_string = "str_store_string"
    assign = "assign"
    reg0 = "reg0"
    s4 = "s4"

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence, Tuple

import src.constants.module_constants as mc

__all__ = [
    "QuestMemorySnapshot",
    "read_quest_memory",
    "summarize_quest_memory",
    "quest_memory_context",
    "describe_quest_memory",
    "read_memory_context",
    "script_sod_quest_dialogue_read_memory",
    "SCRIPT",
    "SCRIPTS",
]


@dataclass(slots=True)
class QuestMemorySnapshot:
    quest_state: Any = 0
    stage_id: Any = 0
    chain_id: Any = 0
    event_kind: Any = ""
    actor_no: Any = 0
    battle_action: Any = 0
    quest_id: Any = 0
    outcome: Any = ""
    day: Any = 0
    interaction_count: Any = 0
    memory_age: Optional[int] = None
    freshness: str = "fresh"
    classification: str = "active"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


_POSitional_FIELD_ORDER = (
    "quest_state",
    "stage_id",
    "chain_id",
    "event_kind",
    "actor_no",
    "battle_action",
    "quest_id",
    "outcome",
    "day",
    "interaction_count",
    "current_day",
)

_SLOT_CANDIDATES = {
    "quest_id": (
        "slot_troop_sod_quest_memory_quest",
        "slot_troop_sod_quest_dialogue_memory_quest_id",
        "slot_troop_sod_quest_memory_quest_id",
        "slot_quest_sod_memory_quest_id",
        "slot_troop_sod_quest_memory_last_quest_id",
        "slot_troop_sod_quest_dialogue_last_quest_id",
    ),
    "quest_state": (
        "slot_troop_sod_quest_memory_state",
        "slot_troop_sod_quest_dialogue_memory_state",
        "slot_troop_sod_quest_memory_last_state",
        "slot_quest_sod_memory_state",
    ),
    "stage_id": (
        "slot_troop_sod_quest_memory_stage",
        "slot_troop_sod_quest_dialogue_memory_stage",
        "slot_troop_sod_quest_memory_last_stage",
        "slot_quest_sod_memory_stage",
    ),
    "chain_id": (
        "slot_troop_sod_quest_memory_chain",
        "slot_troop_sod_quest_dialogue_memory_chain",
        "slot_quest_sod_memory_chain",
    ),
    "event_kind": (
        "slot_troop_sod_quest_memory_event",
        "slot_troop_sod_quest_dialogue_memory_event",
        "slot_quest_sod_memory_event",
    ),
    "outcome": (
        "slot_troop_sod_quest_memory_outcome",
        "slot_troop_sod_quest_dialogue_memory_outcome",
        "slot_quest_sod_memory_outcome",
    ),
    "day": (
        "slot_troop_sod_quest_memory_day",
        "slot_troop_sod_quest_dialogue_memory_day",
        "slot_quest_sod_memory_day",
    ),
    "actor_no": (
        "slot_troop_sod_quest_memory_actor",
        "slot_troop_sod_quest_dialogue_memory_actor",
        "slot_quest_sod_memory_actor",
    ),
    "battle_action": (
        "slot_troop_sod_quest_memory_battle_action",
        "slot_troop_sod_quest_dialogue_memory_battle_action",
        "slot_quest_sod_memory_battle_action",
    ),
    "interaction_count": (
        "slot_troop_sod_quest_memory_interactions",
        "slot_troop_sod_quest_dialogue_memory_interaction_count",
        "slot_troop_sod_quest_memory_interaction_count",
        "slot_quest_sod_memory_interaction_count",
    ),
}

_MEMORY_SOURCE_KEYS = (
    "quest_memory",
    "quest_memory_snapshot",
    "quest_memory_data",
    "quest_memory_state",
    "quest_memory_record",
    "memory_context",
    "memory",
    "last_quest_memory",
    "snapshot",
    "record",
    "state_snapshot",
)

_MEMORY_CONTAINER_KEYS = (
    "slots",
    "memory_slots",
    "quest_slots",
    "npc_slots",
    "slot_values",
)

_MEMORY_FIELD_ALIASES = {
    "quest_id": (
        "quest_id",
        "last_quest_id",
        "quest",
        "last_quest",
        "quest_name",
        "slot_quest_id",
        "slot_last_quest_id",
        "quest_memory_quest_id",
    ),
    "stage_id": (
        "stage_id",
        "last_stage_id",
        "stage",
        "last_stage",
        "quest_stage_id",
        "slot_stage_id",
        "slot_last_stage_id",
        "quest_memory_stage_id",
    ),
    "event_kind": (
        "event_kind",
        "event_type",
        "last_event_kind",
        "last_event_type",
        "event",
        "last_event",
        "kind",
        "action",
        "slot_event_kind",
        "slot_last_event_kind",
        "quest_memory_event_kind",
        "quest_memory_event_type",
    ),
    "actor_no": (
        "actor_no",
        "actor_id",
        "last_actor_no",
        "last_actor_id",
        "actor",
        "speaker",
        "npc_id",
        "agent_id",
        "slot_actor_no",
        "slot_last_actor_no",
        "quest_memory_actor_no",
        "quest_memory_actor_id",
    ),
    "day": (
        "day",
        "last_day",
        "quest_day",
        "recorded_day",
        "memory_day",
        "calendar_day",
        "slot_day",
        "slot_last_day",
        "quest_memory_day",
    ),
    "chain_id": (
        "chain_id",
        "last_chain_id",
        "chain",
        "quest_chain",
        "quest_chain_id",
        "slot_chain_id",
        "slot_last_chain_id",
        "quest_memory_chain_id",
    ),
    "tags": (
        "tags",
        "memory_tags",
        "quest_tags",
        "slot_tags",
        "slot_memory_tags",
        "quest_memory_tags",
    ),
    "freshness": (
        "freshness",
        "memory_freshness",
        "age_label",
        "slot_freshness",
        "quest_memory_freshness",
    ),
    "age_days": (
        "age_days",
        "memory_age_days",
        "age",
        "days_old",
        "slot_age_days",
        "quest_memory_age_days",
    ),
    "classification": (
        "classification",
        "memory_classification",
        "quest_classification",
    ),
    "summary": (
        "summary",
        "memory_summary",
        "s4",
        "text",
        "line",
        "message",
    ),
}

_INFERRED_TAGS_BY_EVENT = {
    "accept": ("quest_accepted",),
    "update": ("quest_updated",),
    "repeat": ("quest_repeat",),
    "complete": ("quest_completed",),
    "fail": ("quest_failed",),
    "abort": ("quest_aborted",),
    "abandon": ("quest_abandoned",),
}

_INFERRED_TAGS_BY_CLASSIFICATION = {
    "completed": ("quest_completed",),
    "failed": ("quest_failed",),
    "aborted": ("quest_aborted",),
    "abandoned": ("quest_abandoned",),
}

_INFERRED_TAGS_BY_OUTCOME = {
    "completed": ("quest_completed",),
    "failed": ("quest_failed",),
    "aborted": ("quest_aborted",),
    "abandoned": ("quest_abandoned",),
}

_INFERRED_TAGS_BY_STATE = {
    "completed": ("quest_completed",),
    "failed": ("quest_failed",),
    "aborted": ("quest_aborted",),
    "expired": ("quest_abandoned",),
    "active": ("quest_active",),
    "offered": ("quest_offered",),
    "accepted": ("quest_accepted",),
    "stage_complete": ("quest_stage_complete",),
}

_INFERRED_FRESHNESS_TAGS = {
    "fresh": ("quest_memory_fresh",),
    "recent": ("quest_memory_recent",),
    "stale": ("quest_memory_stale",),
    "old": ("quest_memory_old",),
    "current": ("quest_memory_current",),
}

_EVENT_ALIASES = {
    "accept": "accept",
    "accepted": "accept",
    "complete": "complete",
    "completed": "complete",
    "success": "complete",
    "fail": "fail",
    "failed": "fail",
    "failure": "fail",
    "abort": "abort",
    "aborted": "abort",
    "expire": "abort",
    "expired": "abort",
    "abandon": "abandon",
    "abandoned": "abandon",
    "update": "update",
    "updated": "update",
    "stage_change": "update",
    "stage-changed": "update",
    "repeat": "repeat",
}

_EVENT_KIND_VALUES = {
    getattr(mc, "sod_quest_event_accept", 1): "accept",
    getattr(mc, "sod_quest_event_update", 2): "update",
    getattr(mc, "sod_quest_event_complete", 3): "complete",
    getattr(mc, "sod_quest_event_fail", 4): "fail",
    getattr(mc, "sod_quest_event_abort", 5): "abort",
    getattr(mc, "sod_quest_event_stage_enter", 6): "update",
    getattr(mc, "sod_quest_event_stage_complete", 7): "complete",
    getattr(mc, "sod_quest_event_battle_start", 8): "update",
    getattr(mc, "sod_quest_event_battle_update", 9): "update",
    getattr(mc, "sod_quest_event_battle_end", 10): "complete",
    getattr(mc, "sod_quest_event_map_conversation", 11): "update",
    getattr(mc, "sod_quest_event_camp_conversation", 12): "update",
    getattr(mc, "sod_quest_event_dialogue", 13): "update",
    getattr(mc, "sod_quest_event_mission", 14): "update",
    getattr(mc, "sod_quest_event_trigger", 15): "update",
    getattr(mc, "sod_quest_event_battle", 16): "update",
    getattr(mc, "sod_quest_event_map_encounter", 17): "update",
    getattr(mc, "sod_quest_event_center_visit", 18): "update",
    getattr(mc, "sod_quest_event_party_movement", 19): "update",
    getattr(mc, "sod_quest_event_time_passed", 20): "update",
    getattr(mc, "sod_quest_event_agent_defeated", 21): "update",
    getattr(mc, "sod_quest_event_prisoner_freed", 22): "complete",
    getattr(mc, "sod_quest_event_wave_progress", 23): "update",
    getattr(mc, "sod_quest_event_position_held", 24): "complete",
}

_STATE_LABEL_VALUES = {
    getattr(mc, "sod_quest_state_inactive", 0): "inactive",
    getattr(mc, "sod_quest_state_offered", 1): "offered",
    getattr(mc, "sod_quest_state_accepted", 2): "accepted",
    getattr(mc, "sod_quest_state_active", 3): "active",
    getattr(mc, "sod_quest_state_paused", 4): "paused",
    getattr(mc, "sod_quest_state_stage_complete", 5): "stage_complete",
    getattr(mc, "sod_quest_state_completed", 6): "completed",
    getattr(mc, "sod_quest_state_failed", 7): "failed",
    getattr(mc, "sod_quest_state_aborted", 8): "aborted",
    getattr(mc, "sod_quest_state_expired", 9): "expired",
    getattr(mc, "sod_quest_state_hidden", 10): "hidden",
    getattr(mc, "sod_quest_state_locked", 11): "locked",
    getattr(mc, "sod_quest_state_revealed", 12): "revealed",
}


def _normalize_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        text = value.strip()
        return text if text else default
    if isinstance(value, (bytes, bytearray)):
        try:
            text = value.decode("utf-8", errors="ignore").strip()
        except Exception:
            return default
        return text if text else default
    return str(value).strip() or default


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _normalize_event_kind(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, int):
        return _EVENT_KIND_VALUES.get(value, str(value))
    text = _normalize_text(value, "")
    if not text:
        return ""
    if text.isdigit():
        return _EVENT_KIND_VALUES.get(_coerce_int(text, 0), text)
    key = text.lower().replace(" ", "_").replace("/", "_")
    if key.startswith("sod_quest_event_"):
        key = key.replace("sod_quest_event_", "")
    return _EVENT_ALIASES.get(key, _EVENT_KIND_VALUES.get(_coerce_int(text, 0), key))


def _normalize_state_label(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, int):
        return _STATE_LABEL_VALUES.get(value, str(value))
    text = _normalize_text(value, "")
    if not text:
        return ""
    if text.isdigit():
        return _STATE_LABEL_VALUES.get(_coerce_int(text, 0), text)
    key = text.lower().replace(" ", "_").replace("/", "_")
    if key.startswith("sod_quest_state_"):
        key = key.replace("sod_quest_state_", "")
    return _STATE_LABEL_VALUES.get(_coerce_int(text, 0), key)


def _is_source_candidate(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, Mapping):
        return True
    for attr_name in (
        "set_slot",
        "get_slot",
        "set_register",
        "registers",
        "s4",
        "metadata",
        "to_dict",
        "to_snapshot",
    ):
        if hasattr(value, attr_name):
            return True
    return False


def _merge_args_with_kwargs(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = dict(kwargs)
    if not args:
        return merged

    positional_offset = 1 if _is_source_candidate(args[0]) else 0
    for index, name in enumerate(_POSitional_FIELD_ORDER, start=positional_offset):
        if index < len(args) and name not in merged and args[index] is not None:
            merged[name] = args[index]
    return merged


def _get_mapping_value(source: Any, key: str, default: Any = None) -> Any:
    if source is None:
        return default
    if isinstance(source, Mapping) and key in source:
        return source[key]
    if hasattr(source, key):
        return getattr(source, key)
    return default


def _get_first(source: Any, names: Sequence[str], default: Any = None) -> Any:
    for name in names:
        value = _get_mapping_value(source, name, None)
        if value is not None:
            return value
    return default


def _resolve_slot(name: str) -> Optional[int]:
    for candidate in _SLOT_CANDIDATES.get(name, ()):
        value = getattr(mc, candidate, None)
        if isinstance(value, int):
            return value
    return None


def _source_to_mapping(source: Any) -> Mapping[str, Any] | None:
    if isinstance(source, Mapping):
        return source
    if hasattr(source, "to_snapshot"):
        try:
            snapshot = source.to_snapshot()
        except Exception:
            snapshot = None
        if isinstance(snapshot, Mapping):
            return snapshot
    if hasattr(source, "to_dict"):
        try:
            snapshot = source.to_dict()
        except Exception:
            snapshot = None
        if isinstance(snapshot, Mapping):
            return snapshot
    if hasattr(source, "__dict__"):
        try:
            return vars(source)
        except Exception:
            return None
    return None


def _source_values(source: Any) -> list[Any]:
    values: list[Any] = []
    if source is None:
        return values
    if isinstance(source, Sequence) and not isinstance(source, (str, bytes, bytearray, Mapping)):
        for item in source:
            values.extend(_source_values(item))
        return values
    values.append(source)
    mapping = _source_to_mapping(source)
    if mapping is None:
        return values

    for key in _MEMORY_SOURCE_KEYS + _MEMORY_CONTAINER_KEYS + ("metadata", "narrative", "npc_state", "world_context", "quest", "stage"):
        value = mapping.get(key)
        if value is not None:
            values.append(value)
    return values


def _extract_source(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> Any:
    for key in (
        "memory",
        "quest_memory",
        "context",
        "state",
        "record",
        "source",
        "target",
        "memory_target",
        "record_target",
        "troop",
        "npc_state",
        "npc",
        "quest",
        "stage",
        "giver_troop",
        "speaker_troop",
    ):
        value = kwargs.get(key)
        if value is not None:
            return value
    if args and _is_source_candidate(args[0]):
        return args[0]
    return None


def _extract_int(source: Any, merged: Mapping[str, Any], names: Sequence[str], default: int = 0) -> int:
    for name in names:
        if name in merged and merged[name] is not None:
            return _coerce_int(merged[name], default)
    value = _get_first(source, names, None)
    return _coerce_int(value, default)


def _extract_value(source: Any, merged: Mapping[str, Any], names: Sequence[str], default: Any = None) -> Any:
    for name in names:
        if name in merged and merged[name] is not None:
            return merged[name]
    value = _get_first(source, names, None)
    if value is None:
        return default
    return value


def _extract_text(source: Any, merged: Mapping[str, Any], names: Sequence[str], default: str = "") -> str:
    for name in names:
        if name in merged and merged[name] is not None:
            return _normalize_text(merged[name], default)
    value = _get_first(source, names, None)
    return _normalize_text(value, default)


def _resolve_current_day(source: Any, merged: Mapping[str, Any]) -> Optional[int]:
    candidates = (
        "current_day",
        "campaign_day",
        "world_day",
        "day",
        "event_day",
        "time_day",
    )
    for name in candidates:
        if name in merged and merged[name] is not None:
            return _coerce_int(merged[name], 0)
    value = _get_first(source, candidates, None)
    if value is None:
        return None
    return _coerce_int(value, 0)


def _classify_snapshot(snapshot: QuestMemorySnapshot) -> QuestMemorySnapshot:
    event_kind = _normalize_event_kind(snapshot.event_kind)
    outcome = _normalize_state_label(snapshot.outcome)
    quest_state_label = _normalize_state_label(snapshot.quest_state)

    classification = "active"
    if event_kind == "complete" or outcome == "completed" or quest_state_label == "completed":
        classification = "completed"
    elif event_kind == "fail" or outcome == "failed" or quest_state_label == "failed":
        classification = "failed"
    elif event_kind == "abort" or outcome in {"aborted", "expired"} or quest_state_label in {"aborted", "expired"}:
        classification = "aborted"
    elif event_kind == "abandon" or outcome == "abandoned" or quest_state_label == "abandoned":
        classification = "abandoned"
    elif event_kind in {"accept", "update", "repeat"} or quest_state_label in {"active", "offered", "accepted", "paused", "stage_complete", "revealed", "locked"}:
        classification = "active"
    elif snapshot.quest_id:
        classification = "active"
    else:
        classification = "stale"

    freshness = "fresh"
    if snapshot.memory_age is not None:
        if snapshot.memory_age <= 0:
            freshness = "current"
        elif snapshot.memory_age == 1:
            freshness = "fresh"
        elif snapshot.memory_age <= 3:
            freshness = "recent"
        elif snapshot.memory_age <= 7:
            freshness = "stale"
        else:
            freshness = "old"
    elif classification in {"completed", "failed", "aborted", "abandoned"}:
        freshness = classification

    snapshot.classification = classification
    snapshot.freshness = freshness
    return snapshot


def _build_snapshot(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> QuestMemorySnapshot:
    merged = _merge_args_with_kwargs(args, kwargs)
    source = _extract_source(args, kwargs)

    quest_state = _extract_value(source, merged, ("quest_state", "state", "memory_state", "current_state"), 0)
    stage_id = _extract_value(source, merged, ("stage_id", "stage", "stage_no", "memory_stage"), 0)
    chain_id = _extract_value(source, merged, ("chain_id", "chain", "chain_no", "quest_chain"), 0)
    event_kind = _extract_value(source, merged, ("event_kind", "event_type", "event", "kind", "memory_event"), "")
    actor_no = _extract_int(source, merged, ("actor_no", "actor_id", "actor", "npc_no", "troop_no"), 0)
    battle_action = _extract_int(source, merged, ("battle_action", "battle", "action"), 0)
    quest_id = _extract_value(source, merged, ("quest_id", "quest", "quest_no", "memory_quest_id"), 0)
    outcome = _extract_value(source, merged, ("outcome", "result", "memory_outcome", "state_label"), "")
    day = _extract_int(source, merged, ("day", "cur_day", "memory_day", "event_day"), 0)
    interaction_count = _extract_int(source, merged, ("interaction_count", "interactions", "count", "memory_count"), 0)

    current_day = _resolve_current_day(source, merged)
    memory_age: Optional[int] = None
    if day and current_day is not None:
        memory_age = max(current_day - day, 0)

    snapshot = QuestMemorySnapshot(
        quest_state=quest_state,
        stage_id=stage_id,
        chain_id=chain_id,
        event_kind=_normalize_event_kind(event_kind),
        actor_no=actor_no,
        battle_action=battle_action,
        quest_id=quest_id,
        outcome=outcome or _normalize_text(quest_state, ""),
        day=day,
        interaction_count=interaction_count,
        memory_age=memory_age,
    )
    return _classify_snapshot(snapshot)


def _summary_text(snapshot: QuestMemorySnapshot) -> str:
    quest_label = f"quest {snapshot.quest_id}" if snapshot.quest_id else "the matter at hand"
    stage_label = f"stage {snapshot.stage_id}" if snapshot.stage_id else ""
    event_kind = _normalize_event_kind(snapshot.event_kind)
    state_phrases = {
        "completed": "is remembered as complete",
        "failed": "is remembered as a setback",
        "aborted": "was cut short",
        "abandoned": "was left unfinished",
        "stale": "has gone quiet",
    }
    event_phrases = {
        "accept": "has been taken up",
        "update": "has moved forward",
        "complete": "has been brought to a close",
        "fail": "has gone badly",
        "abort": "has been cut short",
        "abandon": "has been left unfinished",
        "repeat": "has returned to mind",
    }
    opening = state_phrases.get(snapshot.classification, event_phrases.get(event_kind, "still stirs in memory"))
    parts = [f"{quest_label} {opening}"]
    if stage_label:
        parts.append(f"at {stage_label}")
    outcome_label = _normalize_state_label(snapshot.outcome) or _normalize_text(snapshot.outcome, "")
    if outcome_label and outcome_label not in {"active", "unknown"}:
        parts.append(f"outcome {outcome_label}")
    if snapshot.day:
        parts.append(f"last noted on day {snapshot.day}")
    if snapshot.memory_age is not None:
        if snapshot.memory_age == 0:
            parts.append("still fresh")
        elif snapshot.memory_age == 1:
            parts.append("remembered from yesterday")
        else:
            parts.append(f"remembered {snapshot.memory_age} days ago")
    else:
        parts.append(snapshot.freshness.replace("_", " "))
    if snapshot.interaction_count:
        parts.append(f"spoken of {snapshot.interaction_count} times")
    return ", ".join(parts) + "."


def _apply_registers(target: Any, values: Mapping[str, Any]) -> None:
    if target is None:
        return

    if hasattr(target, "set_register"):
        setter = getattr(target, "set_register")
        for key, value in values.items():
            try:
                setter(key, value)
            except TypeError:
                setter(key, value, None)
        return

    registers = getattr(target, "registers", None)
    if isinstance(registers, MutableMapping):
        registers.update(values)
        return

    if isinstance(target, MutableMapping):
        target.update(values)
        return

    for key, value in values.items():
        try:
            setattr(target, key, value)
        except Exception:
            pass


def _write_slots(target: Any, snapshot: QuestMemorySnapshot) -> None:
    if target is None or not hasattr(target, "set_slot"):
        return

    slot_values = {
        "quest_id": snapshot.quest_id,
        "quest_state": snapshot.quest_state,
        "stage_id": snapshot.stage_id,
        "chain_id": snapshot.chain_id,
        "event_kind": snapshot.event_kind,
        "outcome": snapshot.outcome,
        "day": snapshot.day,
        "actor_no": snapshot.actor_no,
        "battle_action": snapshot.battle_action,
        "interaction_count": snapshot.interaction_count,
    }
    setter = getattr(target, "set_slot")
    for name, value in slot_values.items():
        slot_id = _resolve_slot(name)
        if slot_id is None:
            continue
        try:
            setter(slot_id, value)
        except TypeError:
            setter(slot_id, value, 0)


def _detect_target(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> Any:
    for key in ("target", "memory_target", "record_target", "troop", "context", "state", "source", "npc_state", "npc"):
        value = kwargs.get(key)
        if value is not None:
            return value
    if args and _is_source_candidate(args[0]):
        return args[0]
    return None


def _normalize_tag_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, Mapping):
        collected: list[str] = []
        for key in ("tags", "memory_tags", "quest_tags", "values", "items"):
            collected.extend(_normalize_tag_values(value.get(key)))
        return _unique_texts(collected)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        collected: list[str] = []
        for item in value:
            collected.extend(_normalize_tag_values(item))
        return _unique_texts(collected)
    text = _normalize_text(value, "")
    return [text] if text else []


def _unique_texts(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = _normalize_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _read_slot_value(source: Any, field_name: str) -> Any:
    slot_id = _resolve_slot(field_name)
    if slot_id is None:
        return None

    getter = getattr(source, "get_slot", None)
    if callable(getter):
        try:
            value = getter(slot_id)
        except TypeError:
            try:
                value = getter(slot_id, 0)
            except Exception:
                value = None
        except Exception:
            value = None
        if value not in (None, ""):
            return value

    mapping = _source_to_mapping(source)
    if isinstance(mapping, Mapping):
        for candidate_key in (slot_id, str(slot_id)):
            if candidate_key in mapping and mapping[candidate_key] not in (None, ""):
                return mapping[candidate_key]
        for container_key in _MEMORY_CONTAINER_KEYS:
            container = mapping.get(container_key)
            if isinstance(container, Mapping):
                for candidate_key in (slot_id, str(slot_id), field_name):
                    if candidate_key in container and container[candidate_key] not in (None, ""):
                        return container[candidate_key]
    return None


def _find_field_value(source: Any, field_name: str) -> Any:
    aliases = _MEMORY_FIELD_ALIASES.get(field_name, (field_name,))
    candidates = _source_values(source)
    for candidate in candidates:
        mapping = _source_to_mapping(candidate)
        if mapping is not None:
            for alias in aliases:
                if alias in mapping and mapping[alias] not in (None, ""):
                    return mapping[alias]
            metadata = mapping.get("metadata")
            if isinstance(metadata, Mapping):
                for alias in aliases:
                    if alias in metadata and metadata[alias] not in (None, ""):
                        return metadata[alias]
            narrative = mapping.get("narrative")
            if isinstance(narrative, Mapping):
                for alias in aliases:
                    if alias in narrative and narrative[alias] not in (None, ""):
                        return narrative[alias]
        for alias in aliases:
            if hasattr(candidate, alias):
                value = getattr(candidate, alias)
                if value not in (None, ""):
                    return value
        slot_value = _read_slot_value(candidate, field_name)
        if slot_value not in (None, ""):
            return slot_value
    return None


def _lookup_nested_metadata(source: Any, *names: str) -> Any:
    candidates = _source_values(source)
    for candidate in candidates:
        mapping = _source_to_mapping(candidate)
        if mapping is None:
            continue
        direct = mapping
        for name in names:
            if isinstance(direct, Mapping) and name in direct and direct[name] not in (None, ""):
                return direct[name]
        metadata = mapping.get("metadata")
        if isinstance(metadata, Mapping):
            for name in names:
                if name in metadata and metadata[name] not in (None, ""):
                    return metadata[name]
        narrative = mapping.get("narrative")
        if isinstance(narrative, Mapping):
            for name in names:
                if name in narrative and narrative[name] not in (None, ""):
                    return narrative[name]
            nested = narrative.get("narrative")
            if isinstance(nested, Mapping):
                for name in names:
                    if name in nested and nested[name] not in (None, ""):
                        return nested[name]
    return None


def _collect_source_tags(source: Any) -> list[str]:
    tags: list[str] = []
    candidates = _source_values(source)
    for candidate in candidates:
        mapping = _source_to_mapping(candidate)
        if mapping is None:
            continue
        for key in ("tags", "memory_tags", "quest_tags"):
            tags.extend(_normalize_tag_values(mapping.get(key)))
        metadata = mapping.get("metadata")
        if isinstance(metadata, Mapping):
            for key in ("tags", "memory_tags", "quest_tags", "narrative.memory_tags"):
                tags.extend(_normalize_tag_values(metadata.get(key)))
            narrative = metadata.get("narrative")
            if isinstance(narrative, Mapping):
                for key in ("memory_tags", "tags", "quest_tags"):
                    tags.extend(_normalize_tag_values(narrative.get(key)))
                nested = narrative.get("narrative")
                if isinstance(nested, Mapping):
                    for key in ("memory_tags", "tags", "quest_tags"):
                        tags.extend(_normalize_tag_values(nested.get(key)))
        narrative = mapping.get("narrative")
        if isinstance(narrative, Mapping):
            for key in ("memory_tags", "tags", "quest_tags"):
                tags.extend(_normalize_tag_values(narrative.get(key)))
    return _unique_texts(tags)


def _infer_memory_tags(memory: Mapping[str, Any]) -> list[str]:
    tags: list[str] = []
    for key, inferred in (
        ("event_kind", _INFERRED_TAGS_BY_EVENT),
        ("classification", _INFERRED_TAGS_BY_CLASSIFICATION),
        ("outcome", _INFERRED_TAGS_BY_OUTCOME),
        ("quest_state_label", _INFERRED_TAGS_BY_STATE),
    ):
        label = _normalize_text(memory.get(key), "").lower()
        if not label:
            continue
        if key == "quest_state_label":
            label = _normalize_state_label(memory.get("quest_state")).lower()
        tags.extend(inferred.get(label, ()))

    freshness = _normalize_text(memory.get("freshness"), "").lower()
    if freshness:
        tags.extend(_INFERRED_FRESHNESS_TAGS.get(freshness, ()))

    quest_id = _normalize_text(memory.get("quest_id"))
    if quest_id:
        tags.append(f"quest_{quest_id}")
    stage_id = _normalize_text(memory.get("stage_id"))
    if stage_id:
        tags.append(f"stage_{stage_id}")
    chain_id = _normalize_text(memory.get("chain_id"))
    if chain_id:
        tags.append(f"chain_{chain_id}")

    return _unique_texts(tags)


def _resolve_summary(memory: Mapping[str, Any]) -> str:
    summary = _normalize_text(memory.get("summary") or memory.get("memory_summary"))
    if summary:
        return summary
    return _format_summary(memory)


def _format_summary(memory: Mapping[str, Any]) -> str:
    quest_id = _normalize_text(memory.get("quest_id"))
    stage_id = _normalize_text(memory.get("stage_id"))
    event_kind = _normalize_event_kind(memory.get("event_kind"))
    classification = _normalize_text(memory.get("classification"), "").lower()
    outcome = _normalize_state_label(memory.get("outcome")) or _normalize_text(memory.get("outcome"), "")
    day = _coerce_int(memory.get("day"))
    raw_age = memory.get("age_days")
    if raw_age is None:
        raw_age = memory.get("memory_age")
    age_days = None if raw_age is None else _coerce_int(raw_age, 0)
    freshness = _normalize_text(memory.get("freshness"))
    interaction_count = _coerce_int(memory.get("interaction_count"), 0)

    state_phrases = {
        "completed": "is remembered as complete",
        "failed": "is remembered as a setback",
        "aborted": "was cut short",
        "abandoned": "was left unfinished",
        "stale": "has gone quiet",
    }
    event_phrases = {
        "accept": "has been taken up",
        "update": "has moved forward",
        "complete": "has been brought to a close",
        "fail": "has gone badly",
        "abort": "has been cut short",
        "abandon": "has been left unfinished",
        "repeat": "has returned to mind",
    }

    quest_label = f"quest {quest_id}" if quest_id else "the matter at hand"
    stage_label = f"stage {stage_id}" if stage_id else ""
    opening = state_phrases.get(classification, event_phrases.get(event_kind, "still stirs in memory"))

    parts: list[str] = [f"{quest_label} {opening}"]
    if stage_label:
        parts.append(f"at {stage_label}")
    if outcome and outcome not in {"active", "unknown"}:
        parts.append(f"outcome {outcome}")
    if day:
        parts.append(f"last noted on day {day}")
    if age_days is not None:
        if age_days == 0:
            parts.append("still fresh")
        elif age_days == 1:
            parts.append("remembered from yesterday")
        else:
            parts.append(f"remembered {age_days} days ago")
    elif freshness:
        parts.append(freshness.replace("_", " "))
    if interaction_count:
        parts.append(f"spoken of {interaction_count} times")

    return ", ".join(parts) + "."


def _resolve_memory_snapshot(npc_state_or_snapshot: Any, *, context: Mapping[str, Any] | None = None, world_context: Any = None) -> Dict[str, Any]:
    sources = _source_values(npc_state_or_snapshot)
    if context is not None:
        sources.append(context)
    if world_context is not None:
        sources.append(world_context)

    raw: Dict[str, Any] = {}
    raw["quest_id"] = _find_field_value(sources, "quest_id")
    raw["stage_id"] = _find_field_value(sources, "stage_id")
    raw["event_kind"] = _find_field_value(sources, "event_kind")
    raw["event_type"] = raw["event_kind"]
    raw["actor_no"] = _find_field_value(sources, "actor_no")
    raw["actor_id"] = raw["actor_no"]
    raw["day"] = _find_field_value(sources, "day")
    raw["chain_id"] = _find_field_value(sources, "chain_id")
    raw["quest_state"] = _find_field_value(sources, "quest_state")
    raw["outcome"] = _find_field_value(sources, "outcome")
    raw["interaction_count"] = _find_field_value(sources, "interaction_count")
    raw["memory_age"] = _find_field_value(sources, "age_days")
    raw["freshness"] = _find_field_value(sources, "freshness")
    raw["classification"] = _find_field_value(sources, "classification")
    raw["summary"] = _find_field_value(sources, "summary")

    quest_state_label = _normalize_state_label(raw.get("quest_state"))
    event_kind = _normalize_event_kind(raw.get("event_kind"))
    outcome = _normalize_state_label(raw.get("outcome"))
    classification = _normalize_text(raw.get("classification"), "").lower()

    if not classification:
        if event_kind == "complete" or outcome == "completed" or quest_state_label == "completed":
            classification = "completed"
        elif event_kind == "fail" or outcome == "failed" or quest_state_label == "failed":
            classification = "failed"
        elif event_kind == "abort" or outcome in {"aborted", "expired"} or quest_state_label in {"aborted", "expired"}:
            classification = "aborted"
        elif event_kind == "abandon" or outcome == "abandoned" or quest_state_label == "abandoned":
            classification = "abandoned"
        else:
            classification = "active"

    raw["quest_state_label"] = quest_state_label
    raw["classification"] = classification or "active"

    day = _coerce_int(raw.get("day"), 0)
    age_days = _coerce_int(raw.get("memory_age"), None if raw.get("memory_age") is None else 0)
    world_day = _find_field_value(sources, "world_day")
    if age_days in (None, 0) and day and world_day is not None:
        try:
            age_days = max(_coerce_int(world_day, day) - day, 0)
        except Exception:
            age_days = None
    if age_days is None and day and context is not None:
        current_day = _find_field_value([context], "day")
        if current_day is not None:
            try:
                age_days = max(_coerce_int(current_day, day) - day, 0)
            except Exception:
                age_days = None

    raw["age_days"] = age_days
    raw["memory_age"] = age_days
    raw["freshness"] = _normalize_text(raw.get("freshness"), "")
    if not raw["freshness"]:
        if age_days is None:
            raw["freshness"] = "unknown"
        elif age_days <= 0:
            raw["freshness"] = "current"
        elif age_days == 1:
            raw["freshness"] = "fresh"
        elif age_days <= 3:
            raw["freshness"] = "recent"
        elif age_days <= 7:
            raw["freshness"] = "stale"
        else:
            raw["freshness"] = "old"

    raw["tags"] = _collect_source_tags(sources)
    if not raw["tags"]:
        raw["tags"] = _infer_memory_tags(raw)
    else:
        inferred = _infer_memory_tags(raw)
        raw["tags"] = _unique_texts([*raw["tags"], *inferred])

    raw["memory_tags"] = list(raw["tags"])
    raw["summary"] = _resolve_summary(raw)

    raw["last_quest_id"] = _normalize_text(raw.get("quest_id"))
    raw["last_stage_id"] = _normalize_text(raw.get("stage_id"))
    raw["last_event_kind"] = _normalize_text(raw.get("event_kind"))
    raw["last_event_type"] = raw["last_event_kind"]
    raw["last_actor_no"] = _normalize_text(raw.get("actor_no"))
    raw["last_actor_id"] = raw["last_actor_no"]
    raw["last_day"] = _coerce_int(raw.get("day"), 0)
    raw["last_chain_id"] = _normalize_text(raw.get("chain_id"))
    raw["last_age_days"] = _coerce_int(raw.get("age_days"), 0) if raw.get("age_days") is not None else None

    return raw


def read_quest_memory(*args: Any, default: Any = None, **kwargs: Any) -> Dict[str, Any]:
    """Decode a quest memory snapshot from an NPC state object or mapping."""

    npc_state_or_snapshot = args[0] if args else kwargs.get("npc_state_or_snapshot")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("npc_state")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("snapshot")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("memory")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("quest_memory")

    context = kwargs.get("context")
    world_context = kwargs.get("world_context")

    memory = _resolve_memory_snapshot(npc_state_or_snapshot, context=context, world_context=world_context)
    if not memory:
        if isinstance(default, Mapping):
            return dict(default)
        return {}

    return memory


def summarize_quest_memory(*args: Any, default: str = "", **kwargs: Any) -> str:
    """Render quest memory as a concise line of dialogue text."""

    if args and isinstance(args[0], Mapping) and any(
        key in args[0]
        for key in ("quest_id", "stage_id", "event_kind", "event_type", "summary", "memory_tags")
    ):
        memory = dict(args[0])
    else:
        memory = read_quest_memory(*args, **kwargs)

    if not memory:
        return default

    summary = _resolve_summary(memory)
    return summary or default


def quest_memory_context(*args: Any, world_context: Any = None, default: Any = None, **kwargs: Any) -> Dict[str, Any]:
    """Build a serialisable memory context for later dialogue helpers."""

    npc_state_or_snapshot = args[0] if args else kwargs.get("npc_state_or_snapshot")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("npc_state")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("snapshot")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("memory")
    if npc_state_or_snapshot is None:
        npc_state_or_snapshot = kwargs.get("quest_memory")

    if world_context is None:
        world_context = kwargs.get("world_context")

    if default is None:
        default = {}

    memory = read_quest_memory(
        npc_state_or_snapshot,
        context=kwargs.get("context"),
        world_context=world_context,
        default=default,
    )
    if not memory:
        if isinstance(default, Mapping):
            context = dict(default)
            context.setdefault("quest_memory", {})
            context.setdefault("memory_tags", [])
            context.setdefault("tags", [])
            return context
        return {}

    context: Dict[str, Any] = dict(memory)
    context["quest_memory"] = dict(memory)
    context["quest_id"] = _normalize_text(memory.get("quest_id"))
    context["stage_id"] = _normalize_text(memory.get("stage_id"))
    context["event_kind"] = _normalize_text(memory.get("event_kind"))
    context["event_type"] = _normalize_text(memory.get("event_type") or memory.get("event_kind"))
    context["actor_no"] = _normalize_text(memory.get("actor_no"))
    context["actor_id"] = context["actor_no"]
    context["day"] = memory.get("day")
    context["chain_id"] = _normalize_text(memory.get("chain_id"))
    context["age_days"] = memory.get("age_days")
    context["memory_age"] = memory.get("memory_age")
    context["freshness"] = _normalize_text(memory.get("freshness"), "unknown")
    context["classification"] = _normalize_text(memory.get("classification"), "active")
    context["summary"] = _resolve_summary(memory)
    context["tags"] = list(memory.get("tags", []))
    context["memory_tags"] = list(context["tags"])

    if isinstance(world_context, Mapping):
        context["world_context"] = dict(world_context)
    elif world_context is not None and hasattr(world_context, "to_snapshot"):
        try:
            world_snapshot = world_context.to_snapshot()
        except Exception:
            world_snapshot = None
        if isinstance(world_snapshot, Mapping):
            context["world_context"] = dict(world_snapshot)
    elif world_context is not None and hasattr(world_context, "__dict__"):
        try:
            context["world_context"] = dict(vars(world_context))
        except Exception:
            pass

    world_day = _find_field_value(world_context, "day")
    if world_day is not None:
        context["world_day"] = world_day

    for key in ("location_id", "location_name", "center_id", "party_id", "region", "personality", "chain_id"):
        value = _find_field_value(world_context, key)
        if value not in (None, ""):
            context[key] = value

    # Preserve common aliases that later dialogue helpers expect.
    context["last_quest_id"] = memory.get("last_quest_id", context["quest_id"])
    context["last_stage_id"] = memory.get("last_stage_id", context["stage_id"])
    context["last_event_kind"] = memory.get("last_event_kind", context["event_kind"])
    context["last_event_type"] = memory.get("last_event_type", context["event_type"])
    context["last_actor_no"] = memory.get("last_actor_no", context["actor_no"])
    context["last_actor_id"] = memory.get("last_actor_id", context["actor_id"])
    context["last_day"] = memory.get("last_day", context["day"])
    context["last_chain_id"] = memory.get("last_chain_id", context["chain_id"])
    context["last_age_days"] = memory.get("last_age_days", context["age_days"])

    return context


describe_quest_memory = summarize_quest_memory
read_memory_context = quest_memory_context


def script_sod_quest_dialogue_read_memory(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    target = _detect_target(args, kwargs)
    snapshot = _build_snapshot(args, kwargs)
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


SCRIPT = script_sod_quest_dialogue_read_memory
SCRIPTS = [
        (
            "sod_quest_dialogue_read_memory",
            [
                (str_store_string, s4, "@The matter at hand still stirs in memory."),
                (assign, reg0, 1),
            ],
        )
]
