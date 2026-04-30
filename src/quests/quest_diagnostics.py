from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.quests.quest_generation import DynamicQuestTemplate, QUEST_GENERATION_INPUTS, QUEST_GENERATION_TYPES
from .quest_domain import (
    QuestBattleObjective,
    QuestNPCState,
    QuestStage,
    QuestTemplate,
    QuestWorldContext,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def validate_dynamic_generation_templates(
    templates: Sequence[DynamicQuestTemplate],
    *,
    source: str = "",
) -> list["QuestDiagnostic"]:
    diagnostics: list[QuestDiagnostic] = []
    seen: set[str] = set()
    known_inputs = set(QUEST_GENERATION_INPUTS)
    known_types = set(QUEST_GENERATION_TYPES)
    for template in templates:
        try:
            template.validate()
        except Exception as exc:
            diagnostics.append(
                QuestDiagnostic(
                    severity="error",
                    code="generation_template_validation",
                    message=str(exc),
                    source=source,
                    quest_id=getattr(template, "template_id", ""),
                )
            )
            continue
        if template.template_id in seen:
            diagnostics.append(
                QuestDiagnostic(
                    severity="error",
                    code="duplicate_generation_template",
                    message=f"Duplicate dynamic template id {template.template_id!r}",
                    source=source,
                    quest_id=template.template_id,
                )
            )
        seen.add(template.template_id)
        if template.quest_type not in known_types:
            diagnostics.append(
                QuestDiagnostic(
                    severity="error",
                    code="unknown_generation_type",
                    message=f"Unknown generation type {template.quest_type!r}",
                    source=source,
                    quest_id=template.template_id,
                )
            )
        if template.base_weight <= 0:
            diagnostics.append(
                QuestDiagnostic(
                    severity="warning",
                    code="zero_generation_weight",
                    message="Template has no positive base weight",
                    source=source,
                    quest_id=template.template_id,
                )
            )
        if template.min_difficulty > template.max_difficulty:
            diagnostics.append(
                QuestDiagnostic(
                    severity="error",
                    code="impossible_generation_difficulty",
                    message="Minimum difficulty is greater than maximum difficulty",
                    source=source,
                    quest_id=template.template_id,
                )
            )
        required_positive_weight = template.base_weight
        for rule in template.rules:
            if "." not in rule.input_key and rule.input_key not in known_inputs and not rule.input_key.startswith("metadata."):
                diagnostics.append(
                    QuestDiagnostic(
                        severity="warning",
                        code="unknown_generation_input",
                        message=f"Rule {rule.rule_id!r} references unknown input {rule.input_key!r}",
                        source=source,
                        quest_id=template.template_id,
                    )
                )
            if rule.min_value is not None and rule.max_value is not None and rule.min_value > rule.max_value:
                diagnostics.append(
                    QuestDiagnostic(
                        severity="error",
                        code="impossible_generation_rule",
                        message=f"Rule {rule.rule_id!r} has min_value greater than max_value",
                        source=source,
                        quest_id=template.template_id,
                    )
                )
            if rule.required:
                required_positive_weight += rule.weight_delta
        if required_positive_weight <= 0:
            diagnostics.append(
                QuestDiagnostic(
                    severity="warning",
                    code="impossible_generation_weight",
                    message="Required rule path can never produce a positive offer weight",
                    source=source,
                    quest_id=template.template_id,
                )
            )
    return diagnostics

DEFAULT_DIALOGUE_FILES: tuple[str, ...] = (
    "src/dialogs/ZA01_startup_and_dispatch/anyone_lord_start_quest_memory.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_member_chat_quest_memory.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_start_02.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_quest_flavor_start.py",
    "src/dialogs/ZA01_startup_and_dispatch/anyone_quest_flavor_member_chat.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_battle_reason_quest_memory.py",
    "src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_quest_flavor_battle_reason.py",
)

DEFAULT_NARRATIVE_HELPER_FILES: tuple[str, ...] = (
    "src/scripts/ZG_quests/sod_quest_dialogue_read_memory.py",
    "src/scripts/ZG_quests/sod_quest_dialogue_describe_stage.py",
    "src/scripts/ZG_quests/sod_quest_dialogue_describe_reaction.py",
    "src/scripts/ZG_quests/sod_quest_dialogue_describe_battle_line.py",
    "src/scripts/ZG_quests/sod_quest_dialogue_describe_map_line.py",
    "src/scripts/ZG_quests/sod_quest_dialogue_record_event.py",
)

NARRATIVE_KEYS: tuple[str, ...] = (
    "stage_lines",
    "reaction_lines",
    "battle_lines",
    "map_lines",
    "success_lines",
    "failure_lines",
    "abandon_lines",
    "personality_overrides",
    "memory_tags",
)

REQUIRED_REACTION_OUTCOMES: tuple[str, ...] = (
    "accept",
    "complete",
    "fail",
    "abandon",
    "stage_change",
    "delayed_follow_up",
    "repeat",
)

REQUIRED_BATTLE_PHASES: tuple[str, ...] = (
    "pre",
    "mid",
    "post",
)

REQUIRED_MEMORY_REFERENCES: tuple[str, ...] = (
    "read_quest_memory",
    "summarize_quest_memory",
    "quest_memory_context",
    "script_sod_quest_dialogue_read_memory",
)

REQUIRED_BRANCH_REFERENCES: tuple[str, ...] = (
    "script_sod_quest_dialogue_describe_stage",
    "script_sod_quest_dialogue_describe_reaction",
    "script_sod_quest_dialogue_describe_battle_line",
    "script_sod_quest_dialogue_describe_map_line",
    "script_sod_quest_dialogue_record_event",
)

__all__ = [
    "DEFAULT_DIALOGUE_FILES",
    "DEFAULT_NARRATIVE_HELPER_FILES",
    "NARRATIVE_KEYS",
    "QuestDiagnostic",
    "QuestDiagnosticsReport",
    "build_quest_diagnostics_report",
    "diagnose_battle_objective",
    "diagnose_battle_objectives",
    "diagnose_dialogue_branch_coverage",
    "diagnose_quest_graph",
    "diagnose_quest_narrative",
    "quest_graph_dot",
    "quest_graph_mermaid",
    "quest_graph_report_json",
    "quest_graph_snapshot",
    "quest_graph_snapshots",
    "summarize_report",
    "summarize_quest_diagnostics_report",
    "diagnostics_report_to_dict",
    "validate_dynamic_generation_templates",
    "validate_quest_chain_graph",
    "validate_quest_template_graph",
]


@dataclass
class QuestDiagnostic:
    code: str
    message: str
    severity: str = "warning"
    subject: str = ""
    path: str = ""
    source: str = ""
    quest_id: str = ""
    stage_id: str = ""
    line: int = 0
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        details = dict(self.details)
        for key, value in (
            ("source", self.source),
            ("quest_id", self.quest_id),
            ("stage_id", self.stage_id),
            ("line", self.line),
        ):
            if value not in ("", 0, None) and key not in details:
                details[key] = value
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "subject": self.subject,
            "path": self.path or self.source,
            "details": details,
        }

    def to_tuple(self) -> tuple[str, str, str]:
        return self.code, self.severity, self.message

    def as_legacy_tuple(self) -> tuple[str, str, str]:
        return self.to_tuple()

    def __str__(self) -> str:
        location_bits = [bit for bit in (self.subject, self.path or self.source) if bit]
        location = f" [{', '.join(location_bits)}]" if location_bits else ""
        return f"{self.severity.upper()}: {self.code}: {self.message}{location}"

    def format(self) -> str:
        return str(self)


