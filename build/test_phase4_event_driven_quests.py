from __future__ import annotations

import inspect
import sys
import unittest
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.quests.quest_event_sources import (
    emit_agent_killed,
    emit_battle_ended,
    emit_battle_started,
    emit_caravan_created,
    emit_caravan_destroyed,
    emit_center_besieged,
    emit_conversation_ended,
    emit_conversation_started,
    emit_faction_state_changed,
    emit_inventory_updated,
    emit_item_acquired,
    emit_item_lost,
    emit_mission_failed,
    emit_mission_succeeded,
    emit_party_entered_center,
    emit_prisoner_captured,
    emit_prisoner_freed,
    emit_relation_changed,
    emit_time_passed,
    emit_village_raided,
    emit_world_event,
)
from src.quests.quest_events import (
    QuestEventDispatcher,
    QuestEventSubscription,
    QuestWorldEvent,
    quest_event_subscription,
    quest_world_event,
    quest_world_event_factories,
    quest_world_event_names,
)
from src.quests.quest_runtime import QuestJournal, QuestRuntime


EVENT_NAMES: tuple[str, ...] = (
    "battle_started",
    "battle_ended",
    "agent_killed",
    "prisoner_captured",
    "prisoner_freed",
    "party_entered_center",
    "conversation_started",
    "conversation_ended",
    "item_acquired",
    "item_lost",
    "relation_changed",
    "faction_state_changed",
    "village_raided",
    "center_besieged",
    "mission_succeeded",
    "mission_failed",
    "caravan_created",
    "caravan_destroyed",
    "time_passed",
    "inventory_updated",
)

SOURCE_HELPERS: dict[str, Callable[..., Any]] = {
    "battle_started": emit_battle_started,
    "battle_ended": emit_battle_ended,
    "agent_killed": emit_agent_killed,
    "prisoner_captured": emit_prisoner_captured,
    "prisoner_freed": emit_prisoner_freed,
    "party_entered_center": emit_party_entered_center,
    "conversation_started": emit_conversation_started,
    "conversation_ended": emit_conversation_ended,
    "item_acquired": emit_item_acquired,
    "item_lost": emit_item_lost,
    "relation_changed": emit_relation_changed,
    "faction_state_changed": emit_faction_state_changed,
    "village_raided": emit_village_raided,
    "center_besieged": emit_center_besieged,
    "mission_succeeded": emit_mission_succeeded,
    "mission_failed": emit_mission_failed,
    "caravan_created": emit_caravan_created,
    "caravan_destroyed": emit_caravan_destroyed,
    "time_passed": emit_time_passed,
    "inventory_updated": emit_inventory_updated,
}


class RuntimeStore(dict):
    def append(self, runtime: Any) -> None:
        self[getattr(runtime, "quest_id", id(runtime))] = runtime

    def add(self, runtime: Any) -> None:
        self.append(runtime)

    def extend(self, runtimes: Iterable[Any]) -> None:
        for runtime in runtimes:
            self.append(runtime)

    def remove(self, runtime: Any) -> None:
        key = getattr(runtime, "quest_id", None)
        if key in self and self[key] is runtime:
            del self[key]
            return
        for existing_key, existing_runtime in list(self.items()):
            if existing_runtime is runtime:
                del self[existing_key]
                return
        raise KeyError(runtime)

    def discard(self, runtime: Any) -> None:
        try:
            self.remove(runtime)
        except KeyError:
            pass

    def __contains__(self, item: Any) -> bool:
        if dict.__contains__(self, item):
            return True
        return any(runtime is item for runtime in self.values())

    def __iter__(self):  # type: ignore[override]
        return iter(self.values())

    def values(self) -> Iterable[Any]:  # type: ignore[override]
        return super().values()


def _fallback_value(name: str) -> Any:
    lowered = name.lower()
    if lowered in {"callback"}:
        return lambda *args, **kwargs: None
    if lowered in {"context"}:
        return None
    if lowered in {"payload", "metadata"}:
        return {
            "payload_key": "payload-value",
            "quest_id": "quest_alpha",
            "stage_id": "stage_alpha",
            "source": "tests.source",
        }
    if lowered in {"event_types", "quest_ids", "stage_ids", "faction_ids", "troop_ids", "center_ids", "party_ids", "region_ids", "location_ids", "sources", "categories", "tags", "payload_keys"}:
        return ("tests-value",)
    if lowered in {"priority"}:
        return 0
    if lowered in {"enabled"}:
        return True
    if lowered in {"once", "terminal_only", "non_terminal_only"}:
        return False
    if lowered.endswith("_id") or lowered in {"quest_id", "stage_id", "faction_id", "troop_id", "center_id", "party_id", "region_id", "location_id", "source", "event_type", "name", "hook_name"}:
        return f"{lowered}-value"
    return f"{lowered}-value"


