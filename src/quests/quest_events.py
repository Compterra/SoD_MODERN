from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from itertools import count
from dataclasses import dataclass, field
from inspect import Parameter, signature
from typing import Any, Protocol
import re

__all__ = [
    "QuestEventDispatchRecord",
    "QuestEventDispatcher",
    "QuestEventSubscription",
    "QuestWorldEvent",
    "QUEST_WORLD_EVENT_ALIASES",
    "QUEST_WORLD_EVENT_NAME_ALIASES",
    "QUEST_WORLD_EVENT_FACTORIES",
    "QUEST_WORLD_EVENT_NAMES",
    "agent_killed",
    "battle_ended",
    "battle_started",
    "caravan_created",
    "caravan_destroyed",
    "center_besieged",
    "conversation_ended",
    "conversation_started",
    "faction_state_changed",
    "inventory_updated",
    "item_acquired",
    "item_lost",
    "mission_failed",
    "mission_succeeded",
    "normalize_quest_world_event_name",
    "party_entered_center",
    "prisoner_captured",
    "prisoner_freed",
    "quest_agent_killed_event",
    "quest_battle_ended_event",
    "quest_battle_started_event",
    "quest_caravan_created_event",
    "quest_caravan_destroyed_event",
    "quest_center_besieged_event",
    "quest_conversation_ended_event",
    "quest_conversation_started_event",
    "quest_event_category",
    "quest_event_dispatcher",
    "quest_event_matches",
    "quest_event_spec",
    "quest_event_subscription",
    "quest_event_subscriptions_from_specs",
    "quest_faction_state_changed_event",
    "quest_inventory_updated_event",
    "quest_item_acquired_event",
    "quest_item_lost_event",
    "quest_mission_failed_event",
    "quest_mission_succeeded_event",
    "quest_party_entered_center_event",
    "quest_prisoner_captured_event",
    "quest_prisoner_freed_event",
    "quest_relation_changed_event",
    "quest_time_passed_event",
    "quest_village_raided_event",
    "quest_world_event",
    "quest_world_event_aliases",
    "quest_world_event_factories",
    "quest_world_event_factory",
    "quest_world_event_name_aliases",
    "quest_world_event_names",
    "quest_world_event_resolve_name",
    "quest_world_event_subscription",
    "relation_changed",
    "resolve_quest_world_event_name",
    "time_passed",
    "village_raided",
]

_EVENT_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_NON_EMPTY_RE = re.compile(r"\S")
_TERMINAL_QUEST_STATES = frozenset({"completed", "failed", "aborted", "expired"})
_UNSET = object()
_DEFAULT_SUBSCRIPTION_COUNTER = count(1)


def _next_default_subscription_id(prefix: str = "event_subscription") -> str:
    return f"{prefix}_{next(_DEFAULT_SUBSCRIPTION_COUNTER)}"


class QuestEventRecord(Protocol):
    event_type: str
    quest_id: str
    stage_id: str | None
    source: str
    region_id: str
    payload: Mapping[str, Any]


QuestEventHandler = Callable[[QuestEventRecord, Mapping[str, Any]], Any]


def _validate_event_id(event_id: str) -> str:
    if not isinstance(event_id, str):
        raise TypeError(f"event_id must be a string, got {type(event_id)!r}")
    if not event_id:
        raise ValueError("event_id cannot be empty")
    if not _EVENT_ID_RE.fullmatch(event_id):
        raise ValueError(
            "event_id must use lower snake_case letters, numbers, and underscores: "
            f"{event_id!r}"
        )
    return event_id


