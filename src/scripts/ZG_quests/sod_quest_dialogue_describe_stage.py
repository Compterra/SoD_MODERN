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

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from src.scripts.ZG_quests.sod_quest_dialogue_read_memory import quest_memory_context

OUTPUT_REGISTER = "s2"
SCRIPT_NAME = "sod_quest_dialogue_describe_stage"

s2 = ""


__all__ = [
    "SCRIPT_NAME",
    "OUTPUT_REGISTER",
    "resolve_quest_stage_line",
    "resolve_stage_line",
    "describe_stage_line",
    "sod_quest_dialogue_describe_stage",
    "script_sod_quest_dialogue_describe_stage",
    "SCRIPT",
    "SCRIPTS",
]


_STAGE_LINE_KEYS = (
    "narrative.stage_lines",
    "narrative.stage_text",
    "narrative.lines",
    "narrative.stage_flavor",
    "narrative.flavor_lines",
    "narrative.generic_lines",
    "narrative.default_lines",
    "narrative.default_line",
    "narrative.stage_description",
    "description",
    "flavor",
    "text",
    "line",
    "value",
    "message",
)

_GENERIC_FLAVOR_KEYS = (
    "narrative.stage_flavor",
    "narrative.flavor_lines",
    "narrative.generic_lines",
    "narrative.default_lines",
    "narrative.default_line",
    "narrative.stage_description",
    "description",
    "flavor",
    "text",
    "line",
    "value",
    "message",
)

_DIRECT_TEXT_KEYS = (
    "text",
    "line",
    "value",
    "description",
    "flavor",
    "default",
    "generic",
    "any",
    "fallback",
    "message",
)

_COMPOSITE_KEY_PATTERNS = (
    ("personality", "event_type"),
    ("personality", "stage_id"),
    ("personality", "quest_id"),
    ("event_type", "stage_id"),
    ("quest_id", "stage_id"),
    ("quest_id", "stage_id", "event_type"),
    ("quest_id", "event_type"),
    ("location_id", "stage_id"),
    ("location_name", "stage_id"),
    ("chain_id", "stage_id"),
    ("chain_id", "event_type"),
    ("actor_id", "event_type"),
    ("freshness", "event_type"),
    ("quest_id", "personality"),
    ("stage_id", "personality"),
)


def _is_mapping(value: Any) -> bool:
    return isinstance(value, Mapping)


def _is_context_like(value: Any) -> bool:
    return _is_mapping(value) or hasattr(value, "__dict__") or hasattr(value, "metadata") or hasattr(value, "registers")


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalise_token(value: Any) -> str:
    text = _stringify(value).lower()
    if not text:
        return ""
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _selector_variants(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set, frozenset)):
        variants: list[str] = []
        for item in value:
            variants.extend(_selector_variants(item))
        return _dedupe(variants)
    raw = _stringify(value)
    if not raw:
        return []
    lowered = raw.lower()
    variants = [raw, lowered, lowered.replace(" ", "_"), _normalise_token(raw)]
    return _dedupe(variants)


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "__dict__"):
        try:
            return dict(vars(value))
        except TypeError:
            return {}
    return {}


def _get_value(source: Any, *names: str, default: Any = None) -> Any:
    if source is None:
        return default
    if isinstance(source, Mapping):
        for name in names:
            if name in source and source[name] is not None:
                return source[name]
    for name in names:
        if hasattr(source, name):
            value = getattr(source, name)
            if value is not None:
                return value
    return default


def _merge_context(context: dict[str, Any], value: Any) -> None:
    if value is None:
        return
    if _is_mapping(value):
        context.update(value)
        return
    if hasattr(value, "__dict__"):
        context.update(_as_dict(value))
        return
    context.setdefault("quest_id", value)