@dataclass
class QuestDiagnosticsReport:
    diagnostics: list[QuestDiagnostic] = field(default_factory=list)

    def add(self, diagnostic: QuestDiagnostic) -> QuestDiagnostic:
        self.diagnostics.append(diagnostic)
        return diagnostic

    def append(self, diagnostic: QuestDiagnostic) -> QuestDiagnostic:
        return self.add(diagnostic)

    def add_diagnostic(self, diagnostic: QuestDiagnostic) -> QuestDiagnostic:
        return self.add(diagnostic)

    def extend(self, diagnostics: Iterable[QuestDiagnostic]) -> None:
        self.diagnostics.extend(diagnostics)

    def merge(self, *reports: "QuestDiagnosticsReport") -> "QuestDiagnosticsReport":
        for report in reports:
            self.extend(report.diagnostics)
        return self

    def __iter__(self) -> Iterator[QuestDiagnostic]:
        return iter(self.diagnostics)

    def __len__(self) -> int:
        return len(self.diagnostics)

    def __bool__(self) -> bool:
        return bool(self.diagnostics)

    @property
    def issues(self) -> list[QuestDiagnostic]:
        return self.diagnostics

    @property
    def errors(self) -> list[QuestDiagnostic]:
        return [diagnostic for diagnostic in self.diagnostics if diagnostic.severity == "error"]

    @property
    def warnings(self) -> list[QuestDiagnostic]:
        return [diagnostic for diagnostic in self.diagnostics if diagnostic.severity == "warning"]

    @property
    def info(self) -> list[QuestDiagnostic]:
        return [diagnostic for diagnostic in self.diagnostics if diagnostic.severity == "info"]

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def info_count(self) -> int:
        return len(self.info)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def has_issues(self) -> bool:
        return bool(self.diagnostics)

    def by_code(self, code: str) -> list[QuestDiagnostic]:
        return [diagnostic for diagnostic in self.diagnostics if diagnostic.code == code]

    def to_dict(self) -> dict[str, Any]:
        return {
            "diagnostics": [diagnostic.as_dict() for diagnostic in self.diagnostics],
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "has_errors": self.has_errors,
            "has_warnings": self.has_warnings,
        }

    def as_dict(self) -> dict[str, Any]:
        return self.to_dict()

    @property
    def items(self) -> list[QuestDiagnostic]:
        return self.diagnostics

    def to_lines(self) -> list[str]:
        lines = [
            "Quest Diagnostics Report",
            "========================",
            "",
            f"Errors: {self.error_count}",
            f"Warnings: {self.warning_count}",
            f"Info: {self.info_count}",
            f"Total diagnostics: {len(self.diagnostics)}",
            "",
        ]
        if not self.diagnostics:
            lines.append("No quest diagnostics found.")
            return lines
        for diagnostic in self.diagnostics:
            lines.append(str(diagnostic))
        return lines


def _as_path(value: str | Path) -> Path:
    return value if isinstance(value, Path) else Path(value)


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _as_sequence(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, Mapping):
        return list(value.values())
    if isinstance(value, (str, bytes)):
        return [value]
    if isinstance(value, Sequence):
        return list(value)
    try:
        return list(value)
    except TypeError:
        return [value]


