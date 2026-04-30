"""Quest reaction line resolver.

This module keeps the legacy dialogue layer flexible by resolving outcome-aware
reaction text from quest, stage, world, and memory metadata.
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

__all__ = [
    "resolve_quest_reaction_line",
    "resolve_reaction_line",
    "describe_quest_reaction_line",
    "describe_reaction_line",
    "script_sod_quest_dialogue_describe_reaction",
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
        for field in ("text", "line", "value", "response", "reaction"):
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


def _quest_label(source: Any, fallback: str = "this quest") -> str:
    label = _first_non_empty(
        _get_value(source, "name", "title", "label"),
        _get_value(source, "quest_name", "quest_title"),
        _get_value(source, "id", "quest_id"),
    )
    return label or fallback


def _stage_label(source: Any, fallback: str = "this stage") -> str:
    label = _first_non_empty(
        _get_value(source, "name", "title", "label"),
        _get_value(source, "stage_name", "stage_title"),
        _get_value(source, "id", "stage_id"),
    )
    return label or fallback


def _location_label(world_context: Any, fallback: str = "") -> str:
    return _first_non_empty(
        _get_value(world_context, "location_name", "settlement_name", "town_name", "castle_name", "village_name"),
        _get_value(world_context, "location_id", "settlement_id", "map_location"),
        fallback,
    )


def _personality_label(source: Any) -> str:
    return _normalize_token(
        _first_non_empty(
            _get_value(source, "personality", "persona", "tone"),
            _get_value(source, "npc_personality", "reaction_personality"),
        )
    )


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


def _reaction_candidates(event_kind: str) -> list[str]:
    event_kind = _normalize_token(event_kind)
    mapping = {
        "accept": ["accept", "accepted", "offer_accept", "quest_accept", "quest_accepted"],
        "complete": ["complete", "completed", "success", "quest_completed", "turned_in"],
        "fail": ["fail", "failed", "failure", "quest_failed", "loss"],
        "abandon": ["abandon", "abandoned", "quest_abandoned", "walked_away"],
        "stage_change": ["stage_change", "stage_advance", "advance", "new_stage", "next_stage"],
        "delayed_follow_up": ["delayed_follow_up", "follow_up", "late_follow_up", "returned_late"],
        "repeat_interaction": ["repeat_interaction", "repeat", "again", "back_again", "welcome_back"],
        "trust_broken": ["trust_broken", "betrayal", "betrayed", "broken_trust"],
    }
    return mapping.get(event_kind, [event_kind])


def _generic_reaction_line(
    event_kind: str,
    quest: Any,
    stage: Any,
    memory_context: Any,
    world_context: Any,
) -> str:
    quest_label = _quest_label(quest)
    stage_label = _stage_label(stage)
    location_label = _location_label(world_context)
    chain_label = _first_non_empty(
        _get_value(memory_context, "chain", "chain_id", "quest_chain"),
        _get_value(world_context, "chain", "chain_id", "quest_chain"),
        _get_value(quest, "chain", "chain_id", "quest_chain"),
    )
    event_kind = _normalize_token(event_kind)

    if event_kind in {"accept", "accepted", "offer_accept", "quest_accept", "quest_accepted"}:
        extra = f" at {location_label}" if location_label else ""
        return f"Good. {quest_label}{extra} is now in motion."
    if event_kind in {"complete", "completed", "success", "quest_completed", "turned_in"}:
        return f"You kept your word on {quest_label}. That matters."
    if event_kind in {"fail", "failed", "failure", "quest_failed", "loss"}:
        return f"{quest_label} went badly. We'll have to live with that and learn from it."
    if event_kind in {"abandon", "abandoned", "quest_abandoned", "walked_away"}:
        return f"You walked away from {quest_label}. I won't forget that."
    if event_kind in {"stage_change", "stage_advance", "advance", "new_stage", "next_stage"}:
        return f"{stage_label} is the next part of {quest_label}. Keep moving."
    if event_kind in {"delayed_follow_up", "follow_up", "late_follow_up", "returned_late"}:
        return f"You've returned at last. Let's finish what we started with {quest_label}."
    if event_kind in {"repeat_interaction", "repeat", "again", "back_again", "welcome_back"}:
        if chain_label:
            return f"Back again on the {chain_label} matter? Then let's not waste time."
        return f"Back again? Then let's keep this short and useful."
    if event_kind in {"trust_broken", "betrayal", "betrayed", "broken_trust"}:
        return f"You broke the trust around {quest_label}. That's not easily repaired."
    if location_label:
        return f"{quest_label} still points to {location_label}. Stay sharp."
    return f"We still have business regarding {quest_label}."


def resolve_quest_reaction_line(*args: Any, **kwargs: Any) -> str:
    """Resolve the most appropriate reaction line for a quest outcome."""

    event_kind = kwargs.pop("event_kind", kwargs.pop("reaction_kind", kwargs.pop("outcome", None)))
    quest = kwargs.pop("quest", kwargs.pop("quest_template", None))
    stage = kwargs.pop("stage", kwargs.pop("quest_stage", None))
    memory_context = kwargs.pop("memory_context", kwargs.pop("quest_memory_context", kwargs.pop("memory", None)))
    world_context = kwargs.pop("world_context", kwargs.pop("quest_world_context", kwargs.pop("world", None)))
    personality = kwargs.pop("personality", kwargs.pop("tone", None))

    positional = list(args)
    if positional:
        if event_kind is None and isinstance(positional[0], str):
            event_kind = positional.pop(0)
        if quest is None and positional:
            quest = positional.pop(0)
        if stage is None and positional:
            stage = positional.pop(0)
        if memory_context is None and positional:
            memory_context = positional.pop(0)
        if world_context is None and positional:
            world_context = positional.pop(0)
        if personality is None and positional:
            personality = positional.pop(0)

    event_kind = _event_kind_from_memory(event_kind, memory_context)
    personality = _normalize_token(
        _first_non_empty(
            personality,
            _personality_label(stage),
            _personality_label(quest),
            _personality_label(world_context),
            _get_value(memory_context, "personality", "persona", "tone"),
        )
    )

    narrative_sources = (_source_mapping(stage), _source_mapping(quest), _source_mapping(world_context))
    candidates = _reaction_candidates(event_kind)

    for source in narrative_sources:
        if not source:
            continue
        personality_overrides = _get_block(source, "personality_overrides")
        if personality_overrides is not None:
            override_candidates = [personality, event_kind, *_reaction_candidates(event_kind), "default"]
            text = _select_text(personality_overrides, override_candidates)
            if text:
                return text

    block_names = ("reaction_lines",)
    if event_kind in {"complete", "completed", "success", "quest_completed", "turned_in"}:
        block_names = ("reaction_lines", "success_lines")
    elif event_kind in {"fail", "failed", "failure", "quest_failed", "loss"}:
        block_names = ("reaction_lines", "failure_lines")
    elif event_kind in {"abandon", "abandoned", "quest_abandoned", "walked_away"}:
        block_names = ("reaction_lines", "abandon_lines")

    for source in narrative_sources:
        if not source:
            continue
        for block_name in block_names:
            block = _get_block(source, block_name)
            text = _select_text(block, candidates)
            if text:
                return text

    return _generic_reaction_line(event_kind, quest, stage, memory_context, world_context)


def describe_quest_reaction_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for callers that expect a describe_* style helper."""

    return resolve_quest_reaction_line(*args, **kwargs)


def describe_reaction_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for legacy callers."""

    return resolve_quest_reaction_line(*args, **kwargs)


def resolve_reaction_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for legacy callers."""

    return resolve_quest_reaction_line(*args, **kwargs)


def script_sod_quest_dialogue_describe_reaction(*args: Any, **kwargs: Any) -> str:
    """Legacy script entrypoint used by the dialogue compiler."""

    return resolve_quest_reaction_line(*args, **kwargs)


SCRIPT = script_sod_quest_dialogue_describe_reaction
SCRIPTS = [
    (
        "sod_quest_dialogue_describe_reaction",
        [
            (str_store_string, s4, "@There is more to say about this quest."),
            (assign, reg0, 1),
        ],
    )
]
