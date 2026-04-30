"""Quest runtime, stage runtime, and journal support for quest progression.

This module intentionally stays duck-typed so small quest test doubles can
exercise the journal layer without importing the full Mount & Blade quest
content model.
"""

from __future__ import annotations

import builtins
from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Any


__all__ = [
    "QUEST_STAGE_ACTIVE",
    "QUEST_STAGE_ABORTED",
    "QUEST_STAGE_COMPLETED",
    "QUEST_STAGE_FAILED",
    "QUEST_STAGE_PENDING",
    "QUEST_STATE_ACTIVE",
    "QUEST_STATE_ABORTED",
    "QUEST_STATE_CANCELLED",
    "QUEST_STATE_CANCELED",
    "QUEST_STATE_COMPLETED",
    "QUEST_STATE_FAILED",
    "QUEST_STATE_INACTIVE",
    "QuestStageRuntime",
    "QuestRuntime",
    "QuestJournal",
    "QuestProgressEvent",
    "quest_journal_from_blueprints",
    "quest_journal_from_chain",
    "quest_journal_presentation_summary",
    "quest_runtime_from_blueprint",
]

QUEST_STATE_INACTIVE = "inactive"
QUEST_STATE_ACTIVE = "active"
QUEST_STATE_COMPLETED = "completed"
QUEST_STATE_FAILED = "failed"
QUEST_STATE_ABORTED = "aborted"
QUEST_STATE_CANCELLED = QUEST_STATE_ABORTED
QUEST_STATE_CANCELED = QUEST_STATE_ABORTED
QUEST_STAGE_PENDING = "pending"
QUEST_STAGE_ACTIVE = "active"
QUEST_STAGE_COMPLETED = "completed"
QUEST_STAGE_FAILED = "failed"
QUEST_STAGE_ABORTED = "aborted"


@dataclass(frozen=True)
class QuestProgressEvent:
    quest_id: str = ""
    stage_id: str = ""
    event_name: str = ""
    payload: dict[str, Any] | None = None


def quest_runtime_from_blueprint(blueprint: Any) -> "QuestRuntime":
    return QuestRuntime.from_blueprint(blueprint)


def quest_journal_from_blueprints(blueprints: Any) -> "QuestJournal":
    return QuestJournal.from_blueprints(blueprints)


def quest_journal_from_chain(chain: Any) -> "QuestJournal":
    return QuestJournal.from_chain(chain)


_TERMINAL_STATUSES = {"completed", "failed"}
_CATEGORY_BUCKETS = {"main", "side", "urgent", "misc"}
_WARNING_FLAGS = ("expiration_warning", "failure_warning")


def _is_mapping(value: Any) -> bool:
    return isinstance(value, Mapping)


def _as_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if _is_mapping(value):
        return dict(value)
    try:
        return dict(value)
    except Exception:
        return {}


def _normalize_identifier(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value)


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"", "0", "false", "no", "off", "none", "null"}:
            return False
        return True
    return bool(value)


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            return default
        try:
            return int(float(normalized))
        except (TypeError, ValueError):
            return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            return None
        try:
            return int(float(normalized))
        except (TypeError, ValueError):
            return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            return default
        try:
            return float(normalized)
        except (TypeError, ValueError):
            return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _candidate_sources(obj: Any) -> list[Any]:
    sources: list[Any] = []
    if obj is None:
        return sources
    sources.append(obj)
    for attr in (
        "metadata",
        "meta",
        "data",
        "quest",
        "template",
        "quest_template",
        "stage",
        "current_stage",
    ):
        value = getattr(obj, attr, None)
        if value is not None and value not in sources:
            sources.append(value)
    expanded: list[Any] = []
    for source in sources:
        expanded.append(source)
        nested = getattr(source, "metadata", None)
        if nested is not None and nested not in expanded:
            expanded.append(nested)
    return expanded


def _source_value(source: Any, name: str) -> Any:
    if source is None:
        return None
    if _is_mapping(source) and name in source:
        value = source[name]
        if value is not None:
            return value
    try:
        data = vars(source)
    except TypeError:
        data = None
    if data is not None and name in data:
        value = data[name]
        if value is not None:
            return value
    class_attr = getattr(type(source), name, None)
    if isinstance(class_attr, property):
        return None
    if hasattr(source, name):
        value = getattr(source, name)
        if value is not None and not callable(value):
            return value
    return None


def _ensure_runtime_metadata(runtime: Any) -> dict[str, Any]:
    metadata = getattr(runtime, "metadata", None)
    if isinstance(metadata, dict):
        return metadata
    if metadata is None:
        metadata = {}
    else:
        metadata = dict(metadata)
    try:
        setattr(runtime, "metadata", metadata)
    except Exception:
        pass
    return metadata


def _first_value(obj: Any, *names: str) -> Any:
    for source in _candidate_sources(obj):
        for name in names:
            value = _source_value(source, name)
            if value is not None:
                return value
    return None


def _normalize_category(value: Any) -> str:
    if value is None:
        return "misc"
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in _CATEGORY_BUCKETS:
            return normalized
        if "urgent" in normalized:
            return "urgent"
        if "main" in normalized:
            return "main"
        if "side" in normalized:
            return "side"
        if normalized in {"misc", "other", "optional", "secondary"}:
            return "misc"
    return "misc"


def _normalize_status(value: Any) -> str:
    if value is None:
        return "active"
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"done", "finished", "complete"}:
            return "completed"
        if normalized in {"fail", "failed", "failure"}:
            return "failed"
        if normalized in {"archive", "archived"}:
            return "archived"
        if normalized in {"active", "completed", "failed"}:
            return normalized
        return normalized or "active"
    return "active" if _coerce_bool(value) else "active"


def _flatten_warning_values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        values: list[str] = []
        for item in value.values():
            values.extend(_flatten_warning_values(item))
        return values
    if isinstance(value, Iterable):
        values = []
        for item in value:
            values.extend(_flatten_warning_values(item))
        return values
    return [str(value)]


