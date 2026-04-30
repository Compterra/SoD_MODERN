# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from src.quests.quest_domain import (
    QuestAction,
    QuestBattleObjective,
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
    quest_battle_objective,
    quest_chain,
    quest_condition,
    quest_failure,
    quest_reward,
    quest_stage,
    quest_template,
    validate_quest_id,
)

__all__ = [
    "QuestComponentRegistry",
    "quest_components_from_mapping",
    "quest_component_registry",
    "quest_motif_from_mapping",
    "quest_motif_delivery_complication_reward",
    "quest_motif_escort_ambush_debrief",
    "quest_motif_linear_chain",
    "quest_motif_rescue_pursuit_return",
]


def _snapshot_value(value: Any) -> Any:
    if hasattr(value, "to_snapshot"):
        return value.to_snapshot()
    if isinstance(value, Mapping):
        return {str(key): _snapshot_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_snapshot_value(item) for item in value]
    return value


@dataclass
class QuestComponentRegistry:
    registry_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    conditions: dict[str, QuestCondition] = field(default_factory=dict)
    actions: dict[str, QuestAction] = field(default_factory=dict)
    triggers: dict[str, QuestTrigger] = field(default_factory=dict)
    rewards: dict[str, QuestReward] = field(default_factory=dict)
    failures: dict[str, QuestFailure] = field(default_factory=dict)
    npc_states: dict[str, QuestNPCState] = field(default_factory=dict)
    world_contexts: dict[str, QuestWorldContext] = field(default_factory=dict)
    battle_objectives: dict[str, QuestBattleObjective] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.registry_id = validate_quest_id(self.registry_id)
        self.metadata = dict(self.metadata or {})

    def _register(self, bucket: dict[str, Any], kind: str, name: str, value: Any) -> Any:
        key = validate_quest_id(name)
        if key in bucket:
            raise ValueError(f"Quest component registry {self.registry_id!r} already has {kind} {key!r}")
        if hasattr(value, "validate"):
            value = value.validate()
        bucket[key] = value
        return value

    def _get(self, bucket: dict[str, Any], kind: str, name: str) -> Any:
        key = validate_quest_id(name)
        if key not in bucket:
            raise KeyError(f"Quest component registry {self.registry_id!r} has no {kind} {key!r}")
        return bucket[key]

    def has_condition(self, name: str) -> bool:
        return validate_quest_id(name) in self.conditions

    def has_action(self, name: str) -> bool:
        return validate_quest_id(name) in self.actions

    def has_trigger(self, name: str) -> bool:
        return validate_quest_id(name) in self.triggers

    def has_reward(self, name: str) -> bool:
        return validate_quest_id(name) in self.rewards

    def has_failure(self, name: str) -> bool:
        return validate_quest_id(name) in self.failures

    def register_condition(self, name: str, value: QuestCondition | str) -> QuestCondition:
        item = value if isinstance(value, QuestCondition) else quest_condition(f"{self.registry_id}_{name}", value)
        return self._register(self.conditions, "condition", name, item)

    def get_condition(self, name: str) -> QuestCondition:
        return self._get(self.conditions, "condition", name)

    def register_action(self, name: str, value: QuestAction | str) -> QuestAction:
        item = value if isinstance(value, QuestAction) else quest_action(f"{self.registry_id}_{name}", value)
        return self._register(self.actions, "action", name, item)

    def get_action(self, name: str) -> QuestAction:
        return self._get(self.actions, "action", name)

    def register_trigger(self, name: str, value: QuestTrigger) -> QuestTrigger:
        return self._register(self.triggers, "trigger", name, value)

    def get_trigger(self, name: str) -> QuestTrigger:
        return self._get(self.triggers, "trigger", name)

    def register_reward(self, name: str, value: QuestReward | str) -> QuestReward:
        item = value if isinstance(value, QuestReward) else quest_reward(f"{self.registry_id}_{name}", value)
        return self._register(self.rewards, "reward", name, item)

    def get_reward(self, name: str) -> QuestReward:
        return self._get(self.rewards, "reward", name)

    def register_failure(self, name: str, value: QuestFailure | str) -> QuestFailure:
        item = value if isinstance(value, QuestFailure) else quest_failure(f"{self.registry_id}_{name}", value)
        return self._register(self.failures, "failure", name, item)

    def get_failure(self, name: str) -> QuestFailure:
        return self._get(self.failures, "failure", name)

    def register_npc_state(self, name: str, value: QuestNPCState) -> QuestNPCState:
        return self._register(self.npc_states, "npc_state", name, value)

    def get_npc_state(self, name: str) -> QuestNPCState:
        return self._get(self.npc_states, "npc_state", name)

    def register_world_context(self, name: str, value: QuestWorldContext) -> QuestWorldContext:
        return self._register(self.world_contexts, "world_context", name, value)

    def get_world_context(self, name: str) -> QuestWorldContext:
        return self._get(self.world_contexts, "world_context", name)

    def register_battle_objective(self, name: str, value: QuestBattleObjective) -> QuestBattleObjective:
        return self._register(self.battle_objectives, "battle_objective", name, value)

    def get_battle_objective(self, name: str) -> QuestBattleObjective:
        return self._get(self.battle_objectives, "battle_objective", name)

    def update_from_mapping(self, spec: Mapping[str, Any]) -> "QuestComponentRegistry":
        for name, value in dict(spec.get("conditions", {}) or {}).items():
            self.register_condition(str(name), value)
        for name, value in dict(spec.get("actions", {}) or {}).items():
            self.register_action(str(name), value)
        for name, value in dict(spec.get("triggers", {}) or {}).items():
            self.register_trigger(str(name), value)
        for name, value in dict(spec.get("rewards", {}) or {}).items():
            self.register_reward(str(name), value)
        for name, value in dict(spec.get("failures", {}) or {}).items():
            self.register_failure(str(name), value)
        for name, value in dict(spec.get("npc_states", {}) or {}).items():
            self.register_npc_state(str(name), value)
        for name, value in dict(spec.get("world_contexts", {}) or {}).items():
            self.register_world_context(str(name), value)
        for name, value in dict(spec.get("battle_objectives", {}) or {}).items():
            self.register_battle_objective(str(name), value)
        return self

    def snapshot(self) -> dict[str, Any]:
        return {
            "registry_id": self.registry_id,
            "metadata": dict(self.metadata),
            "conditions": {key: _snapshot_value(value) for key, value in sorted(self.conditions.items())},
            "actions": {key: _snapshot_value(value) for key, value in sorted(self.actions.items())},
            "triggers": {key: _snapshot_value(value) for key, value in sorted(self.triggers.items())},
            "rewards": {key: _snapshot_value(value) for key, value in sorted(self.rewards.items())},
            "failures": {key: _snapshot_value(value) for key, value in sorted(self.failures.items())},
            "npc_states": {key: _snapshot_value(value) for key, value in sorted(self.npc_states.items())},
            "world_contexts": {key: _snapshot_value(value) for key, value in sorted(self.world_contexts.items())},
            "battle_objectives": {key: _snapshot_value(value) for key, value in sorted(self.battle_objectives.items())},
        }


