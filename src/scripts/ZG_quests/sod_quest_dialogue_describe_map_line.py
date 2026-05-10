"""Quest map-line resolver.

This module produces location-aware quest chatter for the live dialogue layer.
It considers quest, stage, world, and quest-memory context so map-facing lines
can react to abandonment, chain state, availability changes, and location-bound
quest progress.
"""

from __future__ import annotations

try:
    from header_common import *  # type: ignore
    from header_operations import *  # type: ignore
except Exception:
    str_store_string = "str_store_string"
    assign = "assign"
    reg0 = "reg0"
    s4 = "s4"

from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from typing import Any

from src.quests.quest_domain import QuestWorldContext

__all__ = [
    "resolve_quest_map_line",
    "resolve_map_line",
    "describe_quest_map_line",
    "describe_map_line",
    "script_sod_quest_dialogue_describe_map_line",
    "SCRIPT",
]


_GENERIC_FALLBACK_KEYS = ("default", "generic", "fallback", "neutral", "any", "other")


def _as_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "__dict__"):
        return {
            key: val
            for key, val in vars(value).items()
            if not key.startswith("_")
        }
    return {}


def _normalize_token(value: Any) -> str:
    text = "" if value is None else str(value)
    chars: list[str] = []
    last_was_separator = False
    for char in text.strip().lower():
        if char.isalnum():
            chars.append(char)
            last_was_separator = False
        elif not last_was_separator:
            chars.append("_")
            last_was_separator = True
    return "".join(chars).strip("_")


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        pieces = [_coerce_text(item) for item in value]
        return " ".join(piece for piece in pieces if piece).strip()
    return str(value).strip()


def _first_non_empty(*values: Any) -> str:
    for value in values:
        text = _coerce_text(value)
        if text:
            return text
    return ""


def _source_mapping(source: Any) -> dict[str, Any]:
    data = _as_mapping(source)
    if not data:
        return {}
    metadata = data.get("metadata")
    if isinstance(metadata, Mapping):
        return dict(metadata)
    narrative = data.get("narrative")
    if isinstance(narrative, Mapping):
        return dict(narrative)
    return data


def _get_block(source: Any, block_name: str) -> Any:
    data = _as_mapping(source)
    if not data:
        return None
    for container_name in ("metadata", "narrative"):
        container = data.get(container_name)
        if not isinstance(container, Mapping):
            continue
        if block_name in container:
            return container[block_name]
        nested = container.get("narrative")
        if isinstance(nested, Mapping) and block_name in nested:
            return nested[block_name]
    if block_name in data:
        return data[block_name]
    return None


def _get_value(source: Any, *names: str, default: Any = None) -> Any:
    data = _as_mapping(source)
    containers = [data]
    metadata = data.get("metadata")
    if isinstance(metadata, Mapping):
        containers.append(metadata)
        nested_narrative = metadata.get("narrative")
        if isinstance(nested_narrative, Mapping):
            containers.append(nested_narrative)
    narrative = data.get("narrative")
    if isinstance(narrative, Mapping):
        containers.append(narrative)
    for name in names:
        for container in containers:
            if name in container:
                return container[name]
    return default


def _select_text(spec: Any, candidates: Sequence[str]) -> str:
    if spec is None:
        return ""
    if isinstance(spec, str):
        return spec.strip()
    if isinstance(spec, Sequence) and not isinstance(spec, (bytes, bytearray, str)):
        for item in spec:
            text = _select_text(item, candidates)
            if text:
                return text
        return ""
    if isinstance(spec, Mapping):
        normalized = {_normalize_token(key): value for key, value in spec.items()}
        for candidate in candidates:
            key = _normalize_token(candidate)
            if key in normalized:
                text = _select_text(normalized[key], candidates)
                if text:
                    return text
        for fallback in _GENERIC_FALLBACK_KEYS:
            key = _normalize_token(fallback)
            if key in normalized:
                text = _select_text(normalized[key], candidates)
                if text:
                    return text
        for field in ("text", "line", "value", "response", "map_line"):
            if field in spec:
                text = _coerce_text(spec[field])
                if text:
                    return text
        if len(spec) == 1:
            return _select_text(next(iter(spec.values())), candidates)
        return ""
    if hasattr(spec, "text"):
        return _coerce_text(getattr(spec, "text"))
    return _coerce_text(spec)


def _quest_label(source: Any, fallback: str = "this quest") -> str:
    return _coerce_text(
        _get_value(source, "name", "title", "label", "quest_name", "quest_title", "id", "quest_id")
    ) or fallback


def _stage_label(source: Any, fallback: str = "this stage") -> str:
    return _coerce_text(
        _get_value(source, "name", "title", "label", "stage_name", "stage_title", "id", "stage_id")
    ) or fallback