def _progress_summary_from_mapping(
    raw_value: Any,
    *,
    default_index: int,
    default_count: int | None,
    total_name: str,
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if _is_mapping(raw_value):
        summary.update(_as_dict(raw_value))

    index = _coerce_int(
        _first_value(summary, "index", "current_index", "stage_index", "chain_index"),
        default_index,
    )
    count = _coerce_optional_int(
        _first_value(summary, "count", "total", "length", total_name, "stage_count", "chain_length"),
    )
    if count is None:
        count = default_count

    completed = _coerce_optional_int(_first_value(summary, "completed", "done", "finished"))
    if completed is None:
        completed = max(0, index)

    remaining = _coerce_optional_int(_first_value(summary, "remaining", "left"))
    if remaining is None and count is not None:
        remaining = max(count - completed, 0)

    percent = _first_value(summary, "percent", "progress", "completion")
    if percent is None:
        if count and count > 0:
            percent = round(min(max(completed, 0), count) / count * 100.0, 3)
        else:
            percent = 0.0
    else:
        percent = _coerce_float(percent, 0.0)
        if percent <= 1.0 and count is None and "progress" in summary:
            percent = round(percent * 100.0, 3)

    cleaned = {
        "index": index,
        "count": count,
        "completed": completed,
        "remaining": remaining,
        "percent": percent,
    }
    for key, value in summary.items():
        if key not in cleaned:
            cleaned[key] = value
    return cleaned


def _datetime_from_value(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        except (TypeError, ValueError, OSError):
            return None
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            return None
        try:
            parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    return None


def _runtime_identity(runtime: Any, quest_id: str | None = None) -> str:
    explicit = _normalize_identifier(quest_id)
    if explicit:
        return explicit

    direct = _first_value(runtime, "quest_id", "id", "uid", "slug", "key", "quest_key")
    direct_id = _normalize_identifier(direct)
    if direct_id:
        return direct_id

    quest = _first_value(runtime, "quest", "template", "quest_template")
    if quest is not None:
        quest_id_value = _first_value(
            quest,
            "quest_id",
            "id",
            "uid",
            "slug",
            "key",
            "template_id",
            "quest_key",
        )
        quest_id_str = _normalize_identifier(quest_id_value)
        if quest_id_str:
            return quest_id_str

    title = _first_value(runtime, "title", "name")
    title_str = _normalize_identifier(title)
    if title_str:
        return title_str

    return f"quest_{id(runtime)}"


def _runtime_title(runtime: Any) -> str:
    title = _first_value(runtime, "title", "name", "display_name")
    if title is None:
        quest = _first_value(runtime, "quest", "template", "quest_template")
        if quest is not None:
            title = _first_value(quest, "title", "name", "display_name")
    if title is None:
        quest_id = _runtime_identity(runtime)
        return quest_id
    title_str = _normalize_identifier(title)
    return title_str or _runtime_identity(runtime)


def _runtime_pinned(runtime: Any) -> bool:
    explicit = _first_value(runtime, "pinned", "is_pinned", "quest_pinned")
    if explicit is not None:
        return _coerce_bool(explicit)
    return False


def _runtime_category(runtime: Any) -> str:
    explicit = _first_value(
        runtime,
        "category",
        "quest_category",
        "quest_line",
        "quest_type",
        "line",
        "line_type",
    )
    if explicit is not None:
        category = _normalize_category(explicit)
        if category != "misc":
            return category

    if _coerce_bool(_first_value(runtime, "urgent", "is_urgent", "urgent_quest")):
        return "urgent"
    if _coerce_bool(_first_value(runtime, "main", "is_main", "main_quest")):
        return "main"
    if _coerce_bool(_first_value(runtime, "side", "is_side", "side_quest")):
        return "side"
    return "misc"


def _runtime_urgent(runtime: Any) -> bool:
    explicit = _first_value(runtime, "urgent", "is_urgent", "urgent_quest")
    if explicit is not None:
        return _coerce_bool(explicit)
    category = _runtime_category(runtime)
    return category == "urgent"


def _runtime_priority(runtime: Any) -> int:
    explicit = _first_value(runtime, "priority", "quest_priority")
    if explicit is not None:
        normalized = _coerce_optional_int(explicit)
        if normalized is not None:
            return normalized
        if isinstance(explicit, str):
            lowered = explicit.strip().lower()
            mapping = {
                "urgent": 300,
                "high": 200,
                "main": 200,
                "normal": 100,
                "side": 50,
                "low": 0,
                "misc": 0,
            }
            if lowered in mapping:
                return mapping[lowered]

    category = _runtime_category(runtime)
    priority = {
        "urgent": 300,
        "main": 200,
        "side": 100,
        "misc": 0,
    }.get(category, 0)
    if _runtime_pinned(runtime):
        priority += 25
    if _first_value(runtime, "chain_id", "quest_line") is not None:
        priority += 5
    return priority


def _runtime_stage_progress(runtime: Any) -> dict[str, Any]:
    raw_progress = _first_value(runtime, "stage_progress")
    if raw_progress is not None:
        summary = _progress_summary_from_mapping(
            raw_progress,
            default_index=_coerce_int(_first_value(runtime, "stage_index"), 0),
            default_count=_coerce_optional_int(_first_value(runtime, "stage_count")),
            total_name="stage_count",
        )
        return summary

    stage_index = _coerce_int(_first_value(runtime, "stage_index"), 0)
    stage_count = _coerce_optional_int(_first_value(runtime, "stage_count"))
    if stage_count is None:
        stage_runtimes = _first_value(runtime, "stage_runtimes")
        if isinstance(stage_runtimes, Iterable):
            try:
                stage_count = len(list(stage_runtimes))
            except TypeError:
                stage_count = None
    if stage_count is None:
        stages = _first_value(runtime, "stages")
        if isinstance(stages, Iterable):
            try:
                stage_count = len(list(stages))
            except TypeError:
                stage_count = None

    completed = max(0, min(stage_index, stage_count if stage_count is not None else stage_index))
    remaining = None if stage_count is None else max(stage_count - completed, 0)
    percent = 0.0
    if stage_count and stage_count > 0:
        percent = round(completed / stage_count * 100.0, 3)

    return {
        "index": stage_index,
        "count": stage_count,
        "completed": completed,
        "remaining": remaining,
        "percent": percent,
    }


def _runtime_chain_progress(runtime: Any) -> dict[str, Any]:
    raw_progress = _first_value(runtime, "chain_progress")
    if raw_progress is not None:
        summary = _progress_summary_from_mapping(
            raw_progress,
            default_index=_coerce_int(_first_value(runtime, "chain_index"), 0),
            default_count=_coerce_optional_int(_first_value(runtime, "chain_length")),
            total_name="chain_length",
        )
        return summary

    chain_index = _coerce_int(_first_value(runtime, "chain_index"), 0)
    chain_length = _coerce_optional_int(_first_value(runtime, "chain_length"))
    if chain_length is None:
        chain = _first_value(runtime, "chain")
        if isinstance(chain, Iterable):
            try:
                chain_length = len(list(chain))
            except TypeError:
                chain_length = None

    completed = max(0, min(chain_index, chain_length if chain_length is not None else chain_index))
    remaining = None if chain_length is None else max(chain_length - completed, 0)
    percent = 0.0
    if chain_length and chain_length > 0:
        percent = round(completed / chain_length * 100.0, 3)

    return {
        "index": chain_index,
        "length": chain_length,
        "completed": completed,
        "remaining": remaining,
        "percent": percent,
    }


def _runtime_warning_flags(runtime: Any) -> tuple[str, ...]:
    metadata = _as_dict(_first_value(runtime, "metadata"))
    values: list[str] = []

    explicit = _first_value(runtime, "warning_flags", "warnings", "warning")
    for warning in _flatten_warning_values(explicit):
        normalized = warning.strip().lower()
        if normalized and normalized not in values:
            values.append(normalized)

    if _coerce_bool(_first_value(runtime, "expiration_warning")) and "expiration_warning" not in values:
        values.append("expiration_warning")
    if _coerce_bool(_first_value(runtime, "failure_warning")) and "failure_warning" not in values:
        values.append("failure_warning")

    expires_in_days = _coerce_optional_int(_first_value(runtime, "expires_in_days"))
    warning_threshold = _coerce_optional_int(_first_value(runtime, "warning_threshold"))
    expires_at = _datetime_from_value(_first_value(runtime, "expires_at"))
    if expires_at is None and "expires_at" in metadata:
        expires_at = _datetime_from_value(metadata.get("expires_at"))

    if expires_in_days is not None:
        if expires_in_days <= 0 and "expiration_warning" not in values:
            values.append("expiration_warning")
        elif warning_threshold is not None and expires_in_days <= warning_threshold:
            if "expiration_warning" not in values:
                values.append("expiration_warning")
    elif expires_at is not None:
        now = datetime.now(timezone.utc)
        if expires_at <= now:
            if "expiration_warning" not in values:
                values.append("expiration_warning")
        elif warning_threshold is not None:
            remaining_days = max((expires_at - now).total_seconds() / 86400.0, 0.0)
            if remaining_days <= warning_threshold and "expiration_warning" not in values:
                values.append("expiration_warning")

    failure_threshold = _coerce_optional_int(_first_value(runtime, "failure_threshold"))
    status = _normalize_status(
        _first_value(runtime, "outcome", "status", "state", "quest_state")
    )
    stage_progress = _runtime_stage_progress(runtime)
    chain_progress = _runtime_chain_progress(runtime)
    if status == "failed" and "failure_warning" not in values:
        values.append("failure_warning")
    elif failure_threshold is not None:
        stage_index = stage_progress.get("index")
        chain_index = chain_progress.get("index")
        stage_remaining = stage_progress.get("remaining")
        chain_remaining = chain_progress.get("remaining")
        if (
            (isinstance(stage_index, int) and stage_index >= failure_threshold)
            or (isinstance(chain_index, int) and chain_index >= failure_threshold)
            or (isinstance(stage_remaining, int) and stage_remaining <= failure_threshold)
            or (isinstance(chain_remaining, int) and chain_remaining <= failure_threshold)
        ):
            if "failure_warning" not in values:
                values.append("failure_warning")

    return tuple(values)


def _runtime_progress_summary(runtime: Any) -> dict[str, Any]:
    quest_id = _runtime_identity(runtime)
    title = _runtime_title(runtime)
    category = _runtime_category(runtime)
    priority = _runtime_priority(runtime)
    pinned = _runtime_pinned(runtime)
    urgent = _runtime_urgent(runtime)
    status = _normalize_status(_first_value(runtime, "outcome", "status", "state", "quest_state"))
    archived = _coerce_bool(_first_value(runtime, "archived", "is_archived"))
    active = _coerce_bool(_first_value(runtime, "active", "is_active"))
    if archived and status == "active":
        status = "archived"
    elif not active and status == "active" and archived:
        status = "archived"

    summary = {
        "quest_id": quest_id,
        "title": title,
        "category": category,
        "priority": priority,
        "pinned": pinned,
        "urgent": urgent,
        "status": status,
        "stage_progress": _runtime_stage_progress(runtime),
        "chain_progress": _runtime_chain_progress(runtime),
        "warnings": list(_runtime_warning_flags(runtime)),
    }
    return summary


def _runtime_sort_key(runtime: Any) -> tuple[Any, ...]:
    summary = _runtime_progress_summary(runtime)
    pinned_rank = 0 if summary["pinned"] else 1
    urgent_rank = 0 if summary["urgent"] else 1
    main_rank = 0 if summary["category"] == "main" else 1
    priority_rank = -_coerce_int(summary["priority"], 0)
    stage_percent = -_coerce_float(summary["stage_progress"].get("percent"), 0.0)
    chain_percent = -_coerce_float(summary["chain_progress"].get("percent"), 0.0)
    quest_id = summary["quest_id"]
    return (pinned_rank, urgent_rank, main_rank, priority_rank, stage_percent, chain_percent, quest_id)


def _runtime_display_status(runtime: Any) -> str:
    summary = _runtime_progress_summary(runtime)
    return summary["status"]


def _blueprint_source_dict(blueprint: Any) -> dict[str, Any]:
    if blueprint is None:
        return {}
    for attr_name in ("to_snapshot", "snapshot", "journal_snapshot", "progress_summary", "summary"):
        attr = getattr(blueprint, attr_name, None)
        if not callable(attr):
            continue
        try:
            snapshot = attr()
        except TypeError:
            try:
                snapshot = attr(blueprint)
            except TypeError:
                continue
        data = _as_dict(snapshot)
        if data:
            return data
    if _is_mapping(blueprint):
        return dict(blueprint)
    try:
        data = dict(vars(blueprint))
    except TypeError:
        return {}
    if data:
        return data
    return _as_dict(blueprint)


def _blueprint_value(blueprint: Any, *names: str) -> Any:
    snapshot = _blueprint_source_dict(blueprint)
    for name in names:
        if name in snapshot and snapshot[name] is not None:
            return snapshot[name]
    metadata = snapshot.get("metadata")
    if isinstance(metadata, Mapping):
        for name in names:
            if name in metadata and metadata[name] is not None:
                return metadata[name]
    return _first_value(blueprint, *names)


class QuestStageRuntime:
    """Duck-typed wrapper for a single stage inside a quest runtime."""

    def __init__(
        self,
        quest_runtime: Any = None,
        stage: Any = None,
        stage_index: int = 0,
        metadata: Mapping[str, Any] | None = None,
        status: str | None = None,
        **extra: Any,
    ) -> None:
        self.quest_runtime = quest_runtime
        self.stage = stage
        self.stage_index = _coerce_int(stage_index, 0)
        self.metadata = dict(metadata or {})
        self.status = _normalize_status(status or self.metadata.get("status"))
        self.active = _coerce_bool(extra.pop("active", True))
        self.archived = _coerce_bool(extra.pop("archived", False))
        if self.status in _TERMINAL_STATUSES:
            self.active = False
        for key, value in extra.items():
            setattr(self, key, value)

    @property
    def quest_id(self) -> str:
        runtime = getattr(self, "quest_runtime", None)
        if runtime is not None:
            return _runtime_identity(runtime)
        quest_id = _first_value(self, "quest_id")
        return _normalize_identifier(quest_id) or f"stage_{id(self)}"

    @property
    def title(self) -> str:
        stage_title = _first_value(self, "title", "name", "display_name")
        if stage_title is None and self.stage is not None:
            stage_title = _first_value(self.stage, "title", "name", "display_name")
        if stage_title is None:
            return self.quest_id
        title = _normalize_identifier(stage_title)
        return title or self.quest_id

    def is_active(self) -> bool:
        return _coerce_bool(getattr(self, "active", True)) and not _coerce_bool(getattr(self, "archived", False)) and _normalize_status(getattr(self, "status", None)) not in _TERMINAL_STATUSES

    def is_terminal(self) -> bool:
        return _normalize_status(getattr(self, "status", None)) in _TERMINAL_STATUSES

    def mark_completed(self) -> None:
        self.status = "completed"
        self.active = False
        self.metadata["status"] = "completed"
        self.metadata["outcome"] = "completed"

    def mark_failed(self) -> None:
        self.status = "failed"
        self.active = False
        self.metadata["status"] = "failed"
        self.metadata["outcome"] = "failed"

    def progress_summary(self) -> dict[str, Any]:
        quest_title = self.title
        quest_id = self.quest_id
        completed = 1 if self.is_terminal() else 0
        summary = {
            "quest_id": quest_id,
            "title": quest_title,
            "status": _normalize_status(getattr(self, "status", None)),
            "stage_index": self.stage_index,
            "completed": completed,
            "warnings": [],
        }
        return summary

    def journal_snapshot(self) -> dict[str, Any]:
        return dict(self.progress_summary())


class QuestRuntime:
    """Duck-typed quest runtime that tracks stages, status, and journal state."""

    def __init__(
        self,
        quest: Any = None,
        journal: Any = None,
        quest_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        stages: Iterable[Any] | None = None,
        stage_runtimes: Iterable[Any] | None = None,
        stage_index: int = 0,
        stage_count: int | None = None,
        status: str | None = None,
        active: bool | None = None,
        archived: bool | None = None,
        title: str | None = None,
        category: str | None = None,
        pinned: bool | None = None,
        urgent: bool | None = None,
        main: bool | None = None,
        side: bool | None = None,
        completed: bool | None = None,
        failed: bool | None = None,
        progress_current: int | None = None,
        progress_goal: int | None = None,
        days_remaining: int | None = None,
        warnings: Iterable[str] | None = None,
        warning_flags: Iterable[str] | None = None,
        warning_list: Iterable[str] | None = None,
        **extra: Any,
    ) -> None:
        self.quest = quest
        self.journal = journal
        self.metadata = dict(metadata or {})

        self.quest_id = _runtime_identity(self, quest_id=quest_id)
        self.metadata.setdefault("quest_id", self.quest_id)

        if title is not None:
            self.metadata.setdefault("title", title)
            self.metadata.setdefault("name", title)
            self.metadata.setdefault("display_name", title)
        if category is not None:
            normalized_category = _normalize_category(category)
            self.metadata["category"] = category
            self.metadata["quest_category"] = category
            self.metadata["main"] = _coerce_bool(main) or normalized_category == "main"
            self.metadata["side"] = _coerce_bool(side) or normalized_category == "side"
            self.metadata["urgent"] = _coerce_bool(urgent) or normalized_category == "urgent"
        if pinned is not None:
            self.metadata["pinned"] = _coerce_bool(pinned)
        if urgent is not None:
            self.metadata["urgent"] = _coerce_bool(urgent)
        if main is not None:
            self.metadata["main"] = _coerce_bool(main)
        if side is not None:
            self.metadata["side"] = _coerce_bool(side)
        warning_sources = [value for value in (warnings, warning_flags, warning_list) if value is not None]
        if warning_sources:
            flattened_warnings: list[str] = []
            for value in warning_sources:
                flattened_warnings.extend(_flatten_warning_values(value))
            self.metadata["warnings"] = flattened_warnings
            self.metadata["warning_flags"] = flattened_warnings
            self.metadata["warning_list"] = flattened_warnings
        if days_remaining is not None:
            self.metadata["expires_in_days"] = days_remaining
        if progress_current is not None:
            stage_index = progress_current
        if progress_goal is not None:
            stage_count = progress_goal

        self.stages = list(stages) if stages is not None else list(_first_value(self, "stages") or [])
        self.stage_runtimes = list(stage_runtimes) if stage_runtimes is not None else []
        self.stage_index = _coerce_int(stage_index, 0)
        self.stage_count = _coerce_optional_int(stage_count)

        resolved_status = status or self.metadata.get("outcome") or self.metadata.get("status")
        if resolved_status is None:
            if _coerce_bool(completed):
                resolved_status = "completed"
            elif _coerce_bool(failed):
                resolved_status = "failed"
            elif _coerce_bool(archived):
                resolved_status = "archived"
            else:
                resolved_status = "active"
        self.status = _normalize_status(resolved_status)

        self.active = _coerce_bool(True if active is None else active)
        self.archived = _coerce_bool(False if archived is None else archived)
        if _coerce_bool(completed) or _coerce_bool(failed):
            self.active = False
            self.archived = True
        if self.status in _TERMINAL_STATUSES:
            self.active = False
        if self.archived and self.status == "active":
            self.status = "archived"
        self.metadata.setdefault("status", self.status)
        if self.status in _TERMINAL_STATUSES:
            self.metadata["outcome"] = self.status

        for key, value in extra.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def from_blueprint(
        cls,
        blueprint: Any,
        *,
        journal: Any = None,
        quest: Any = None,
        **extra: Any,
    ) -> "QuestRuntime":
        blueprint_metadata = _as_dict(_blueprint_value(blueprint, "metadata"))
        explicit_metadata = _as_dict(extra.pop("metadata", None))
        metadata = dict(explicit_metadata)
        metadata.update(blueprint_metadata)

        quest_source = quest
        if quest_source is None:
            quest_source = _blueprint_value(blueprint, "quest", "template", "quest_template")
        if quest_source is None:
            quest_source = blueprint

        category = _blueprint_value(
            blueprint,
            "category",
            "quest_category",
            "quest_line",
            "quest_type",
            "line",
            "line_type",
        )
        warning_values = _blueprint_value(blueprint, "warnings", "warning_flags", "warning_list")

        runtime = cls(
            quest=quest_source,
            journal=journal,
            quest_id=_blueprint_value(blueprint, "quest_id", "id", "uid", "slug", "key", "quest_key", "template_id"),
            metadata=metadata,
            stages=_blueprint_value(blueprint, "stages"),
            stage_runtimes=_blueprint_value(blueprint, "stage_runtimes"),
            stage_index=_coerce_int(_blueprint_value(blueprint, "stage_index", "current_stage_index"), 0),
            stage_count=_coerce_optional_int(
                _blueprint_value(blueprint, "stage_count", "total_stages", "stage_total")
            ),
            status=_blueprint_value(blueprint, "status", "state", "quest_state", "outcome"),
            active=_blueprint_value(blueprint, "active", "is_active"),
            archived=_blueprint_value(blueprint, "archived", "is_archived"),
            title=_blueprint_value(blueprint, "title", "name", "display_name"),
            category=category,
            pinned=_blueprint_value(blueprint, "pinned", "is_pinned", "quest_pinned"),
            urgent=_blueprint_value(blueprint, "urgent", "is_urgent", "urgent_quest"),
            main=_blueprint_value(blueprint, "main", "is_main", "main_quest"),
            side=_blueprint_value(blueprint, "side", "is_side", "side_quest"),
            completed=_blueprint_value(blueprint, "completed", "is_completed"),
            failed=_blueprint_value(blueprint, "failed", "is_failed"),
            progress_current=_blueprint_value(
                blueprint, "progress_current", "current_progress", "progress"
            ),
            progress_goal=_blueprint_value(blueprint, "progress_goal", "goal", "target_progress"),
            days_remaining=_blueprint_value(blueprint, "days_remaining", "turns_remaining", "expires_in_days"),
            warnings=warning_values,
            warning_flags=warning_values,
            warning_list=warning_values,
            **extra,
        )
        if blueprint_metadata:
            runtime.metadata.update(blueprint_metadata)
        return runtime

    @property
    def title(self) -> str:
        return _runtime_title(self)

    def _status_value(self) -> str:
        status = _normalize_status(
            _first_value(self, "outcome", "status", "state", "quest_state")
            or getattr(self, "status", None)
        )
        if _coerce_bool(getattr(self, "archived", False)) and status == "active":
            return "archived"
        return status

    def is_active(self) -> bool:
        status = self._status_value()
        return _coerce_bool(getattr(self, "active", True)) and not _coerce_bool(getattr(self, "archived", False)) and status == "active"

    def is_terminal(self) -> bool:
        return self._status_value() in _TERMINAL_STATUSES

    def is_completed(self) -> bool:
        return self._status_value() == "completed"

    def is_failed(self) -> bool:
        return self._status_value() == "failed"

    def is_pinned(self) -> bool:
        return _runtime_pinned(self)

    def is_main_quest(self) -> bool:
        return self.quest_category() == "main"

    def is_side_quest(self) -> bool:
        return self.quest_category() == "side"

    def is_urgent_quest(self) -> bool:
        return _runtime_urgent(self)

    @property
    def category(self) -> str:
        return self.quest_category()

    def quest_category(self) -> str:
        category = _runtime_category(self)
        return category if category in _CATEGORY_BUCKETS else "misc"

    def quest_priority(self) -> int:
        return _runtime_priority(self)

    def warning_flags(self) -> tuple[str, ...]:
        return _runtime_warning_flags(self)

    def _stage_progress(self) -> dict[str, Any]:
        return _runtime_stage_progress(self)

    def _chain_progress(self) -> dict[str, Any]:
        return _runtime_chain_progress(self)

    def progress_summary(self) -> dict[str, Any]:
        status = self._status_value()
        if self.archived and status == "active":
            status = "archived"
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "category": self.quest_category(),
            "priority": self.quest_priority(),
            "pinned": self.is_pinned(),
            "urgent": self.is_urgent_quest(),
            "status": status,
            "stage_progress": self._stage_progress(),
            "chain_progress": self._chain_progress(),
            "warnings": list(self.warning_flags()),
        }

    def journal_snapshot(self) -> dict[str, Any]:
        return dict(self.progress_summary())

    def summary(self) -> dict[str, Any]:
        return self.progress_summary()

    def snapshot(self) -> dict[str, Any]:
        return self.journal_snapshot()

    def mark_completed(self) -> None:
        self.status = "completed"
        self.active = False
        self.metadata["status"] = "completed"
        self.metadata["outcome"] = "completed"

    def mark_failed(self) -> None:
        self.status = "failed"
        self.active = False
        self.metadata["status"] = "failed"
        self.metadata["outcome"] = "failed"

    def add_stage_runtime(
        self,
        stage: Any,
        *,
        stage_index: int | None = None,
        metadata: Mapping[str, Any] | None = None,
        status: str | None = None,
        **extra: Any,
    ) -> QuestStageRuntime:
        runtime = QuestStageRuntime(
            quest_runtime=self,
            stage=stage,
            stage_index=self.stage_index if stage_index is None else stage_index,
            metadata=metadata,
            status=status,
            **extra,
        )
        self.stage_runtimes.append(runtime)
        return runtime

    def current_stage_runtime(self) -> Any:
        if not self.stage_runtimes:
            return None
        index = self.stage_index
        if 0 <= index < len(self.stage_runtimes):
            return self.stage_runtimes[index]
        return self.stage_runtimes[-1]

    def dispatch_event(self, event: Any) -> list[Any]:
        results: list[Any] = []
        handler_names = ("dispatch_event", "handle_event", "on_event")
        stage_runtime = self.current_stage_runtime()

        for handler_name in handler_names:
            handler = getattr(self, handler_name, None)
            if callable(handler) and handler is not self.dispatch_event:
                try:
                    results.append(handler(event))
                except TypeError:
                    try:
                        results.append(handler(event, self))
                    except TypeError:
                        continue
                break

        if stage_runtime is not None:
            for handler_name in handler_names:
                handler = getattr(stage_runtime, handler_name, None)
                if callable(handler):
                    try:
                        results.append(handler(event))
                    except TypeError:
                        try:
                            results.append(handler(event, self))
                        except TypeError:
                            continue
                    break

        quest = getattr(self, "quest", None)
        if quest is not None:
            for handler_name in handler_names:
                handler = getattr(quest, handler_name, None)
                if callable(handler):
                    try:
                        results.append(handler(event))
                    except TypeError:
                        try:
                            results.append(handler(event, self))
                        except TypeError:
                            continue
                    break

        return results

    def handle_event(self, event: Any) -> list[Any]:
        return self.dispatch_event(event)

    def advance_stage(self, stage: Any | None = None, *, stage_index: int | None = None, metadata: Mapping[str, Any] | None = None, status: str | None = None) -> Any:
        if stage_index is not None:
            self.stage_index = _coerce_int(stage_index, self.stage_index)
        else:
            self.stage_index += 1
        if stage is None and self.stage_runtimes:
            current = self.current_stage_runtime()
            if current is not None:
                return current
        return self.add_stage_runtime(stage, stage_index=self.stage_index, metadata=metadata, status=status)

    def is_terminal_state(self) -> bool:
        return self.is_terminal()


class QuestJournal:
    """Active quest journal with capacity, pinning, and archive tracking."""

    def __init__(
        self,
        runtimes: Mapping[str, Any] | None = None,
        archived_runtimes: Mapping[str, Any] | None = None,
        max_active_quests: int | None = None,
        capacity: int | None = None,
        active_capacity: int | None = None,
        capacity_limit: int | None = None,
        pinned_quest_ids: Iterable[str] | None = None,
        main_quest_ids: Iterable[str] | None = None,
        side_quest_ids: Iterable[str] | None = None,
        urgent_quest_ids: Iterable[str] | None = None,
        completed_quest_ids: Iterable[str] | None = None,
        failed_quest_ids: Iterable[str] | None = None,
        **extra: Any,
    ) -> None:
        self.runtimes: dict[str, Any] = self._coerce_runtime_mapping(runtimes)
        self.archived_runtimes: dict[str, Any] = self._coerce_runtime_mapping(archived_runtimes)

        resolved_capacity = _coerce_optional_int(max_active_quests)
        capacity_aliases = [
            _coerce_optional_int(capacity),
            _coerce_optional_int(active_capacity),
            _coerce_optional_int(capacity_limit),
        ]
        if resolved_capacity in (None, 0):
            for alias_value in capacity_aliases:
                if alias_value is not None:
                    resolved_capacity = alias_value
                    break
        self.max_active_quests = resolved_capacity
        self.capacity = _coerce_optional_int(capacity)
        self.active_capacity = _coerce_optional_int(active_capacity)
        self.capacity_limit = _coerce_optional_int(capacity_limit)

        self.pinned_quest_ids: set[str] = set(pinned_quest_ids or [])
        self.main_quest_ids: set[str] = set(main_quest_ids or [])
        self.side_quest_ids: set[str] = set(side_quest_ids or [])
        self.urgent_quest_ids: set[str] = set(urgent_quest_ids or [])
        self.completed_quest_ids: set[str] = set(completed_quest_ids or [])
        self.failed_quest_ids: set[str] = set(failed_quest_ids or [])
        for key, value in extra.items():
            if not hasattr(self, key):
                setattr(self, key, value)
        self._sync_journal_storage_aliases()
        for runtime in self.runtimes.values():
            self._attach_runtime(runtime)
        for runtime in self.archived_runtimes.values():
            self._attach_runtime(runtime)
        if self.runtimes or self.archived_runtimes:
            self._refresh_indexes()

    @classmethod
    def from_blueprints(
        cls,
        blueprints: Any,
        *,
        max_active_quests: int | None = None,
        capacity: int | None = None,
        active_capacity: int | None = None,
        capacity_limit: int | None = None,
        **extra: Any,
    ) -> "QuestJournal":
        journal = cls(
            max_active_quests=max_active_quests,
            capacity=capacity,
            active_capacity=active_capacity,
            capacity_limit=capacity_limit,
            **extra,
        )
        if blueprints is None:
            return journal
        if _is_mapping(blueprints):
            blueprint_items = list(blueprints.values())
        elif isinstance(blueprints, (str, bytes)):
            blueprint_items = [blueprints]
        else:
            try:
                blueprint_items = list(blueprints)
            except TypeError:
                blueprint_items = [blueprints]
        for blueprint in blueprint_items:
            runtime = QuestRuntime.from_blueprint(blueprint, journal=journal)
            journal.register_runtime(runtime, allow_overflow=True)
        return journal

    @classmethod
    def from_chain(
        cls,
        chain: Any,
        *,
        max_active_quests: int | None = None,
        capacity: int | None = None,
        active_capacity: int | None = None,
        capacity_limit: int | None = None,
        **extra: Any,
    ) -> "QuestJournal":
        journal = cls(
            max_active_quests=max_active_quests,
            capacity=capacity,
            active_capacity=active_capacity,
            capacity_limit=capacity_limit,
            **extra,
        )
        if chain is None:
            return journal
        chain_id = _normalize_identifier(_blueprint_value(chain, "chain_id", "id", "uid", "slug", "key"))
        chain_title = _blueprint_value(chain, "title", "name")
        entry_quest_id = _normalize_identifier(_blueprint_value(chain, "entry_quest_id", "entry_id"))
        chain_metadata = _as_dict(_blueprint_value(chain, "metadata"))
        if chain_id:
            setattr(journal, "chain_id", chain_id)
        if chain_title is not None:
            setattr(journal, "chain_title", chain_title)
        if entry_quest_id:
            setattr(journal, "entry_quest_id", entry_quest_id)
        if chain_metadata:
            setattr(journal, "chain_metadata", chain_metadata)

        if callable(getattr(chain, "normalized_quests", None)):
            blueprints = chain.normalized_quests()
        else:
            blueprints = _blueprint_value(chain, "quests", "templates")
        if blueprints is None:
            return journal
        if _is_mapping(blueprints):
            blueprint_items = list(blueprints.values())
        elif isinstance(blueprints, (str, bytes)):
            blueprint_items = [blueprints]
        else:
            try:
                blueprint_items = list(blueprints)
            except TypeError:
                blueprint_items = [blueprints]
        for blueprint in blueprint_items:
            runtime = QuestRuntime.from_blueprint(blueprint, journal=journal)
            if chain_id or chain_title or entry_quest_id or chain_metadata:
                metadata = _ensure_runtime_metadata(runtime)
                if chain_id:
                    metadata.setdefault("chain_id", chain_id)
                    metadata.setdefault("quest_chain_id", chain_id)
                if chain_title is not None:
                    metadata.setdefault("chain_title", chain_title)
                if entry_quest_id:
                    metadata.setdefault("entry_quest_id", entry_quest_id)
                if chain_metadata:
                    metadata.setdefault("chain_metadata", dict(chain_metadata))
            journal.register_runtime(runtime, allow_overflow=True)
        return journal

    @staticmethod
    def _coerce_runtime_mapping(value: Any) -> dict[str, Any]:
        if value is None:
            return {}
        if isinstance(value, Mapping):
            return dict(value)
        if isinstance(value, (str, bytes)):
            return {}
        try:
            items = list(value)
        except TypeError:
            return {}
        mapping: dict[str, Any] = {}
        for runtime in items:
            runtime_id = _runtime_identity(runtime)
            mapping[runtime_id] = runtime
        return mapping

    def _sync_journal_storage_aliases(self) -> None:
        for attr_name, default in (
            ("runtimes", {}),
            ("archived_runtimes", {}),
            ("pinned_quest_ids", set()),
            ("main_quest_ids", set()),
            ("side_quest_ids", set()),
            ("urgent_quest_ids", set()),
            ("completed_quest_ids", set()),
            ("failed_quest_ids", set()),
        ):
            if not hasattr(self, attr_name):
                setattr(self, attr_name, default.copy() if isinstance(default, dict) else set(default))
        if isinstance(getattr(self, "runtimes", None), list):
            self.runtimes = self._coerce_runtime_mapping(self.runtimes)
        if isinstance(getattr(self, "archived_runtimes", None), list):
            self.archived_runtimes = self._coerce_runtime_mapping(self.archived_runtimes)

        capacity_alias = _coerce_optional_int(_first_value(self, "capacity", "active_capacity", "capacity_limit"))
        if capacity_alias is not None and (getattr(self, "max_active_quests", None) in (None, 0)):
            self.max_active_quests = capacity_alias
        if getattr(self, "capacity", None) is None:
            setattr(self, "capacity", self.max_active_quests)
        if getattr(self, "active_capacity", None) is None:
            setattr(self, "active_capacity", self.max_active_quests)
        if getattr(self, "capacity_limit", None) is None:
            setattr(self, "capacity_limit", self.max_active_quests)

    def __len__(self) -> int:
        return len(self._active_runtimes())

    def __iter__(self):
        return iter(self._active_runtimes())

    def _attach_runtime(self, runtime: Any, quest_id: str | None = None) -> Any:
        runtime_id = _runtime_identity(runtime, quest_id=quest_id)
        metadata = _ensure_runtime_metadata(runtime)
        metadata.setdefault("quest_id", runtime_id)
        try:
            setattr(runtime, "quest_id", runtime_id)
        except Exception:
            pass
        try:
            setattr(runtime, "journal", self)
        except Exception:
            pass
        return runtime

    def _purge_runtime_references(self, runtime: Any | None = None, quest_id: str | None = None) -> None:
        candidate_ids: set[str] = set()
        runtime_id = _normalize_identifier(quest_id)
        if runtime_id:
            candidate_ids.add(runtime_id)
        if runtime is not None:
            resolved = _runtime_identity(runtime)
            if resolved:
                candidate_ids.add(resolved)

        for mapping in (self.runtimes, self.archived_runtimes):
            for key, value in list(mapping.items()):
                if value is runtime or (key in candidate_ids):
                    mapping.pop(key, None)

    def _active_runtimes(self) -> list[Any]:
        self._sync_journal_storage_aliases()
        active: list[Any] = []
        for runtime in self.runtimes.values():
            if _coerce_bool(getattr(runtime, "active", True)) and not _coerce_bool(getattr(runtime, "archived", False)):
                status = _runtime_display_status(runtime)
                if status == "active":
                    active.append(runtime)
        return active

    def _archived_runtimes(self) -> list[Any]:
        self._sync_journal_storage_aliases()
        archived: list[Any] = []
        seen_ids: set[str] = set()
        for runtime in self.archived_runtimes.values():
            quest_id = _runtime_identity(runtime)
            if quest_id not in seen_ids:
                archived.append(runtime)
                seen_ids.add(quest_id)
        for runtime in self.runtimes.values():
            quest_id = _runtime_identity(runtime)
            if quest_id in seen_ids:
                continue
            if _coerce_bool(getattr(runtime, "archived", False)) or _runtime_display_status(runtime) in _TERMINAL_STATUSES or not _coerce_bool(getattr(runtime, "active", True)):
                archived.append(runtime)
                seen_ids.add(quest_id)
        return archived

    def _all_known_runtimes(self) -> list[Any]:
        self._sync_journal_storage_aliases()
        combined: list[Any] = []
        combined.extend(self._active_runtimes())
        combined.extend(self._archived_runtimes())
        return combined

    def _refresh_indexes(self) -> None:
        self._sync_journal_storage_aliases()
        self.pinned_quest_ids.clear()
        self.main_quest_ids.clear()
        self.side_quest_ids.clear()
        self.urgent_quest_ids.clear()
        self.completed_quest_ids.clear()
        self.failed_quest_ids.clear()

        for runtime in self._active_runtimes():
            quest_id = _runtime_identity(runtime)
            category = _runtime_category(runtime)
            if _runtime_pinned(runtime):
                self.pinned_quest_ids.add(quest_id)
            if category == "main":
                self.main_quest_ids.add(quest_id)
            elif category == "side":
                self.side_quest_ids.add(quest_id)
            if _runtime_urgent(runtime):
                self.urgent_quest_ids.add(quest_id)

        for runtime in self._archived_runtimes():
            quest_id = _runtime_identity(runtime)
            status = _runtime_display_status(runtime)
            if status == "completed":
                self.completed_quest_ids.add(quest_id)
            elif status == "failed":
                self.failed_quest_ids.add(quest_id)

    def _active_non_pinned_count(self) -> int:
        count = 0
        for runtime in self._active_runtimes():
            if not _runtime_pinned(runtime):
                count += 1
        return count

    def _resolve_runtime(self, runtime_or_quest_id: Any) -> Any | None:
        if runtime_or_quest_id is None:
            return None
        if isinstance(runtime_or_quest_id, str):
            runtime = self.runtimes.get(runtime_or_quest_id)
            if runtime is not None:
                return runtime
            return self.archived_runtimes.get(runtime_or_quest_id)
        runtime_id = _runtime_identity(runtime_or_quest_id)
        runtime = self.runtimes.get(runtime_id)
        if runtime is not None:
            return runtime
        archived = self.archived_runtimes.get(runtime_id)
        if archived is not None:
            return archived
        return runtime_or_quest_id

    def _resolve_runtime_id(self, runtime_or_quest_id: Any, runtime: Any | None = None) -> str:
        if isinstance(runtime_or_quest_id, str):
            return runtime_or_quest_id
        if runtime is not None:
            return _runtime_identity(runtime)
        return _runtime_identity(runtime_or_quest_id)

    def _apply_runtime_category_updates(
        self,
        runtime: Any,
        *,
        category: str | None = None,
        pinned: bool | None = None,
        urgent: bool | None = None,
    ) -> None:
        metadata = _ensure_runtime_metadata(runtime)
        if category is not None:
            normalized = _normalize_category(category)
            metadata["category"] = category
            metadata["quest_category"] = category
            if normalized == "main":
                metadata["main"] = True
                metadata["side"] = False
                metadata["urgent"] = False
            elif normalized == "side":
                metadata["side"] = True
                metadata["main"] = False
                metadata["urgent"] = False
            elif normalized == "urgent":
                metadata["urgent"] = True
                metadata["main"] = False
                metadata["side"] = False
            else:
                metadata["main"] = False
                metadata["side"] = False
                metadata["urgent"] = False
        if pinned is not None:
            metadata["pinned"] = bool(pinned)
        if urgent is not None:
            metadata["urgent"] = bool(urgent)
            if urgent:
                metadata["main"] = False
                metadata["side"] = False
        self._attach_runtime(runtime)

    def _prepare_register(self, runtime: Any, quest_id: str | None = None) -> tuple[str, Any]:
        resolved_id = self._resolve_runtime_id(runtime, quest_id)
        self._attach_runtime(runtime, resolved_id)
        return resolved_id, runtime

    def set_max_active_quests(self, limit: int | None) -> None:
        if limit is None:
            self.max_active_quests = None
            self.capacity = None
            self.active_capacity = None
            self.capacity_limit = None
            return
        limit_value = _coerce_optional_int(limit)
        if limit_value is None:
            raise ValueError("max_active_quests must be an integer or None")
        if limit_value < 0:
            raise ValueError("max_active_quests cannot be negative")
        self.max_active_quests = limit_value
        self.capacity = limit_value
        self.active_capacity = limit_value
        self.capacity_limit = limit_value

    def can_register_runtime(self, runtime: Any) -> bool:
        runtime_id = _runtime_identity(runtime)
        existing = self.runtimes.get(runtime_id)
        if existing is runtime:
            return True
        if self.max_active_quests is None:
            return True
        if _runtime_pinned(runtime):
            return True
        active_non_pinned = self._active_non_pinned_count()
        return active_non_pinned < self.max_active_quests

    def register_runtime(
        self,
        runtime: Any,
        *,
        quest_id: str | None = None,
        allow_overflow: bool = False,
    ) -> Any:
        resolved_id, runtime = self._prepare_register(runtime, quest_id=quest_id)
        pinned = _runtime_pinned(runtime)
        existing = self.runtimes.get(resolved_id)
        if existing is runtime:
            self._refresh_indexes()
            return runtime

        if not allow_overflow and self.max_active_quests is not None and not pinned:
            active_non_pinned = self._active_non_pinned_count()
            if existing is None and active_non_pinned >= self.max_active_quests:
                raise RuntimeError(
                    f"Cannot register quest {resolved_id!r}: non-pinned active quest capacity "
                    f"of {self.max_active_quests} has been reached."
                )

        self._purge_runtime_references(runtime=runtime, quest_id=resolved_id)
        self.runtimes[resolved_id] = runtime
        try:
            setattr(runtime, "active", True)
        except Exception:
            pass
        try:
            setattr(runtime, "archived", False)
        except Exception:
            pass
        self._refresh_indexes()
        return runtime

    def pin_runtime(self, runtime_or_quest_id: Any) -> bool:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return False
        if _runtime_pinned(runtime):
            return False
        metadata = _ensure_runtime_metadata(runtime)
        metadata["pinned"] = True
        try:
            setattr(runtime, "pinned", True)
        except Exception:
            pass
        self._attach_runtime(runtime)
        self._refresh_indexes()
        return True

    def unpin_runtime(self, runtime_or_quest_id: Any) -> bool:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return False
        if not _runtime_pinned(runtime):
            return False
        metadata = _ensure_runtime_metadata(runtime)
        metadata["pinned"] = False
        try:
            setattr(runtime, "pinned", False)
        except Exception:
            pass
        self._attach_runtime(runtime)
        self._refresh_indexes()
        return True

    def categorize_runtime(
        self,
        runtime_or_quest_id: Any,
        *,
        category: str | None = None,
        pinned: bool | None = None,
        urgent: bool | None = None,
    ) -> dict[str, Any]:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return {}
        self._apply_runtime_category_updates(runtime, category=category, pinned=pinned, urgent=urgent)
        self._refresh_indexes()
        return self.quest_progress_summary(runtime)

    def active_runtime_ids(self, *, sorted: bool = False) -> list[str]:
        active = self._active_runtimes()
        if sorted:
            active = self.sorted_active_runtimes()
        return [_runtime_identity(runtime) for runtime in active]

    def sorted_active_runtimes(
        self,
        *,
        category: str | None = None,
        pinned: bool | None = None,
        urgent: bool | None = None,
        reverse: bool = True,
    ) -> list[Any]:
        filtered = self.filtered_active_runtimes(category=category, pinned=pinned, urgent=urgent)
        ordered = builtins.sorted(filtered, key=_runtime_sort_key)
        if not reverse:
            ordered.reverse()
        return ordered

    def filtered_active_runtimes(self, **filters: Any) -> list[Any]:
        active = self._active_runtimes()
        if not filters:
            return active

        results: list[Any] = []
        for runtime in active:
            if self._runtime_matches_filters(runtime, filters):
                results.append(runtime)
        return builtins.sorted(results, key=_runtime_sort_key)

    def _runtime_matches_filters(self, runtime: Any, filters: Mapping[str, Any]) -> bool:
        summary = _runtime_progress_summary(runtime)
        runtime_id = summary["quest_id"]
        category = summary["category"]
        pinned = summary["pinned"]
        urgent = summary["urgent"]
        status = summary["status"]
        priority = summary["priority"]

        for key, expected in filters.items():
            if expected is None:
                continue
            if key in {"category", "quest_category"}:
                if isinstance(expected, (list, tuple, set, frozenset)):
                    normalized = {_normalize_category(value) for value in expected}
                    if category not in normalized:
                        return False
                elif category != _normalize_category(expected):
                    return False
            elif key == "pinned":
                if pinned != _coerce_bool(expected):
                    return False
            elif key == "urgent":
                if urgent != _coerce_bool(expected):
                    return False
            elif key in {"main", "side"}:
                value = category == key
                if value != _coerce_bool(expected):
                    return False
            elif key in {"status", "state"}:
                if status != _normalize_status(expected):
                    return False
            elif key == "active":
                if _coerce_bool(expected) != (status == "active"):
                    return False
            elif key == "archived":
                if _coerce_bool(expected) != (status == "archived"):
                    return False
            elif key == "completed":
                if _coerce_bool(expected) != (status == "completed"):
                    return False
            elif key == "failed":
                if _coerce_bool(expected) != (status == "failed"):
                    return False
            elif key in {"quest_id", "id", "uid"}:
                if _normalize_identifier(expected) != runtime_id:
                    return False
            elif key in {"quest_ids", "ids"}:
                expected_ids = {_normalize_identifier(value) for value in expected}
                if runtime_id not in expected_ids:
                    return False
            elif key == "priority":
                if priority != _coerce_int(expected, priority):
                    return False
            elif key == "min_priority":
                if priority < _coerce_int(expected, priority):
                    return False
            elif key == "max_priority":
                if priority > _coerce_int(expected, priority):
                    return False
            elif key in {"title", "name"}:
                runtime_title = _runtime_title(runtime)
                if isinstance(expected, (list, tuple, set, frozenset)):
                    candidates = {_normalize_identifier(value) for value in expected}
                    if runtime_title not in candidates:
                        return False
                elif runtime_title != _normalize_identifier(expected):
                    return False
            elif key in {"warnings", "warning_flags"}:
                warning_flags = set(summary["warnings"])
                expected_flags = set(_flatten_warning_values(expected))
                expected_flags = {flag.strip().lower() for flag in expected_flags if flag.strip().lower() in _WARNING_FLAGS}
                if not expected_flags.issubset(warning_flags):
                    return False
            else:
                value = _first_value(runtime, key)
                if isinstance(expected, (list, tuple, set, frozenset)):
                    candidates = {_normalize_identifier(value) for value in expected}
                    runtime_value = _first_value(runtime, key)
                    normalized_runtime_value = _normalize_identifier(runtime_value)
                    if normalized_runtime_value not in candidates:
                        return False
                else:
                    runtime_value = _first_value(runtime, key)
                    if _is_mapping(runtime_value) and _is_mapping(expected):
                        if dict(runtime_value) != dict(expected):
                            return False
                    elif runtime_value != expected:
                        return False
        return True

    def get_runtime(self, quest_id: str) -> Any | None:
        runtime = self.runtimes.get(quest_id)
        if runtime is not None:
            return runtime
        return self.archived_runtimes.get(quest_id)

    def quest_summary(self, quest_id: str) -> dict[str, Any] | None:
        runtime = self.get_runtime(quest_id)
        if runtime is None:
            return None
        return self.quest_progress_summary(runtime)

    def quest_progress_summary(self, runtime_or_quest_id: Any) -> dict[str, Any]:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return {}
        if hasattr(runtime, "progress_summary") and callable(getattr(runtime, "progress_summary")):
            try:
                summary = runtime.progress_summary()
            except TypeError:
                summary = _runtime_progress_summary(runtime)
        else:
            summary = _runtime_progress_summary(runtime)
        return dict(summary)

    def journal_snapshot(self) -> dict[str, Any]:
        self._refresh_indexes()
        active_runtimes = self.sorted_active_runtimes()
        archived_runtimes = self._archived_runtimes()

        pinned_runtimes = [runtime for runtime in active_runtimes if _runtime_pinned(runtime)]
        main_runtimes = [runtime for runtime in active_runtimes if _runtime_category(runtime) == "main"]
        side_runtimes = [runtime for runtime in active_runtimes if _runtime_category(runtime) == "side"]
        urgent_runtimes = [runtime for runtime in active_runtimes if _runtime_urgent(runtime)]
        completed_archive = [
            runtime
            for runtime in archived_runtimes
            if _runtime_display_status(runtime) == "completed"
        ]
        failed_archive = [
            runtime
            for runtime in archived_runtimes
            if _runtime_display_status(runtime) == "failed"
        ]

        quests = [
            runtime.journal_snapshot() if hasattr(runtime, "journal_snapshot") else _runtime_progress_summary(runtime)
            for runtime in active_runtimes
        ]

        capacity_remaining: int | None
        if self.max_active_quests is None:
            capacity_remaining = None
        else:
            capacity_remaining = max(self.max_active_quests - self._active_non_pinned_count(), 0)

        warning_flags: list[str] = []
        for runtime in active_runtimes + archived_runtimes:
            for warning in _runtime_warning_flags(runtime):
                if warning not in warning_flags:
                    warning_flags.append(warning)

        return {
            "active_runtimes": active_runtimes,
            "archived_runtimes": archived_runtimes,
            "pinned_runtimes": pinned_runtimes,
            "main_runtimes": main_runtimes,
            "side_runtimes": side_runtimes,
            "urgent_runtimes": urgent_runtimes,
            "completed_archive": completed_archive,
            "failed_archive": failed_archive,
            "warnings": warning_flags,
            "warning_flags": warning_flags,
            "quests": quests,
            "archives": {
                "completed": completed_archive,
                "failed": failed_archive,
            },
            "active_quest_ids": [_runtime_identity(runtime) for runtime in active_runtimes],
            "archived_quest_ids": [_runtime_identity(runtime) for runtime in archived_runtimes],
            "completed_quest_ids": builtins.sorted(self.completed_quest_ids),
            "failed_quest_ids": builtins.sorted(self.failed_quest_ids),
            "pinned_quest_ids": builtins.sorted(self.pinned_quest_ids),
            "main_quest_ids": builtins.sorted(self.main_quest_ids),
            "side_quest_ids": builtins.sorted(self.side_quest_ids),
            "urgent_quest_ids": builtins.sorted(self.urgent_quest_ids),
            "active_count": len(active_runtimes),
            "capacity": self.max_active_quests,
            "active_capacity": self.max_active_quests,
            "capacity_limit": self.max_active_quests,
            "capacity_remaining": capacity_remaining,
        }

    def archive_runtime(self, runtime_or_quest_id: Any, *, outcome: str | None = None) -> Any | None:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return None
        quest_id = self._resolve_runtime_id(runtime_or_quest_id, runtime)
        self._purge_runtime_references(runtime=runtime, quest_id=quest_id)
        if outcome is not None:
            normalized_outcome = _normalize_status(outcome)
            if normalized_outcome in _TERMINAL_STATUSES:
                try:
                    setattr(runtime, "status", normalized_outcome)
                except Exception:
                    pass
                metadata = _ensure_runtime_metadata(runtime)
                metadata["status"] = normalized_outcome
                metadata["outcome"] = normalized_outcome
        try:
            setattr(runtime, "active", False)
        except Exception:
            pass
        try:
            setattr(runtime, "archived", True)
        except Exception:
            pass
        self.archived_runtimes[quest_id] = runtime
        self._attach_runtime(runtime, quest_id)
        self._refresh_indexes()
        return runtime

    def archive(self, runtime_or_quest_id: Any, *, outcome: str | None = None) -> Any | None:
        return self.archive_runtime(runtime_or_quest_id, outcome=outcome)

    def archive_terminal_runtimes(self) -> list[Any]:
        archived: list[Any] = []
        for runtime in list(self._active_runtimes()):
            if _runtime_display_status(runtime) in _TERMINAL_STATUSES:
                archived_runtime = self.archive_runtime(runtime)
                if archived_runtime is not None:
                    archived.append(archived_runtime)
        return archived

    def complete_runtime(self, runtime_or_quest_id: Any) -> Any | None:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return None
        if hasattr(runtime, "mark_completed") and callable(getattr(runtime, "mark_completed")):
            runtime.mark_completed()
        else:
            metadata = _ensure_runtime_metadata(runtime)
            metadata["status"] = "completed"
            metadata["outcome"] = "completed"
            try:
                setattr(runtime, "status", "completed")
            except Exception:
                pass
            try:
                setattr(runtime, "active", False)
            except Exception:
                pass
        quest_id = self._resolve_runtime_id(runtime_or_quest_id, runtime)
        self.completed_quest_ids.add(quest_id)
        archived = self.archive_runtime(runtime, outcome="completed")
        self._refresh_indexes()
        return archived

    def fail_runtime(self, runtime_or_quest_id: Any) -> Any | None:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        if runtime is None:
            return None
        if hasattr(runtime, "mark_failed") and callable(getattr(runtime, "mark_failed")):
            runtime.mark_failed()
        else:
            metadata = _ensure_runtime_metadata(runtime)
            metadata["status"] = "failed"
            metadata["outcome"] = "failed"
            try:
                setattr(runtime, "status", "failed")
            except Exception:
                pass
            try:
                setattr(runtime, "active", False)
            except Exception:
                pass
        quest_id = self._resolve_runtime_id(runtime_or_quest_id, runtime)
        self.failed_quest_ids.add(quest_id)
        archived = self.archive_runtime(runtime, outcome="failed")
        self._refresh_indexes()
        return archived

    def dispatch_event(self, event: Any) -> list[Any]:
        results: list[Any] = []
        active_runtimes = list(self._active_runtimes())
        target_quest_id = _normalize_identifier(_first_value(event, "quest_id", "id", "uid")) if _first_value(event, "quest_id", "id", "uid") is not None else None

        for runtime in active_runtimes:
            if target_quest_id is not None and _runtime_identity(runtime) != target_quest_id:
                continue
            handler = getattr(runtime, "dispatch_event", None)
            if callable(handler):
                try:
                    result = handler(event)
                except TypeError:
                    result = handler(event, self)
                results.append(result)
            elif callable(getattr(runtime, "handle_event", None)):
                handler = getattr(runtime, "handle_event")
                try:
                    result = handler(event)
                except TypeError:
                    result = handler(event, self)
                results.append(result)

            if _runtime_display_status(runtime) in _TERMINAL_STATUSES:
                self.archive_runtime(runtime, outcome=_runtime_display_status(runtime))
        return results

    def dispatch(self, event: Any) -> list[Any]:
        return self.dispatch_event(event)

    def register(self, runtime: Any, *, quest_id: str | None = None, allow_overflow: bool = False) -> Any:
        return self.register_runtime(runtime, quest_id=quest_id, allow_overflow=allow_overflow)

    def can_archive_runtime(self, runtime_or_quest_id: Any) -> bool:
        runtime = self._resolve_runtime(runtime_or_quest_id)
        return runtime is not None

    def quest_progress_summary_for_active(self) -> list[dict[str, Any]]:
        return [runtime.journal_snapshot() if hasattr(runtime, "journal_snapshot") else _runtime_progress_summary(runtime) for runtime in self.sorted_active_runtimes()]

    def summary(self) -> dict[str, Any]:
        return self.journal_snapshot()

    def presentation_summary(self) -> dict[str, Any]:
        return quest_journal_presentation_summary(self)

    def presentation_snapshot(self) -> dict[str, Any]:
        return self.presentation_summary()

    def quest_sections(self) -> dict[str, list[Any]]:
        self._refresh_indexes()
        active_runtimes = self.sorted_active_runtimes()
        archived_runtimes = self._archived_runtimes()
        return {
            "active": active_runtimes,
            "pinned": [runtime for runtime in active_runtimes if _runtime_pinned(runtime)],
            "main": [runtime for runtime in active_runtimes if _runtime_category(runtime) == "main"],
            "side": [runtime for runtime in active_runtimes if _runtime_category(runtime) == "side"],
            "urgent": [runtime for runtime in active_runtimes if _runtime_urgent(runtime)],
            "completed": [runtime for runtime in archived_runtimes if _runtime_display_status(runtime) == "completed"],
            "failed": [runtime for runtime in archived_runtimes if _runtime_display_status(runtime) == "failed"],
        }

    def quest_section_snapshots(self) -> dict[str, list[dict[str, Any]]]:
        sections = self.quest_sections()
        return {
            name: [
                runtime.journal_snapshot() if hasattr(runtime, "journal_snapshot") else _runtime_progress_summary(runtime)
                for runtime in runtimes
            ]
            for name, runtimes in sections.items()
        }

    def quest_section_counts(self) -> dict[str, int]:
        sections = self.quest_sections()
        return {name: len(runtimes) for name, runtimes in sections.items()}

    def find_runtimes(self, **filters: Any) -> list[Any]:
        known_runtimes = self._all_known_runtimes()
        if not filters:
            return builtins.sorted(known_runtimes, key=_runtime_sort_key)
        results = [
            runtime
            for runtime in known_runtimes
            if self._runtime_matches_filters(runtime, filters)
        ]
        return builtins.sorted(results, key=_runtime_sort_key)


def quest_journal_presentation_summary(journal: Any) -> dict[str, Any]:
    """Return a presentation-friendly snapshot for the quest journal."""
    def _ensure_dict(value: Any) -> dict[str, Any]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return dict(value)
        if _is_mapping(value):
            return dict(value)
        try:
            return dict(value)
        except Exception:
            return {}

    def _iter_runtimes(value: Any) -> list[Any]:
        if value is None:
            return []
        if isinstance(value, Mapping):
            return [value[key] for key in builtins.sorted(value)]
        if isinstance(value, (str, bytes)):
            return [value]
        if isinstance(value, Iterable):
            try:
                return list(value)
            except TypeError:
                return [value]
        return [value]

    def _entry_snapshot(runtime: Any) -> dict[str, Any]:
        summary: dict[str, Any] = {}
        for attr_name in ("journal_snapshot", "progress_summary", "summary", "snapshot"):
            attr = getattr(runtime, attr_name, None)
            if not callable(attr):
                continue
            try:
                value = attr()
            except TypeError:
                try:
                    value = attr(runtime)
                except TypeError:
                    continue
            summary = _ensure_dict(value)
            if summary:
                break
        if not summary:
            summary = _runtime_progress_summary(runtime)
        else:
            fallback = _runtime_progress_summary(runtime)
            for key, value in fallback.items():
                summary.setdefault(key, value)

        metadata = _as_dict(_first_value(runtime, "metadata"))
        archive_day = _first_value(runtime, "archive_day", "journal_archive_day", "archive_day_index")
        if archive_day is None:
            archive_day = metadata.get("archive_day")
        if archive_day is None:
            archive_day = metadata.get("journal_archive_day")
        if archive_day is None:
            archive_day = metadata.get("archive_day_index")
        if archive_day is not None:
            summary["archive_day"] = archive_day
        return summary

    if journal is None:
        return {}

    snapshot: dict[str, Any] = {}
    journal_snapshot_method = getattr(journal, "journal_snapshot", None)
    if callable(journal_snapshot_method):
        try:
            snapshot = _ensure_dict(journal_snapshot_method())
        except TypeError:
            snapshot = {}

    active_runtimes: list[Any] = []
    sorted_active = getattr(journal, "sorted_active_runtimes", None)
    if callable(sorted_active):
        try:
            active_runtimes = list(sorted_active())
        except TypeError:
            active_runtimes = _iter_runtimes(getattr(journal, "runtimes", None))
    else:
        active_runtimes = _iter_runtimes(getattr(journal, "runtimes", None))

    archived_map = getattr(journal, "archived_runtimes", None)
    archived_runtimes = _iter_runtimes(archived_map)

    active_entries = [_entry_snapshot(runtime) for runtime in active_runtimes]
    archived_entries = [_entry_snapshot(runtime) for runtime in archived_runtimes]

    completed_ids = {
        _normalize_identifier(quest_id)
        for quest_id in _iter_runtimes(getattr(journal, "completed_quest_ids", None))
    }
    completed_ids.discard(None)
    failed_ids = {
        _normalize_identifier(quest_id)
        for quest_id in _iter_runtimes(getattr(journal, "failed_quest_ids", None))
    }
    failed_ids.discard(None)

    completed_entries = [
        entry
        for entry in archived_entries
        if entry.get("quest_id") in completed_ids or entry.get("status") == "completed"
    ]
    failed_entries = [
        entry
        for entry in archived_entries
        if entry.get("quest_id") in failed_ids or entry.get("status") == "failed"
    ]

    section_entries: dict[str, list[dict[str, Any]]] = {}
    quest_sections_method = getattr(journal, "quest_sections", None)
    if callable(quest_sections_method):
        try:
            quest_sections = quest_sections_method()
        except TypeError:
            quest_sections = {}
        if isinstance(quest_sections, Mapping):
            for section_name, runtimes in quest_sections.items():
                section_entries[section_name] = [_entry_snapshot(runtime) for runtime in _iter_runtimes(runtimes)]
    if not section_entries:
        section_entries = {
            "active": active_entries,
            "pinned": [entry for entry in active_entries if entry.get("pinned")],
            "main": [entry for entry in active_entries if entry.get("category") == "main"],
            "side": [entry for entry in active_entries if entry.get("category") == "side"],
            "urgent": [entry for entry in active_entries if entry.get("urgent")],
            "completed": completed_entries,
            "failed": failed_entries,
        }

    active_count = len(active_entries)
    completed_count = len(completed_entries)
    failed_count = len(failed_entries)
    archive_count = len(archived_entries)
    archive_days = [
        entry.get("archive_day")
        for entry in archived_entries
        if entry.get("archive_day") is not None
    ]

    main_ids = getattr(journal, "main_quest_ids", None)
    side_ids = getattr(journal, "side_quest_ids", None)
    urgent_ids = getattr(journal, "urgent_quest_ids", None)
    pinned_ids = getattr(journal, "pinned_quest_ids", None)

    category_counts = {
        "main": len(main_ids or []),
        "side": len(side_ids or []),
        "urgent": len(urgent_ids or []),
        "pinned": len(pinned_ids or []),
        "completed": completed_count,
        "failed": failed_count,
        "active": active_count,
        "archive": archive_count,
    }
    misc_count = active_count - category_counts["main"] - category_counts["side"] - category_counts["urgent"]
    if misc_count < 0:
        misc_count = 0
    category_counts["misc"] = misc_count

    snapshot["active_count"] = active_count
    snapshot["completed_count"] = completed_count
    snapshot["failed_count"] = failed_count
    snapshot["archive_count"] = archive_count
    snapshot["active_entries"] = active_entries
    snapshot["completed_entries"] = completed_entries
    snapshot["failed_entries"] = failed_entries
    snapshot["archive_entries"] = archived_entries
    snapshot["archive_days"] = archive_days
    snapshot["category_counts"] = category_counts
    snapshot["quests"] = active_entries
    snapshot["active_quests"] = active_entries
    snapshot["archived_quests"] = archived_entries
    snapshot["active_quest_ids"] = [entry.get("quest_id") for entry in active_entries if entry.get("quest_id")]
    snapshot["archived_quest_ids"] = [entry.get("quest_id") for entry in archived_entries if entry.get("quest_id")]
    snapshot["completed_quest_ids"] = [entry.get("quest_id") for entry in completed_entries if entry.get("quest_id")]
    snapshot["failed_quest_ids"] = [entry.get("quest_id") for entry in failed_entries if entry.get("quest_id")]
    snapshot["active_summary"] = active_entries
    snapshot["archive_summary"] = archived_entries
    snapshot["sections"] = section_entries
    snapshot["section_counts"] = {name: len(entries) for name, entries in section_entries.items()}
    return snapshot
