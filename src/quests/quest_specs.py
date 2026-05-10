# -*- coding: utf-8 -*-
"""
Declarative quest specification helpers for the modular quest framework.

These specs sit above `src.quests.quest_domain` and make it easier to author
long quest chains from compact data. They are intentionally lightweight so a
single source file can drive both one-off story quests and larger quest arcs
without repeating boilerplate.

The spec layer intentionally mirrors the domain layer while adding:
- mapping-friendly helper constructors for content authoring
- chain-level defaults for quest and stage metadata
- a chain spec object that can expand nested quest specs into legacy tuples
- corrected stage action coercion so quest actions stay distinct from triggers
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from src.quests.quest_domain import (
    QuestAction,
    QuestChain,
    QuestCondition,
    QuestFailure,
    QuestNPCState,
    QuestReward,
    QuestStage,
    QuestTemplate,
    QuestTrigger,
    QuestWorldContext,
    quest_action,
    quest_chain,
    quest_condition,
    quest_failure,
    quest_reward,
    quest_single_stage_quest,
    quest_stage,
    quest_template,
    quest_trigger,
    validate_quest_id,
)

__all__ = [
    "QuestChainSpec",
    "QuestStageSpec",
    "QuestTemplateSpec",
    "quest_chain_from_specs",
    "quest_chain_spec",
    "quest_chain_spec_from_mapping",
    "quest_stage_spec",
    "quest_stage_spec_from_mapping",
    "quest_template_spec",
    "quest_template_spec_from_mapping",
]


def _merge_metadata(
    defaults: Mapping[str, Any] | None,
    overrides: Mapping[str, Any] | None,
) -> dict[str, Any]:
    merged = dict(defaults or {})
    merged.update(dict(overrides or {}))
    return merged


def _apply_interactive_metadata_defaults(metadata: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(metadata or {})
    if result.get("companion") and not result.get("availability_mode"):
        phase = str(result.get("phase", "") or "").strip().lower()
        if phase in {"opening", "aftermath"}:
            result["availability_mode"] = "dialog"
        elif phase in {"scene", "mission", "duel", "challenge"}:
            result["availability_mode"] = "scene"
        elif phase in {"battle", "combat"}:
            result["availability_mode"] = "battle"
        else:
            result["availability_mode"] = "travel"
    return result


def _coerce_spec_sequence(value: Any) -> tuple[Any, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(value)
    return (value,)


def _coerce_branch_map(branches: Mapping[str, Any] | None) -> dict[str, tuple[str, ...]]:
    if not branches:
        return {}
    result: dict[str, tuple[str, ...]] = {}
    for key, value in branches.items():
        if not isinstance(key, str):
            raise TypeError(f"chain branch keys must be strings, got {type(key)!r}")
        validate_quest_id(key)
        result[key] = tuple(str(item).strip() for item in _coerce_spec_sequence(value) if str(item).strip())
    return result


def _coerce_condition_item(
    value: QuestCondition | str,
    prefix: str,
    index: int,
) -> QuestCondition:
    if isinstance(value, QuestCondition):
        return value.validate()
    if isinstance(value, str):
        return quest_condition(
            f"{prefix}_condition_{index}",
            value,
        )
    raise TypeError(
        f"Expected QuestCondition or str for {prefix} condition, got {type(value)!r}"
    )


def _coerce_action_item(
    value: QuestAction | str,
    prefix: str,
    index: int,
) -> QuestAction:
    if isinstance(value, QuestAction):
        return value.validate()
    if isinstance(value, str):
        return quest_action(
            f"{prefix}_action_{index}",
            value,
        )
    raise TypeError(
        f"Expected QuestAction or str for {prefix} action, got {type(value)!r}"
    )


def _coerce_reward_item(
    value: QuestReward | str,
    prefix: str,
    index: int,
) -> QuestReward:
    if isinstance(value, QuestReward):
        return value.validate()
    if isinstance(value, str):
        return quest_reward(
            f"{prefix}_reward_{index}",
            value,
        )
    raise TypeError(
        f"Expected QuestReward or str for {prefix} reward, got {type(value)!r}"
    )


def _coerce_failure_item(
    value: QuestFailure | str,
    prefix: str,
    index: int,
) -> QuestFailure:
    if isinstance(value, QuestFailure):
        return value.validate()
    if isinstance(value, str):
        return quest_failure(
            f"{prefix}_failure_{index}",
            value,
        )
    raise TypeError(
        f"Expected QuestFailure or str for {prefix} failure, got {type(value)!r}"
    )


def _coerce_trigger_item(
    value: QuestTrigger | str,
    prefix: str,
    index: int,
) -> QuestTrigger:
    if isinstance(value, QuestTrigger):
        return value.validate()
    if isinstance(value, str):
        return quest_trigger(
            f"{prefix}_trigger_{index}",
            value,
        )
    raise TypeError(
        f"Expected QuestTrigger or str for {prefix} trigger, got {type(value)!r}"
    )


def _build_stage_from_spec(
    stage: QuestStageSpec | QuestStage | Mapping[str, Any] | str,
    *,
    quest_id: str,
    index: int,
    stage_metadata: Mapping[str, Any] | None = None,
) -> QuestStage:
    if isinstance(stage, QuestStageSpec):
        return stage.build(quest_id, index=index, metadata=stage_metadata)
    if isinstance(stage, QuestStage):
        return stage.validate()
    if isinstance(stage, Mapping):
        return quest_stage_spec_from_mapping(
            stage,
            default_key=f"stage_{index}",
        ).build(quest_id, index=index, metadata=stage_metadata)
    if isinstance(stage, str):
        return quest_stage_spec(
            f"stage_{index}",
            stage,
            stage,
            metadata=stage_metadata,
        ).build(quest_id, index=index, metadata=stage_metadata)
    raise TypeError(
        f"Expected QuestStage, QuestStageSpec, Mapping, or str for quest {quest_id!r}, got "
        f"{type(stage)!r}"
    )


def _build_template_from_spec(
    quest: QuestTemplate | QuestTemplateSpec | Mapping[str, Any] | str,
    *,
    chain_id: str,
    index: int,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
) -> QuestTemplate:
    if isinstance(quest, QuestTemplateSpec):
        return quest.build(metadata=quest_metadata, stage_metadata=stage_metadata)
    if isinstance(quest, QuestTemplate):
        return quest.validate()
    if isinstance(quest, Mapping):
        return quest_template_spec_from_mapping(
            quest,
            default_quest_id=f"{chain_id}_quest_{index}",
        ).build(metadata=quest_metadata, stage_metadata=stage_metadata)
    if isinstance(quest, str):
        return quest_template_spec(
            f"{chain_id}_quest_{index}",
            quest,
            None,
            quest,
        ).build(metadata=quest_metadata, stage_metadata=stage_metadata)
    raise TypeError(
        f"Expected QuestTemplate, QuestTemplateSpec, Mapping, or str for chain {chain_id!r}, got "
        f"{type(quest)!r}"
    )


def quest_stage_spec_from_mapping(
    spec: Mapping[str, Any],
    *,
    default_key: str = "stage",
) -> QuestStageSpec:
    if not isinstance(spec, Mapping):
        raise TypeError(f"spec must be a mapping, got {type(spec)!r}")

    key = (
        spec.get("key")
        or spec.get("stage_key")
        or spec.get("stage_id")
        or spec.get("id")
        or default_key
    )
    title = spec.get("title") or spec.get("name") or spec.get("label") or key
    objective = spec.get("objective") or spec.get("goal") or spec.get("summary") or title

    return quest_stage_spec(
        str(key),
        str(title),
        str(objective),
        description=str(spec.get("description", "")),
        conditions=_coerce_spec_sequence(spec.get("conditions")),
        actions=_coerce_spec_sequence(spec.get("actions")),
        battle_hooks=tuple(spec.get("battle_hooks", ()) or ()),
        triggers=_coerce_spec_sequence(spec.get("triggers")),
        rewards=_coerce_spec_sequence(spec.get("rewards")),
        failures=_coerce_spec_sequence(spec.get("failures")),
        transitions=dict(spec.get("transitions", {}) or {}),
        metadata=dict(spec.get("metadata", spec.get("stage_metadata", {})) or {}),
    )


def quest_template_spec_from_mapping(
    spec: Mapping[str, Any],
    *,
    default_quest_id: str = "quest",
) -> QuestTemplateSpec:
    if not isinstance(spec, Mapping):
        raise TypeError(f"spec must be a mapping, got {type(spec)!r}")

    quest_id = spec.get("quest_id") or spec.get("id") or default_quest_id
    name = spec.get("name") or spec.get("title") or quest_id
    description = spec.get("description") or spec.get("summary") or ""

    return quest_template_spec(
        str(quest_id),
        str(name),
        spec.get("flags", spec.get("quest_flags")),
        str(description),
        stages=_coerce_spec_sequence(spec.get("stages")),
        stage_title=str(spec.get("stage_title", "")),
        stage_objective=str(spec.get("stage_objective", "")),
        stage_id=spec.get("stage_id"),
        stage_description=str(spec.get("stage_description", "")),
        conditions=_coerce_spec_sequence(spec.get("conditions")),
        actions=_coerce_spec_sequence(spec.get("actions")),
        battle_hooks=tuple(spec.get("battle_hooks", ()) or ()),
        triggers=_coerce_spec_sequence(spec.get("triggers")),
        rewards=_coerce_spec_sequence(spec.get("rewards")),
        failures=_coerce_spec_sequence(spec.get("failures")),
        transitions=dict(spec.get("transitions", {}) or {}),
        npc_state=spec.get("npc_state"),
        world_context=spec.get("world_context"),
        metadata=dict(spec.get("metadata", spec.get("quest_metadata", {})) or {}),
        stage_metadata=dict(spec.get("stage_metadata", {}) or {}),
    )


def quest_chain_spec_from_mapping(
    spec: Mapping[str, Any],
    *,
    default_chain_id: str = "chain",
) -> QuestChainSpec:
    if not isinstance(spec, Mapping):
        raise TypeError(f"spec must be a mapping, got {type(spec)!r}")

    chain_id = spec.get("chain_id") or spec.get("id") or default_chain_id
    title = spec.get("title") or spec.get("name") or chain_id

    return quest_chain_spec(
        str(chain_id),
        str(title),
        quests=_coerce_spec_sequence(spec.get("quests")),
        entry_quest_id=str(
            spec.get("entry_quest_id")
            or spec.get("start_quest_id")
            or spec.get("entry")
            or ""
        ),
        branches=spec.get("branches") or spec.get("branch_map"),
        metadata=dict(spec.get("metadata", spec.get("chain_metadata", {})) or {}),
        quest_metadata=dict(spec.get("quest_metadata", {}) or {}),
        stage_metadata=dict(spec.get("stage_metadata", {}) or {}),
    )


@dataclass(frozen=True)
class QuestStageSpec:
    """
    Declarative description for a quest stage.

    The `key` field is used to generate a stable stage id relative to the
    parent quest id. This keeps long quest chains predictable while still
    allowing each stage to be declared compactly.
    """

    key: str
    title: str
    objective: str
    description: str = ""
    conditions: tuple[QuestCondition | str, ...] = ()
    actions: tuple[QuestAction | str, ...] = ()
    battle_hooks: tuple[str, ...] = ()
    triggers: tuple[QuestTrigger | str, ...] = ()
    rewards: tuple[QuestReward | str, ...] = ()
    failures: tuple[QuestFailure | str, ...] = ()
    transitions: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_conditions(self) -> tuple[QuestCondition, ...]:
        return tuple(
            _coerce_condition_item(condition, self.key, index)
            for index, condition in enumerate(self.conditions, start=1)
        )

    def normalized_actions(self) -> tuple[QuestAction, ...]:
        return tuple(
            _coerce_action_item(action, self.key, index)
            for index, action in enumerate(self.actions, start=1)
        )

    def normalized_triggers(self) -> tuple[QuestTrigger, ...]:
        return tuple(
            _coerce_trigger_item(trigger, self.key, index)
            for index, trigger in enumerate(self.triggers, start=1)
        )

    def normalized_rewards(self) -> tuple[QuestReward, ...]:
        return tuple(
            _coerce_reward_item(reward, self.key, index)
            for index, reward in enumerate(self.rewards, start=1)
        )

    def normalized_failures(self) -> tuple[QuestFailure, ...]:
        return tuple(
            _coerce_failure_item(failure, self.key, index)
            for index, failure in enumerate(self.failures, start=1)
        )

    def build(
        self,
        quest_id: str,
        *,
        index: int = 1,
        metadata: Mapping[str, Any] | None = None,
    ) -> QuestStage:
        validate_quest_id(quest_id)
        key = validate_quest_id(self.key)
        stage_id = f"{quest_id}_{key}" if key else f"{quest_id}_stage_{index}"
        merged_metadata = _apply_interactive_metadata_defaults(_merge_metadata(metadata, self.metadata))
        return quest_stage(
            stage_id,
            self.title,
            self.objective,
            description=self.description,
            conditions=self.normalized_conditions(),
            actions=self.normalized_actions(),
            battle_hooks=self.battle_hooks,
            triggers=self.normalized_triggers(),
            rewards=self.normalized_rewards(),
            failures=self.normalized_failures(),
            transitions=self.transitions,
            metadata=merged_metadata,
        )


@dataclass(frozen=True)
class QuestTemplateSpec:
    """
    Declarative quest template that can expand into either a single-stage quest
    or a fully authored multi-stage quest.

    If `stages` is supplied, the template is built from the provided stages.
    Otherwise, the helper falls back to the compact single-stage quest shape
    used by most Warband-era content.
    """

    quest_id: str
    name: str
    flags: Any
    description: str
    stages: tuple[QuestStage | QuestStageSpec, ...] = ()
    stage_title: str = ""
    stage_objective: str = ""
    stage_id: str | None = None
    stage_description: str = ""
    conditions: tuple[QuestCondition | str, ...] = ()
    actions: tuple[QuestAction | str, ...] = ()
    battle_hooks: tuple[str, ...] = ()
    triggers: tuple[QuestTrigger | str, ...] = ()
    rewards: tuple[QuestReward | str, ...] = ()
    failures: tuple[QuestFailure | str, ...] = ()
    transitions: dict[str, str] = field(default_factory=dict)
    npc_state: QuestNPCState | None = None
    world_context: QuestWorldContext | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    stage_metadata: dict[str, Any] = field(default_factory=dict)

    def build(
        self,
        *,
        metadata: Mapping[str, Any] | None = None,
        stage_metadata: Mapping[str, Any] | None = None,
    ) -> QuestTemplate:
        quest_id = validate_quest_id(self.quest_id)

        if self.stages and (
            self.stage_title
            or self.stage_objective
            or self.stage_id is not None
            or self.stage_description
            or self.conditions
            or self.actions
            or self.battle_hooks
            or self.triggers
            or self.rewards
            or self.failures
            or self.transitions
        ):
            raise ValueError(
                f"QuestTemplateSpec {self.quest_id!r} cannot mix explicit stages with "
                "single-stage helper fields."
            )

        merged_metadata = _merge_metadata(metadata, self.metadata)
        merged_stage_metadata = _merge_metadata(stage_metadata, self.stage_metadata)

        if self.stages:
            built_stages = [
                _build_stage_from_spec(
                    stage,
                    quest_id=quest_id,
                    index=index,
                    stage_metadata=merged_stage_metadata,
                )
                for index, stage in enumerate(self.stages, start=1)
            ]
            return quest_template(
                quest_id,
                self.name,
                self.flags,
                self.description,
                stages=tuple(built_stages),
                transitions=self.transitions,
                npc_state=self.npc_state,
                world_context=self.world_context,
                metadata=merged_metadata,
            )

        has_single_stage_payload = any(
            (
                self.stage_title,
                self.stage_objective,
                self.stage_id is not None,
                self.stage_description,
                self.conditions,
                self.actions,
                self.battle_hooks,
                self.triggers,
                self.rewards,
                self.failures,
                self.transitions,
            )
        )

        if has_single_stage_payload:
            if not self.stage_title or not self.stage_objective:
                raise ValueError(
                    f"QuestTemplateSpec {self.quest_id!r} requires both stage_title and "
                    "stage_objective when using single-stage helper fields."
                )
            return quest_single_stage_quest(
                quest_id,
                self.name,
                self.flags,
                self.description,
                stage_title=self.stage_title,
                stage_objective=self.stage_objective,
                stage_id=self.stage_id,
                stage_description=self.stage_description,
                conditions=self.conditions,
                actions=self.actions,
                battle_hooks=self.battle_hooks,
                triggers=self.triggers,
                rewards=self.rewards,
                failures=self.failures,
                transitions=self.transitions,
                quest_metadata=merged_metadata,
                stage_metadata=merged_stage_metadata,
                npc_state=self.npc_state,
                world_context=self.world_context,
            )

        return quest_template(
            quest_id,
            self.name,
            self.flags,
            self.description,
            transitions=self.transitions,
            npc_state=self.npc_state,
            world_context=self.world_context,
            metadata=merged_metadata,
        )


@dataclass(frozen=True)
class QuestChainSpec:
    """
    Declarative quest chain that can expand into the legacy chain tuple list.

    This keeps chain metadata, quest-level defaults, and stage-level defaults
    together so long, multi-quest arcs stay easy to author from a single source.
    """

    chain_id: str
    title: str
    quests: tuple[QuestTemplate | QuestTemplateSpec | Mapping[str, Any] | str, ...] = ()
    entry_quest_id: str = ""
    branches: dict[str, tuple[str, ...]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    quest_metadata: dict[str, Any] = field(default_factory=dict)
    stage_metadata: dict[str, Any] = field(default_factory=dict)

    def build(
        self,
        *,
        metadata: Mapping[str, Any] | None = None,
        quest_metadata: Mapping[str, Any] | None = None,
        stage_metadata: Mapping[str, Any] | None = None,
    ) -> QuestChain:
        chain_id = validate_quest_id(self.chain_id)
        merged_metadata = _merge_metadata(metadata, self.metadata)
        merged_quest_metadata = _merge_metadata(quest_metadata, self.quest_metadata)
        merged_stage_metadata = _merge_metadata(stage_metadata, self.stage_metadata)

        built_quests = [
            _build_template_from_spec(
                quest,
                chain_id=chain_id,
                index=index,
                quest_metadata=merged_quest_metadata,
                stage_metadata=merged_stage_metadata,
            )
            for index, quest in enumerate(self.quests, start=1)
        ]

        return quest_chain(
            chain_id,
            self.title,
            quests=tuple(built_quests),
            entry_quest_id=self.entry_quest_id,
            branches=self.branches,
            metadata=merged_metadata,
        )


def quest_stage_spec(
    key: str,
    title: str,
    objective: str,
    *,
    description: str = "",
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestStageSpec:
    return QuestStageSpec(
        key=validate_quest_id(key),
        title=title,
        objective=objective,
        description=description,
        conditions=tuple(conditions),
        actions=tuple(actions),
        battle_hooks=tuple(battle_hooks),
        triggers=tuple(triggers),
        rewards=tuple(rewards),
        failures=tuple(failures),
        transitions=dict(transitions or {}),
        metadata=dict(metadata or {}),
    )


def quest_template_spec(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    stages: Sequence[QuestStage | QuestStageSpec | Mapping[str, Any] | str] = (),
    stage_title: str = "",
    stage_objective: str = "",
    stage_id: str | None = None,
    stage_description: str = "",
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
    metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
) -> QuestTemplateSpec:
    return QuestTemplateSpec(
        quest_id=validate_quest_id(quest_id),
        name=name,
        flags=flags,
        description=description,
        stages=tuple(stages),
        stage_title=stage_title,
        stage_objective=stage_objective,
        stage_id=stage_id,
        stage_description=stage_description,
        conditions=tuple(conditions),
        actions=tuple(actions),
        battle_hooks=tuple(battle_hooks),
        triggers=tuple(triggers),
        rewards=tuple(rewards),
        failures=tuple(failures),
        transitions=dict(transitions or {}),
        npc_state=npc_state,
        world_context=world_context,
        metadata=dict(metadata or {}),
        stage_metadata=dict(stage_metadata or {}),
    )


def quest_chain_spec(
    chain_id: str,
    title: str,
    quests: Sequence[QuestTemplate | QuestTemplateSpec | Mapping[str, Any] | str] = (),
    *,
    entry_quest_id: str = "",
    branches: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
) -> QuestChainSpec:
    return QuestChainSpec(
        chain_id=validate_quest_id(chain_id),
        title=title,
        quests=tuple(quests),
        entry_quest_id=entry_quest_id,
        branches=_coerce_branch_map(branches),
        metadata=dict(metadata or {}),
        quest_metadata=dict(quest_metadata or {}),
        stage_metadata=dict(stage_metadata or {}),
    )


def quest_chain_from_specs(
    chain_id: str,
    title: str,
    quests: Sequence[QuestTemplate | QuestTemplateSpec | Mapping[str, Any] | str] = (),
    *,
    entry_quest_id: str = "",
    branches: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
) -> QuestChain:
    return quest_chain_spec(
        chain_id,
        title,
        quests=quests,
        entry_quest_id=entry_quest_id,
        branches=branches,
        metadata=metadata,
        quest_metadata=quest_metadata,
        stage_metadata=stage_metadata,
    ).build()


def quest_offer(
    offer_id: str,
    quest_id: str = "",
    *,
    template: QuestTemplate | None = None,
    giver_id: str = "",
    title: str = "",
    summary: str = "",
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
    expires_in_days: int = 0,
    transitions: Mapping[str, str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestOffer:
    from src.quests.quest_domain import quest_offer as _quest_offer

    return _quest_offer(
        offer_id=offer_id,
        quest_id=quest_id,
        template=template,
        giver_id=giver_id,
        title=title,
        summary=summary,
        conditions=conditions,
        actions=actions,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        npc_state=npc_state,
        world_context=world_context,
        expires_in_days=expires_in_days,
        transitions=transitions,
        metadata=metadata,
    )
