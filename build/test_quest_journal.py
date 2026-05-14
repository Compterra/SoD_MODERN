from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.quests.quest_runtime import QuestJournal, QuestRuntime


def read_source(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def lower_source(relative_path: str) -> str:
    return read_source(relative_path).lower()


def as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    return {
        name: getattr(value, name)
        for name in dir(value)
        if not name.startswith("_") and not callable(getattr(value, name))
    }


def find_key(mapping: dict[str, Any], *needles: str) -> str:
    lowered_needles = tuple(needle.lower() for needle in needles)
    for key in mapping:
        lowered_key = key.lower()
        if all(needle in lowered_key for needle in lowered_needles):
            return key
    raise AssertionError(f"Could not find key containing {needles!r} in {sorted(mapping)!r}")


def find_collection(mapping: dict[str, Any], *needles: str) -> tuple[str, list[Any]]:
    lowered_needles = tuple(needle.lower() for needle in needles)
    for key, value in mapping.items():
        lowered_key = key.lower()
        if not all(needle in lowered_key for needle in lowered_needles):
            continue
        if isinstance(value, (list, tuple, set)):
            return key, list(value)
    raise AssertionError(f"Could not find collection containing {needles!r} in {sorted(mapping)!r}")


def find_collection_any(
    mapping: dict[str, Any], options: Iterable[tuple[str, ...]]
) -> tuple[str, list[Any]]:
    last_error: AssertionError | None = None
    for option in options:
        try:
            return find_collection(mapping, *option)
        except AssertionError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    raise AssertionError(f"Could not find any collection in {sorted(mapping)!r}")


def label_for(value: Any) -> str:
    for attr in ("title", "name", "quest_title", "quest_name", "id"):
        if hasattr(value, attr):
            candidate = getattr(value, attr)
            if candidate is not None:
                return str(candidate)
    return str(value)


def category_for(value: Any) -> str:
    for attr in ("category", "quest_category", "type", "quest_type", "group"):
        if hasattr(value, attr):
            candidate = getattr(value, attr)
            if candidate is not None:
                return str(candidate).lower()
    return ""


def make_instance(cls: type[Any], attrs: dict[str, Any]) -> Any:
    try:
        signature = inspect.signature(cls)
    except (TypeError, ValueError):
        signature = None

    if signature is not None:
        kwargs: dict[str, Any] = {}
        for name, parameter in signature.parameters.items():
            if name == "self" or parameter.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            if name in attrs:
                kwargs[name] = attrs[name]
                continue

            lowered = name.lower()
            if any(token in lowered for token in ("title", "name", "id", "label")):
                kwargs[name] = attrs.get("title", f"{cls.__name__}:{name}")
            elif any(token in lowered for token in ("category", "type", "group")):
                kwargs[name] = attrs.get("category", "quest")
            elif any(token in lowered for token in ("pinned", "urgent", "active", "completed", "failed", "archived", "visible")):
                kwargs[name] = attrs.get(name, False)
            elif any(token in lowered for token in ("count", "capacity", "limit", "goal", "progress", "days", "turn", "order", "rank")):
                kwargs[name] = attrs.get(name, 0)
            elif any(token in lowered for token in ("list", "items", "runtimes", "quests", "warnings", "archives", "entries")):
                kwargs[name] = attrs.get(name, [])
            else:
                if parameter.default is not inspect._empty:
                    kwargs[name] = parameter.default
                else:
                    kwargs[name] = None

        try:
            return cls(**kwargs)
        except Exception:
            pass

    obj = cls.__new__(cls)
    for key, value in attrs.items():
        try:
            setattr(obj, key, value)
        except Exception:
            continue

    for key, value in list(attrs.items()):
        alias = f"_{key}"
        if not hasattr(obj, alias):
            try:
                setattr(obj, alias, value)
            except Exception:
                continue

    return obj


def make_blueprint(
    title: str,
    category: str,
    *,
    quest_id: str | None = None,
    pinned: bool = False,
    status: str | None = None,
    warnings: Iterable[str] | None = None,
    stages: Iterable[Any] | None = None,
) -> Any:
    blueprint_id = quest_id or title.lower().replace(" ", "_")
    stage_list = list(stages or [])
    warning_list = list(warnings or [])
    metadata: dict[str, Any] = {
        "quest_id": blueprint_id,
        "id": blueprint_id,
        "title": title,
        "name": title,
        "category": category,
    }
    if status is not None:
        metadata["status"] = status
        metadata["outcome"] = status
    if warning_list:
        metadata["warnings"] = warning_list
    return SimpleNamespace(
        quest_id=blueprint_id,
        id=blueprint_id,
        uid=blueprint_id,
        slug=blueprint_id,
        key=blueprint_id,
        template_id=blueprint_id,
        title=title,
        name=title,
        display_name=title,
        category=category,
        quest_category=category,
        quest_type=category,
        pinned=pinned,
        is_pinned=pinned,
        active=status not in {"completed", "failed"} if status else True,
        is_active=status not in {"completed", "failed"} if status else True,
        archived=status in {"completed", "failed"} if status else False,
        status=status,
        state=status,
        quest_state=status,
        outcome=status,
        stages=stage_list,
        stage_runtimes=[],
        stage_index=0,
        stage_count=len(stage_list) if stage_list else None,
        metadata=metadata,
        warnings=warning_list,
        warning_flags=warning_list,
        warning_list=warning_list,
    )


def make_runtime(
    title: str,
    category: str,
    *,
    pinned: bool = False,
    active: bool = True,
    completed: bool = False,
    failed: bool = False,
    urgent: bool = False,
    progress_current: int = 0,
    progress_goal: int = 0,
    days_remaining: int = 0,
    warnings: Iterable[str] | None = None,
) -> Any:
    warning_list = list(warnings or [])
    attrs: dict[str, Any] = {
        "title": title,
        "name": title,
        "quest_title": title,
        "quest_name": title,
        "id": title,
        "category": category,
        "quest_category": category,
        "type": category,
        "quest_type": category,
        "active": active,
        "is_active": active,
        "pinned": pinned,
        "is_pinned": pinned,
        "urgent": urgent,
        "is_urgent": urgent,
        "completed": completed,
        "is_completed": completed,
        "failed": failed,
        "is_failed": failed,
        "archived": completed or failed,
        "progress": progress_current,
        "progress_current": progress_current,
        "current_progress": progress_current,
        "progress_goal": progress_goal,
        "goal": progress_goal,
        "target_progress": progress_goal,
        "days_remaining": days_remaining,
        "turns_remaining": days_remaining,
        "warning_flags": warning_list,
        "warnings": warning_list,
        "warning_list": warning_list,
    }
    return make_instance(QuestRuntime, attrs)


def make_journal(active_runtimes: list[Any], capacity: int = 5) -> Any:
    completed_runtime = make_runtime(
        "Completed Quest",
        "main",
        active=False,
        completed=True,
        progress_current=3,
        progress_goal=3,
    )
    failed_runtime = make_runtime(
        "Failed Quest",
        "side",
        active=False,
        failed=True,
        progress_current=1,
        progress_goal=4,
    )

    active_runtime_list = list(active_runtimes)
    completed_archive = [completed_runtime]
    failed_archive = [failed_runtime]
    pinned_runtime_list = [runtime for runtime in active_runtime_list if getattr(runtime, "pinned", False)]
    main_runtime_list = [runtime for runtime in active_runtime_list if category_for(runtime) == "main"]
    side_runtime_list = [runtime for runtime in active_runtime_list if category_for(runtime) == "side"]
    urgent_runtime_list = [runtime for runtime in active_runtime_list if category_for(runtime) == "urgent"]

    attrs: dict[str, Any] = {
        "active_runtimes": active_runtime_list,
        "active_quests": active_runtime_list,
        "active_entries": active_runtime_list,
        "runtimes": active_runtime_list + completed_archive + failed_archive,
        "quests": active_runtime_list + completed_archive + failed_archive,
        "entries": active_runtime_list + completed_archive + failed_archive,
        "journal_entries": active_runtime_list + completed_archive + failed_archive,
        "quest_runtimes": active_runtime_list + completed_archive + failed_archive,
        "completed_runtimes": completed_archive,
        "completed_quests": completed_archive,
        "completed_entries": completed_archive,
        "failed_runtimes": failed_archive,
        "failed_quests": failed_archive,
        "failed_entries": failed_archive,
        "completed_archive": completed_archive,
        "failed_archive": failed_archive,
        "archives": {
            "completed": completed_archive,
            "failed": failed_archive,
        },
        "capacity": capacity,
        "active_capacity": capacity,
        "active_count": len(active_runtime_list),
        "completed_count": len(completed_archive),
        "failed_count": len(failed_archive),
        "pinned_count": len(pinned_runtime_list),
        "main_count": len(main_runtime_list),
        "side_count": len(side_runtime_list),
        "urgent_count": len(urgent_runtime_list),
        "pinned_runtimes": pinned_runtime_list,
        "pinned_quests": pinned_runtime_list,
        "main_runtimes": main_runtime_list,
        "main_quests": main_runtime_list,
        "side_runtimes": side_runtime_list,
        "side_quests": side_runtime_list,
        "urgent_runtimes": urgent_runtime_list,
        "urgent_quests": urgent_runtime_list,
        "warnings": ["capacity", "expiration"],
        "warning_flags": ["capacity", "expiration"],
    }
    return make_instance(QuestJournal, attrs)


class QuestJournalContractTests(unittest.TestCase):
    def test_reports_menu_routes_to_quest_journal_report(self) -> None:
        text = lower_source("src/menus/0000_hardcoded_mb1011/reports.py")
        self.assertIn("view_quest_journal_report", text)
        self.assertIn("mnu_quest_journal_report", text)
        self.assertIn("jump_to_menu", text)

    def test_journal_report_menu_uses_canonical_describe_script(self) -> None:
        text = lower_source("src/menus/reports/quest_journal_report.py")
        self.assertIn("mnu_quest_journal_report", text)
        self.assertIn("script_sod_quest_journal_describe_to_s2", text)
        self.assertIn("script_sod_quest_chain_describe_to_s2", text)
        self.assertIn("script_sod_quest_outcome_describe_to_s2", text)

    def test_report_menu_modules_import_and_export_menu_data(self) -> None:
        self.assertIn("MENUS = [", read_source("src/menus/reports/report_submenus.py"))
        self.assertIn("MENUS = [", read_source("src/menus/reports/quest_journal_report.py"))

    def test_runtime_contract_exposes_journal_summary_methods(self) -> None:
        for member in (
            "journal_snapshot",
            "sorted_active_runtimes",
            "filtered_active_runtimes",
        ):
            self.assertTrue(hasattr(QuestJournal, member), member)

        for member in ("progress_summary", "warning_flags"):
            self.assertTrue(hasattr(QuestRuntime, member), member)

    def test_runtime_source_mentions_the_journal_summary_contract(self) -> None:
        text = lower_source("src/quests/quest_runtime.py")
        for phrase in (
            "journal_snapshot",
            "sorted_active_runtimes",
            "filtered_active_runtimes",
            "progress_summary",
            "warning_flags",
            "active_count",
            "capacity",
            "pinned",
            "main",
            "side",
            "urgent",
            "completed",
            "failed",
            "warning",
        ):
            self.assertIn(phrase, text)

    def test_quest_journal_source_defines_register_runtime_once(self) -> None:
        source = inspect.getsource(QuestJournal)
        self.assertEqual(source.count("def register_runtime("), 1)

    def test_runtime_summary_methods_surface_progress_and_warning_data(self) -> None:
        main = make_runtime(
            "Main Quest",
            "main",
            pinned=True,
            active=True,
            progress_current=2,
            progress_goal=5,
            days_remaining=7,
        )
        side = make_runtime(
            "Side Quest",
            "side",
            active=True,
            progress_current=1,
            progress_goal=4,
            days_remaining=6,
        )
        urgent = make_runtime(
            "Urgent Quest",
            "urgent",
            urgent=True,
            active=True,
            progress_current=0,
            progress_goal=3,
            days_remaining=1,
            warnings=["expiring"],
        )
        completed = make_runtime(
            "Completed Quest",
            "main",
            active=False,
            completed=True,
            progress_current=3,
            progress_goal=3,
        )
        failed = make_runtime(
            "Failed Quest",
            "side",
            active=False,
            failed=True,
            progress_current=1,
            progress_goal=4,
            warnings=["failed"],
        )

        journal = make_journal([main, side, urgent], capacity=5)
        snapshot = as_mapping(journal.journal_snapshot())

        active_count_key = find_key(snapshot, "active", "count")
        capacity_key = find_key(snapshot, "capacity")
        self.assertEqual(snapshot[active_count_key], 3)
        self.assertEqual(snapshot[capacity_key], 5)

        pinned_key, pinned_group = find_collection(snapshot, "pinned")
        self.assertEqual([label_for(runtime) for runtime in pinned_group], ["Main Quest"], pinned_key)

        main_key, main_group = find_collection(snapshot, "main")
        side_key, side_group = find_collection(snapshot, "side")
        urgent_key, urgent_group = find_collection(snapshot, "urgent")
        self.assertEqual([label_for(runtime) for runtime in main_group], ["Main Quest"], main_key)
        self.assertEqual([label_for(runtime) for runtime in side_group], ["Side Quest"], side_key)
        self.assertEqual([label_for(runtime) for runtime in urgent_group], ["Urgent Quest"], urgent_key)

        completed_key, completed_archive = find_collection(snapshot, "completed", "archive")
        failed_key, failed_archive = find_collection(snapshot, "failed", "archive")
        self.assertEqual([label_for(runtime) for runtime in completed_archive], ["Completed Quest"], completed_key)
        self.assertEqual([label_for(runtime) for runtime in failed_archive], ["Failed Quest"], failed_key)

        warning_key = find_key(snapshot, "warning")
        warning_value = snapshot[warning_key]
        self.assertTrue(warning_value, warning_key)

        sorted_active = list(journal.sorted_active_runtimes())
        filtered_active = list(journal.filtered_active_runtimes())
        sorted_labels = [label_for(runtime) for runtime in sorted_active]
        filtered_labels = [label_for(runtime) for runtime in filtered_active]
        self.assertEqual(sorted_labels[0], "Main Quest")
        self.assertEqual(filtered_labels[0], "Main Quest")
        self.assertCountEqual(sorted_labels, ["Main Quest", "Side Quest", "Urgent Quest"])
        self.assertCountEqual(filtered_labels, ["Main Quest", "Side Quest", "Urgent Quest"])

        progress_summary_text = str(main.progress_summary()).lower()
        self.assertIn("2", progress_summary_text)
        self.assertIn("5", progress_summary_text)

        warning_flags = urgent.warning_flags()
        warning_text = str(warning_flags).lower()
        self.assertTrue(warning_flags)
        self.assertTrue(
            any(term in warning_text for term in ("expir", "warn", "fail")),
            warning_text,
        )

    def test_runtime_from_blueprint_consumes_authoring_blueprint_shape(self) -> None:
        blueprint = make_blueprint(
            "Bridge Quest",
            "main",
            quest_id="bridge-quest",
            pinned=True,
            warnings=["expiring"],
            stages=[SimpleNamespace(name="Stage 1")],
        )
        runtime = QuestRuntime.from_blueprint(blueprint)
        snapshot = as_mapping(runtime.progress_summary())

        self.assertEqual(snapshot["quest_id"], "bridge-quest")
        self.assertEqual(snapshot["title"], "Bridge Quest")
        self.assertEqual(snapshot["category"], "main")
        self.assertTrue(snapshot["pinned"])
        self.assertIn("expiring", snapshot["warnings"])
        self.assertTrue(runtime.is_main_quest())
        self.assertEqual(runtime.metadata["title"], "Bridge Quest")

    def test_journal_from_blueprints_and_chain_preserve_authoring_metadata(self) -> None:
        main_blueprint = make_blueprint("Bridge Main", "main", quest_id="bridge-main", pinned=True)
        side_blueprint = make_blueprint(
            "Bridge Side",
            "side",
            quest_id="bridge-side",
            warnings=["deadline"],
        )

        journal = QuestJournal.from_blueprints([main_blueprint, side_blueprint], capacity=3)
        snapshot = as_mapping(journal.journal_snapshot())
        active_key, active_runtimes = find_collection(snapshot, "active")
        self.assertEqual(snapshot[find_key(snapshot, "active", "count")], 2, active_key)
        self.assertEqual(
            [label_for(runtime) for runtime in active_runtimes],
            ["Bridge Main", "Bridge Side"],
        )
        self.assertEqual(journal.max_active_quests, 3)
        self.assertEqual(
            [label_for(runtime) for runtime in journal.sorted_active_runtimes()],
            ["Bridge Main", "Bridge Side"],
        )
        self.assertEqual({category_for(runtime) for runtime in journal.sorted_active_runtimes()}, {"main", "side"})

        chain = SimpleNamespace(
            chain_id="bridge-chain",
            title="Bridge Chain",
            name="Bridge Chain",
            entry_quest_id="bridge-main",
            metadata={"chapter": "authoring"},
            quests=[main_blueprint, side_blueprint],
            normalized_quests=lambda: [main_blueprint, side_blueprint],
        )
        chain_journal = QuestJournal.from_chain(chain, capacity=4)
        chain_snapshot = as_mapping(chain_journal.journal_snapshot())
        chain_active_key, chain_active_runtimes = find_collection(chain_snapshot, "active")
        self.assertEqual(chain_journal.chain_id, "bridge-chain")
        self.assertEqual(chain_journal.entry_quest_id, "bridge-main")
        self.assertEqual(chain_journal.chain_title, "Bridge Chain")
        self.assertEqual(chain_snapshot[find_key(chain_snapshot, "active", "count")], 2, chain_active_key)
        self.assertEqual(
            [label_for(runtime) for runtime in chain_active_runtimes],
            ["Bridge Main", "Bridge Side"],
        )
        self.assertEqual(
            [label_for(runtime) for runtime in chain_journal.sorted_active_runtimes()],
            ["Bridge Main", "Bridge Side"],
        )
        self.assertEqual(chain_journal.max_active_quests, 4)


if __name__ == "__main__":
    unittest.main()