def _has_meaningful_text(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return any(_has_meaningful_text(item) for item in value.values())
    if isinstance(value, (list, tuple, set)):
        return any(_has_meaningful_text(item) for item in value)
    return bool(value)


def _get_attr(value: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if isinstance(value, Mapping) and name in value:
            return value[name]
        if hasattr(value, name):
            return getattr(value, name)
    return default


def _quest_identifier(quest: Any, fallback_index: int | None = None) -> str:
    identifier = _get_attr(quest, "quest_id", "id", "name", "slug", default="")
    if identifier:
        return str(identifier)
    if fallback_index is not None:
        return f"quest_{fallback_index}"
    return "quest"


def _quest_metadata(quest: Any) -> dict[str, Any]:
    metadata = _as_mapping(_get_attr(quest, "metadata", default={}))
    narrative = metadata.get("narrative")
    if isinstance(narrative, Mapping):
        return dict(narrative)
    if any(key in metadata for key in NARRATIVE_KEYS):
        return metadata
    return dict(narrative) if isinstance(narrative, Mapping) else metadata


def _quest_stages(quest: Any) -> list[Any]:
    stages = _get_attr(quest, "stages", "quest_stages", default=[])
    return _as_sequence(stages)


def _stage_metadata(stage: Any) -> dict[str, Any]:
    return _as_mapping(_get_attr(stage, "metadata", default={}))


def _chain_quests(chain: Any) -> list[Any]:
    quests = _get_attr(chain, "quests", "templates", "quest_templates", default=[])
    return _as_sequence(quests)


def _stage_identifier(stage: Any, fallback_index: int | None = None) -> str:
    identifier = _get_attr(stage, "stage_id", "id", "name", "slug", "key", default="")
    if identifier:
        return str(identifier)
    if fallback_index is not None:
        return f"stage_{fallback_index}"
    return "stage"


def _transition_map(value: Any) -> dict[str, str]:
    transitions = _get_attr(value, "transitions", "next", "edges", default={})
    if not isinstance(transitions, Mapping):
        return {}
    result: dict[str, str] = {}
    for label, target in transitions.items():
        if target in (None, ""):
            continue
        result[str(label)] = str(target)
    return result


def _has_outcome_items(stage: Any) -> bool:
    if _as_sequence(_get_attr(stage, "rewards", default=[])):
        return True
    if _as_sequence(_get_attr(stage, "failures", default=[])):
        return True
    metadata = _stage_metadata(stage)
    return any(bool(metadata.get(key)) for key in ("terminal", "terminal_stage", "outcome", "success", "failure"))


def _transition_label_group(label: str) -> str:
    normalized = str(label).strip().lower()
    if normalized in {"advance", "next", "continue"}:
        return "advance"
    if normalized in {"success", "succeed", "complete"}:
        return "success"
    if normalized in {"failure", "fail", "failed"}:
        return "failure"
    if normalized in {"done", "end", "finish"}:
        return "done"
    if normalized in {"accepted", "declined", "choice", "choose"}:
        return "choice"
    return normalized


def _lane_contract_data(value: Any) -> dict[str, Any]:
    metadata = _as_mapping(_get_attr(value, "metadata", default={}))
    contract = metadata.get("lane_contract")
    if hasattr(contract, "to_snapshot"):
        contract = contract.to_snapshot()
    if isinstance(contract, Mapping):
        data = dict(contract)
    else:
        data = {}
    for key in ("dialogue_lanes", "outcome_triggers", "journal_lanes", "required_lanes", "required_outcomes"):
        if key in metadata and key not in data:
            data[key] = metadata[key]
    return data


def _lane_map(data: Mapping[str, Any], key: str) -> dict[str, str]:
    value = data.get(key, {})
    if not isinstance(value, Mapping):
        return {}
    return {str(item_key): str(item_value) for item_key, item_value in value.items() if str(item_value).strip()}


def _lane_sequence(data: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = data.get(key, ())
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, Sequence):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return ()


def _emit_lane_contract_diagnostics(
    report: "QuestDiagnosticsReport",
    *,
    quest_id: str,
    subject_id: str,
    contract_owner: Any,
    transition_labels: set[str],
    has_reward_path: bool,
    has_failure_path: bool,
    has_battle_objective: bool,
) -> None:
    data = _lane_contract_data(contract_owner)
    if not data:
        return
    dialogue_lanes = _lane_map(data, "dialogue_lanes")
    outcome_triggers = _lane_map(data, "outcome_triggers")
    journal_lanes = _lane_map(data, "journal_lanes")
    required_lanes = set(_lane_sequence(data, "required_lanes"))
    required_outcomes = set(_lane_sequence(data, "required_outcomes"))

    needed_dialogue = set(required_lanes) | {label for label in transition_labels if label not in {"next", "advance", "done"}}
    for lane in sorted(needed_dialogue):
        if lane not in dialogue_lanes:
            _emit(
                report,
                code="missing_dialogue_lane",
                message=f"Quest {quest_id!r} subject {subject_id!r} requires dialogue lane {lane!r}.",
                severity="warning",
                subject=quest_id,
                lane=lane,
                lane_subject=subject_id,
            )

    needed_outcomes = set(required_outcomes)
    if has_reward_path:
        needed_outcomes.add("success")
    if has_failure_path:
        needed_outcomes.add("failure")
    if has_battle_objective:
        needed_outcomes.update(("success", "failure"))
    for outcome in sorted(needed_outcomes):
        if outcome not in outcome_triggers:
            _emit(
                report,
                code="missing_outcome_trigger",
                message=f"Quest {quest_id!r} subject {subject_id!r} requires outcome trigger {outcome!r}.",
                severity="warning",
                subject=quest_id,
                outcome=outcome,
                lane_subject=subject_id,
            )

    if transition_labels and not journal_lanes:
        _emit(
            report,
            code="missing_journal_lanes",
            message=f"Quest {quest_id!r} subject {subject_id!r} has transitions but no journal lanes.",
            severity="warning",
            subject=quest_id,
            lane_subject=subject_id,
        )


def _quest_battle_objectives(quest: Any) -> list[Any]:
    objectives = _get_attr(quest, "battle_objectives", "objectives", default=[])
    return _as_sequence(objectives)


def _quest_world_context(quest: Any) -> Any:
    return _get_attr(quest, "world_context", "quest_world_context", default=None)


def _world_context_metadata(world_context: Any) -> dict[str, Any]:
    if world_context is None:
        return {}
    metadata = _as_mapping(_get_attr(world_context, "metadata", default={}))
    if metadata:
        return metadata
    return _as_mapping(world_context)


def _candidate_stage_keys(stage: Any, index: int) -> list[str]:
    keys: list[str] = []
    for name in ("stage_id", "id", "name", "slug", "key"):
        value = _get_attr(stage, name, default=None)
        if value not in (None, ""):
            keys.append(str(value))
    keys.append(str(index))
    keys.append(f"stage_{index}")
    if keys:
        seen: set[str] = set()
        unique: list[str] = []
        for key in keys:
            if key not in seen:
                unique.append(key)
                seen.add(key)
        return unique
    return [str(index)]


def _candidate_battle_keys(objective: Any, index: int) -> list[str]:
    keys: list[str] = []
    for name in ("action_kind", "kind", "objective_kind", "type", "name", "slug", "key"):
        value = _get_attr(objective, name, default=None)
        if value not in (None, ""):
            keys.append(str(value))
    keys.append(str(index))
    keys.append(f"objective_{index}")
    seen: set[str] = set()
    unique: list[str] = []
    for key in keys:
        if key not in seen:
            unique.append(key)
            seen.add(key)
    return unique


def _lookup_text(container: Any, keys: Iterable[str]) -> Any:
    if isinstance(container, Mapping):
        for key in keys:
            if key in container and _has_meaningful_text(container[key]):
                return container[key]
            try:
                numeric_key = int(key)
            except (TypeError, ValueError):
                continue
            if numeric_key in container and _has_meaningful_text(container[numeric_key]):
                return container[numeric_key]
        return None
    if isinstance(container, Sequence) and not isinstance(container, (str, bytes)):
        values = list(container)
        for key in keys:
            try:
                index = int(key)
            except (TypeError, ValueError):
                continue
            if 0 <= index < len(values) and _has_meaningful_text(values[index]):
                return values[index]
        return None
    return container if _has_meaningful_text(container) else None


def _load_relative_text(root: Path, file_path: str | Path) -> tuple[Path, str]:
    path = _as_path(file_path)
    if not path.is_absolute():
        path = root / path
    return path, _safe_read_text(path)


def _collect_texts(root: Path, file_paths: Iterable[str | Path]) -> list[tuple[Path, str]]:
    collected: list[tuple[Path, str]] = []
    for file_path in file_paths:
        path = _as_path(file_path)
        if not path.is_absolute():
            path = root / path
        collected.append((path, _safe_read_text(path)))
    return collected


def _emit(report: QuestDiagnosticsReport, *, code: str, message: str, severity: str, subject: str = "", path: str = "", **details: Any) -> None:
    report.add(
        QuestDiagnostic(
            code=code,
            message=message,
            severity=severity,
            subject=subject,
            path=path,
            details=dict(details),
        )
    )


def _iter_loaded_quests(quests: Iterable[Any] | None = None) -> list[Any]:
    if quests is not None:
        if isinstance(quests, Mapping):
            return list(quests.values())
        if isinstance(quests, (str, Path)):
            return [quests]
        if hasattr(quests, "metadata") or hasattr(quests, "stages") or hasattr(quests, "battle_objectives"):
            return [quests]
        try:
            return list(quests)
        except TypeError:
            return [quests]

    try:
        from . import quest_domain as domain
    except Exception:
        return []

    for loader_name in (
        "iter_quest_templates",
        "iter_quests",
        "get_quest_templates",
        "get_all_quests",
        "load_quest_templates",
        "load_quests",
    ):
        loader = getattr(domain, loader_name, None)
        if callable(loader):
            try:
                loaded = loader()
            except TypeError:
                try:
                    loaded = loader(PROJECT_ROOT)
                except TypeError:
                    continue
            return list(loaded)

    for collection_name in (
        "QUEST_TEMPLATES",
        "QUESTS",
        "quest_templates",
        "quests",
        "QUEST_REGISTRY",
    ):
        collection = getattr(domain, collection_name, None)
        if collection is None:
            continue
        if isinstance(collection, Mapping):
            return list(collection.values())
        return list(collection)

    return []


def _quest_has_narrative_surface(quest: Any) -> bool:
    metadata = _quest_metadata(quest)
    if metadata and any(key in metadata for key in NARRATIVE_KEYS):
        return True
    if _quest_stages(quest):
        return True
    if _quest_battle_objectives(quest):
        return True
    world_context = _quest_world_context(quest)
    return world_context is not None


def _diagnose_quest_metadata(report: QuestDiagnosticsReport, quest: Any, index: int) -> None:
    quest_id = _quest_identifier(quest, index)
    metadata = _quest_metadata(quest)
    stages = _quest_stages(quest)
    objectives = _quest_battle_objectives(quest)
    world_context = _quest_world_context(quest)
    world_metadata = _world_context_metadata(world_context)
    narrative = metadata

    if not narrative:
        if _quest_has_narrative_surface(quest):
            _emit(
                report,
                code="missing_narrative_metadata",
                message="Quest is missing narrative metadata.",
                severity="error",
                subject=quest_id,
                missing_keys=list(NARRATIVE_KEYS),
            )
        return

    missing_keys = [key for key in NARRATIVE_KEYS if key not in narrative]
    if missing_keys:
        _emit(
            report,
            code="missing_narrative_metadata",
            message="Quest narrative metadata is incomplete.",
            severity="error",
            subject=quest_id,
            missing_keys=missing_keys,
        )

    stage_lines = narrative.get("stage_lines")
    if stages:
        for stage_index, stage in enumerate(stages):
            stage_keys = _candidate_stage_keys(stage, stage_index)
            line = _lookup_text(stage_lines, stage_keys)
            if not _has_meaningful_text(line):
                _emit(
                    report,
                    code="missing_stage_dialogue",
                    message="Quest stage dialogue is missing.",
                    severity="error",
                    subject=quest_id,
                    stage=str(_get_attr(stage, "stage_id", "id", "name", "slug", default=stage_index)),
                    missing_keys=stage_keys,
                )

    reaction_lines = narrative.get("reaction_lines")
    missing_reactions = [outcome for outcome in REQUIRED_REACTION_OUTCOMES if not _has_meaningful_text(_lookup_text(reaction_lines, (outcome,)))]
    if missing_reactions:
        _emit(
            report,
            code="missing_reaction_text",
            message="Quest reaction text is incomplete.",
            severity="error",
            subject=quest_id,
            missing_outcomes=missing_reactions,
        )

    battle_lines = narrative.get("battle_lines")
    if objectives:
        for objective_index, objective in enumerate(objectives):
            keys = _candidate_battle_keys(objective, objective_index)
            battle_entry = _lookup_text(battle_lines, keys)
            if isinstance(battle_entry, Mapping):
                missing_phases = [phase for phase in REQUIRED_BATTLE_PHASES if not _has_meaningful_text(_lookup_text(battle_entry, (phase,)))]
                if missing_phases:
                    _emit(
                        report,
                        code="missing_battle_line",
                        message="Quest battle-line text is missing one or more battle phases.",
                        severity="error",
                        subject=quest_id,
                        objective_kind=str(_get_attr(objective, "action_kind", "kind", "objective_kind", "type", default=f"objective_{objective_index}")),
                        missing_keys=keys,
                        missing_phases=missing_phases,
                    )
            elif not _has_meaningful_text(battle_entry):
                _emit(
                    report,
                    code="missing_battle_line",
                    message="Quest battle-line text is missing.",
                    severity="error",
                    subject=quest_id,
                    objective_kind=str(_get_attr(objective, "action_kind", "kind", "objective_kind", "type", default=f"objective_{objective_index}")),
                    missing_keys=keys,
                )

    map_lines = narrative.get("map_lines")
    location_bound = any(
        _get_attr(world_context, name, default=None) not in (None, "")
        for name in ("location_id", "location", "scene_id", "map_id", "town_id", "castle_id", "village_id")
    ) or any(
        _get_attr(world_metadata, name, default=None) not in (None, "")
        for name in ("location_id", "location", "scene_id", "map_id", "town_id", "castle_id", "village_id")
    )
    chain_bound = any(
        _get_attr(world_context, name, default=None) not in (None, "")
        for name in ("chain_id", "chain", "quest_chain", "availability", "state")
    ) or any(
        _get_attr(world_metadata, name, default=None) not in (None, "")
        for name in ("chain_id", "chain", "quest_chain", "availability", "state")
    )

    if location_bound or chain_bound:
        map_keys = [
            str(key)
            for key in (
                _get_attr(world_context, "location_id", "location", "scene_id", "map_id", default=""),
                _get_attr(world_context, "chain_id", "chain", "quest_chain", default=""),
                "location",
                "chain",
                "abandon",
                "availability",
            )
            if key not in (None, "")
        ]
        if not _has_meaningful_text(_lookup_text(map_lines, map_keys)):
            _emit(
                report,
                code="missing_map_line",
                message="Quest map/location text is missing.",
                severity="error",
                subject=quest_id,
                missing_keys=map_keys,
            )


def _scan_branch_references(files: Iterable[str | Path], required_symbols: Iterable[str]) -> dict[str, list[Path]]:
    references: dict[str, list[Path]] = {symbol: [] for symbol in required_symbols}
    for file_path in files:
        path = _as_path(file_path)
        text = _safe_read_text(path)
        for symbol in required_symbols:
            if symbol in text:
                references[symbol].append(path)
    return references


def diagnose_dialogue_branch_coverage(
    dialogue_files: Iterable[str | Path] | None = None,
    helper_files: Iterable[str | Path] | None = None,
    *,
    root: str | Path | None = None,
    project_root: str | Path | None = None,
) -> QuestDiagnosticsReport:
    root_value = root if root is not None else project_root
    project_root = root_value if isinstance(root_value, Path) else Path(root_value) if root_value is not None else PROJECT_ROOT
    if not project_root.is_absolute():
        project_root = PROJECT_ROOT / project_root
    report = QuestDiagnosticsReport()

    dialogue_paths = list(dialogue_files or DEFAULT_DIALOGUE_FILES)
    helper_paths = list(helper_files or DEFAULT_NARRATIVE_HELPER_FILES)

    dialogue_texts = _collect_texts(project_root, dialogue_paths)
    helper_texts = _collect_texts(project_root, helper_paths)

    for symbol in REQUIRED_BRANCH_REFERENCES:
        if not any(symbol in text for _, text in dialogue_texts):
            _emit(
                report,
                code="missing_dialogue_branch",
                message="Live dialogue files do not reference the required quest narrative branch.",
                severity="error",
                subject=symbol,
                missing_files=[path.as_posix() for path, _ in dialogue_texts],
            )

    memory_hits = [path for path, text in dialogue_texts if any(symbol in text for symbol in REQUIRED_MEMORY_REFERENCES)]
    helper_memory_hits = [path for path, text in helper_texts if any(symbol in text for symbol in REQUIRED_MEMORY_REFERENCES)]

    if not memory_hits or not helper_memory_hits:
        _emit(
            report,
            code="unread_quest_memory",
            message="Quest memory is not being read by both the live dialog layer and the helper scripts.",
            severity="warning",
            subject="quest_memory",
            dialogue_files=[path.as_posix() for path in memory_hits],
            helper_files=[path.as_posix() for path in helper_memory_hits],
        )

    for path, text in helper_texts:
        if path.name == "sod_quest_dialogue_read_memory.py":
            if not any(symbol in text for symbol in REQUIRED_MEMORY_REFERENCES):
                _emit(
                    report,
                    code="unread_quest_memory",
                    message="Quest memory helper file does not reference the memory reader/context API.",
                    severity="warning",
                    subject=path.name,
                    path=path.as_posix(),
                )
        elif path.name in {
            "sod_quest_dialogue_describe_stage.py",
            "sod_quest_dialogue_describe_reaction.py",
            "sod_quest_dialogue_describe_battle_line.py",
            "sod_quest_dialogue_describe_map_line.py",
        }:
            if not any(symbol in text for symbol in REQUIRED_BRANCH_REFERENCES):
                _emit(
                    report,
                    code="missing_dialogue_branch",
                    message="Quest narrative helper file does not reference the canonical branch resolver API.",
                    severity="error",
                    subject=path.name,
                    path=path.as_posix(),
                )

    return report


def diagnose_quest_narrative(
    quests: Iterable[Any] | None = None,
    *,
    root: str | Path | None = None,
    project_root: str | Path | None = None,
    dialogue_files: Iterable[str | Path] | None = None,
    helper_files: Iterable[str | Path] | None = None,
) -> QuestDiagnosticsReport:
    report = QuestDiagnosticsReport()

    loaded_quests = _iter_loaded_quests(quests)
    for index, quest in enumerate(loaded_quests):
        _diagnose_quest_metadata(report, quest, index)

    if dialogue_files is not None or helper_files is not None:
        report.merge(
            diagnose_dialogue_branch_coverage(
                dialogue_files=dialogue_files,
                helper_files=helper_files,
                root=root,
                project_root=project_root,
            )
        )

    return report


def diagnose_quest_graph(
    quests: Iterable[Any] | None = None,
    *,
    root: str | Path | None = None,
    project_root: str | Path | None = None,
) -> QuestDiagnosticsReport:
    report = QuestDiagnosticsReport()
    for index, quest in enumerate(_iter_loaded_quests(quests)):
        quest_id = _quest_identifier(quest, index)
        if not quest_id.strip():
            _emit(
                report,
                code="missing_quest_identifier",
                message="Quest is missing a stable identifier.",
                severity="error",
                subject=f"quest_{index}",
            )

        stages = _quest_stages(quest)
        if not stages:
            _emit(
                report,
                code="quest_without_stages",
                message=f"Quest {quest_id!r} has no authored stages.",
                severity="warning",
                subject=quest_id,
            )
            continue

        stage_ids: list[str] = []
        seen_stage_ids: set[str] = set()
        duplicate_stage_ids: set[str] = set()
        for stage_index, stage in enumerate(stages, start=1):
            stage_id = _stage_identifier(stage, stage_index)
            stage_ids.append(stage_id)
            if stage_id in seen_stage_ids:
                duplicate_stage_ids.add(stage_id)
            seen_stage_ids.add(stage_id)

        for stage_id in sorted(duplicate_stage_ids):
            _emit(
                report,
                code="duplicate_stage_id",
                message=f"Quest {quest_id!r} defines stage {stage_id!r} more than once.",
                severity="error",
                subject=quest_id,
                stage_id=stage_id,
            )

        known_stage_ids = set(stage_ids)
        edges: dict[str, set[str]] = {stage_id: set() for stage_id in stage_ids}
        incoming: dict[str, set[str]] = {stage_id: set() for stage_id in stage_ids}
        label_groups: set[str] = set()
        for stage_index, stage in enumerate(stages, start=1):
            stage_id = _stage_identifier(stage, stage_index)
            for transition_name, target_stage_id in _transition_map(stage).items():
                label_groups.add(_transition_label_group(transition_name))
                if target_stage_id not in known_stage_ids:
                    _emit(
                        report,
                        code="unknown_stage_transition",
                        message=(
                            f"Quest {quest_id!r} stage {stage_id!r} transition "
                            f"{transition_name!r} targets unknown stage {target_stage_id!r}."
                        ),
                        severity="error",
                        subject=quest_id,
                        stage_id=stage_id,
                        transition=transition_name,
                        target_stage_id=target_stage_id,
                    )
                    continue
                edges.setdefault(stage_id, set()).add(target_stage_id)
                incoming.setdefault(target_stage_id, set()).add(stage_id)

        meaningful_label_groups = {group for group in label_groups if group not in {"repeat"}}
        if len(meaningful_label_groups) > 1:
            _emit(
                report,
                code="inconsistent_transition_labels",
                message=f"Quest {quest_id!r} mixes transition label families: {', '.join(sorted(meaningful_label_groups))}.",
                severity="warning",
                subject=quest_id,
                transition_groups=sorted(meaningful_label_groups),
            )

        for stage_index, stage in enumerate(stages, start=1):
            stage_id = _stage_identifier(stage, stage_index)
            metadata = _stage_metadata(stage)
            stage_transition_labels = set(_transition_map(stage))
            if stage_index > 1 and not incoming.get(stage_id) and not metadata.get("entry"):
                _emit(
                    report,
                    code="stage_without_incoming_transition",
                    message=f"Quest {quest_id!r} stage {stage_id!r} has no incoming transition.",
                    severity="warning",
                    subject=quest_id,
                    stage_id=stage_id,
                )
            if not edges.get(stage_id) and not _has_outcome_items(stage):
                _emit(
                    report,
                    code="terminal_stage_without_outcome",
                    message=f"Quest {quest_id!r} terminal stage {stage_id!r} has no rewards, failures, or terminal metadata.",
                    severity="warning",
                    subject=quest_id,
                    stage_id=stage_id,
                )
            _emit_lane_contract_diagnostics(
                report,
                quest_id=quest_id,
                subject_id=stage_id,
                contract_owner=stage,
                transition_labels=stage_transition_labels,
                has_reward_path=bool(_as_sequence(_get_attr(stage, "rewards", default=[]))),
                has_failure_path=bool(_as_sequence(_get_attr(stage, "failures", default=[]))),
                has_battle_objective=_get_attr(stage, "battle_objective", default=None) is not None,
            )

        reachable: set[str] = set()
        pending: list[str] = [stage_ids[0]]
        while pending:
            current = pending.pop()
            if current in reachable:
                continue
            reachable.add(current)
            pending.extend(sorted(edges.get(current, ()), reverse=True))

        for stage_id in stage_ids:
            if stage_id not in reachable:
                _emit(
                    report,
                    code="unreachable_stage",
                    message=f"Quest {quest_id!r} stage {stage_id!r} is not reachable from the first stage.",
                    severity="warning",
                    subject=quest_id,
                    stage_id=stage_id,
                )
        _emit_lane_contract_diagnostics(
            report,
            quest_id=quest_id,
            subject_id=quest_id,
            contract_owner=quest,
            transition_labels=set(_transition_map(quest)),
            has_reward_path=bool(_as_sequence(_get_attr(quest, "rewards", default=[]))),
            has_failure_path=bool(_as_sequence(_get_attr(quest, "failures", default=[]))),
            has_battle_objective=bool(_quest_battle_objectives(quest)),
        )
    return report


def validate_quest_template_graph(
    template: Any,
    *,
    source: str = "",
    line: int = 0,
) -> list[QuestDiagnostic]:
    report = diagnose_quest_graph(quests=[template], root=source or None)
    report.merge(diagnose_quest_narrative(quests=[template], root=source or None))
    return list(report.diagnostics)


def validate_quest_chain_graph(
    chain: Any,
    *,
    source: str = "",
    line: int = 0,
) -> list[QuestDiagnostic]:
    report = QuestDiagnosticsReport()
    chain_id = str(_get_attr(chain, "chain_id", "id", "name", "slug", default="chain"))
    chain_quests = _chain_quests(chain)
    if not chain_quests:
        _emit(
            report,
            code="chain_without_quests",
            message=f"Quest chain {chain_id!r} has no quests.",
            severity="error",
            subject=chain_id,
        )
        return list(report.diagnostics)

    quest_ids: list[str] = []
    seen_quest_ids: set[str] = set()
    duplicate_quest_ids: set[str] = set()
    for index, quest in enumerate(chain_quests, start=1):
        quest_id = _quest_identifier(quest, index)
        quest_ids.append(quest_id)
        if quest_id in seen_quest_ids:
            duplicate_quest_ids.add(quest_id)
        seen_quest_ids.add(quest_id)

    for quest_id in sorted(duplicate_quest_ids):
        _emit(
            report,
            code="duplicate_chain_quest_id",
            message=f"Quest chain {chain_id!r} defines quest {quest_id!r} more than once.",
            severity="error",
            subject=chain_id,
            quest_id=quest_id,
        )

    known_quest_ids = set(quest_ids)
    entry_quest_id = str(_get_attr(chain, "entry_quest_id", "entry", "start", default="") or quest_ids[0])
    if entry_quest_id not in known_quest_ids:
        _emit(
            report,
            code="unknown_chain_entry",
            message=f"Quest chain {chain_id!r} entry quest {entry_quest_id!r} is not defined.",
            severity="error",
            subject=chain_id,
            quest_id=entry_quest_id,
        )

    edges: dict[str, set[str]] = {quest_id: set() for quest_id in quest_ids}
    quests_end_sources: set[str] = set()
    for index, quest in enumerate(chain_quests, start=1):
        quest_id = _quest_identifier(quest, index)
        for transition_name, target_quest_id in _transition_map(quest).items():
            if target_quest_id == "quests_end":
                quests_end_sources.add(quest_id)
                continue
            if target_quest_id not in known_quest_ids:
                _emit(
                    report,
                    code="unknown_quest_transition",
                    message=(
                        f"Quest chain {chain_id!r} quest {quest_id!r} transition "
                        f"{transition_name!r} targets unknown quest {target_quest_id!r}."
                    ),
                    severity="error",
                    subject=chain_id,
                    quest_id=quest_id,
                    transition=transition_name,
                    target_quest_id=target_quest_id,
                )
                continue
            edges.setdefault(quest_id, set()).add(target_quest_id)

    branches = _get_attr(chain, "branches", default={})
    if isinstance(branches, Mapping):
        for branch_name, branch_quest_ids in branches.items():
            branch_sequence = [str(target_quest_id) for target_quest_id in _as_sequence(branch_quest_ids)]
            if branch_sequence and entry_quest_id in known_quest_ids and branch_sequence[0] != entry_quest_id:
                edges.setdefault(entry_quest_id, set()).add(branch_sequence[0])
            for source_quest_id, target_quest_id in zip(branch_sequence, branch_sequence[1:]):
                if source_quest_id in known_quest_ids and target_quest_id in known_quest_ids:
                    edges.setdefault(source_quest_id, set()).add(target_quest_id)
            for target_quest_id in branch_sequence:
                target_quest_id = str(target_quest_id)
                if target_quest_id not in known_quest_ids:
                    _emit(
                        report,
                        code="unknown_chain_branch_quest",
                        message=(
                            f"Quest chain {chain_id!r} branch {branch_name!r} references "
                            f"unknown quest {target_quest_id!r}."
                        ),
                        severity="error",
                        subject=chain_id,
                        branch=str(branch_name),
                        target_quest_id=target_quest_id,
                    )

    if entry_quest_id in known_quest_ids:
        reachable: set[str] = set()
        pending: list[str] = [entry_quest_id]
        while pending:
            current = pending.pop()
            if current in reachable:
                continue
            reachable.add(current)
            pending.extend(sorted(edges.get(current, ()), reverse=True))
        for quest_id in quest_ids:
            if quest_id not in reachable:
                _emit(
                    report,
                    code="unreachable_chain_quest",
                    message=f"Quest chain {chain_id!r} quest {quest_id!r} is not reachable from entry {entry_quest_id!r}.",
                    severity="warning",
                    subject=chain_id,
                    quest_id=quest_id,
                )
        for source_quest_id in sorted(quests_end_sources):
            source_index = quest_ids.index(source_quest_id)
            later_reachable = [quest_id for quest_id in quest_ids[source_index + 1 :] if quest_id in reachable]
            if later_reachable:
                _emit(
                    report,
                    code="early_quests_end_transition",
                    message=(
                        f"Quest chain {chain_id!r} quest {source_quest_id!r} can end the chain "
                        f"before later reachable quest(s): {', '.join(later_reachable)}."
                    ),
                    severity="warning",
                    subject=chain_id,
                    quest_id=source_quest_id,
                    bypassed_quest_ids=later_reachable,
                )

    report.merge(diagnose_quest_graph(quests=chain_quests, root=source or None))
    return list(report.diagnostics)


def diagnose_battle_objectives(
    quests: Iterable[Any] | None = None,
    *,
    root: str | Path | None = None,
    project_root: str | Path | None = None,
) -> QuestDiagnosticsReport:
    report = QuestDiagnosticsReport()
    for index, quest in enumerate(_iter_loaded_quests(quests)):
        quest_id = _quest_identifier(quest, index)
        objectives = _quest_battle_objectives(quest)
        for objective_index, objective in enumerate(objectives):
            action_kind = _get_attr(objective, "action_kind", "kind", "objective_kind", "type", default="")
            if not str(action_kind).strip():
                _emit(
                    report,
                    code="missing_battle_objective_kind",
                    message="Quest battle objective is missing an action kind.",
                    severity="error",
                    subject=quest_id,
                    objective_index=objective_index,
                )
    return report


def diagnose_battle_objective(
    objective: Any,
    *,
    quest_id: str = "",
    stage_id: str = "",
    source: str = "",
    line: int = 0,
    stage: Any = None,
) -> list[QuestDiagnostic]:
    if _get_attr(objective, "action_kind", "kind", "objective_kind", "type", default="") in (None, ""):
        wrapped_objective = _get_attr(objective, "battle_objective", default=None)
        if wrapped_objective is not None:
            if stage is None:
                stage = objective
            objective = wrapped_objective
    action_kind = str(_get_attr(objective, "action_kind", "kind", "objective_kind", "type", default="") or "").strip()
    resolved_quest_id = str(_get_attr(objective, "quest_id", default=quest_id) or quest_id)
    resolved_stage_id = str(_get_attr(objective, "stage_id", default=stage_id) or stage_id)
    resolved_source = str(_get_attr(objective, "source", default=source) or source)
    resolved_line = int(_get_attr(objective, "line", default=line) or line or 0)
    details = {
        "quest_id": resolved_quest_id,
        "stage_id": resolved_stage_id,
        "source": resolved_source,
        "line": resolved_line,
    }
    diagnostics: list[QuestDiagnostic] = []

    def add(code: str, message: str) -> None:
        diagnostics.append(
            QuestDiagnostic(
                code=code,
                message=message,
                severity="error",
                subject=resolved_stage_id or resolved_quest_id,
                path=resolved_source,
                source=resolved_source,
                quest_id=resolved_quest_id,
                stage_id=resolved_stage_id,
                line=resolved_line,
                details=dict(details),
            )
        )

    known_action_kinds = {
        "capture_target",
        "defeat_wave",
        "escort_party",
        "hold_position",
        "kill_target",
        "rescue_target",
        "survive_timer",
    }
    if not action_kind:
        add("missing_battle_objective_kind", "Battle objective is missing an action kind.")
        return diagnostics
    if action_kind not in known_action_kinds:
        add("invalid_battle_action_kind", f"Unknown battle objective action kind {action_kind!r}.")
        return diagnostics

    has_target = any(
        _get_attr(objective, name, default=None) not in (None, "")
        for name in (
            "target_troop_id",
            "target_party_id",
            "target_center_id",
            "target_troop",
            "target_party",
            "target_center",
            "target",
        )
    )
    if action_kind in {"capture_target", "escort_party", "hold_position", "kill_target", "rescue_target"} and not has_target:
        add("missing_battle_target", f"Battle objective {action_kind!r} requires a target.")

    timer_duration = _get_attr(objective, "timer_duration", "duration", "timer", default=None)
    if action_kind == "survive_timer" and (timer_duration is None or int(timer_duration) <= 0):
        add("impossible_battle_timer", "Survive-timer objective requires a positive timer duration.")

    if action_kind == "defeat_wave":
        progress = _get_attr(objective, "progress", "required_count", "required", default=None)
        wave_index = _get_attr(objective, "wave_index", "wave", default=None)
        if progress is None or wave_index is None:
            add("unsupported_battle_objective", "Defeat-wave objective requires progress and wave data.")

    stage_value = stage if stage is not None else objective
    battle_objective = _get_attr(stage_value, "battle_objective", default=None)
    stage_has_battle_objective = battle_objective is not None or bool(_get_attr(stage_value, "battle", default=False))
    stage_hooks = _as_sequence(_get_attr(stage_value, "battle_hooks", "battle_hook", "hook_path", default=[]))
    if stage_has_battle_objective and not any(str(hook).strip() for hook in stage_hooks):
        add("missing_battle_hook_path", "Stage battle objective requires a battle hook path.")

    return diagnostics


def _graph_node_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in str(value)).strip("_") or "node"


def _template_graph_snapshot(template: Any, fallback_index: int = 1) -> dict[str, Any]:
    quest_id = _quest_identifier(template, fallback_index)
    stages = _quest_stages(template)
    nodes = [
        {
            "id": _stage_identifier(stage, index),
            "label": str(_get_attr(stage, "title", default=_stage_identifier(stage, index))),
            "kind": "stage",
            "metadata": _stage_metadata(stage),
        }
        for index, stage in enumerate(stages, start=1)
    ]
    edges = []
    for index, stage in enumerate(stages, start=1):
        stage_id = _stage_identifier(stage, index)
        for label, target in sorted(_transition_map(stage).items()):
            edges.append({"from": stage_id, "to": target, "label": label, "kind": "stage_transition"})
    return {
        "graph_id": quest_id,
        "kind": "template",
        "entry": nodes[0]["id"] if nodes else "",
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(edges, key=lambda item: (item["from"], item["to"], item["label"], item["kind"])),
        "metadata": _as_mapping(_get_attr(template, "metadata", default={})),
    }


def quest_graph_snapshot(chain_or_template: Any) -> dict[str, Any]:
    chain_quests = _chain_quests(chain_or_template)
    if chain_quests:
        chain_id = str(_get_attr(chain_or_template, "chain_id", "id", "name", "slug", default="chain"))
        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, str]] = []
        for index, quest in enumerate(chain_quests, start=1):
            quest_id = _quest_identifier(quest, index)
            nodes.append(
                {
                    "id": quest_id,
                    "label": str(_get_attr(quest, "name", "title", default=quest_id)),
                    "kind": "quest",
                    "stage_count": len(_quest_stages(quest)),
                    "metadata": _as_mapping(_get_attr(quest, "metadata", default={})),
                }
            )
            for label, target in sorted(_transition_map(quest).items()):
                edges.append({"from": quest_id, "to": target, "label": label, "kind": "quest_transition"})
        branches = _get_attr(chain_or_template, "branches", default={})
        if isinstance(branches, Mapping):
            for branch_name, branch_quests in sorted(branches.items()):
                sequence = [str(item) for item in _as_sequence(branch_quests)]
                for source, target in zip(sequence, sequence[1:]):
                    edges.append({"from": source, "to": target, "label": str(branch_name), "kind": "branch"})
        return {
            "graph_id": chain_id,
            "kind": "chain",
            "entry": str(_get_attr(chain_or_template, "entry_quest_id", default="")),
            "nodes": sorted(nodes, key=lambda item: item["id"]),
            "edges": sorted(edges, key=lambda item: (item["from"], item["to"], item["label"], item["kind"])),
            "templates": [_template_graph_snapshot(quest, index) for index, quest in enumerate(chain_quests, start=1)],
            "metadata": _as_mapping(_get_attr(chain_or_template, "metadata", default={})),
        }

    return _template_graph_snapshot(chain_or_template, 1)


