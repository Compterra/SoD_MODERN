# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from src.quests.quest_domain import (
    QuestFailure,
    QuestReward,
    QuestStage,
    QuestTemplate,
    quest_action,
    quest_blueprint,
    quest_chain,
    quest_condition,
    quest_failure,
    quest_reward,
    quest_single_stage_quest,
    quest_stage,
    quest_trigger,
    validate_quest_id,
)


__all__ = [
    "QuestBranch",
    "ambush_quest",
    "delivery_quest",
    "diplomacy_quest",
    "escort_quest",
    "hunt_quest",
    "investigation_quest",
    "quest_branch",
    "quest_failure_bundle",
    "quest_optional_stage",
    "quest_repeatable_stage",
    "quest_reward_bundle",
    "quest_timed_stage",
    "rescue_quest",
    "siege_quest",
]


def _merge_metadata(*parts: Mapping[str, Any] | None) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for part in parts:
        merged.update(dict(part or {}))
    return merged


def _as_tuple(value: Sequence[Any] | Any) -> tuple[Any, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(value)
    return (value,)


@dataclass(frozen=True)
class QuestBranch:
    branch_id: str
    from_stage: str = ""
    to_stage: str = ""
    condition: str = ""
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestBranch":
        validate_quest_id(self.branch_id)
        if self.from_stage:
            validate_quest_id(self.from_stage)
        if self.to_stage:
            validate_quest_id(self.to_stage)
        if not self.to_stage:
            raise ValueError("QuestBranch.to_stage cannot be empty")
        return self

    def as_transition(self) -> tuple[str, str]:
        self.validate()
        key = self.condition or self.branch_id
        return key, self.to_stage


def quest_branch(
    branch_id: str,
    to_stage: str,
    *,
    from_stage: str = "",
    condition: str = "",
    description: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestBranch:
    return QuestBranch(
        branch_id=branch_id,
        from_stage=from_stage,
        to_stage=to_stage,
        condition=condition,
        description=description,
        metadata=dict(metadata or {}),
    ).validate()


def quest_reward_bundle(
    bundle_id: str,
    *rewards: QuestReward | str,
    gold: int = 0,
    xp: int = 0,
    renown: int = 0,
    honor: int = 0,
    relation: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> tuple[QuestReward, ...]:
    validate_quest_id(bundle_id)
    result: list[QuestReward] = []
    for index, reward in enumerate(rewards, start=1):
        if isinstance(reward, QuestReward):
            result.append(reward.validate())
        else:
            result.append(
                quest_reward(
                    f"{bundle_id}_reward_{index}",
                    str(reward),
                    metadata=_merge_metadata(metadata, {"bundle": bundle_id}),
                )
            )
    numeric_rewards = (
        ("gold", gold, "Award gold"),
        ("xp", xp, "Award experience"),
        ("renown", renown, "Award renown"),
        ("honor", honor, "Change honor"),
        ("relation", relation, "Change relation"),
    )
    for key, amount, description in numeric_rewards:
        if amount:
            result.append(
                quest_reward(
                    f"{bundle_id}_{key}",
                    f"{key}:{int(amount)}",
                    description=description,
                    metadata=_merge_metadata(metadata, {"bundle": bundle_id, "amount": int(amount)}),
                )
            )
    return tuple(result)


def quest_failure_bundle(
    bundle_id: str,
    *failures: QuestFailure | str,
    relation: int = 0,
    honor: int = 0,
    renown: int = 0,
    cooldown_days: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> tuple[QuestFailure, ...]:
    validate_quest_id(bundle_id)
    result: list[QuestFailure] = []
    for index, failure in enumerate(failures, start=1):
        if isinstance(failure, QuestFailure):
            result.append(failure.validate())
        else:
            result.append(
                quest_failure(
                    f"{bundle_id}_failure_{index}",
                    str(failure),
                    metadata=_merge_metadata(metadata, {"bundle": bundle_id}),
                )
            )
    numeric_failures = (
        ("relation", relation, "Lose relation"),
        ("honor", honor, "Change honor"),
        ("renown", renown, "Change renown"),
        ("cooldown_days", cooldown_days, "Apply quest-giver cooldown"),
    )
    for key, amount, description in numeric_failures:
        if amount:
            result.append(
                quest_failure(
                    f"{bundle_id}_{key}",
                    f"{key}:{int(amount)}",
                    description=description,
                    metadata=_merge_metadata(metadata, {"bundle": bundle_id, "amount": int(amount)}),
                )
            )
    return tuple(result)


def _stage_with_kind(
    kind: str,
    stage_id: str,
    title: str,
    objective: str,
    *,
    description: str = "",
    conditions: Sequence[Any] = (),
    actions: Sequence[Any] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[Any] = (),
    rewards: Sequence[Any] = (),
    failures: Sequence[Any] = (),
    transitions: Mapping[str, str] | Sequence[QuestBranch] | None = None,
    metadata: Mapping[str, Any] | None = None,
    **kind_metadata: Any,
) -> QuestStage:
    transition_map: dict[str, str] = {}
    if isinstance(transitions, Mapping):
        transition_map.update(dict(transitions))
    else:
        for branch in _as_tuple(transitions):
            if isinstance(branch, QuestBranch):
                key, value = branch.as_transition()
                transition_map[key] = value
            elif branch:
                raise TypeError(f"Expected QuestBranch in transitions, got {type(branch)!r}")
    return quest_stage(
        stage_id,
        title,
        objective,
        description=description,
        conditions=conditions,
        actions=actions,
        battle_hooks=battle_hooks,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transition_map,
        metadata=_merge_metadata(metadata, {"dsl_stage_kind": kind}, kind_metadata),
    )


def quest_optional_stage(stage_id: str, title: str, objective: str, **kwargs: Any) -> QuestStage:
    return _stage_with_kind("optional", stage_id, title, objective, optional=True, **kwargs)


def quest_timed_stage(
    stage_id: str,
    title: str,
    objective: str,
    *,
    duration_days: int = 0,
    duration_hours: int = 0,
    timeout_transition: str = "",
    **kwargs: Any,
) -> QuestStage:
    if duration_days <= 0 and duration_hours <= 0:
        raise ValueError("quest_timed_stage requires duration_days or duration_hours")
    return _stage_with_kind(
        "timed",
        stage_id,
        title,
        objective,
        duration_days=int(duration_days),
        duration_hours=int(duration_hours),
        timeout_transition=timeout_transition,
        **kwargs,
    )


def quest_repeatable_stage(
    stage_id: str,
    title: str,
    objective: str,
    *,
    max_repeats: int = 0,
    repeat_cooldown_days: int = 0,
    **kwargs: Any,
) -> QuestStage:
    return _stage_with_kind(
        "repeatable",
        stage_id,
        title,
        objective,
        max_repeats=max(0, int(max_repeats)),
        repeat_cooldown_days=max(0, int(repeat_cooldown_days)),
        **kwargs,
    )


def _single_stage_pattern(
    quest_id: str,
    name: str,
    description: str,
    *,
    stage_title: str,
    stage_objective: str,
    pattern: str,
    flags: Any = 0,
    conditions: Sequence[Any] = (),
    actions: Sequence[Any] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[Any] = (),
    rewards: Sequence[Any] = (),
    failures: Sequence[Any] = (),
    metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
) -> QuestTemplate:
    return quest_single_stage_quest(
        quest_id,
        name,
        flags,
        description,
        stage_title=stage_title,
        stage_objective=stage_objective,
        actions=actions,
        battle_hooks=battle_hooks,
        conditions=conditions,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        quest_metadata=_merge_metadata(metadata, {"dsl_pattern": pattern}),
        stage_metadata=_merge_metadata(stage_metadata, {"dsl_pattern": pattern}),
    )


def delivery_quest(
    quest_id: str,
    item_name: str,
    destination: str,
    *,
    giver: str = "A local sponsor",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Deliver {item_name}",
        f"{giver} needs {item_name} delivered to {destination}.",
        stage_title="Make the delivery",
        stage_objective=f"Deliver {item_name} to {destination}.",
        pattern="delivery",
        **kwargs,
    )


def hunt_quest(
    quest_id: str,
    target_name: str,
    *,
    region: str = "the region",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Hunt {target_name}",
        f"{target_name} is causing trouble around {region}.",
        stage_title="Track and defeat the target",
        stage_objective=f"Find and defeat {target_name}.",
        pattern="hunt",
        battle_hooks=tuple(_as_tuple(kwargs.pop("battle_hooks", ())) + ("party_defeated",)),
        **kwargs,
    )


def escort_quest(
    quest_id: str,
    escort_name: str,
    destination: str,
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Escort {escort_name}",
        f"{escort_name} needs protection on the road to {destination}.",
        stage_title="Protect the escort",
        stage_objective=f"Escort {escort_name} safely to {destination}.",
        pattern="escort",
        **kwargs,
    )


def rescue_quest(
    quest_id: str,
    captive_name: str,
    *,
    captor_name: str = "their captors",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Rescue {captive_name}",
        f"{captive_name} must be rescued from {captor_name}.",
        stage_title="Recover the captive",
        stage_objective=f"Free {captive_name} and return safely.",
        pattern="rescue",
        battle_hooks=tuple(_as_tuple(kwargs.pop("battle_hooks", ())) + ("prisoner_freed",)),
        **kwargs,
    )


def siege_quest(
    quest_id: str,
    center_name: str,
    *,
    role: str = "support",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Siege {role.title()} at {center_name}",
        f"The siege around {center_name} needs {role}.",
        stage_title="Aid the siege effort",
        stage_objective=f"Provide {role} for the siege at {center_name}.",
        pattern="siege",
        battle_hooks=tuple(_as_tuple(kwargs.pop("battle_hooks", ())) + ("siege_event",)),
        **kwargs,
    )


def diplomacy_quest(
    quest_id: str,
    counterpart: str,
    *,
    matter: str = "a delicate matter",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Negotiate with {counterpart}",
        f"A sponsor needs you to negotiate with {counterpart} over {matter}.",
        stage_title="Complete the negotiation",
        stage_objective=f"Speak with {counterpart} and resolve {matter}.",
        pattern="diplomacy",
        **kwargs,
    )


def ambush_quest(
    quest_id: str,
    target_name: str,
    *,
    location_hint: str = "a nearby road",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Ambush {target_name}",
        f"{target_name} can be intercepted near {location_hint}.",
        stage_title="Spring the ambush",
        stage_objective=f"Intercept and defeat {target_name}.",
        pattern="ambush",
        battle_hooks=tuple(_as_tuple(kwargs.pop("battle_hooks", ())) + ("party_defeated",)),
        **kwargs,
    )


def investigation_quest(
    quest_id: str,
    mystery_name: str,
    *,
    location: str = "the area",
    **kwargs: Any,
) -> QuestTemplate:
    return _single_stage_pattern(
        quest_id,
        f"Investigate {mystery_name}",
        f"Something is wrong in {location}, and {mystery_name} may be the key.",
        stage_title="Gather evidence",
        stage_objective=f"Investigate {mystery_name} around {location}.",
        pattern="investigation",
        **kwargs,
    )