def _location_label(source: Any) -> str:
    return _first_non_empty(
        _get_value(source, "location_name", "settlement_name", "town_name", "castle_name", "village_name"),
        _get_value(source, "location_id", "settlement_id", "map_location"),
    )


def _chain_label(*sources: Any) -> str:
    for source in sources:
        label = _first_non_empty(
            _get_value(source, "chain", "chain_id", "quest_chain", "chain_name"),
            _get_value(source, "chain_label", "quest_chain_label"),
        )
        if label:
            return label
    return ""


def _availability_label(*sources: Any) -> str:
    for source in sources:
        label = _first_non_empty(
            _get_value(source, "availability", "status", "state", "quest_state"),
            _get_value(source, "availability_state", "availability_label"),
        )
        if label:
            return _normalize_token(label)
    return ""


def _looks_like_world_context(value: Any) -> bool:
    data = _as_mapping(value)
    if not data:
        return False
    keys = {
        "location_name",
        "settlement_name",
        "town_name",
        "castle_name",
        "village_name",
        "location_id",
        "map_location",
        "availability",
        "status",
        "state",
        "availability_state",
        "location_bound",
        "requires_location",
    }
    if keys.intersection(data.keys()):
        return True
    narrative = data.get("narrative")
    return isinstance(narrative, Mapping) and bool(keys.intersection(narrative.keys()))


def _looks_like_memory_context(value: Any) -> bool:
    data = _as_mapping(value)
    if not data:
        return False
    keys = {"last_quest", "last_stage", "last_event", "last_actor", "day", "chain", "freshness", "tags", "memory_tags"}
    if keys.intersection(data.keys()):
        return True
    narrative = data.get("narrative")
    return isinstance(narrative, Mapping) and bool(keys.intersection(narrative.keys()))


def _event_kind_from_memory(event_kind: str | None, memory_context: Any) -> str:
    if event_kind:
        return _normalize_token(event_kind)
    tags = _memory_tags(memory_context)
    if "quest_completed" in tags:
        return "complete"
    if "quest_failed" in tags:
        return "fail"
    if "quest_abandoned" in tags:
        return "abandon"
    if "trust_broken" in tags:
        return "trust_broken"
    if "quest_stage_changed" in tags:
        return "stage_change"
    if "follow_up" in tags or "delayed_follow_up" in tags:
        return "delayed_follow_up"
    freshness = _normalize_token(_get_value(memory_context, "freshness", "memory_freshness", "age_state"))
    if freshness in {"stale", "old", "aged", "late", "delayed"}:
        return "delayed_follow_up"
    return _normalize_token(_first_non_empty(_get_value(memory_context, "last_event", "event"), ""))


def _memory_tags(memory_context: Any) -> set[str]:
    data = _as_mapping(memory_context)
    tags = data.get("tags", data.get("memory_tags", data.get("tag_list", [])))
    if isinstance(tags, str):
        return {_normalize_token(tags)}
    if isinstance(tags, Mapping):
        return {_normalize_token(key) for key, value in tags.items() if value}
    if isinstance(tags, Sequence) and not isinstance(tags, (bytes, bytearray, str)):
        return {_normalize_token(item) for item in tags if _coerce_text(item)}
    return set()


def _is_location_bound(*sources: Any) -> bool:
    keys = ("location_bound", "location_locked", "requires_location", "requires_map", "map_bound")
    for source in sources:
        data = _as_mapping(source)
        for key in keys:
            if key in data and bool(data[key]):
                return True
        narrative = data.get("narrative")
        if isinstance(narrative, Mapping):
            for key in keys:
                if key in narrative and bool(narrative[key]):
                    return True
    return False


def _map_candidates(event_kind: str, availability: str, location_label: str, chain_label: str) -> list[str]:
    candidates = [
        event_kind,
        availability,
        location_label,
        chain_label,
    ]
    if event_kind == "abandon":
        candidates.extend(["abandon", "abandoned", "quest_abandoned"])
    if event_kind == "complete":
        candidates.extend(["complete", "completed", "quest_completed"])
    if event_kind == "fail":
        candidates.extend(["fail", "failed", "quest_failed"])
    if event_kind == "stage_change":
        candidates.extend(["stage_change", "next_stage", "advance"])
    if event_kind == "delayed_follow_up":
        candidates.extend(["delayed_follow_up", "follow_up", "returned_late"])
    if event_kind == "repeat_interaction":
        candidates.extend(["repeat_interaction", "repeat", "again"])
    if availability:
        candidates.append(availability)
    if location_label:
        candidates.append(_normalize_token(location_label))
    if chain_label:
        candidates.append(_normalize_token(chain_label))
    return [candidate for candidate in candidates if candidate]