def quest_graph_snapshots(items: Iterable[Any]) -> list[dict[str, Any]]:
    return [quest_graph_snapshot(item) for item in items]


def quest_graph_report_json(items: Iterable[Any], diagnostics: Iterable[Any] | None = None) -> dict[str, Any]:
    diagnostic_items = []
    for diagnostic in diagnostics or ():
        if hasattr(diagnostic, "as_dict"):
            diagnostic_items.append(diagnostic.as_dict())
        elif isinstance(diagnostic, Mapping):
            diagnostic_items.append(dict(diagnostic))
    graphs = quest_graph_snapshots(items)
    node_count = sum(len(graph.get("nodes", ())) for graph in graphs)
    edge_count = sum(len(graph.get("edges", ())) for graph in graphs)
    template_count = sum(len(graph.get("templates", ())) for graph in graphs)
    stage_count = sum(len(template.get("nodes", ())) for graph in graphs for template in graph.get("templates", ()))
    return {
        "summary": {
            "graph_count": len(graphs),
            "node_count": node_count,
            "edge_count": edge_count,
            "template_count": template_count,
            "stage_count": stage_count,
            "diagnostic_count": len(diagnostic_items),
        },
        "graphs": graphs,
        "diagnostics": sorted(diagnostic_items, key=lambda item: (str(item.get("severity", "")), str(item.get("code", "")), str(item.get("subject", "")))),
    }