def _build_context(args: Sequence[Any], kwargs: Mapping[str, Any], positional_keys: Sequence[str]) -> dict[str, Any]:
    context: dict[str, Any] = dict(kwargs)
    remaining_args = list(args)
    if remaining_args and _is_context_like(remaining_args[0]):
        context["source"] = remaining_args[0]
        _merge_context(context, remaining_args.pop(0))
    for key, value in zip(positional_keys, remaining_args):
        context.setdefault(key, value)
    for name in ("s1", "s2", "s3", "s4", "reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6", "reg7", "reg8", "reg9"):
        context.setdefault(name, globals().get(name))
    return context


def _metadata_map(source: Any) -> dict[str, Any]:
    if source is None:
        return {}
    if isinstance(source, Mapping):
        metadata = source.get("metadata")
        if isinstance(metadata, Mapping):
            return dict(metadata)
        if "narrative" in source and isinstance(source["narrative"], Mapping):
            return dict(source)
        return dict(source)
    metadata = getattr(source, "metadata", None)
    if isinstance(metadata, Mapping):
        return dict(metadata)
    if metadata is not None and hasattr(metadata, "items"):
        try:
            return dict(metadata)  # type: ignore[arg-type]
        except Exception:
            pass
    if hasattr(source, "to_snapshot"):
        try:
            snapshot = source.to_snapshot()
        except Exception:
            snapshot = None
        if isinstance(snapshot, Mapping):
            metadata = snapshot.get("metadata")
            if isinstance(metadata, Mapping):
                return dict(metadata)
            return dict(snapshot)
    if hasattr(source, "to_dict"):
        try:
            snapshot = source.to_dict()
        except Exception:
            snapshot = None
        if isinstance(snapshot, Mapping):
            metadata = snapshot.get("metadata")
            if isinstance(metadata, Mapping):
                return dict(metadata)
            return dict(snapshot)
    return {}


def _metadata_lookup(metadata: Mapping[str, Any], key: str) -> Any:
    if not isinstance(metadata, Mapping):
        return None
    if key in metadata:
        return metadata[key]
    parts = key.split(".")
    current: Any = metadata
    for part in parts:
        if not isinstance(current, Mapping) or part not in current:
            break
        current = current[part]
    else:
        return current
    narrative = metadata.get("narrative")
    if isinstance(narrative, Mapping):
        if key in narrative:
            return narrative[key]
        short_key = key.split(".", 1)[-1]
        if short_key in narrative:
            return narrative[short_key]
        nested = narrative.get("narrative")
        if isinstance(nested, Mapping):
            if key in nested:
                return nested[key]
            if short_key in nested:
                return nested[short_key]
    return None


def _metadata_block(source: Any, key: str) -> Any:
    metadata = _metadata_map(source)
    if not metadata:
        return None
    return _metadata_lookup(metadata, key)


def _memory_freshness(context: Mapping[str, Any]) -> dict[str, Any]:
    remembered_day = _get_value(context, "remembered_day", "memory_day", "last_day", "day", "reg8", default=None)
    current_day = _get_value(context, "current_day", "world_day", "campaign_day", default=None)
    age = _get_value(context, "memory_age", "age", "days_since_memory", "last_age_days", default=None)
    interaction_count = _get_value(context, "interaction_count", "reg9", default=None)
    event_day = _get_value(context, "event_day", default=None)

    if age in ("", None) and remembered_day is not None and current_day is not None:
        try:
            age = int(current_day) - int(remembered_day)
        except (TypeError, ValueError):
            age = None
    if age in ("", None) and remembered_day is not None and event_day is not None:
        try:
            age = int(event_day) - int(remembered_day)
        except (TypeError, ValueError):
            age = None

    age_int: int | None
    try:
        age_int = int(age) if age not in ("", None) else None
    except (TypeError, ValueError):
        age_int = None

    try:
        interaction_int = int(interaction_count) if interaction_count not in ("", None) else None
    except (TypeError, ValueError):
        interaction_int = None

    if age_int is None:
        if interaction_int is None or interaction_int <= 1:
            label = "fresh"
        else:
            label = "stale"
    elif age_int <= 1:
        label = "fresh"
    elif age_int <= 3:
        label = "recent"
    else:
        label = "stale"

    return {
        "age": age_int,
        "interaction_count": interaction_int,
        "label": label,
        "fresh": label == "fresh",
        "recent": label in {"fresh", "recent"},
        "stale": label == "stale",
    }