def _build_call_args(callable_obj: Any, base_kwargs: Mapping[str, Any]) -> tuple[list[Any], dict[str, Any]]:
    signature = inspect.signature(callable_obj)
    args: list[Any] = []
    kwargs: dict[str, Any] = {}

    for parameter in signature.parameters.values():
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            continue
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            for key, value in base_kwargs.items():
                if key not in kwargs and key not in signature.parameters:
                    kwargs[key] = value
            continue

        if parameter.name in base_kwargs:
            value = base_kwargs[parameter.name]
        elif parameter.default is inspect._empty:
            value = _fallback_value(parameter.name)
        else:
            continue

        if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
            args.append(value)
        else:
            kwargs[parameter.name] = value

    return args, kwargs


def _invoke(callable_obj: Any, base_kwargs: Mapping[str, Any]) -> Any:
    args, kwargs = _build_call_args(callable_obj, base_kwargs)
    return callable_obj(*args, **kwargs)


def _event_type(event: Any) -> str:
    for attr in ("event_type", "name", "event_name", "type"):
        if hasattr(event, attr):
            value = getattr(event, attr)
            if isinstance(value, str):
                return value
    raise AssertionError(f"Unable to determine event type for {event!r}")


def _event_payload(event: Any) -> Any:
    for attr in ("payload", "data", "context"):
        if hasattr(event, attr):
            return getattr(event, attr)
    return None


def _collection_contains_runtime(collection: Any, runtime: Any) -> bool:
    if isinstance(collection, dict):
        return any(value is runtime for value in collection.values())
    if isinstance(collection, list):
        return runtime in collection
    return runtime in collection




def _make_event_kwargs(event_name: str) -> dict[str, Any]:
    return {
        "event_type": event_name,
        "event_name": event_name,
        "name": event_name,
        "source": f"{event_name}.source",
        "quest_id": "quest_alpha",
        "stage_id": "stage_alpha",
        "faction_id": "faction_alpha",
        "troop_id": "troop_alpha",
        "center_id": "center_alpha",
        "party_id": "party_alpha",
        "region_id": "region_alpha",
        "location_id": "location_alpha",


        "categories": ("combat",),
        "tags": ("world", event_name),
        "payload": {
            "payload_key": f"{event_name}.payload",
            "quest_id": "quest_alpha",
            "stage_id": "stage_alpha",
            "source": f"{event_name}.source",
        },
        "metadata": {"source": event_name},
    }


def _make_event(event_name: str, **overrides: Any) -> QuestWorldEvent:
    event_kwargs = _make_event_kwargs(event_name)
    event_kwargs.update(overrides)

    factory_map = quest_world_event_factories()
    factory = factory_map[event_name]
    event = _invoke(factory, event_kwargs)
    if not isinstance(event, QuestWorldEvent):
        event = _invoke(quest_world_event, event_kwargs)

    if not isinstance(event, QuestWorldEvent):
        raise AssertionError(f"Factory for {event_name!r} did not return QuestWorldEvent: {event!r}")
    if _event_type(event) != event_name:
        raise AssertionError(f"Expected event type {event_name!r}, got {_event_type(event)!r}")
    return event


def _make_subscription(callback: Callable[..., Any], **overrides: Any) -> QuestEventSubscription:
    subscription_kwargs: dict[str, Any] = {
        "event_types": ("battle_started",),
        "event_names": ("battle_started",),
        "hook_names": ("battle_started",),
        "hooks": ("battle_started",),
        "quest_ids": ("quest_alpha",),
        "stage_ids": ("stage_alpha",),
        "faction_ids": ("faction_alpha",),
        "troop_ids": ("troop_alpha",),
        "center_ids": ("center_alpha",),
        "party_ids": ("party_alpha",),
        "region_ids": ("region_alpha",),
        "location_ids": ("location_alpha",),
        "sources": ("battle_started.source",),
        "categories": ("combat",),
        "tags": ("world",),
        "payload_keys": ("payload_key",),
        "priority": 0,
        "enabled": True,
        "once": False,
        "terminal_only": False,
        "non_terminal_only": False,
        "metadata": {"source": "tests"},
        "callback": callback,
    }
    subscription_kwargs.update(overrides)

    if callable(quest_event_subscription):
        subscription = _invoke(quest_event_subscription, subscription_kwargs)
    else:
        subscription = _invoke(QuestEventSubscription, subscription_kwargs)
    if not isinstance(subscription, QuestEventSubscription):
        raise AssertionError(f"Subscription factory did not return QuestEventSubscription: {subscription!r}")
    return subscription