def quest_component_registry(registry_id: str, *, metadata: Mapping[str, Any] | None = None) -> QuestComponentRegistry:
    return QuestComponentRegistry(registry_id, metadata=dict(metadata or {}))


def quest_components_from_mapping(
    registry_id: str,
    spec: Mapping[str, Any],
    *,
    metadata: Mapping[str, Any] | None = None,
) -> QuestComponentRegistry:
    registry = quest_component_registry(registry_id, metadata=metadata)
    return registry.update_from_mapping(spec)


def _registry_items(registry: QuestComponentRegistry | None, bucket_name: str, names: Sequence[str]) -> tuple[Any, ...]:
    if registry is None:
        return ()
    bucket = getattr(registry, bucket_name)
    result = []
    for name in names:
        key = validate_quest_id(name)
        if key not in bucket:
            raise KeyError(f"Quest component registry {registry.registry_id!r} has no {bucket_name[:-1]} {key!r}")
        result.append(bucket[key])
    return tuple(result)


def _ensure_stage_outcome(
    quest_id: str,
    stage: QuestStage,
    *,
    default_reward: QuestReward | None = None,
) -> QuestStage:
    if stage.rewards or stage.failures or stage.metadata.get("terminal"):
        return stage
    stage.rewards = (default_reward or quest_reward(f"{quest_id}_stage_reward", "stage complete"),)
    return stage.validate()