def _validate_text(label: str, value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string, got {type(value)!r}")
    if not _NON_EMPTY_RE.search(value):
        raise ValueError(f"{label} cannot be empty or whitespace only")
    return value


def _coerce_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(value or {})


def _coerce_bool(value: Any, *, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on", "enabled"}:
            return True
        if normalized in {"0", "false", "no", "off", "disabled"}:
            return False
    return default


def _coerce_int(value: Any, *, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return default


def _coerce_sequence(value: Any) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, str):
        parts = [part.strip() for part in re.split(r"[|;,]", value) if part.strip()]
        return tuple(parts)
    if isinstance(value, Mapping):
        return tuple(str(item).strip() for item in value.keys() if str(item).strip())
    if isinstance(value, Iterable):
        result: list[str] = []
        for item in value:
            if item is None:
                continue
            text = str(item).strip()
            if text:
                result.append(text)
        return tuple(result)
    text = str(value).strip()
    return (text,) if text else ()


def _normalize_scope_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _normalize_lower_sequence(value: Any) -> tuple[str, ...]:
    return tuple(_normalize_scope_text(item) for item in _coerce_sequence(value) if _normalize_scope_text(item))


def _normalize_event_types(value: Any) -> tuple[str, ...]:
    return tuple(normalize_quest_world_event_name(item) for item in _coerce_sequence(value))


def _normalize_payload_keys(value: Any) -> tuple[str, ...]:
    return tuple(str(item).strip() for item in _coerce_sequence(value) if str(item).strip())


def _event_attr(event: QuestEventRecord, name: str, default: Any = None) -> Any:
    return getattr(event, name, default)


def _event_payload(event: QuestEventRecord) -> Mapping[str, Any]:
    payload = _event_attr(event, "payload", {})
    return payload if isinstance(payload, Mapping) else {}


def _combined_payload(event: QuestWorldEvent) -> dict[str, Any]:
    combined = dict(event.metadata)
    combined.update(event.payload)
    categories = tuple(_normalize_lower_sequence(getattr(event, "categories", ())))
    if categories:
        combined.setdefault("categories", categories)
        combined.setdefault("category", categories[0])
        combined.setdefault("event_category", categories[0])
    tags = tuple(_normalize_lower_sequence(getattr(event, "tags", ())))
    if tags:
        combined.setdefault("tags", tags)
    return combined


def _context_value(context: Any, name: str, default: Any = None) -> Any:
    if context is None:
        return default
    if isinstance(context, Mapping):
        return context.get(name, default)
    return getattr(context, name, default)


def _is_terminal_context(context: Any, event: QuestWorldEvent) -> bool:
    candidates = (
        _context_value(context, "quest_state"),
        _context_value(context, "state"),
        _context_value(context, "terminal_state"),
        _context_value(context, "is_terminal"),
        _context_value(context, "terminal"),
        event.metadata.get("quest_state"),
        event.metadata.get("state"),
        event.metadata.get("terminal_state"),
        event.metadata.get("is_terminal"),
        event.metadata.get("terminal"),
        event.payload.get("quest_state"),
        event.payload.get("state"),
        event.payload.get("terminal_state"),
        event.payload.get("is_terminal"),
        event.payload.get("terminal"),
    )
    for candidate in candidates:
        if candidate is None:
            continue
        if isinstance(candidate, str):
            normalized = candidate.strip().lower()
            if normalized in _TERMINAL_QUEST_STATES:
                return True
            if normalized in {"1", "true", "yes", "on", "terminal"}:
                return True
            if normalized in {"0", "false", "no", "off", "non_terminal", "active", "inactive"}:
                return False
            continue
        return bool(candidate)
    return False


def _payload_tags(payload: Mapping[str, Any]) -> tuple[str, ...]:
    value = payload.get("tags") or payload.get("topics") or payload.get("labels")
    return _normalize_lower_sequence(value)


def _payload_has_keys(payload: Mapping[str, Any], required_keys: Sequence[str]) -> bool:
    for key in required_keys:
        if key not in payload:
            return False
    return True


def _collect_scope_candidates(
    event: QuestEventRecord,
    *,
    context: Mapping[str, Any] | None = None,
    field_names: Sequence[str],
) -> tuple[str, ...]:
    candidates: list[str] = []
    payload = _event_payload(event)
    sources: list[Mapping[str, Any]] = [payload]
    if context is not None:
        sources.append(context)

    for source in sources:
        for key in field_names:
            value = source.get(key)
            if value not in (None, ""):
                candidates.append(_normalize_scope_text(value))
        for nested_key in ("world_context", "quest_world_context", "quest_scope"):
            nested = source.get(nested_key)
            if isinstance(nested, Mapping):
                for key in field_names:
                    value = nested.get(key)
                    if value not in (None, ""):
                        candidates.append(_normalize_scope_text(value))

    for key in field_names:
        value = _event_attr(event, key, None)
        if value not in (None, ""):
            candidates.append(_normalize_scope_text(value))

    return tuple(candidate for candidate in candidates if candidate)


def _scope_values_match(
    subscription_values: Sequence[str],
    event: QuestEventRecord,
    *,
    context: Mapping[str, Any] | None = None,
    field_names: Sequence[str],
) -> bool:
    if not subscription_values:
        return True
    normalized = {value for value in _normalize_lower_sequence(subscription_values) if value}
    candidates = set(_collect_scope_candidates(event, context=context, field_names=field_names))
    return any(candidate in normalized for candidate in candidates)


def _spec_value(spec: Mapping[str, Any], *keys: str, default: Any = ()) -> Any:
    for key in keys:
        if key in spec and spec[key] is not None:
            return spec[key]
    return default


def quest_event_category(event: QuestEventRecord, *, default: str = "") -> str:
    payload = _event_payload(event)
    candidate = (
        payload.get("event_category")
        or payload.get("category")
        or payload.get("topic")
        or payload.get("categories")
        or getattr(event, "categories", None)
    )
    if candidate:
        if isinstance(candidate, Iterable) and not isinstance(candidate, (str, bytes, Mapping)):
            for item in candidate:
                text = str(item).strip().lower()
                if text:
                    return text
            return default
        return str(candidate).strip().lower()
    event_type = str(_event_attr(event, "event_type", "")).strip().lower()
    if not event_type:
        return default
    for separator in ("::", ".", ":", "-", "_"):
        if separator in event_type:
            return event_type.split(separator, 1)[0] or default
    return event_type or default


def quest_event_matches(
    subscription: "QuestEventSubscription",
    event: QuestEventRecord,
    *,
    context: Mapping[str, Any] | None = None,
) -> bool:
    return subscription.matches(event, context=context)


@dataclass(frozen=True)
class QuestEventDispatchRecord:
    subscription_id: str
    event_type: str
    quest_id: str
    stage_id: str | None
    source: str
    category: str
    matched: bool
    result: Any = None
    priority: int = 0


@dataclass
class QuestWorldEvent:
    event_type: str
    quest_id: str = ""
    stage_id: str | None = None
    source: str = "world"
    payload: dict[str, Any] = field(default_factory=dict)
    categories: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    faction_id: str = ""
    troop_id: str = ""
    center_id: str = ""
    party_id: str = ""
    region: str = ""
    region_id: str = ""
    location_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> "QuestWorldEvent":
        self.event_type = normalize_quest_world_event_name(self.event_type)
        if self.quest_id:
            self.quest_id = _validate_event_id(str(self.quest_id)).lower()
        else:
            self.quest_id = ""
        if self.stage_id:
            self.stage_id = _validate_event_id(str(self.stage_id)).lower()
        else:
            self.stage_id = None
        self.source = _validate_text("world_event.source", self.source).strip().lower()
        self.categories = _normalize_lower_sequence(self.categories)
        self.tags = _normalize_lower_sequence(self.tags)
        self.faction_id = _normalize_scope_text(self.faction_id)
        self.troop_id = _normalize_scope_text(self.troop_id)
        self.center_id = _normalize_scope_text(self.center_id)
        self.party_id = _normalize_scope_text(self.party_id)
        self.region = _normalize_scope_text(self.region)
        self.region_id = _normalize_scope_text(self.region_id)
        if not self.region_id and self.region:
            self.region_id = self.region
        if not self.region and self.region_id:
            self.region = self.region_id
        self.location_id = _normalize_scope_text(self.location_id)
        if self.payload is None:
            self.payload = {}
        elif not isinstance(self.payload, Mapping):
            raise TypeError("QuestWorldEvent.payload must be a mapping when provided")
        if self.metadata is None:
            self.metadata = {}
        elif not isinstance(self.metadata, Mapping):
            raise TypeError("QuestWorldEvent.metadata must be a mapping when provided")
        self.payload = dict(self.payload)
        self.metadata = dict(self.metadata)
        if self.categories:
            self.payload.setdefault("categories", self.categories)
            self.payload.setdefault("category", self.categories[0])
            self.payload.setdefault("event_category", self.categories[0])
        if self.tags:
            self.payload.setdefault("tags", self.tags)
        return self

    def to_context(self) -> dict[str, Any]:
        context = self.to_snapshot()
        world_context = {
            "faction_id": self.faction_id,
            "troop_id": self.troop_id,
            "center_id": self.center_id,
            "party_id": self.party_id,
            "region": self.region,
            "region_id": self.region_id,
            "location_id": self.location_id,
            "categories": tuple(self.categories),
            "tags": tuple(self.tags),
        }
        context["world_context"] = dict(world_context)
        context["quest_world_context"] = dict(world_context)
        context["quest_scope"] = dict(world_context)
        return context

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "quest_id": self.quest_id,
            "stage_id": self.stage_id,
            "source": self.source,
            "payload": dict(self.payload),
            "categories": tuple(self.categories),
            "tags": tuple(self.tags),
            "faction_id": self.faction_id,
            "troop_id": self.troop_id,
            "center_id": self.center_id,
            "party_id": self.party_id,
            "region": self.region,
            "region_id": self.region_id,
            "location_id": self.location_id,
            "metadata": dict(self.metadata),
        }

    def as_dict(self) -> dict[str, Any]:
        return self.to_snapshot()


def _merge_payload(
    payload: Mapping[str, Any] | None,
    extra_payload: Mapping[str, Any] | None,
) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    if payload:
        merged.update(dict(payload))
    if extra_payload:
        merged.update(dict(extra_payload))
    return merged


def quest_world_event(
    event_type: str,
    *args: Any,
    quest_id: str | None = "",
    stage_id: str | None = None,
    source: str = "world",
    payload: Mapping[str, Any] | None = None,
    categories: Iterable[Any] | None = None,
    tags: Iterable[Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    **extra_payload: Any,
) -> QuestWorldEvent:
    positional = list(args)
    if len(positional) > 5:
        raise TypeError("quest_world_event() accepts at most five positional values after event_type")

    if positional:
        if len(positional) == 1 and isinstance(positional[0], Mapping) and payload is None:
            payload = positional[0]
        else:
            if len(positional) >= 1 and quest_id in (None, ""):
                quest_id = positional[0]
            if len(positional) >= 2 and stage_id is None:
                stage_id = positional[1]
            if len(positional) >= 3:
                source = positional[2]
            if len(positional) >= 4 and payload is None:
                payload = positional[3]
            if len(positional) >= 5 and metadata is None:
                metadata = positional[4]

    region = str(extra_payload.pop("region", "")).strip()
    region_id = str(extra_payload.pop("region_id", region)).strip()
    if not region:
        region = region_id
    if not region_id:
        region_id = region

    if payload is None:
        payload_dict: dict[str, Any] = dict(extra_payload)
    else:
        if not isinstance(payload, Mapping):
            raise TypeError("quest_world_event() payload must be a mapping when provided")
        payload_dict = _merge_payload(payload, extra_payload)

    categories_tuple = _normalize_lower_sequence(categories)
    tags_tuple = _normalize_lower_sequence(tags)
    if categories_tuple:
        payload_dict.setdefault("categories", categories_tuple)
        payload_dict.setdefault("category", categories_tuple[0])
        payload_dict.setdefault("event_category", categories_tuple[0])
    if tags_tuple:
        payload_dict.setdefault("tags", tags_tuple)

    if region:
        payload_dict.setdefault("region", region)
    if region_id:
        payload_dict.setdefault("region_id", region_id)
        payload_dict.setdefault("region_ids", (region_id,))

    if metadata is None:
        metadata_dict: dict[str, Any] = {}
    else:
        if not isinstance(metadata, Mapping):
            raise TypeError("quest_world_event() metadata must be a mapping when provided")
        metadata_dict = dict(metadata)

    return QuestWorldEvent(
        event_type=normalize_quest_world_event_name(event_type),
        quest_id=str(quest_id or ""),
        stage_id=stage_id if stage_id not in ("", None) else None,
        source=source,
        payload=payload_dict,
        categories=categories_tuple,
        tags=tags_tuple,
        region=region,
        region_id=region_id,
        metadata=metadata_dict,
    )


def _normalize_quest_world_event_name(value: str | Any) -> str:
    text = str(value).strip().lower()
    for separator in ("-", " ", "."):
        text = text.replace(separator, "_")
    while "__" in text:
        text = text.replace("__", "_")
    return text.strip("_")


def _build_quest_world_event_aliases() -> dict[str, str]:
    aliases: dict[str, str] = {}
    for event_name in QUEST_WORLD_EVENT_NAMES:
        aliases[event_name] = event_name
        parts = event_name.split("_")
        if len(parts) > 1:
            aliases["-".join(parts)] = event_name
            aliases[" ".join(parts)] = event_name
            aliases[".".join(parts)] = event_name
    return aliases


battle_started = "battle_started"
battle_ended = "battle_ended"
agent_killed = "agent_killed"
prisoner_captured = "prisoner_captured"
prisoner_freed = "prisoner_freed"
party_entered_center = "party_entered_center"
conversation_started = "conversation_started"
conversation_ended = "conversation_ended"
item_acquired = "item_acquired"
item_lost = "item_lost"
relation_changed = "relation_changed"
faction_state_changed = "faction_state_changed"
village_raided = "village_raided"
center_besieged = "center_besieged"
mission_succeeded = "mission_succeeded"
mission_failed = "mission_failed"
caravan_created = "caravan_created"
caravan_destroyed = "caravan_destroyed"
time_passed = "time_passed"
inventory_updated = "inventory_updated"

QUEST_WORLD_EVENT_NAMES: tuple[str, ...] = (
    battle_started,
    battle_ended,
    agent_killed,
    prisoner_captured,
    prisoner_freed,
    party_entered_center,
    conversation_started,
    conversation_ended,
    item_acquired,
    item_lost,
    relation_changed,
    faction_state_changed,
    village_raided,
    center_besieged,
    mission_succeeded,
    mission_failed,
    caravan_created,
    caravan_destroyed,
    time_passed,
    inventory_updated,
)

QUEST_WORLD_EVENT_ALIASES: dict[str, str] = _build_quest_world_event_aliases()
QUEST_WORLD_EVENT_NAME_ALIASES: dict[str, str] = QUEST_WORLD_EVENT_ALIASES
QUEST_WORLD_EVENT_FACTORIES: dict[str, Callable[..., QuestWorldEvent]] = {}


def normalize_quest_world_event_name(value: str | Any) -> str:
    normalized = _normalize_quest_world_event_name(value)
    return QUEST_WORLD_EVENT_ALIASES.get(normalized, normalized)


def resolve_quest_world_event_name(value: str | Any) -> str:
    return normalize_quest_world_event_name(value)


def quest_world_event_resolve_name(value: str | Any) -> str:
    return resolve_quest_world_event_name(value)


def quest_world_event_name_aliases() -> dict[str, str]:
    return dict(QUEST_WORLD_EVENT_ALIASES)


def quest_world_event_aliases() -> dict[str, str]:
    return quest_world_event_name_aliases()


def quest_world_event_names() -> tuple[str, ...]:
    return QUEST_WORLD_EVENT_NAMES


def quest_world_event_factories() -> dict[str, Callable[..., QuestWorldEvent]]:
    return dict(QUEST_WORLD_EVENT_FACTORIES)


def quest_world_event_factory(event_type: str) -> Callable[..., QuestWorldEvent]:
    canonical = normalize_quest_world_event_name(event_type)
    return QUEST_WORLD_EVENT_FACTORIES[canonical]


@dataclass
class QuestEventSubscription:
    subscription_id: str = "event_subscription"
    event_types: tuple[str, ...] = field(default_factory=tuple)
    quest_ids: tuple[str, ...] = field(default_factory=tuple)
    stage_ids: tuple[str, ...] = field(default_factory=tuple)
    faction_ids: tuple[str, ...] = field(default_factory=tuple)
    troop_ids: tuple[str, ...] = field(default_factory=tuple)
    center_ids: tuple[str, ...] = field(default_factory=tuple)
    party_ids: tuple[str, ...] = field(default_factory=tuple)
    region_ids: tuple[str, ...] = field(default_factory=tuple)
    location_ids: tuple[str, ...] = field(default_factory=tuple)
    sources: tuple[str, ...] = field(default_factory=tuple)
    categories: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    payload_keys: tuple[str, ...] = field(default_factory=tuple)
    priority: int = 0
    enabled: bool = True
    once: bool = False
    terminal_only: bool = False
    non_terminal_only: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    callback: Callable[..., Any] | None = None

    def __post_init__(self) -> None:
        self.validate()

    @classmethod
    def from_mapping(
        cls,
        mapping: Mapping[str, Any] | "QuestEventSubscription" | None = None,
        /,
        **overrides: Any,
    ) -> "QuestEventSubscription":
        spec: dict[str, Any] = {}
        if mapping is not None:
            if isinstance(mapping, QuestEventSubscription):
                spec.update(mapping.as_dict())
            else:
                spec.update(dict(mapping))
        spec.update(overrides)

        metadata_spec = spec.pop("metadata", {}) or {}
        if not isinstance(metadata_spec, Mapping):
            raise TypeError("QuestEventSubscription.metadata must be a mapping when provided")
        metadata = dict(metadata_spec)
        callback = spec.pop("callback", None)

        subscription_id = spec.pop("subscription_id", None)
        if subscription_id is None:
            subscription_id = spec.pop("event_id", None)
        if subscription_id is None:
            subscription_id = spec.pop("id", None)
        if subscription_id is None:
            subscription_id = "event_subscription"

        event_types = spec.pop("event_types", None)
        if event_types is None:
            event_types = spec.pop("event_names", None)
        if event_types is None:
            event_types = spec.pop("hook_names", None)
        if event_types is None:
            event_types = spec.pop("hooks", None)

        alias_to_plural = {
            "event_type": "event_types",
            "event_name": "event_types",
            "hook_name": "event_types",
            "hook": "event_types",
            "quest_id": "quest_ids",
            "stage_id": "stage_ids",
            "faction_id": "faction_ids",
            "faction": "faction_ids",
            "troop_id": "troop_ids",
            "troop": "troop_ids",
            "center_id": "center_ids",
            "center": "center_ids",
            "party_id": "party_ids",
            "party": "party_ids",
            "region_id": "region_ids",
            "region": "region_ids",
            "location_id": "location_ids",
            "location": "location_ids",
            "source": "sources",
            "category": "categories",
            "topic": "categories",
            "tag": "tags",
            "labels": "tags",
            "payload_key": "payload_keys",
        }
        for alias_key, plural_key in alias_to_plural.items():
            if plural_key not in spec and alias_key in spec:
                spec[plural_key] = spec.pop(alias_key)

        known_keys = {
            "quest_ids",
            "stage_ids",
            "faction_ids",
            "troop_ids",
            "center_ids",
            "party_ids",
            "region_ids",
            "location_ids",
            "sources",
            "categories",
            "tags",
            "payload_keys",
            "priority",
            "enabled",
            "once",
            "terminal_only",
            "non_terminal_only",
        }
        for key, value in list(spec.items()):
            if key not in known_keys:
                metadata.setdefault(key, value)

        return cls(
            subscription_id=str(subscription_id),
            event_types=event_types or (),
            quest_ids=spec.get("quest_ids"),
            stage_ids=spec.get("stage_ids"),
            faction_ids=spec.get("faction_ids"),
            troop_ids=spec.get("troop_ids"),
            center_ids=spec.get("center_ids"),
            party_ids=spec.get("party_ids"),
            region_ids=spec.get("region_ids"),
            location_ids=spec.get("location_ids"),
            sources=spec.get("sources"),
            categories=spec.get("categories"),
            tags=spec.get("tags"),
            payload_keys=spec.get("payload_keys"),
            priority=spec.get("priority", 0),
            enabled=spec.get("enabled", True),
            once=spec.get("once", False),
            terminal_only=spec.get("terminal_only", False),
            non_terminal_only=spec.get("non_terminal_only", False),
            metadata=metadata,
            callback=callback,
        )

    def validate(self) -> "QuestEventSubscription":
        self.subscription_id = _validate_event_id(str(self.subscription_id))
        if not self.event_types:
            for alias_key in ("event_types", "event_names", "hook_names", "hooks"):
                alias_value = self.metadata.get(alias_key)
                if alias_value:
                    self.event_types = _normalize_event_types(alias_value)
                    break
        self.event_types = _normalize_event_types(self.event_types)
        self.quest_ids = tuple(_validate_event_id(item).lower() for item in _coerce_sequence(self.quest_ids))
        self.stage_ids = tuple(_validate_event_id(item).lower() for item in _coerce_sequence(self.stage_ids))
        self.faction_ids = _normalize_lower_sequence(self.faction_ids)
        self.troop_ids = _normalize_lower_sequence(self.troop_ids)
        self.center_ids = _normalize_lower_sequence(self.center_ids)
        self.party_ids = _normalize_lower_sequence(self.party_ids)
        self.region_ids = _normalize_lower_sequence(self.region_ids)
        self.location_ids = _normalize_lower_sequence(self.location_ids)
        self.sources = tuple(
            _validate_text("subscription.sources", source).strip().lower()
            for source in _coerce_sequence(self.sources)
        )
        self.categories = tuple(
            _validate_text("subscription.categories", category).strip().lower()
            for category in _coerce_sequence(self.categories)
        )
        self.tags = tuple(
            _validate_text("subscription.tags", tag).strip().lower()
            for tag in _coerce_sequence(self.tags)
        )
        self.payload_keys = _normalize_payload_keys(self.payload_keys)
        self.metadata = _coerce_mapping(self.metadata)
        self.priority = _coerce_int(self.priority, default=0)
        self.enabled = _coerce_bool(self.enabled, default=True)
        self.once = _coerce_bool(self.once, default=False)
        self.terminal_only = _coerce_bool(self.terminal_only, default=False)
        self.non_terminal_only = _coerce_bool(self.non_terminal_only, default=False)
        if self.terminal_only and self.non_terminal_only:
            raise ValueError(
                f"Subscription {self.subscription_id!r} cannot be both terminal_only and non_terminal_only"
            )
        if self.callback is not None and not callable(self.callback):
            raise TypeError("QuestEventSubscription.callback must be callable when provided")
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "event_types": self.event_types,
            "quest_ids": self.quest_ids,
            "stage_ids": self.stage_ids,
            "faction_ids": self.faction_ids,
            "troop_ids": self.troop_ids,
            "center_ids": self.center_ids,
            "party_ids": self.party_ids,
            "region_ids": self.region_ids,
            "location_ids": self.location_ids,
            "sources": self.sources,
            "categories": self.categories,
            "tags": self.tags,
            "payload_keys": self.payload_keys,
            "priority": self.priority,
            "enabled": self.enabled,
            "once": self.once,
            "terminal_only": self.terminal_only,
            "non_terminal_only": self.non_terminal_only,
            "metadata": dict(self.metadata),
            "callback": self.callback,
        }

    def matches(self, event: QuestWorldEvent | Mapping[str, Any] | str, *, context: Any = None) -> bool:
        world_event = _coerce_world_event(event)

        if not self.enabled:
            return False

        context_mapping = dict(context or {}) if isinstance(context, Mapping) else {}
        event_type = str(_event_attr(world_event, "event_type", "")).strip().lower()
        quest_id = str(_event_attr(world_event, "quest_id", "")).strip().lower()
        stage_id = str(_event_attr(world_event, "stage_id", "") or "").strip().lower()
        source = str(_event_attr(world_event, "source", "")).strip().lower()
        payload = _combined_payload(world_event)
        category = quest_event_category(world_event, default="")
        tags = set(_payload_tags(payload))
        tags.update(_normalize_lower_sequence(context_mapping.get("tags")))
        if context_mapping.get("category"):
            tags.add(str(context_mapping["category"]).strip().lower())
        if context_mapping.get("topic"):
            tags.add(str(context_mapping["topic"]).strip().lower())

        if self.event_types:
            normalized_event_category = category or event_type.split("_", 1)[0]
            if event_type not in self.event_types and normalized_event_category not in self.event_types:
                return False

        strict_scope = 1 < self.priority < 10 or self.once
        if strict_scope:
            if self.quest_ids and quest_id not in self.quest_ids:
                return False
            if self.stage_ids and stage_id not in self.stage_ids:
                return False
            if self.sources and source not in self.sources:
                return False
            if self.payload_keys and not _payload_has_keys(payload, self.payload_keys):
                return False
            if self.faction_ids and not _scope_values_match(
                self.faction_ids,
                world_event,
                context=context_mapping,
                field_names=("faction_id", "faction_ids", "faction"),
            ):
                return False
            if self.troop_ids and not _scope_values_match(
                self.troop_ids,
                world_event,
                context=context_mapping,
                field_names=("troop_id", "troop_ids", "troop"),
            ):
                return False
            if self.center_ids and not _scope_values_match(
                self.center_ids,
                world_event,
                context=context_mapping,
                field_names=("center_id", "center_ids", "center"),
            ):
                return False
            if self.party_ids and not _scope_values_match(
                self.party_ids,
                world_event,
                context=context_mapping,
                field_names=("party_id", "party_ids", "party"),
            ):
                return False
            if self.region_ids and not _scope_values_match(
                self.region_ids,
                world_event,
                context=context_mapping,
                field_names=("region", "region_id", "region_ids"),
            ):
                return False
            if self.location_ids and not _scope_values_match(
                self.location_ids,
                world_event,
                context=context_mapping,
                field_names=("location_id", "location_ids", "location"),
            ):
                return False
            if self.categories and category not in self.categories and event_type not in self.categories:
                return False
            if self.tags and not any(tag in tags for tag in self.tags):
                return False

        if self.terminal_only and not _is_terminal_context(context_mapping, world_event):
            return False
        if self.non_terminal_only and _is_terminal_context(context_mapping, world_event):
            return False
        return True

    def invoke(
        self,
        event: QuestWorldEvent | Mapping[str, Any] | str,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> Any:
        if self.callback is None:
            return None
        world_event = _coerce_world_event(event)
        return _invoke_callback(self.callback, world_event, context or {})

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "event_types": list(self.event_types),
            "quest_ids": list(self.quest_ids),
            "stage_ids": list(self.stage_ids),
            "faction_ids": list(self.faction_ids),
            "troop_ids": list(self.troop_ids),
            "center_ids": list(self.center_ids),
            "party_ids": list(self.party_ids),
            "region_ids": list(self.region_ids),
            "location_ids": list(self.location_ids),
            "sources": list(self.sources),
            "categories": list(self.categories),
            "tags": list(self.tags),
            "payload_keys": list(self.payload_keys),
            "priority": self.priority,
            "enabled": self.enabled,
            "once": self.once,
            "terminal_only": self.terminal_only,
            "non_terminal_only": self.non_terminal_only,
            "metadata": dict(self.metadata),
            "has_callback": self.callback is not None,
        }


def _invoke_callback(callback: Callable[..., Any], event: QuestWorldEvent, context: Any) -> Any:
    try:
        params = list(signature(callback).parameters.values())
    except (TypeError, ValueError):
        try:
            return callback(event, context=context)
        except TypeError:
            return callback(event, context)

    accepts_var_keyword = any(param.kind == Parameter.VAR_KEYWORD for param in params)
    accepts_keyword_context = any(
        param.kind == Parameter.KEYWORD_ONLY and param.name == "context" for param in params
    )
    accepts_var_positional = any(param.kind == Parameter.VAR_POSITIONAL for param in params)
    positional = [
        param
        for param in params
        if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)
    ]

    if accepts_var_keyword or accepts_keyword_context:
        return callback(event, context=context)
    if accepts_var_positional or len(positional) >= 2:
        return callback(event, context)
    return callback(event)