def _quest_state_label(context: Mapping[str, Any]) -> str:
    event_kind = _normalise_token(_get_value(context, "event_kind", "event_type", "event", "action", "kind", "last_event_kind", "reg3", default=""))
    state = _normalise_token(_get_value(context, "state", "status", "quest_state", "quest_status", "reg0", default=""))
    outcome = _normalise_token(_get_value(context, "outcome", "last_outcome", "result", "reg7", default=""))
    for candidate in (event_kind, outcome, state):
        if candidate in {"accept", "accepted", "active", "start", "started", "ongoing", "in_progress"}:
            return "active"
        if candidate in {"complete", "completed", "success", "succeeded", "finished"}:
            return "completed"
        if candidate in {"fail", "failed", "failure", "lost"}:
            return "failed"
        if candidate in {"abort", "aborted", "abandon", "abandoned", "expired", "expiration"}:
            return "aborted" if candidate in {"abort", "aborted", "expired", "expiration"} else "abandoned"
    return state or outcome or event_kind or "active"


def _collect_personality_selectors(context: Mapping[str, Any]) -> list[str]:
    selectors: list[str] = []
    for name in (
        "personality",
        "npc_personality",
        "personality_state",
        "actor_personality",
        "reaction_personality",
        "tone",
        "temperament",
    ):
        selectors.extend(_selector_variants(context.get(name)))
    npc = context.get("npc") or context.get("actor") or context.get("speaker")
    for name in ("personality", "personality_tags", "traits", "state", "attitude", "tone", "temperament"):
        selectors.extend(_selector_variants(_get_value(npc, name, default=None)))
    return _dedupe(selectors)


def _collect_world_selectors(context: Mapping[str, Any]) -> list[str]:
    selectors: list[str] = []
    for name in (
        "world_context",
        "world",
        "location",
        "scene",
        "map_context",
        "region",
        "settlement",
        "place",
        "terrain",
    ):
        selectors.extend(_selector_variants(context.get(name)))
    world = context.get("world_context") or context.get("world")
    if world is not None:
        for name in (
            "location_id",
            "location_name",
            "center_id",
            "party_id",
            "location_type",
            "place_type",
            "settlement_type",
            "scene_type",
            "terrain_type",
            "kind",
            "state",
            "label",
            "name",
            "region",
        ):
            selectors.extend(_selector_variants(_get_value(world, name, default=None)))
    return _dedupe(selectors)


def _collect_memory_selectors(context: Mapping[str, Any]) -> list[str]:
    selectors: list[str] = []
    for name in ("memory_tags", "quest_memory_tags", "tags"):
        selectors.extend(_selector_variants(context.get(name)))
    selectors.extend(_selector_variants(context.get("s4")))
    selectors.extend(_selector_variants(context.get("memory_summary")))
    selectors.extend(_selector_variants(context.get("memory_state")))
    selectors.extend(_selector_variants(context.get("classification")))
    selectors.extend(_selector_variants(context.get("freshness")))
    return _dedupe(selectors)


def _collect_chain_selectors(context: Mapping[str, Any]) -> list[str]:
    selectors: list[str] = []
    for name in ("chain_id", "chain", "quest_chain", "chain_state"):
        selectors.extend(_selector_variants(context.get(name)))
    return _dedupe(selectors)