def quest_graph_mermaid(chain_or_template: Any) -> str:
    snapshot = quest_graph_snapshot(chain_or_template)
    lines = ["flowchart TD"]
    for node in snapshot["nodes"]:
        lines.append(f"  {_graph_node_id(node['id'])}[\"{node['label']}\"]")
    for edge in snapshot["edges"]:
        lines.append(f"  {_graph_node_id(edge['from'])} -->|{edge['label']}| {_graph_node_id(edge['to'])}")
    for template in snapshot.get("templates", ()):
        lines.append(f"  subgraph {_graph_node_id(template['graph_id'])}_stages[\"{template['graph_id']} stages\"]")
        for node in template["nodes"]:
            scoped_id = _graph_node_id(f"{template['graph_id']}_{node['id']}")
            lines.append(f"    {scoped_id}[\"{node['label']}\"]")
        for edge in template["edges"]:
            source_id = _graph_node_id(f"{template['graph_id']}_{edge['from']}")
            target_id = _graph_node_id(f"{template['graph_id']}_{edge['to']}")
            lines.append(f"    {source_id} -->|{edge['label']}| {target_id}")
        lines.append("  end")
    return "\n".join(lines) + "\n"


def quest_graph_dot(chain_or_template: Any) -> str:
    snapshot = quest_graph_snapshot(chain_or_template)
    lines = [f"digraph {_graph_node_id(snapshot['graph_id'])} {{"]
    for node in snapshot["nodes"]:
        lines.append(f"  {_graph_node_id(node['id'])} [label=\"{node['label']}\"];")
    for edge in snapshot["edges"]:
        lines.append(f"  {_graph_node_id(edge['from'])} -> {_graph_node_id(edge['to'])} [label=\"{edge['label']}\"];")
    for template in snapshot.get("templates", ()):
        lines.append(f"  subgraph cluster_{_graph_node_id(template['graph_id'])} {{")
        lines.append(f"    label=\"{template['graph_id']} stages\";")
        for node in template["nodes"]:
            scoped_id = _graph_node_id(f"{template['graph_id']}_{node['id']}")
            lines.append(f"    {scoped_id} [label=\"{node['label']}\"];")
        for edge in template["edges"]:
            source_id = _graph_node_id(f"{template['graph_id']}_{edge['from']}")
            target_id = _graph_node_id(f"{template['graph_id']}_{edge['to']}")
            lines.append(f"    {source_id} -> {target_id} [label=\"{edge['label']}\"];")
        lines.append("  }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def build_quest_diagnostics_report(
    quests: Iterable[Any] | None = None,
    *,
    root: str | Path | None = None,
    project_root: str | Path | None = None,
    dialogue_files: Iterable[str | Path] | None = None,
    helper_files: Iterable[str | Path] | None = None,
) -> QuestDiagnosticsReport:
    report = QuestDiagnosticsReport()
    report.merge(diagnose_quest_graph(quests=quests, root=root, project_root=project_root))
    report.merge(diagnose_battle_objectives(quests=quests, root=root, project_root=project_root))
    report.merge(diagnose_dialogue_branch_coverage(dialogue_files=dialogue_files, helper_files=helper_files, root=root, project_root=project_root))
    report.merge(
        diagnose_quest_narrative(
            quests=quests,
            root=root,
            project_root=project_root,
        )
    )
    return report


def summarize_report(report: QuestDiagnosticsReport) -> dict[str, Any]:
    return report.to_dict()


def summarize_quest_diagnostics_report(report: QuestDiagnosticsReport) -> dict[str, Any]:
    return summarize_report(report)


def diagnostics_report_to_dict(report: QuestDiagnosticsReport) -> dict[str, Any]:
    return summarize_report(report)


def _legacy_tuple_diagnostic(diagnostic: QuestDiagnostic) -> tuple[str, str, str]:
    return diagnostic.code, diagnostic.severity, diagnostic.message


def _default_world_context(value: Any) -> QuestWorldContext | None:
    if isinstance(value, QuestWorldContext):
        return value
    return None


def _default_npc_state(value: Any) -> QuestNPCState | None:
    if isinstance(value, QuestNPCState):
        return value
    return None


def _default_stage(value: Any) -> QuestStage | None:
    if isinstance(value, QuestStage):
        return value
    return None


def _default_battle_objective(value: Any) -> QuestBattleObjective | None:
    if isinstance(value, QuestBattleObjective):
        return value
    return None