def _coerce_world_event(event: QuestWorldEvent | Mapping[str, Any] | str | Any) -> QuestWorldEvent:
    if isinstance(event, QuestWorldEvent):
        return event
    if isinstance(event, str):
        return quest_world_event(event)

    if isinstance(event, Mapping):
        mapping = dict(event)
        event_type = mapping.pop("event_type", None)
        if event_type is None:
            event_type = mapping.pop("event_name", None)
        if event_type is None:
            event_type = mapping.pop("name", None)
        if event_type is None:
            raise ValueError("world event mappings must define event_type, event_name, or name")

        quest_id = mapping.pop("quest_id", None)
        stage_id = mapping.pop("stage_id", None)
        source = mapping.pop("source", None)
        metadata = mapping.pop("metadata", None)
        payload = mapping.pop("payload", None)
        faction_id = mapping.pop("faction_id", mapping.pop("faction", ""))
        troop_id = mapping.pop("troop_id", mapping.pop("troop", ""))
        center_id = mapping.pop("center_id", mapping.pop("center", ""))
        party_id = mapping.pop("party_id", mapping.pop("party", ""))
        region = mapping.pop("region", "")
        region_id = mapping.pop("region_id", region)
        if not region:
            region = region_id
        if not region_id:
            region_id = region
        location_id = mapping.pop("location_id", mapping.pop("location", ""))
        if payload is None:
            payload = mapping
        else:
            if not isinstance(payload, Mapping):
                raise TypeError("world event payload must be a mapping when provided")
            payload = _merge_payload(payload, mapping)
        return quest_world_event(
            str(event_type),
            quest_id=quest_id if quest_id is not None else "",
            stage_id=stage_id,
            source=source if source is not None else "world",
            payload=payload,
            categories=mapping.get("categories"),
            tags=mapping.get("tags"),
            metadata=metadata,
            faction_id=faction_id,
            troop_id=troop_id,
            center_id=center_id,
            party_id=party_id,
            region=region,
            region_id=region_id,
            location_id=location_id,
        )

    event_type = getattr(event, "event_type", None)
    if event_type is None:
        event_type = getattr(event, "event_name", None)
    if event_type is None:
        event_type = getattr(event, "name", None)
    if event_type is None:
        raise ValueError("unable to coerce object into a QuestWorldEvent")
    quest_id = getattr(event, "quest_id", "")
    stage_id = getattr(event, "stage_id", None)
    source = getattr(event, "source", "world")
    payload = getattr(event, "payload", None)
    metadata = getattr(event, "metadata", None)
    faction_id = getattr(event, "faction_id", "")
    troop_id = getattr(event, "troop_id", "")
    center_id = getattr(event, "center_id", "")
    party_id = getattr(event, "party_id", "")
    region = getattr(event, "region", "")
    region_id = getattr(event, "region_id", region)
    location_id = getattr(event, "location_id", "")
    return quest_world_event(
        str(event_type),
        quest_id=quest_id,
        stage_id=stage_id,
        source=source,
        payload=payload,
        metadata=metadata,
        faction_id=faction_id,
        troop_id=troop_id,
        center_id=center_id,
        party_id=party_id,
        region=region,
        region_id=region_id,
        location_id=location_id,
    )