def _stage_phase_selectors(context: Mapping[str, Any]) -> list[str]:
    selectors: list[str] = []
    event_kind = _normalise_token(_get_value(context, "event_kind", "event_type", "event", "kind", "last_event_kind", "reg3", default=""))
    state_label = _quest_state_label(context)
    freshness = _memory_freshness(context)
    selectors.extend(_selector_variants(event_kind))
    selectors.extend(_selector_variants(state_label))
    selectors.extend(_selector_variants(freshness["label"]))
    if freshness["stale"]:
        selectors.extend(["delayed_follow_up", "follow_up", "repeat_interaction"])
    if freshness["fresh"]:
        selectors.extend(["fresh", "recent"])
    interaction_count = freshness.get("interaction_count")
    if interaction_count is not None and interaction_count > 1:
        selectors.extend(["repeat_interaction", "again", "follow_up"])
    return _dedupe(selectors)


def _candidate_keys(selectors: Mapping[str, Any]) -> list[str]:
    keys: list[str] = []
    for pattern in _COMPOSITE_KEY_PATTERNS:
        values = [_stringify(selectors.get(name)) for name in pattern]
        values = [value for value in values if value]
        if len(values) != len(pattern):
            continue
        joined_variants = (
            ":".join(values),
            ".".join(values),
            "/".join(values),
            "|".join(values),
            "_".join(values),
            "-".join(values),
        )
        for candidate in joined_variants:
            if candidate and candidate not in keys:
                keys.append(candidate)
    return keys


def _score_entry(entry: Mapping[str, Any], selectors: Mapping[str, Any]) -> int:
    score = 0
    for key in ("personality", "event_type", "stage_id", "quest_id", "chain_id", "location_id", "location_name", "actor_id", "freshness"):
        expected = _normalise_token(selectors.get(key))
        if not expected:
            continue
        actual = _normalise_token(entry.get(key))
        if actual and actual == expected:
            score += 2
    selector_tags = _selector_variants(selectors.get("tags"))
    if selector_tags:
        entry_tags = _selector_variants(entry.get("tags") or entry.get("memory_tags"))
        score += len(set(selector_tags).intersection(entry_tags))
    for key in ("priority", "weight", "score"):
        value = entry.get(key)
        if isinstance(value, (int, float)):
            score += int(value)
    return score


def _resolve_entry(entry: Any, selectors: Mapping[str, Any]) -> str:
    if entry is None:
        return ""
    if isinstance(entry, str):
        return entry.strip()
    if isinstance(entry, (bytes, bytearray)):
        try:
            return entry.decode("utf-8", errors="ignore").strip()
        except Exception:
            return ""
    if isinstance(entry, Sequence) and not isinstance(entry, (str, bytes, bytearray)):
        scored: list[tuple[int, str]] = []
        for item in entry:
            line = _resolve_entry(item, selectors)
            if not line:
                continue
            score = _score_entry(item, selectors) if isinstance(item, Mapping) else 0
            scored.append((score, line))
        if scored:
            scored.sort(key=lambda item: item[0], reverse=True)
            return scored[0][1]
        return ""
    mapping = _as_dict(entry)
    if not mapping:
        return _stringify(entry)

    for key in _candidate_keys(selectors):
        if key in mapping:
            line = _resolve_entry(mapping[key], selectors)
            if line:
                return line
        lower_key = key.lower()
        if lower_key in mapping:
            line = _resolve_entry(mapping[lower_key], selectors)
            if line:
                return line

    for selector_name in ("personality", "event_type", "stage_id", "quest_id", "chain_id", "location_id", "location_name", "actor_id", "freshness"):
        selector_value = selectors.get(selector_name)
        for variant in _selector_variants(selector_value):
            if variant in mapping:
                line = _resolve_entry(mapping[variant], selectors)
                if line:
                    return line
            lowered = variant.lower()
            if lowered in mapping:
                line = _resolve_entry(mapping[lowered], selectors)
                if line:
                    return line

    for fallback_key in ("default", "generic", "fallback", "any", "other", "base", "neutral", "text", "line", "value", "description", "message"):
        if fallback_key in mapping:
            line = _resolve_entry(mapping[fallback_key], selectors)
            if line:
                return line

    nested_entries: list[tuple[int, Any]] = []
    for value in mapping.values():
        if isinstance(value, Mapping):
            nested_entries.append((_score_entry(value, selectors), value))
    if nested_entries:
        nested_entries.sort(key=lambda item: item[0], reverse=True)
        best_score, best_entry = nested_entries[0]
        if best_score > 0:
            line = _resolve_entry(best_entry, selectors)
            if line:
                return line

    for key in _DIRECT_TEXT_KEYS:
        if key in mapping:
            line = _resolve_entry(mapping[key], selectors)
            if line:
                return line

    for value in mapping.values():
        line = _resolve_entry(value, selectors)
        if line:
            return line

    return ""


