"""Source adapters for emitting quest world events.

This module provides a compact facade over the existing quest event model.
Callers can either build a :class:`QuestWorldEvent` or dispatch it directly
through a runtime, journal, or dispatcher-like object.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from inspect import Parameter, signature
import re
from typing import Any, Callable

from . import quest_events as _quest_events

QuestWorldEvent = _quest_events.QuestWorldEvent

__all__ = [
    "emit_world_event",
    "emit_battle_started",
    "emit_battle_ended",
    "emit_agent_killed",
    "emit_prisoner_captured",
    "emit_prisoner_freed",
    "emit_party_entered_center",
    "emit_conversation_started",
    "emit_conversation_ended",
    "emit_item_acquired",
    "emit_item_lost",
    "emit_relation_changed",
    "emit_faction_state_changed",
    "emit_village_raided",
    "emit_center_besieged",
    "emit_mission_succeeded",
    "emit_mission_failed",
    "emit_caravan_created",
    "emit_caravan_destroyed",
    "emit_time_passed",
    "emit_inventory_updated",
]

_DEFAULT_SOURCE_BY_EVENT_TYPE: dict[str, str] = {
    "battle_started": "battle",
    "battle_ended": "battle",
    "agent_killed": "battle",
    "prisoner_captured": "prisoner",
    "prisoner_freed": "prisoner",
    "party_entered_center": "party",
    "conversation_started": "conversation",
    "conversation_ended": "conversation",
    "item_acquired": "item",
    "item_lost": "item",
    "relation_changed": "relation",
    "faction_state_changed": "faction",
    "village_raided": "village",
    "center_besieged": "center",
    "mission_succeeded": "mission",
    "mission_failed": "mission",
    "caravan_created": "caravan",
    "caravan_destroyed": "caravan",
    "time_passed": "time",
    "inventory_updated": "inventory",
}


def _normalize_event_type(event_type: str) -> str:
    normalized = str(event_type).strip().lower()
    normalized = normalized.replace("-", "_").replace(" ", "_").replace(".", "_")
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.strip("_")


def _normalize_source(source: str | None, *, event_type: str) -> str:
    if source is None or not str(source).strip():
        source = _DEFAULT_SOURCE_BY_EVENT_TYPE.get(event_type, "world")
    normalized = str(source).strip().lower()
    normalized = normalized.replace("-", "_").replace(" ", "_").replace(".", "_")
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.strip("_") or "world"


def _coerce_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return dict(value)


def _coerce_text_sequence(value: Sequence[str] | str | None) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in re.split(r"[|;,]", value) if part.strip())
    result: list[str] = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            result.append(text)
    return tuple(result)


def _build_event_payload(
    *,
    event_type: str,
    source: str,
    quest_id: str | None,
    stage_id: str | None,
    faction_id: str | None,
    troop_id: str | None,
    center_id: str | None,
    party_id: str | None,
    region: str | None,
    region_id: str | None,
    location_id: str | None,
    categories: Sequence[str] | str | None,
    tags: Sequence[str] | str | None,
    metadata: Mapping[str, Any] | None,
    payload: Mapping[str, Any] | None,
) -> dict[str, Any]:
    payload_dict = _coerce_mapping(payload)

    payload_dict.setdefault("event_type", event_type)
    payload_dict.setdefault("source", source)

    if quest_id is not None:
        payload_dict.setdefault("quest_id", quest_id)
        payload_dict.setdefault("quest_ids", (quest_id,))
    if stage_id is not None:
        payload_dict.setdefault("stage_id", stage_id)
        payload_dict.setdefault("stage_ids", (stage_id,))

    if faction_id is not None:
        payload_dict.setdefault("faction_id", faction_id)
        payload_dict.setdefault("faction_ids", (faction_id,))
    if troop_id is not None:
        payload_dict.setdefault("troop_id", troop_id)
        payload_dict.setdefault("troop_ids", (troop_id,))
    if center_id is not None:
        payload_dict.setdefault("center_id", center_id)
        payload_dict.setdefault("center_ids", (center_id,))
    if party_id is not None:
        payload_dict.setdefault("party_id", party_id)
        payload_dict.setdefault("party_ids", (party_id,))

    region_value = region if region not in (None, "") else region_id
    if region_value is not None:
        payload_dict.setdefault("region", region_value)
        payload_dict.setdefault("region_id", region_value)
        payload_dict.setdefault("region_ids", (region_value,))
    if location_id is not None:
        payload_dict.setdefault("location_id", location_id)
        payload_dict.setdefault("location_ids", (location_id,))

    category_values = _coerce_text_sequence(categories)
    if category_values:
        payload_dict.setdefault("event_category", category_values[0])
        payload_dict.setdefault("category", category_values[0])
        payload_dict.setdefault("topic", category_values[0])
        payload_dict.setdefault("categories", category_values)

    tag_values = _coerce_text_sequence(tags)
    if tag_values:
        payload_dict.setdefault("tags", tag_values)
        payload_dict.setdefault("topics", tag_values)
        payload_dict.setdefault("labels", tag_values)

    metadata_dict = _coerce_mapping(metadata)
    if metadata_dict:
        payload_dict.setdefault("metadata", metadata_dict)
        payload_dict.setdefault("event_metadata", metadata_dict)

    return payload_dict


def _build_world_event(
    event_type: str,
    *,
    quest_id: str | None = None,
    stage_id: str | None = None,
    source: str | None = None,
    payload: Mapping[str, Any] | None = None,
    faction_id: str | None = None,
    troop_id: str | None = None,
    center_id: str | None = None,
    party_id: str | None = None,
    region: str | None = None,
    region_id: str | None = None,
    location_id: str | None = None,
    categories: Sequence[str] | str | None = None,
    tags: Sequence[str] | str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestWorldEvent:
    canonical_event_type = _normalize_event_type(event_type)
    if not canonical_event_type:
        raise ValueError("event_type must not be empty")

    source_value = _normalize_source(source, event_type=canonical_event_type)
    event_payload = _build_event_payload(
        event_type=canonical_event_type,
        source=source_value,
        quest_id=quest_id,
        stage_id=stage_id,
        faction_id=faction_id,
        troop_id=troop_id,
        center_id=center_id,
        party_id=party_id,
        region=region,
        region_id=region_id,
        location_id=location_id,
        categories=categories,
        tags=tags,
        metadata=metadata,
        payload=payload,
    )

    helper = getattr(_quest_events, f"quest_{canonical_event_type}_event", None)
    if callable(helper):
        return helper(
            quest_id=quest_id or "",
            stage_id=stage_id,
            source=source_value,
            payload=event_payload,
            categories=categories,
            tags=tags,
            faction_id=faction_id or "",
            troop_id=troop_id or "",
            center_id=center_id or "",
            party_id=party_id or "",
            region=region if region not in (None, "") else (region_id or ""),
            region_id=region_id or "",
            location_id=location_id or "",
            metadata=_coerce_mapping(metadata),
        )

    return _quest_events.quest_world_event(
        canonical_event_type,
        quest_id=quest_id or "",
        stage_id=stage_id,
        source=source_value,
        payload=event_payload,
        faction_id=faction_id or "",
        troop_id=troop_id or "",
        center_id=center_id or "",
        party_id=party_id or "",
        region=region if region not in (None, "") else (region_id or ""),
        location_id=location_id or "",
        metadata=_coerce_mapping(metadata),
    )


def _resolve_dispatch_target(target: Any, runtime: Any, journal: Any, dispatcher: Any) -> Any:
    if target is not None:
        return target
    if runtime is not None:
        return runtime
    if journal is not None:
        return journal
    if dispatcher is not None:
        return dispatcher
    return None


def _dispatch_world_event(
    target: Any,
    event: QuestWorldEvent,
    *,
    context: Mapping[str, Any] | None = None,
    quest_id: str | None = None,
) -> Any:
    dispatch = getattr(target, "dispatch_event", None)
    if dispatch is None:
        dispatch = getattr(target, "dispatch", None)
    if dispatch is None:
        dispatch = target
    if not callable(dispatch):
        raise TypeError("target must provide dispatch_event(...), dispatch(...), or be callable")

    dispatch_kwargs: dict[str, Any] = {}
    try:
        params = signature(dispatch).parameters
    except (TypeError, ValueError):
        params = None

    accepts_var_kwargs = params is not None and any(
        parameter.kind == Parameter.VAR_KEYWORD for parameter in params.values()
    )

    if context is not None and (
        params is None or accepts_var_kwargs or "context" in params
    ):
        dispatch_kwargs["context"] = context

    if quest_id is not None and (
        params is None or accepts_var_kwargs or "quest_id" in params
    ):
        dispatch_kwargs["quest_id"] = quest_id

    try:
        return dispatch(event, **dispatch_kwargs)
    except TypeError:
        if dispatch_kwargs:
            return dispatch(event)
        raise


def emit_world_event(
    event_type: str,
    *,
    quest_id: str | None = None,
    stage_id: str | None = None,
    source: str | None = None,
    payload: Mapping[str, Any] | None = None,
    faction_id: str | None = None,
    troop_id: str | None = None,
    center_id: str | None = None,
    party_id: str | None = None,
    region: str | None = None,
    region_id: str | None = None,
    location_id: str | None = None,
    categories: Sequence[str] | str | None = None,
    tags: Sequence[str] | str | None = None,
    metadata: Mapping[str, Any] | None = None,
    target: Any = None,
    context: Mapping[str, Any] | None = None,
    runtime: Any = None,
    journal: Any = None,
    dispatcher: Any = None,
) -> Any:
    event = _build_world_event(
        event_type,
        quest_id=quest_id,
        stage_id=stage_id,
        source=source,
        payload=payload,
        faction_id=faction_id,
        troop_id=troop_id,
        center_id=center_id,
        party_id=party_id,
        region=region,
        region_id=region_id,
        location_id=location_id,
        categories=categories,
        tags=tags,
        metadata=metadata,
    )

    dispatch_target = _resolve_dispatch_target(target, runtime, journal, dispatcher)
    if dispatch_target is None:
        return event
    return _dispatch_world_event(dispatch_target, event, context=context, quest_id=quest_id)


def _make_emitter(event_type: str) -> Callable[..., Any]:
    def _emit(
        *,
        quest_id: str | None = None,
        stage_id: str | None = None,
        source: str | None = None,
        payload: Mapping[str, Any] | None = None,
        faction_id: str | None = None,
        troop_id: str | None = None,
        center_id: str | None = None,
        party_id: str | None = None,
        region: str | None = None,
        region_id: str | None = None,
        location_id: str | None = None,
        categories: Sequence[str] | str | None = None,
        tags: Sequence[str] | str | None = None,
        metadata: Mapping[str, Any] | None = None,
        target: Any = None,
        context: Mapping[str, Any] | None = None,
        runtime: Any = None,
        journal: Any = None,
        dispatcher: Any = None,
    ) -> Any:
        return emit_world_event(
            event_type,
            quest_id=quest_id,
            stage_id=stage_id,
            source=source,
            payload=payload,
            faction_id=faction_id,
            troop_id=troop_id,
            center_id=center_id,
            party_id=party_id,
            region=region,
            region_id=region_id,
            location_id=location_id,
            categories=categories,
            tags=tags,
            metadata=metadata,
            target=target,
            context=context,
            runtime=runtime,
            journal=journal,
            dispatcher=dispatcher,
        )

    _emit.__name__ = f"emit_{event_type}"
    _emit.__qualname__ = _emit.__name__
    _emit.__doc__ = f"Emit the canonical '{event_type}' quest world event."
    return _emit


emit_battle_started = _make_emitter("battle_started")
emit_battle_ended = _make_emitter("battle_ended")
emit_agent_killed = _make_emitter("agent_killed")
emit_prisoner_captured = _make_emitter("prisoner_captured")
emit_prisoner_freed = _make_emitter("prisoner_freed")
emit_party_entered_center = _make_emitter("party_entered_center")
emit_conversation_started = _make_emitter("conversation_started")
emit_conversation_ended = _make_emitter("conversation_ended")
emit_item_acquired = _make_emitter("item_acquired")
emit_item_lost = _make_emitter("item_lost")
emit_relation_changed = _make_emitter("relation_changed")
emit_faction_state_changed = _make_emitter("faction_state_changed")
emit_village_raided = _make_emitter("village_raided")
emit_center_besieged = _make_emitter("center_besieged")
emit_mission_succeeded = _make_emitter("mission_succeeded")
emit_mission_failed = _make_emitter("mission_failed")
emit_caravan_created = _make_emitter("caravan_created")
emit_caravan_destroyed = _make_emitter("caravan_destroyed")
emit_time_passed = _make_emitter("time_passed")
emit_inventory_updated = _make_emitter("inventory_updated")