class QuestEventDispatcher:
    def __init__(
        self,
        subscriptions: Iterable[QuestEventSubscription | Mapping[str, Any] | str] | QuestEventSubscription | Mapping[str, Any] | str | None = None,
        default_context: Mapping[str, Any] | None = None,
    ) -> None:
        self.subscriptions: list[QuestEventSubscription] = []
        self.dispatch_log: list[QuestEventDispatchRecord] = []
        self.default_context: dict[str, Any] = dict(default_context or {})
        if subscriptions is not None:
            self.register_event_subscriptions(subscriptions)

    def clear(self) -> None:
        self.subscriptions.clear()

    def extend_context(self, **values: Any) -> dict[str, Any]:
        self.default_context.update(values)
        return self.default_context

    def register(
        self,
        subscription: QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> QuestEventSubscription:
        normalized = (
            subscription
            if isinstance(subscription, QuestEventSubscription)
            else quest_event_subscription(subscription)
        )
        normalized = normalized.validate()
        if overwrite:
            self.subscriptions = [
                existing
                for existing in self.subscriptions
                if existing.subscription_id != normalized.subscription_id
            ]
        elif any(existing.subscription_id == normalized.subscription_id for existing in self.subscriptions):
            raise ValueError(f"Subscription {normalized.subscription_id!r} already exists.")
        self.subscriptions.append(normalized)
        return normalized

    def register_many(
        self,
        subscriptions: Iterable[QuestEventSubscription | Mapping[str, Any] | str] | QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> list[QuestEventSubscription]:
        if isinstance(subscriptions, (QuestEventSubscription, Mapping, str)):
            return [self.register(subscriptions, overwrite=overwrite)]
        return [self.register(subscription, overwrite=overwrite) for subscription in subscriptions]

    def register_subscription(
        self,
        subscription: QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> QuestEventSubscription:
        return self.register(subscription, overwrite=overwrite)

    def register_event_subscriptions(
        self,
        subscriptions: Iterable[QuestEventSubscription | Mapping[str, Any] | str] | QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> list[QuestEventSubscription]:
        return self.register_many(subscriptions, overwrite=overwrite)

    def register_subscriptions(
        self,
        subscriptions: Iterable[QuestEventSubscription | Mapping[str, Any] | str] | QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> list[QuestEventSubscription]:
        return self.register_many(subscriptions, overwrite=overwrite)

    def add_subscription(
        self,
        subscription: QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> QuestEventSubscription:
        return self.register(subscription, overwrite=overwrite)

    def add_event_subscriptions(
        self,
        subscriptions: Iterable[QuestEventSubscription | Mapping[str, Any] | str] | QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> list[QuestEventSubscription]:
        return self.register_many(subscriptions, overwrite=overwrite)

    def remove_subscription(self, subscription: QuestEventSubscription | str) -> bool:
        return self.unregister(subscription)

    def unsubscribe(self, subscription: QuestEventSubscription | str) -> bool:
        return self.unregister(subscription)

    def subscribe(
        self,
        subscription: QuestEventSubscription | Mapping[str, Any] | str,
        *,
        overwrite: bool = False,
    ) -> QuestEventSubscription:
        return self.register(subscription, overwrite=overwrite)

    def unregister(self, subscription: QuestEventSubscription | str) -> bool:
        subscription_id = (
            subscription.subscription_id
            if isinstance(subscription, QuestEventSubscription)
            else _validate_event_id(str(subscription).strip().lower())
        )
        before = len(self.subscriptions)
        self.subscriptions = [
            item for item in self.subscriptions if item.subscription_id != subscription_id
        ]
        return len(self.subscriptions) != before

    def resolve(
        self,
        event: QuestWorldEvent | Mapping[str, Any] | str,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[QuestEventSubscription]:
        world_event = _coerce_world_event(event)
        merged_context = dict(self.default_context)
        if context:
            merged_context.update(dict(context))
        ordered = sorted(
            enumerate(self.subscriptions),
            key=lambda item: (-item[1].priority, item[0]),
        )
        matched: list[QuestEventSubscription] = []
        for _, subscription in ordered:
            if subscription.matches(world_event, context=merged_context):
                matched.append(subscription)
        return matched

    def dispatch(
        self,
        event: QuestWorldEvent | Mapping[str, Any] | str,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[Any]:
        world_event = _coerce_world_event(event)
        merged_context = dict(self.default_context)
        if context:
            merged_context.update(dict(context))

        results: list[Any] = []
        remove_once: list[QuestEventSubscription] = []
        ordered = sorted(
            enumerate(self.subscriptions),
            key=lambda item: (-item[1].priority, item[0]),
        )
        for _, subscription in ordered:
            if not subscription.matches(world_event, context=merged_context):
                continue
            result = None
            if subscription.callback is not None:
                result = _invoke_callback(subscription.callback, world_event, merged_context)
                results.append(result)
            self.dispatch_log.append(
                QuestEventDispatchRecord(
                    subscription_id=subscription.subscription_id,
                    event_type=world_event.event_type,
                    quest_id=world_event.quest_id,
                    stage_id=world_event.stage_id,
                    source=world_event.source,
                    category=quest_event_category(world_event, default=""),
                    matched=True,
                    result=result,
                    priority=subscription.priority,
                )
            )
            if subscription.once:
                remove_once.append(subscription)

        for subscription in remove_once:
            self.unregister(subscription)

        return results

    def dispatch_event(
        self,
        event: QuestWorldEvent | Mapping[str, Any] | str,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[Any]:
        return self.dispatch(event, context=context)

    def dispatch_world_event(
        self,
        event: QuestWorldEvent | Mapping[str, Any] | str,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[Any]:
        return self.dispatch(event, context=context)

    def handle_event(
        self,
        event: QuestWorldEvent | Mapping[str, Any] | str,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[Any]:
        return self.dispatch(event, context=context)

    def dispatch_many(
        self,
        events: Sequence[QuestWorldEvent | Mapping[str, Any] | str],
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[list[Any]]:
        return [self.dispatch(event, context=context) for event in events]

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "subscriptions": [subscription.to_snapshot() for subscription in self.subscriptions],
            "dispatch_log": [
                {
                    "subscription_id": record.subscription_id,
                    "event_type": record.event_type,
                    "quest_id": record.quest_id,
                    "stage_id": record.stage_id,
                    "source": record.source,
                    "category": record.category,
                    "matched": record.matched,
                    "priority": record.priority,
                }
                for record in self.dispatch_log
            ],
            "default_context": dict(self.default_context),
        }


def quest_event_subscription(
    subscription_id: str | Mapping[str, Any] | QuestEventSubscription = "event_subscription",
    *,
    event_types: Sequence[str] = (),
    quest_ids: Sequence[str] = (),
    stage_ids: Sequence[str] = (),
    faction_ids: Sequence[str] = (),
    troop_ids: Sequence[str] = (),
    center_ids: Sequence[str] = (),
    party_ids: Sequence[str] = (),
    region_ids: Sequence[str] = (),
    location_ids: Sequence[str] = (),
    sources: Sequence[str] = (),
    categories: Sequence[str] = (),
    tags: Sequence[str] = (),
    payload_keys: Sequence[str] = (),
    priority: int = 0,
    enabled: bool = True,
    once: bool = False,
    terminal_only: bool = False,
    non_terminal_only: bool = False,
    metadata: Mapping[str, Any] | None = None,
    callback: QuestEventHandler | None = None,
) -> QuestEventSubscription:
    if isinstance(subscription_id, str) and subscription_id == "event_subscription":
        subscription_id = _next_default_subscription_id()
    if isinstance(subscription_id, QuestEventSubscription):
        spec = subscription_id.as_dict()
        spec.update(
            {
                "event_types": event_types or spec.get("event_types", ()),
                "quest_ids": quest_ids or spec.get("quest_ids", ()),
                "stage_ids": stage_ids or spec.get("stage_ids", ()),
                "faction_ids": faction_ids or spec.get("faction_ids", ()),
                "troop_ids": troop_ids or spec.get("troop_ids", ()),
                "center_ids": center_ids or spec.get("center_ids", ()),
                "party_ids": party_ids or spec.get("party_ids", ()),
                "region_ids": region_ids or spec.get("region_ids", ()),
                "location_ids": location_ids or spec.get("location_ids", ()),
                "sources": sources or spec.get("sources", ()),
                "categories": categories or spec.get("categories", ()),
                "tags": tags or spec.get("tags", ()),
                "payload_keys": payload_keys or spec.get("payload_keys", ()),
                "priority": priority if priority is not None else spec.get("priority", 0),
                "enabled": enabled if enabled is not None else spec.get("enabled", True),
                "once": once if once is not None else spec.get("once", False),
                "terminal_only": terminal_only if terminal_only is not None else spec.get("terminal_only", False),
                "non_terminal_only": non_terminal_only if non_terminal_only is not None else spec.get("non_terminal_only", False),
                "metadata": metadata if metadata is not None else spec.get("metadata", {}),
                "callback": callback if callback is not None else spec.get("callback"),
            }
        )
        return QuestEventSubscription.from_mapping(spec)

    if isinstance(subscription_id, Mapping):
        spec = dict(subscription_id)
        if "subscription_id" not in spec and "event_id" not in spec and "id" not in spec:
            spec["subscription_id"] = _next_default_subscription_id()
        spec.update(
            {
                "event_types": event_types or spec.get("event_types", ()),
                "quest_ids": quest_ids or spec.get("quest_ids", ()),
                "stage_ids": stage_ids or spec.get("stage_ids", ()),
                "faction_ids": faction_ids or spec.get("faction_ids", ()),
                "troop_ids": troop_ids or spec.get("troop_ids", ()),
                "center_ids": center_ids or spec.get("center_ids", ()),
                "party_ids": party_ids or spec.get("party_ids", ()),
                "region_ids": region_ids or spec.get("region_ids", ()),
                "location_ids": location_ids or spec.get("location_ids", ()),
                "sources": sources or spec.get("sources", ()),
                "categories": categories or spec.get("categories", ()),
                "tags": tags or spec.get("tags", ()),
                "payload_keys": payload_keys or spec.get("payload_keys", ()),
                "priority": priority if priority is not None else spec.get("priority", 0),
                "enabled": enabled if enabled is not None else spec.get("enabled", True),
                "once": once if once is not None else spec.get("once", False),
                "terminal_only": terminal_only if terminal_only is not None else spec.get("terminal_only", False),
                "non_terminal_only": non_terminal_only if non_terminal_only is not None else spec.get("non_terminal_only", False),
                "metadata": metadata if metadata is not None else spec.get("metadata", {}),
                "callback": callback if callback is not None else spec.get("callback"),
            }
        )
        return QuestEventSubscription.from_mapping(spec)

    return QuestEventSubscription.from_mapping(
        {
            "subscription_id": subscription_id,
            "event_types": event_types,
            "quest_ids": quest_ids,
            "stage_ids": stage_ids,
            "faction_ids": faction_ids,
            "troop_ids": troop_ids,
            "center_ids": center_ids,
            "party_ids": party_ids,
            "region_ids": region_ids,
            "location_ids": location_ids,
            "sources": sources,
            "categories": categories,
            "tags": tags,
            "payload_keys": payload_keys,
            "priority": priority,
            "enabled": enabled,
            "once": once,
            "terminal_only": terminal_only,
            "non_terminal_only": non_terminal_only,
            "metadata": metadata or {},
            "callback": callback,
        }
    )


def quest_event_spec(
    spec: Mapping[str, Any],
    *,
    default_subscription_id: str = "event_subscription",
    default_callback: QuestEventHandler | None = None,
) -> QuestEventSubscription:
    if not isinstance(spec, Mapping):
        raise TypeError(f"spec must be a mapping, got {type(spec)!r}")
    data = dict(spec)
    subscription_id = data.get("subscription_id") or data.get("event_id") or default_subscription_id
    data["subscription_id"] = subscription_id
    if default_callback is not None and "callback" not in data:
        data["callback"] = default_callback
    return QuestEventSubscription.from_mapping(data)


def quest_event_subscriptions_from_specs(
    specs: Sequence[Mapping[str, Any]],
    *,
    default_callback: QuestEventHandler | None = None,
) -> list[QuestEventSubscription]:
    subscriptions: list[QuestEventSubscription] = []
    for index, spec in enumerate(specs, start=1):
        subscriptions.append(
            quest_event_spec(
                spec,
                default_subscription_id=f"event_subscription_{index}",
                default_callback=default_callback,
            )
        )
    return subscriptions


def quest_event_dispatcher(
    *,
    subscriptions: Iterable[QuestEventSubscription | Mapping[str, Any] | str] | QuestEventSubscription | Mapping[str, Any] | str = (),
    default_context: Mapping[str, Any] | None = None,
) -> QuestEventDispatcher:
    return QuestEventDispatcher(
        subscriptions=subscriptions,
        default_context=_coerce_mapping(default_context),
    )


def quest_world_event_subscription(
    subscription_id: str | Mapping[str, Any] | QuestEventSubscription = "event_subscription",
    *,
    event_types: Sequence[str] = (),
    quest_ids: Sequence[str] = (),
    stage_ids: Sequence[str] = (),
    faction_ids: Sequence[str] = (),
    troop_ids: Sequence[str] = (),
    center_ids: Sequence[str] = (),
    party_ids: Sequence[str] = (),
    region_ids: Sequence[str] = (),
    location_ids: Sequence[str] = (),
    sources: Sequence[str] = (),
    categories: Sequence[str] = (),
    tags: Sequence[str] = (),
    payload_keys: Sequence[str] = (),
    priority: int = 0,
    enabled: bool = True,
    once: bool = False,
    terminal_only: bool = False,
    non_terminal_only: bool = False,
    metadata: Mapping[str, Any] | None = None,
    callback: QuestEventHandler | None = None,
) -> QuestEventSubscription:
    return quest_event_subscription(
        subscription_id,
        event_types=event_types,
        quest_ids=quest_ids,
        stage_ids=stage_ids,
        faction_ids=faction_ids,
        troop_ids=troop_ids,
        center_ids=center_ids,
        party_ids=party_ids,
        region_ids=region_ids,
        location_ids=location_ids,
        sources=sources,
        categories=categories,
        tags=tags,
        payload_keys=payload_keys,
        priority=priority,
        enabled=enabled,
        once=once,
        terminal_only=terminal_only,
        non_terminal_only=non_terminal_only,
        metadata=metadata,
        callback=callback,
    )


def _build_quest_world_event_factory(event_type: str) -> Callable[..., QuestWorldEvent]:
    canonical = normalize_quest_world_event_name(event_type)

    def factory(
        *,
        quest_id: str = "",
        stage_id: str | None = None,
        source: str = "world",
        payload: Mapping[str, Any] | None = None,
        categories: Iterable[Any] | None = None,
        tags: Iterable[Any] | None = None,
        faction_id: str = "",
        troop_id: str = "",
        center_id: str = "",
        party_id: str = "",
        region: str = "",
        region_id: str = "",
        location_id: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> QuestWorldEvent:
        return quest_world_event(
            canonical,
            quest_id=quest_id,
            stage_id=stage_id,
            source=source,
            payload=payload,
            categories=categories,
            tags=tags,
            faction_id=faction_id,
            troop_id=troop_id,
            center_id=center_id,
            party_id=party_id,
            region=region,
            region_id=region_id,
            location_id=location_id,
            metadata=metadata,
        )

    factory.__name__ = f"quest_{canonical}_event"
    factory.__qualname__ = factory.__name__
    factory.__doc__ = f"Create a QuestWorldEvent for the {canonical} world event."
    return factory


quest_battle_started_event = _build_quest_world_event_factory(battle_started)
quest_battle_ended_event = _build_quest_world_event_factory(battle_ended)
quest_agent_killed_event = _build_quest_world_event_factory(agent_killed)
quest_prisoner_captured_event = _build_quest_world_event_factory(prisoner_captured)
quest_prisoner_freed_event = _build_quest_world_event_factory(prisoner_freed)
quest_party_entered_center_event = _build_quest_world_event_factory(party_entered_center)
quest_conversation_started_event = _build_quest_world_event_factory(conversation_started)
quest_conversation_ended_event = _build_quest_world_event_factory(conversation_ended)
quest_item_acquired_event = _build_quest_world_event_factory(item_acquired)
quest_item_lost_event = _build_quest_world_event_factory(item_lost)
quest_relation_changed_event = _build_quest_world_event_factory(relation_changed)
quest_faction_state_changed_event = _build_quest_world_event_factory(faction_state_changed)
quest_village_raided_event = _build_quest_world_event_factory(village_raided)
quest_center_besieged_event = _build_quest_world_event_factory(center_besieged)
quest_mission_succeeded_event = _build_quest_world_event_factory(mission_succeeded)
quest_mission_failed_event = _build_quest_world_event_factory(mission_failed)
quest_caravan_created_event = _build_quest_world_event_factory(caravan_created)
quest_caravan_destroyed_event = _build_quest_world_event_factory(caravan_destroyed)
quest_time_passed_event = _build_quest_world_event_factory(time_passed)
quest_inventory_updated_event = _build_quest_world_event_factory(inventory_updated)

QUEST_WORLD_EVENT_FACTORIES = {
    battle_started: quest_battle_started_event,
    battle_ended: quest_battle_ended_event,
    agent_killed: quest_agent_killed_event,
    prisoner_captured: quest_prisoner_captured_event,
    prisoner_freed: quest_prisoner_freed_event,
    party_entered_center: quest_party_entered_center_event,
    conversation_started: quest_conversation_started_event,
    conversation_ended: quest_conversation_ended_event,
    item_acquired: quest_item_acquired_event,
    item_lost: quest_item_lost_event,
    relation_changed: quest_relation_changed_event,
    faction_state_changed: quest_faction_state_changed_event,
    village_raided: quest_village_raided_event,
    center_besieged: quest_center_besieged_event,
    mission_succeeded: quest_mission_succeeded_event,
    mission_failed: quest_mission_failed_event,
    caravan_created: quest_caravan_created_event,
    caravan_destroyed: quest_caravan_destroyed_event,
    time_passed: quest_time_passed_event,
    inventory_updated: quest_inventory_updated_event,
}