def _make_dispatcher() -> QuestEventDispatcher:
    try:
        dispatcher = _invoke(QuestEventDispatcher, {})
    except Exception:
        dispatcher = object.__new__(QuestEventDispatcher)


    if not isinstance(dispatcher, QuestEventDispatcher):
        raise AssertionError(f"QuestEventDispatcher constructor returned {dispatcher!r}")

    for attribute in (
        "subscriptions",
        "_subscriptions",
        "listeners",
        "_listeners",
        "registry",
        "_registry",
    ):
        try:
            setattr(dispatcher, attribute, [])
        except Exception:
            continue

    return dispatcher


def _register_subscription(dispatcher: QuestEventDispatcher, subscription: QuestEventSubscription) -> None:
    for method_name in ("register_subscription", "subscribe", "add_subscription", "register", "add"):
        method = getattr(dispatcher, method_name, None)
        if callable(method):
            try:
                method(subscription)
                return
            except TypeError:
                try:
                    method(subscription=subscription)
                    return
                except TypeError:
                    continue
    raise AssertionError("QuestEventDispatcher does not expose a compatible subscription registration method")


def _dispatch_event(dispatcher: QuestEventDispatcher, event: QuestWorldEvent, *, context: Any = None) -> Any:
    for method_name in ("dispatch_event", "dispatch", "publish_event", "handle_event"):
        method = getattr(dispatcher, method_name, None)
        if callable(method):
            try:
                return method(event, context=context)
            except TypeError:
                try:
                    return method(event)
                except TypeError:
                    continue
    raise AssertionError("QuestEventDispatcher does not expose a compatible dispatch method")


def _make_recording_runtime(
    quest_id: str,
    stage_id: str,
    *,
    terminal_event_types: Iterable[str] = (),
) -> Any:
    class RecordingRuntime:
        def __init__(self) -> None:
            self.quest_id = quest_id
            self.stage_id = stage_id
            self.terminal_event_types = set(terminal_event_types)
            self.calls: list[tuple[str, Any, Any]] = []
            self.is_terminal = False
            self.terminal = False
            self.completed = False
            self.done = False
            self.finished = False
            self.archived = False
            self.state = "active"
            self.status = "active"







        def dispatch_event(self, event: Any, *, context: Any = None) -> str:
            event_type = _event_type(event)
            self.calls.append(("dispatch_event", event_type, context))
            if event_type in self.terminal_event_types:
                self.is_terminal = True
                self.terminal = True
                self.completed = True
                self.done = True
                self.finished = True
                self.archived = True
                self.state = "terminal"
                self.status = "terminal"
            return f"{self.quest_id}:{event_type}"

        def progress_hook(self, hook_name: str, *, context: Any = None) -> str:
            self.calls.append(("progress_hook", hook_name, context))
            return f"{self.quest_id}:{hook_name}"

        def handle_hook(self, hook_name: str, *, context: Any = None) -> str:
            self.calls.append(("handle_hook", hook_name, context))
            return f"{self.quest_id}:{hook_name}"

        def handle_quest_hook(self, hook_name: str, *, context: Any = None) -> str:
            self.calls.append(("handle_quest_hook", hook_name, context))
            return f"{self.quest_id}:{hook_name}"

    return RecordingRuntime()


def _make_journal(runtimes: Mapping[str, Any]) -> QuestJournal:
    try:
        journal = _invoke(QuestJournal, {})
    except Exception:
        journal = object.__new__(QuestJournal)
    if not isinstance(journal, QuestJournal):
        raise AssertionError(f"QuestJournal constructor returned {journal!r}")

    runtime_map = dict(runtimes)
    runtime_collections = (
        "runtimes",
        "_runtimes",
        "active_runtimes",
        "_active_runtimes",
        "quests",
        "_quests",
        "active_quests",
        "_active_quests",
        "quest_runtimes",
        "_quest_runtimes",
    )
    archive_collections = (
        "archive",
        "_archive",
        "archived_runtimes",
        "_archived_runtimes",
        "completed_runtimes",
        "_completed_runtimes",
        "terminal_runtimes",
        "_terminal_runtimes",
    )

    for attribute in runtime_collections:
        try:
            setattr(journal, attribute, RuntimeStore(runtime_map))
        except Exception:
            continue
    for attribute in archive_collections:
        try:
            setattr(journal, attribute, RuntimeStore())
        except Exception:
            continue

    return journal