def _resolve_personality_overrides(block: Any, selectors: Mapping[str, Any]) -> str:
    if not isinstance(block, Mapping):
        return _resolve_entry(block, selectors)
    for selector in selectors.get("personality_variants", []) or _selector_variants(selectors.get("personality")):
        for variant in _selector_variants(selector):
            if variant in block:
                line = _resolve_entry(block[variant], selectors)
                if line:
                    return line
            lowered = variant.lower()
            if lowered in block:
                line = _resolve_entry(block[lowered], selectors)
                if line:
                    return line
    for fallback_key in ("default", "generic", "fallback", "any", "other", "base", "neutral"):
        if fallback_key in block:
            line = _resolve_entry(block[fallback_key], selectors)
            if line:
                return line
    return ""


def _resolve_source_line(source: Any, selectors: Mapping[str, Any]) -> str:
    if source is None:
        return ""
    metadata = _metadata_map(source)
    if not metadata:
        return ""

    overrides = _metadata_lookup(metadata, "narrative.personality_overrides")
    if overrides is not None:
        line = _resolve_personality_overrides(overrides, selectors)
        if line:
            return line

    stage_lines = _metadata_lookup(metadata, "narrative.stage_lines")
    if stage_lines is not None:
        line = _resolve_entry(stage_lines, selectors)
        if line:
            return line

    for key in _GENERIC_FLAVOR_KEYS:
        block = _metadata_lookup(metadata, key)
        if block is None:
            continue
        line = _resolve_entry(block, selectors)
        if line:
            return line

    return ""