def _generic_map_line(
    event_kind: str,
    quest: Any,
    stage: Any,
    world_context: Any,
    memory_context: Any,
) -> str:
    quest_label = _quest_label(quest)
    stage_label = _stage_label(stage)
    location_label = _location_label(world_context) or _location_label(memory_context)
    chain_label = _chain_label(memory_context, world_context, quest)
    availability = _availability_label(world_context, quest, stage, memory_context)
    location_bound = _is_location_bound(world_context, quest, stage)

    if event_kind == "abandon" or "quest_abandoned" in _memory_tags(memory_context):
        if location_label:
            return f"You left {quest_label} hanging at {location_label}; that place still remembers."
        return f"You walked away from {quest_label}, and the trail still waits for you."
    if availability in {"available", "open", "ready", "active"}:
        if location_label:
            return f"{quest_label} is open again at {location_label}."
        return f"{quest_label} is open again."
    if availability in {"locked", "closed", "unavailable", "inactive", "expired"}:
        if location_label:
            return f"{quest_label} is closed to you at {location_label} for now."
        return f"{quest_label} is closed to you for now."
    if event_kind in {"complete", "completed", "quest_completed"}:
        if location_label:
            return f"The work tied to {location_label} is finished."
        return f"The work for {quest_label} is finished."
    if event_kind in {"fail", "failed", "quest_failed"}:
        if location_label:
            return f"The matter at {location_label} went badly."
        return f"The matter for {quest_label} went badly."
    if chain_label:
        if location_label and location_bound:
            return f"{quest_label} at {location_label} still belongs to the {chain_label} chain."
        return f"{quest_label} still sits inside the {chain_label} chain."
    if location_label:
        if location_bound:
            return f"{quest_label} is still tied to {location_label}."
        return f"{quest_label} points toward {location_label}."
    if stage_label:
        return f"{stage_label} still matters for {quest_label}."
    return ""


def resolve_quest_map_line(*args: Any, **kwargs: Any) -> str:
    """Resolve a map-facing quest line from world and quest memory context."""

    quest = kwargs.pop("quest", kwargs.pop("quest_template", None))
    stage = kwargs.pop("stage", kwargs.pop("quest_stage", None))
    memory_context = kwargs.pop("memory_context", kwargs.pop("quest_memory_context", kwargs.pop("memory", None)))
    world_context = kwargs.pop("world_context", kwargs.pop("quest_world_context", kwargs.pop("world", None)))
    event_kind = kwargs.pop("event_kind", kwargs.pop("reaction_kind", kwargs.pop("outcome", None)))

    positional = list(args)
    if positional:
        if event_kind is None and isinstance(positional[0], str):
            event_kind = positional.pop(0)
        if world_context is None and positional and _looks_like_world_context(positional[0]):
            world_context = positional.pop(0)
        if memory_context is None and positional and _looks_like_memory_context(positional[0]):
            memory_context = positional.pop(0)
        if quest is None and positional:
            quest = positional.pop(0)
        if stage is None and positional:
            stage = positional.pop(0)
        if memory_context is None and positional and _looks_like_memory_context(positional[0]):
            memory_context = positional.pop(0)
        if world_context is None and positional and _looks_like_world_context(positional[0]):
            world_context = positional.pop(0)
        if event_kind is None and positional:
            event_kind = positional.pop(0)

    event_kind = _event_kind_from_memory(event_kind, memory_context)
    location_label = _location_label(world_context) or _location_label(quest) or _location_label(stage)
    chain_label = _chain_label(memory_context, world_context, quest, stage)
    availability = _availability_label(world_context, quest, stage, memory_context)

    narrative_sources = (_source_mapping(stage), _source_mapping(quest), _source_mapping(world_context))
    candidates = _map_candidates(event_kind, availability, location_label, chain_label)

    for source in narrative_sources:
        if not source:
            continue
        block = _get_block(source, "map_lines")
        text = _select_text(block, candidates)
        if text:
            return text

    generic = _generic_map_line(event_kind, quest, stage, world_context, memory_context)
    if generic:
        return generic

    quest_label = _quest_label(quest)
    if location_label:
        return f"{quest_label} still points toward {location_label}."
    if chain_label:
        return f"{quest_label} remains part of the {chain_label} chain."
    return ""


def describe_quest_map_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for callers that expect a describe_* helper."""

    return resolve_quest_map_line(*args, **kwargs)


def describe_map_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for legacy callers."""

    return resolve_quest_map_line(*args, **kwargs)


def resolve_map_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for legacy callers."""

    return resolve_quest_map_line(*args, **kwargs)


def script_sod_quest_dialogue_describe_map_line(*args: Any, **kwargs: Any) -> str:
    """Legacy script entrypoint used by the dialogue compiler."""

    return resolve_quest_map_line(*args, **kwargs)


SCRIPT = script_sod_quest_dialogue_describe_map_line
SCRIPTS = [
    (
        "sod_quest_dialogue_describe_map_line",
        [
            (str_store_string, s4, "@The road ahead still carries unfinished business."),
            (assign, reg0, 1),
        ],
    )
]