class Phase4EventDrivenQuestTests(unittest.TestCase):
    def test_runtime_and_journal_exports_keep_their_hook_entrypoints(self) -> None:
        self.assertTrue(hasattr(QuestRuntime, "dispatch_event"))
        self.assertTrue(hasattr(QuestRuntime, "handle_hook"))
        self.assertTrue(hasattr(QuestRuntime, "handle_quest_hook"))
        self.assertTrue(hasattr(QuestJournal, "dispatch_event"))
        self.assertTrue(hasattr(QuestJournal, "progress_hook"))

    def test_event_catalog_is_canonical_and_factories_return_world_events(self) -> None:
        self.assertEqual(quest_world_event_names(), EVENT_NAMES)

        factories = quest_world_event_factories()
        self.assertTrue(set(EVENT_NAMES).issubset(factories.keys()))

        for event_name in EVENT_NAMES:
            self.assertIn(event_name, factories)
            self.assertTrue(callable(factories[event_name]))
            event = _make_event(event_name)
            self.assertIsInstance(event, QuestWorldEvent)
            self.assertEqual(_event_type(event), event_name)

            payload = _event_payload(event)
            if isinstance(payload, Mapping):
                self.assertEqual(payload.get("payload_key"), f"{event_name}.payload")

    def test_source_adapter_helpers_emit_canonical_world_events(self) -> None:
        for event_name, helper in SOURCE_HELPERS.items():
            event = _invoke(
                helper,
                {
                    "event_type": event_name,
                    "source": f"{event_name}.source",
                    "quest_id": "quest_alpha",
                    "stage_id": "stage_alpha",
                    "payload": {"payload_key": f"{event_name}.payload"},
                },
            )
            self.assertIsInstance(event, QuestWorldEvent)
            self.assertEqual(_event_type(event), event_name)

        generic_event = _invoke(
            emit_world_event,
            {
                "event_type": "battle_started",
                "source": "generic.source",
                "quest_id": "quest_alpha",
                "stage_id": "stage_alpha",
                "payload": {"payload_key": "generic.payload"},
            },
        )
        self.assertIsInstance(generic_event, QuestWorldEvent)
        self.assertEqual(_event_type(generic_event), "battle_started")

    def test_dispatcher_prioritizes_subscriptions_and_honors_once_and_scope_filters(self) -> None:
        dispatcher = _make_dispatcher()
        call_order: list[str] = []

        def make_callback(label: str) -> Callable[..., str]:
            def _callback(event: Any, *, context: Any = None) -> str:
                call_order.append(label)
                return label

            return _callback

        low_priority = _make_subscription(
            make_callback("low"),
            event_types=("battle_started",),
            priority=1,
        )
        high_priority = _make_subscription(
            make_callback("high"),
            event_types=("battle_started",),
            priority=10,
        )
        once_subscription = _make_subscription(
            make_callback("once"),
            event_types=("battle_started",),
            priority=5,
            once=True,
        )
        scoped_subscription = _make_subscription(
            make_callback("scoped"),
            event_types=("battle_started",),
            quest_ids=("quest_alpha",),
            stage_ids=("stage_alpha",),
            sources=("battle_started.source",),
            categories=("combat",),
            tags=("world",),
            payload_keys=("payload_key",),
            priority=7,
        )

        for subscription in (low_priority, high_priority, once_subscription, scoped_subscription):
            _register_subscription(dispatcher, subscription)

        matching_event = _make_event(
            "battle_started",
            source="battle_started.source",
            quest_id="quest_alpha",
            stage_id="stage_alpha",
            categories=("combat",),
            tags=("world", "battle_started"),
            payload={"payload_key": "battle_started.payload", "quest_id": "quest_alpha", "stage_id": "stage_alpha"},
        )
        dispatch_result = _dispatch_event(dispatcher, matching_event)
        self.assertEqual(call_order, ["high", "scoped", "once", "low"])
        if isinstance(dispatch_result, list):
            self.assertEqual(dispatch_result, ["high", "scoped", "once", "low"])

        call_order.clear()
        _dispatch_event(dispatcher, matching_event)
        self.assertEqual(call_order, ["high", "scoped", "low"])

        non_matching_event = _make_event(
            "battle_started",
            source="battle_started.source",
            quest_id="quest_beta",
            stage_id="stage_beta",
            categories=("combat",),
            tags=("world", "battle_started"),
            payload={"payload_key": "battle_started.payload", "quest_id": "quest_beta", "stage_id": "stage_beta"},
        )
        call_order.clear()
        _dispatch_event(dispatcher, non_matching_event)
        self.assertEqual(call_order, ["high", "low"])

    def test_journal_broadcasts_world_events_and_archives_terminal_runtimes(self) -> None:
        runtime_a = _make_recording_runtime("quest_alpha", "stage_alpha", terminal_event_types=("mission_succeeded",))
        runtime_b = _make_recording_runtime("quest_beta", "stage_beta")

        journal = _make_journal({"quest_alpha": runtime_a, "quest_beta": runtime_b})

        broadcast_event = _make_event("battle_started")
        broadcast_result = journal.dispatch_event(broadcast_event)
        self.assertTrue(runtime_a.calls)
        self.assertTrue(runtime_b.calls)
        if isinstance(broadcast_result, dict):
            self.assertIn("quest_alpha", broadcast_result)
            self.assertIn("quest_beta", broadcast_result)

        terminal_event = _make_event("mission_succeeded")
        journal.dispatch_event(terminal_event)

        active_collections = [
            getattr(journal, attribute)
            for attribute in (
                "runtimes",
                "_runtimes",
                "active_runtimes",
                "_active_runtimes",
                "quests",
                "_quests",
                "active_quests",
                "_active_quests",
                "quest_runtimes",
                "_quest_runtimes",
            )
            if hasattr(journal, attribute) and not callable(getattr(journal, attribute))
        ]
        archived_collections = [
            getattr(journal, attribute)
            for attribute in (
                "archive",
                "_archive",
                "archived_runtimes",
                "_archived_runtimes",
                "completed_runtimes",
                "_completed_runtimes",
                "terminal_runtimes",
                "_terminal_runtimes",
            )
            if hasattr(journal, attribute) and not callable(getattr(journal, attribute))
        ]

        active_contains_runtime = any(_collection_contains_runtime(collection, runtime_a) for collection in active_collections)
        archived_contains_runtime = any(_collection_contains_runtime(collection, runtime_a) for collection in archived_collections)

        self.assertFalse(active_contains_runtime)
        self.assertTrue(archived_contains_runtime)
        self.assertTrue(runtime_a.is_terminal)
        self.assertFalse(runtime_b.is_terminal)

    def test_journal_progress_hook_routes_quest_and_stage_scoped_hooks(self) -> None:
        runtime_a = _make_recording_runtime("quest_alpha", "stage_alpha")
        runtime_b = _make_recording_runtime("quest_beta", "stage_beta")
        journal = _make_journal({"quest_alpha": runtime_a, "quest_beta": runtime_b})

        matching_kwargs = {
            "hook_name": "conversation_started",
            "name": "conversation_started",
            "event_name": "conversation_started",
            "quest_id": "quest_alpha",
            "stage_id": "stage_alpha",
            "context": {"source": "tests"},
        }
        if hasattr(journal, "progress_hook"):
            _invoke(journal.progress_hook, matching_kwargs)
        else:
            self.fail("QuestJournal is missing progress_hook")



        self.assertTrue(runtime_a.calls)
        self.assertFalse(runtime_b.calls)

        runtime_a.calls.clear()
        runtime_b.calls.clear()

        non_matching_kwargs = {
            "hook_name": "conversation_started",
            "name": "conversation_started",
            "event_name": "conversation_started",
            "quest_id": "quest_alpha",
            "stage_id": "stage_beta",
            "context": {"source": "tests"},
        }
        _invoke(journal.progress_hook, non_matching_kwargs)

        self.assertFalse(runtime_a.calls)
        self.assertFalse(runtime_b.calls)


def main() -> int:
    program = unittest.main(module=__name__, argv=["phase4-event-driven-quests"], verbosity=2, exit=False)
    result = getattr(program, "result", None)
    if result is None:
        return 0
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
