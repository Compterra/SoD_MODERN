"""Quest battle-line resolver.

The dialogue layer uses this module to produce objective-aware battle text from
quest, stage, memory, and world metadata.
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

from src.quests.quest_domain import QuestBattleObjective

__all__ = [
    "resolve_quest_battle_line",
    "resolve_battle_line",
    "describe_quest_battle_line",
    "describe_battle_line",
    "script_sod_quest_dialogue_describe_battle_line",
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
        for field in ("text", "line", "value", "response", "battle_line"):
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


def _objective_name(objective: Any, fallback: str = "the objective") -> str:
    return _coerce_text(
        _get_value(
            objective,
            "name",
            "title",
            "label",
            "objective_name",
            "target_name",
            "target_label",
            "id",
            "target_id",
        )
    ) or fallback


def _objective_action_kind(objective: Any) -> str:
    if objective is None:
        return ""
    data = _as_mapping(objective)
    if not data:
        return _normalize_token(getattr(objective, "action_kind", getattr(objective, "kind", "")))
    return _normalize_token(
        _first_non_empty(
            data.get("action_kind"),
            data.get("objective_kind"),
            data.get("kind"),
            data.get("type"),
            data.get("battle_kind"),
        )
    )


def _first_non_empty(*values: Any) -> str:
    for value in values:
        text = _coerce_text(value)
        if text:
            return text
    return ""


def _phase_from_context(battle_phase: str | None, progress: Any, objective: Any) -> str:
    phase = _normalize_token(battle_phase)
    if phase in {"pre", "before", "setup", "intro"}:
        return "pre"
    if phase in {"mid", "during", "battle", "active", "in_progress"}:
        return "mid"
    if phase in {"post", "after", "complete", "done", "resolved"}:
        return "post"

    status = _normalize_token(_first_non_empty(_get_value(objective, "status", "state"), _get_value(objective, "progress_state")))
    if status in {"complete", "completed", "done", "resolved", "succeeded", "success"}:
        return "post"
    if status in {"active", "in_progress", "ongoing", "mid"}:
        return "mid"

    progress_text = _normalize_token(progress)
    if progress_text in {"complete", "completed", "done", "resolved", "succeeded", "success"}:
        return "post"
    if progress_text in {"ongoing", "active", "in_progress", "mid"}:
        return "mid"

    numeric_progress = _get_value(objective, "progress", "completion", "completion_ratio")
    try:
        numeric_value = float(numeric_progress)
    except (TypeError, ValueError):
        numeric_value = None
    if numeric_value is not None:
        if numeric_value >= 1.0:
            return "post"
        if numeric_value > 0.0:
            return "mid"

    if progress is not None and _coerce_text(progress):
        return "mid"

    return "pre"


def _action_phrase(action_kind: str, target: str) -> str:
    action_kind = _normalize_token(action_kind)
    if action_kind in {"escort", "escort_npc", "protect", "guard", "defend"}:
        return f"keep {target} safe"
    if action_kind in {"deliver", "bring", "carry", "transport"}:
        return f"get {target} where it needs to go"
    if action_kind in {"collect", "gather", "recover", "retrieve", "fetch"}:
        return f"recover {target}"
    if action_kind in {"hunt", "kill", "slay", "eliminate", "defeat", "attack", "destroy"}:
        return f"put {target} down"
    if action_kind in {"capture", "seize", "arrest"}:
        return f"take {target} alive"
    if action_kind in {"scout", "spy", "recon", "survey", "observe"}:
        return f"watch {target} closely and return with answers"
    if action_kind in {"raid", "strike", "ambush"}:
        return f"hit {target} hard and fast"
    if action_kind in {"survive", "hold", "hold_out", "endure"}:
        return f"hold the line until the pressure breaks"
    if action_kind in {"rescue", "free", "save"}:
        return f"reach {target} and bring them out"
    return f"finish the task around {target}"


def _generic_battle_line(
    action_kind: str,
    phase: str,
    objective: Any,
    quest: Any,
    stage: Any,
    world_context: Any,
    memory_context: Any,
) -> str:
    target = _objective_name(objective)
    quest_label = _quest_label(quest)
    stage_label = _stage_label(stage)
    action_phrase = _action_phrase(action_kind, target)

    if phase == "pre":
        return f"Before this begins, {action_phrase} for {quest_label}."
    if phase == "mid":
        return f"While the fight is on, stay focused on {action_phrase}."
    if phase == "post":
        return f"That part is done; {action_phrase} for {quest_label} is over now."

    location_label = _coerce_text(
        _first_non_empty(
            _get_value(world_context, "location_name", "settlement_name", "town_name", "castle_name", "village_name"),
            _get_value(memory_context, "location_name", "last_location"),
        )
    )
    if location_label:
        return f"{quest_label} at {location_label} needs you to {action_phrase}."
    if stage_label:
        return f"{stage_label} asks you to {action_phrase}."
    return f"{quest_label} asks you to {action_phrase}."


def resolve_quest_battle_line(*args: Any, **kwargs: Any) -> str:
    """Resolve a battle line from objective kind, progress, and combat phase."""

    objective = kwargs.pop("objective", kwargs.pop("quest_battle_objective", kwargs.pop("battle_objective", None)))
    quest = kwargs.pop("quest", kwargs.pop("quest_template", None))
    stage = kwargs.pop("stage", kwargs.pop("quest_stage", None))
    memory_context = kwargs.pop("memory_context", kwargs.pop("quest_memory_context", kwargs.pop("memory", None)))
    world_context = kwargs.pop("world_context", kwargs.pop("quest_world_context", kwargs.pop("world", None)))
    battle_phase = kwargs.pop("battle_phase", kwargs.pop("phase", None))
    progress = kwargs.pop("progress", kwargs.pop("objective_progress", None))

    positional = list(args)
    if positional:
        if objective is None:
            objective = positional.pop(0)
        if quest is None and positional:
            quest = positional.pop(0)
        if stage is None and positional:
            stage = positional.pop(0)
        if memory_context is None and positional:
            memory_context = positional.pop(0)
        if world_context is None and positional:
            world_context = positional.pop(0)
        if battle_phase is None and positional:
            battle_phase = positional.pop(0)
        if progress is None and positional:
            progress = positional.pop(0)

    action_kind = _objective_action_kind(objective)
    phase = _phase_from_context(battle_phase, progress, objective)

    narrative_sources = (_source_mapping(stage), _source_mapping(quest), _source_mapping(world_context))
    candidates = [
        action_kind,
        _normalize_token(_objective_name(objective, "")),
        phase,
        _normalize_token(progress),
        _normalize_token(_get_value(objective, "status", "state")),
    ]

    block_candidates = ["battle_lines", "reaction_lines"]
    for source in narrative_sources:
        if not source:
            continue
        for block_name in block_candidates:
            block = _get_block(source, block_name)
            text = _select_text(block, candidates)
            if text:
                return text

    return _generic_battle_line(action_kind, phase, objective, quest, stage, world_context, memory_context)


def describe_quest_battle_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for callers that expect a describe_* helper."""

    return resolve_quest_battle_line(*args, **kwargs)


def describe_battle_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for legacy callers."""

    return resolve_quest_battle_line(*args, **kwargs)


def resolve_battle_line(*args: Any, **kwargs: Any) -> str:
    """Compatibility alias for legacy callers."""

    return resolve_quest_battle_line(*args, **kwargs)


def script_sod_quest_dialogue_describe_battle_line(*args: Any, **kwargs: Any) -> str:
    """Legacy script entrypoint used by the dialogue compiler."""

    return resolve_quest_battle_line(*args, **kwargs)


SCRIPT = script_sod_quest_dialogue_describe_battle_line
SCRIPTS = [
    (
        "sod_quest_dialogue_describe_battle_line",
        [
            (str_store_string, s4, "@The battle is tied to unfinished business."),
            (assign, reg0, 1),
        ],
    )
]