def _apply_template_defaults(
    template: QuestTemplate,
    *,
    registry: QuestComponentRegistry | None = None,
    condition_names: Sequence[str] = (),
    action_names: Sequence[str] = (),
    reward_names: Sequence[str] = (),
    failure_names: Sequence[str] = (),
    npc_state_name: str = "",
    world_context_name: str = "",
) -> QuestTemplate:
    conditions = tuple(template.conditions) + _registry_items(registry, "conditions", condition_names)
    actions = tuple(template.actions) + _registry_items(registry, "actions", action_names)
    rewards = tuple(template.rewards) + _registry_items(registry, "rewards", reward_names)
    failures = tuple(template.failures) + _registry_items(registry, "failures", failure_names)
    npc_state = template.npc_state
    world_context = template.world_context
    if registry is not None and npc_state_name:
        npc_state = registry.get_npc_state(npc_state_name)
    if registry is not None and world_context_name:
        world_context = registry.get_world_context(world_context_name)
    template.conditions = conditions
    template.actions = actions
    template.rewards = rewards
    template.failures = failures
    template.npc_state = npc_state
    template.world_context = world_context
    template.metadata = {
        **dict(template.metadata),
        "component_registry": registry.registry_id if registry is not None else "",
    }
    return template.validate()


def quest_motif_linear_chain(
    chain_id: str,
    title: str,
    quest_titles: Sequence[str],
    *,
    flags: Any = 0,
    description_prefix: str = "",
    registry: QuestComponentRegistry | None = None,
    condition_names: Sequence[str] = (),
    action_names: Sequence[str] = (),
    reward_names: Sequence[str] = (),
    failure_names: Sequence[str] = (),
    npc_state_name: str = "",
    world_context_name: str = "",
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestChain:
    chain_id = validate_quest_id(chain_id)
    quests = []
    for index, quest_title in enumerate(quest_titles, start=1):
        quest_id = validate_quest_id(f"{chain_id}_{index}")
        next_id = validate_quest_id(f"{chain_id}_{index + 1}") if index < len(quest_titles) else "quests_end"
        reward = registry.get_reward(reward_names[0]) if registry is not None and reward_names else None
        stage = _ensure_stage_outcome(
            quest_id,
            quest_stage(
                f"{quest_id}_stage",
                quest_title,
                quest_title,
                metadata={"entry": True, "motif": "linear_chain", **dict(stage_metadata or {})},
            ),
            default_reward=reward,
        )
        template = quest_template(
            quest_id,
            quest_title,
            flags,
            f"{description_prefix}{quest_title}" if description_prefix else quest_title,
            stages=(stage,),
            transitions={"done": next_id},
            metadata={"motif": "linear_chain", **dict(quest_metadata or {})},
        )
        quests.append(
            _apply_template_defaults(
                template,
                registry=registry,
                condition_names=condition_names,
                action_names=action_names,
                reward_names=reward_names,
                failure_names=failure_names,
                npc_state_name=npc_state_name,
                world_context_name=world_context_name,
            )
        )
    return quest_chain(
        chain_id,
        title,
        quests=tuple(quests),
        entry_quest_id=quests[0].quest_id if quests else "",
        branches={"main": tuple(quest.quest_id for quest in quests)},
        metadata={
            "motif": "linear_chain",
            "component_registry": registry.registry_id if registry is not None else "",
            **dict(metadata or {}),
        },
    )


def _motif_defaults_from_mapping(spec: Mapping[str, Any]) -> dict[str, Any]:
    defaults = dict(spec.get("defaults", {}) or {})
    return {
        "condition_names": tuple(defaults.get("conditions", ()) or ()),
        "action_names": tuple(defaults.get("actions", ()) or ()),
        "reward_names": tuple(defaults.get("rewards", ()) or ()),
        "failure_names": tuple(defaults.get("failures", ()) or ()),
        "npc_state_name": str(defaults.get("npc_state", "") or ""),
        "world_context_name": str(defaults.get("world_context", "") or ""),
    }


def quest_motif_from_mapping(spec: Mapping[str, Any]) -> QuestChain:
    if not isinstance(spec, Mapping):
        raise TypeError(f"motif spec must be a mapping, got {type(spec)!r}")

    chain_id = str(spec.get("chain_id") or spec.get("id") or "")
    title = str(spec.get("title") or spec.get("name") or chain_id)
    motif = str(spec.get("motif") or spec.get("kind") or "linear_chain")
    flags = spec.get("flags", 0)
    metadata = dict(spec.get("metadata", {}) or {})
    registry_spec = spec.get("registry")
    registry = None
    if isinstance(registry_spec, QuestComponentRegistry):
        registry = registry_spec
    elif isinstance(registry_spec, Mapping):
        registry_id = str(registry_spec.get("registry_id") or registry_spec.get("id") or f"{chain_id}_registry")
        registry = quest_components_from_mapping(
            registry_id,
            registry_spec,
            metadata=registry_spec.get("metadata", {}),
        )

    defaults = _motif_defaults_from_mapping(spec)
    if motif == "linear_chain":
        quest_titles = tuple(spec.get("quest_titles") or spec.get("quests") or ())
        return quest_motif_linear_chain(
            chain_id,
            title,
            quest_titles,
            flags=flags,
            registry=registry,
            metadata=metadata,
            quest_metadata=spec.get("quest_metadata", {}),
            stage_metadata=spec.get("stage_metadata", {}),
            **defaults,
        )
    if motif == "escort_ambush_debrief":
        return quest_motif_escort_ambush_debrief(chain_id, title, flags=flags, registry=registry, metadata=metadata)
    if motif == "delivery_complication_reward":
        return quest_motif_delivery_complication_reward(chain_id, title, flags=flags, registry=registry, metadata=metadata)
    if motif == "rescue_pursuit_return":
        return quest_motif_rescue_pursuit_return(chain_id, title, flags=flags, registry=registry, metadata=metadata)
    raise ValueError(f"Unknown quest motif {motif!r}")


def quest_motif_escort_ambush_debrief(
    chain_id: str,
    title: str,
    *,
    flags: Any = 0,
    registry: QuestComponentRegistry | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestChain:
    return quest_motif_linear_chain(
        chain_id,
        title,
        ("Escort the Party", "Break the Ambush", "Debrief the Escort"),
        flags=flags,
        registry=registry,
        metadata={"motif": "escort_ambush_debrief", **dict(metadata or {})},
    )


def quest_motif_delivery_complication_reward(
    chain_id: str,
    title: str,
    *,
    flags: Any = 0,
    registry: QuestComponentRegistry | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestChain:
    return quest_motif_linear_chain(
        chain_id,
        title,
        ("Carry the Delivery", "Handle the Complication", "Collect the Reward"),
        flags=flags,
        registry=registry,
        metadata={"motif": "delivery_complication_reward", **dict(metadata or {})},
    )


def quest_motif_rescue_pursuit_return(
    chain_id: str,
    title: str,
    *,
    flags: Any = 0,
    registry: QuestComponentRegistry | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestChain:
    chain = quest_motif_linear_chain(
        chain_id,
        title,
        ("Rescue the Captive", "Pursue the Captors", "Return the Captive"),
        flags=flags,
        registry=registry,
        metadata={"motif": "rescue_pursuit_return", **dict(metadata or {})},
    )
    first = chain.normalized_quests()[0]
    objective = quest_battle_objective(f"{first.quest_id}_objective", "rescue_target", target_troop_id="trp_prisoner")
    first.stages = (
        quest_stage(
            f"{first.quest_id}_stage",
            "Rescue the Captive",
            "Free the captive and start the pursuit.",
            battle_hooks=(f"{first.quest_id}_battle_hook",),
            battle_objective=objective,
            rewards=(quest_reward(f"{first.quest_id}_stage_reward", "stage complete"),),
            metadata={"entry": True, "motif": "rescue_pursuit_return"},
        ),
    )
    return chain.validate()