def _resolve_quest_stage_line(context: Mapping[str, Any]) -> str:
    memory_context = context.get("memory_context")
    world_context = context.get("world_context")

    if memory_context is None and any(name in context for name in ("quest_memory", "memory", "snapshot")):
        memory_context = quest_memory_context(
            context.get("quest_memory") or context.get("memory") or context.get("snapshot"),
            world_context=world_context,
        )
    elif memory_context is not None and not isinstance(memory_context, Mapping):
        memory_context = quest_memory_context(memory_context, world_context=world_context)
    elif isinstance(memory_context, Mapping) and not any(key in memory_context for key in ("quest_id", "stage_id", "event_type", "event_kind", "quest_memory")):
        memory_context = quest_memory_context(memory_context, world_context=world_context)

    memory_context = dict(memory_context or {})
    world_context_data = world_context
    if world_context_data is None:
        world_context_data = memory_context.get("world_context")

    quest = context.get("quest") or context.get("quest_template") or context.get("quest_data")
    stage = context.get("stage") or context.get("quest_stage") or context.get("stage_data")

    selectors: dict[str, Any] = {
        "quest_id": _stringify(context.get("quest_id") or memory_context.get("quest_id") or _get_value(quest, "quest_id", "id", "slug", "name", default="")),
        "stage_id": _stringify(context.get("stage_id") or memory_context.get("stage_id") or _get_value(stage, "stage_id", "id", "slug", "name", default="")),
        "event_type": _stringify(
            context.get("event_type")
            or context.get("event_kind")
            or memory_context.get("event_type")
            or memory_context.get("event_kind")
            or _get_value(stage, "event_type", "kind", "action", default="")
        ),
        "personality": _stringify(
            context.get("personality")
            or memory_context.get("personality")
            or _get_value(world_context_data, "personality", "personality_override", "npc_personality", "stance", default="")
            or _get_value(quest, "personality", "npc_personality", default="")
        ),
        "chain_id": _stringify(memory_context.get("chain_id") or _get_value(world_context_data, "chain_id", "quest_chain_id", "chain", default="")),
        "location_id": _stringify(memory_context.get("location_id") or _get_value(world_context_data, "location_id", "current_location_id", "map_location_id", "scene_id", default="")),
        "location_name": _stringify(memory_context.get("location_name") or _get_value(world_context_data, "location_name", "current_location_name", "map_location_name", "scene_name", default="")),
        "actor_id": _stringify(memory_context.get("actor_id") or _get_value(world_context_data, "actor_id", "speaker_id", "npc_id", default="")),
        "freshness": _stringify(memory_context.get("freshness")),
        "classification": _stringify(memory_context.get("classification")),
        "state_label": _quest_state_label(memory_context or context),
        "tags": list(memory_context.get("tags", [])),
        "memory_tags": list(memory_context.get("memory_tags", [])),
        "memory_summary": _stringify(memory_context.get("summary") or context.get("memory_summary")),
    }
    selectors["personality_variants"] = _selector_variants(selectors["personality"])

    if not selectors["quest_id"]:
        selectors["quest_id"] = _stringify(_get_value(world_context_data, "quest_id", "quest", "current_quest_id", default=""))
    if not selectors["stage_id"]:
        selectors["stage_id"] = _stringify(_get_value(world_context_data, "stage_id", "current_stage_id", default=""))
    if not selectors["event_type"]:
        selectors["event_type"] = _stringify(_get_value(memory_context, "event_kind", "event_type", default=""))

    for source in (stage, quest):
        line = _resolve_source_line(source, selectors)
        if line:
            return line

    return ""


def resolve_quest_stage_line(*args: Any, **kwargs: Any) -> str:
    """Resolve a quest stage line from stage and quest metadata."""

    positional_keys = (
        "quest",
        "stage",
        "event_type",
        "personality",
        "memory_context",
        "world_context",
        "quest_id",
        "stage_id",
        "default",
    )
    context = _build_context(args, kwargs, positional_keys)
    return _resolve_quest_stage_line(context)


def resolve_stage_line(*args: Any, **kwargs: Any) -> str:
    return resolve_quest_stage_line(*args, **kwargs)


def describe_stage_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for stage-line resolution."""

    return resolve_quest_stage_line(*args, **kwargs)


def _set_output(context: Mapping[str, Any] | None, register_name: str, value: str) -> None:
    globals()[register_name] = value
    if context is None:
        return
    if isinstance(context, dict):
        context[register_name] = value
        return
    registers = _get_value(context, "registers", default=None)
    if isinstance(registers, dict):
        registers[register_name] = value
        return
    setter = _get_value(context, "set_register", default=None)
    if callable(setter):
        setter(register_name, value)
        return
    try:
        setattr(context, register_name, value)
    except Exception:
        pass


def sod_quest_dialogue_describe_stage(*args: Any, **kwargs: Any) -> str:
    context = _build_context(args, kwargs, (
        "quest_id",
        "stage_id",
        "event_kind",
        "personality",
        "world_context",
        "memory_summary",
        "chain_id",
        "state",
        "quest",
        "stage",
        "npc",
    ))
    line = _resolve_quest_stage_line(context)
    _set_output(context.get("source"), OUTPUT_REGISTER, line)
    _set_output(context, OUTPUT_REGISTER, line)
    return line


script_sod_quest_dialogue_describe_stage = sod_quest_dialogue_describe_stage

SCRIPT = script_sod_quest_dialogue_describe_stage
SCRIPTS = [
    (
        "sod_quest_dialogue_describe_stage",
        [
            (str_store_string, s4, "@The task is still unfolding."),
            (assign, reg0, 1),
        ],
    )
]
