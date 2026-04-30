# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

__all__ = [
    "QuestAction",
    "QuestBlueprint",
    "QuestChain",
    "QuestCondition",
    "QuestFailure",
    "QuestNPCState",
    "QuestOffer",
    "QuestReward",
    "QuestBattleObjective",
    "QuestStage",
    "QuestTemplate",
    "QuestTrigger",
    "QuestWorldContext",
    "ensure_unique_quest_ids",
    "ensure_unique_stage_ids",
    "quest_action",
    "quest_blueprint",
    "quest_chain",
    "quest_condition",
    "quest_delivery_quest",
    "quest_escort_quest",
    "quest_failure",
    "quest_hunt_quest",
    "quest_npc_state",
    "quest_offer",
    "quest_reward",
    "quest_rescue_quest",
    "quest_single_stage_quest",
    "quest_stage",
    "quest_template",
    "quest_trigger",
    "quest_world_context",
    "quest_battle_objective",
    "normalize_battle_objective_action_kind",
    "QUEST_BATTLE_OBJECTIVE_ACTION_KINDS",
    "QUEST_BATTLE_OBJECTIVE_ACTION_ALIASES",
    "QUEST_BATTLE_OBJECTIVE_REQUIRED_PAYLOAD_KEYS",
    "QUEST_BATTLE_OBJECTIVE_MESSAGE_TEMPLATES",
    "validate_quest_id",
]

_QUEST_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_NON_EMPTY_RE = re.compile(r"\S")

QUEST_BATTLE_OBJECTIVE_ACTION_KINDS = (
    "kill_target",
    "capture_target",
    "protect_target",
    "survive_timer",
    "break_siege_line",
    "hold_position",
    "destroy_force",
    "escort_during_battle",
    "free_prisoner_during_mission",
    "rescue_allied_captain",
    "defeat_wave_objective",
)

QUEST_BATTLE_OBJECTIVE_ACTION_ALIASES = {
    "kill": "kill_target",
    "capture": "capture_target",
    "protect": "protect_target",
    "survive": "survive_timer",
    "break_siege": "break_siege_line",
    "hold": "hold_position",
    "destroy": "destroy_force",
    "escort": "escort_during_battle",
    "free_prisoner": "free_prisoner_during_mission",
    "rescue_captain": "rescue_allied_captain",
    "defeat_wave": "defeat_wave_objective",
}

QUEST_BATTLE_OBJECTIVE_REQUIRED_PAYLOAD_KEYS = {
    "kill_target": ("target_troop_id",),
    "capture_target": ("target_troop_id", "target_party_id"),
    "protect_target": ("target_troop_id", "target_party_id"),
    "survive_timer": ("timer_duration",),
    "break_siege_line": ("target_party_id", "target_center_id"),
    "hold_position": ("target_party_id", "timer_duration"),
    "destroy_force": ("target_party_id",),
    "escort_during_battle": ("target_troop_id", "target_party_id"),
    "free_prisoner_during_mission": ("target_troop_id", "target_party_id"),
    "rescue_allied_captain": ("target_troop_id", "target_party_id"),
    "defeat_wave_objective": ("wave_index", "required_count"),
}

QUEST_BATTLE_OBJECTIVE_MESSAGE_TEMPLATES = {
    "kill_target": {
        "success": "The target has been eliminated.",
        "failure": "The target escaped or survived.",
    },
    "capture_target": {
        "success": "The target has been captured.",
        "failure": "The capture objective failed.",
    },
    "protect_target": {
        "success": "The protected target survived the battle.",
        "failure": "The protected target was lost.",
    },
    "survive_timer": {
        "success": "The force held out long enough.",
        "failure": "The force did not survive long enough.",
    },
    "break_siege_line": {
        "success": "The siege line has been broken.",
        "failure": "The assault failed to break through.",
    },
    "hold_position": {
        "success": "The position was held.",
        "failure": "The position was lost.",
    },
    "destroy_force": {
        "success": "The enemy force has been destroyed.",
        "failure": "The enemy force remains intact.",
    },
    "escort_during_battle": {
        "success": "The escort made it through the battle.",
        "failure": "The escort was lost.",
    },
    "free_prisoner_during_mission": {
        "success": "The prisoner was freed.",
        "failure": "The prisoner could not be rescued.",
    },
    "rescue_allied_captain": {
        "success": "The allied captain was rescued.",
        "failure": "The allied captain was not recovered.",
    },
    "defeat_wave_objective": {
        "success": "The wave was defeated.",
        "failure": "The current wave held the field.",
    },
}


def normalize_battle_objective_action_kind(value: str | Any) -> str:
    if not isinstance(value, str):
        raise TypeError(f"battle objective action kind must be a string, got {type(value)!r}")
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_").replace(".", "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")
    if not normalized:
        raise ValueError("battle objective action kind cannot be empty")
    normalized = QUEST_BATTLE_OBJECTIVE_ACTION_ALIASES.get(normalized, normalized)
    if normalized not in QUEST_BATTLE_OBJECTIVE_ACTION_KINDS:
        raise ValueError(
            "battle objective action kind must be one of "
            f"{QUEST_BATTLE_OBJECTIVE_ACTION_KINDS!r}: {value!r}"
        )
    return normalized


def validate_quest_id(quest_id: str) -> str:
    """
    Validate a quest-style identifier used by the quest domain model.

    The quest system uses lower snake_case identifiers for stable generated
    output, predictable lookups, and compatibility with the legacy compiler.
    """
    if not isinstance(quest_id, str):
        raise TypeError(f"quest_id must be a string, got {type(quest_id)!r}")
    if not quest_id:
        raise ValueError("quest_id cannot be empty")
    if not _QUEST_ID_RE.fullmatch(quest_id):
        raise ValueError(
            "quest_id must use lower snake_case letters, numbers, and underscores: "
            f"{quest_id!r}"
        )
    return quest_id


def _validate_text(label: str, value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string, got {type(value)!r}")
    if not _NON_EMPTY_RE.search(value):
        raise ValueError(f"{label} cannot be empty or whitespace only")
    return value


def _validate_optional_text(label: str, value: str) -> str:
    if value == "":
        return value
    return _validate_text(label, value)


def _validate_optional_int(label: str, value: int | None) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int):
        raise TypeError(f"{label} must be an int or None, got {type(value)!r}")
    return value


def _coerce_metadata(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(metadata or {})


def _validate_transition_map(label: str, transitions: Mapping[str, str]) -> dict[str, str]:
    if not isinstance(transitions, Mapping):
        raise TypeError(f"{label} must be a mapping, got {type(transitions)!r}")
    result: dict[str, str] = {}
    for key, value in transitions.items():
        if not isinstance(key, str):
            raise TypeError(f"{label} keys must be strings, got {type(key)!r}")
        _validate_text(f"{label}.key", key)
        if not isinstance(value, str):
            raise TypeError(f"{label}[{key!r}] must be a string, got {type(value)!r}")
        _validate_text(f"{label}[{key!r}]", value)
        result[key] = value
    return result


def _coerce_condition_item(
    value: "QuestCondition | str",
    prefix: str,
    index: int,
) -> "QuestCondition":
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
    value: "QuestAction | str",
    prefix: str,
    index: int,
) -> "QuestAction":
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
    value: "QuestReward | str",
    prefix: str,
    index: int,
) -> "QuestReward":
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
    value: "QuestFailure | str",
    prefix: str,
    index: int,
) -> "QuestFailure":
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
    value: "QuestTrigger | str",
    prefix: str,
    index: int,
) -> "QuestTrigger":
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


def _coerce_stage_item(
    value: "QuestStage | str",
    prefix: str,
    index: int,
) -> "QuestStage":
    if isinstance(value, QuestStage):
        return value.validate()
    if isinstance(value, str):
        return quest_stage(
            f"{prefix}_stage_{index}",
            value,
            value,
        )
    raise TypeError(
        f"Expected QuestStage or str for {prefix} stage, got {type(value)!r}"
    )


def _narrative_mapping(source: Mapping[str, Any] | None, *keys: str) -> dict[str, Any]:
    if not isinstance(source, Mapping):
        return {}
    for key in keys:
        value = source.get(key)
        if isinstance(value, Mapping):
            return dict(value)
        if isinstance(value, Sequence) and not isinstance(value, str):
            return {
                str(index): item
                for index, item in enumerate(value, start=1)
                if item is not None
            }
        if isinstance(value, str) and value.strip():
            return {"default": value.strip()}
    return {}


def _coerce_narrative_entry(entry: Any) -> dict[str, Any]:
    if isinstance(entry, Mapping):
        return dict(entry)
    if entry is None:
        return {}
    return {"action": str(entry).strip()}


@dataclass
class QuestCondition:
    condition_id: str
    expression: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestCondition":
        validate_quest_id(self.condition_id)
        _validate_text("condition.expression", self.expression)
        if self.description:
            _validate_text("condition.description", self.description)
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "condition_id": self.condition_id,
            "expression": self.expression,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestAction:
    action_id: str
    expression: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestAction":
        validate_quest_id(self.action_id)
        _validate_text("action.expression", self.expression)
        if self.description:
            _validate_text("action.description", self.description)
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "expression": self.expression,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestReward:
    reward_id: str
    expression: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestReward":
        validate_quest_id(self.reward_id)
        _validate_text("reward.expression", self.expression)
        if self.description:
            _validate_text("reward.description", self.description)
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "reward_id": self.reward_id,
            "expression": self.expression,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestFailure:
    failure_id: str
    expression: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestFailure":
        validate_quest_id(self.failure_id)
        _validate_text("failure.expression", self.expression)
        if self.description:
            _validate_text("failure.description", self.description)
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "failure_id": self.failure_id,
            "expression": self.expression,
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestTrigger:
    trigger_id: str
    event_name: str
    conditions: tuple[QuestCondition | str, ...] = ()
    actions: tuple[QuestAction | str, ...] = ()
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_conditions(self) -> tuple[QuestCondition, ...]:
        return tuple(
            _coerce_condition_item(condition, self.trigger_id, index)
            for index, condition in enumerate(self.conditions, start=1)
        )

    def normalized_actions(self) -> tuple[QuestAction, ...]:
        return tuple(
            _coerce_action_item(action, self.trigger_id, index)
            for index, action in enumerate(self.actions, start=1)
        )

    def matches(self, event_name: str) -> bool:
        return self.event_name == event_name

    def validate(self) -> "QuestTrigger":
        validate_quest_id(self.trigger_id)
        _validate_text("trigger.event_name", self.event_name)
        if self.description:
            _validate_text("trigger.description", self.description)
        for condition in self.normalized_conditions():
            condition.validate()
        for action in self.normalized_actions():
            action.validate()
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "trigger_id": self.trigger_id,
            "event_name": self.event_name,
            "conditions": [condition.to_snapshot() for condition in self.normalized_conditions()],
            "actions": [action.to_snapshot() for action in self.normalized_actions()],
            "description": self.description,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestNPCState:
    """
    Stateful quest-giver model used to drive NPC availability and dialogue.

    The state keeps enough structured information to support 108-style living
    quest-giver logic without hard-coding the game engine into the authoring
    model.
    """

    npc_id: str
    state: str = "idle"
    last_quest_id: str = ""
    cooldown_days: int = 0
    dialogue_state: str = ""
    available_quests: list[str] = field(default_factory=list)
    completed_quests: list[str] = field(default_factory=list)
    failed_quests: list[str] = field(default_factory=list)
    locked_chains: list[str] = field(default_factory=list)
    cooldowns: dict[str, int] = field(default_factory=dict)
    relationship_thresholds: dict[str, int] = field(default_factory=dict)
    faction_alignment: str = ""
    story_arc_progression: dict[str, Any] = field(default_factory=dict)
    player_reputation: dict[str, int] = field(default_factory=dict)
    special_flags: dict[str, Any] = field(default_factory=dict)
    dialogue_mode: str = ""
    personality: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def _coerce_sequence(value: Any) -> tuple[str, ...]:
        if value in (None, ""):
            return ()
        if isinstance(value, str):
            return tuple(part.strip() for part in re.split(r"[|;,]", value) if part.strip())
        if isinstance(value, Sequence):
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

    @staticmethod
    def _add_unique(collection: list[str], value: str) -> None:
        if value not in collection:
            collection.append(value)

    @staticmethod
    def _remove_value(collection: list[str], value: str) -> None:
        while value in collection:
            collection.remove(value)

    @staticmethod
    def _normalize_id_list(values: Sequence[str], *, label: str) -> list[str]:
        normalized: list[str] = []
        for value in values:
            if not isinstance(value, str):
                raise TypeError(f"{label} entries must be strings, got {type(value)!r}")
            quest_id = validate_quest_id(value)
            if quest_id not in normalized:
                normalized.append(quest_id)
        return normalized

    @staticmethod
    def _normalize_int_mapping(
        mapping: Mapping[str, Any],
        *,
        label: str,
        allow_negative: bool = True,
    ) -> dict[str, int]:
        if not isinstance(mapping, Mapping):
            raise TypeError(f"{label} must be a mapping, got {type(mapping)!r}")
        result: dict[str, int] = {}
        for key, value in mapping.items():
            if not isinstance(key, str):
                raise TypeError(f"{label} keys must be strings, got {type(key)!r}")
            validate_quest_id(key)
            if not isinstance(value, int):
                raise TypeError(f"{label}[{key!r}] must be an int, got {type(value)!r}")
            if not allow_negative and value < 0:
                raise ValueError(f"{label}[{key!r}] cannot be negative")
            result[key] = value
        return result

    @staticmethod
    def _normalize_any_mapping(mapping: Mapping[str, Any], *, label: str) -> dict[str, Any]:
        if not isinstance(mapping, Mapping):
            raise TypeError(f"{label} must be a mapping, got {type(mapping)!r}")
        result: dict[str, Any] = {}
        for key, value in mapping.items():
            if not isinstance(key, str):
                raise TypeError(f"{label} keys must be strings, got {type(key)!r}")
            validate_quest_id(key)
            result[key] = value
        return result

    def validate(self) -> "QuestNPCState":
        validate_quest_id(self.npc_id)
        _validate_text("npc_state.state", self.state)
        _validate_optional_text("npc_state.last_quest_id", self.last_quest_id)
        if not isinstance(self.cooldown_days, int):
            raise TypeError(
                f"npc_state.cooldown_days must be an int, got {type(self.cooldown_days)!r}"
            )
        if self.cooldown_days < 0:
            raise ValueError("npc_state.cooldown_days cannot be negative")
        if self.dialogue_state:
            _validate_text("npc_state.dialogue_state", self.dialogue_state)
        if self.dialogue_mode:
            _validate_text("npc_state.dialogue_mode", self.dialogue_mode)
        if self.personality:
            _validate_text("npc_state.personality", self.personality)

        self.available_quests = self._normalize_id_list(
            self.available_quests,
            label="npc_state.available_quests",
        )
        self.completed_quests = self._normalize_id_list(
            self.completed_quests,
            label="npc_state.completed_quests",
        )
        self.failed_quests = self._normalize_id_list(
            self.failed_quests,
            label="npc_state.failed_quests",
        )
        self.locked_chains = self._normalize_id_list(
            self.locked_chains,
            label="npc_state.locked_chains",
        )
        self.cooldowns = self._normalize_int_mapping(
            self.cooldowns,
            label="npc_state.cooldowns",
            allow_negative=False,
        )
        self.relationship_thresholds = self._normalize_int_mapping(
            self.relationship_thresholds,
            label="npc_state.relationship_thresholds",
        )
        self.player_reputation = self._normalize_int_mapping(
            self.player_reputation,
            label="npc_state.player_reputation",
        )
        self.story_arc_progression = self._normalize_any_mapping(
            self.story_arc_progression,
            label="npc_state.story_arc_progression",
        )
        self.special_flags = self._normalize_any_mapping(
            self.special_flags,
            label="npc_state.special_flags",
        )
        self.metadata = _coerce_metadata(self.metadata)
        return self

    @property
    def is_available(self) -> bool:
        return self.state not in {"locked", "cooldown"} and self.cooldown_days <= 0

    def has_completed_quest(self, quest_id: str) -> bool:
        validate_quest_id(quest_id)
        return quest_id in self.completed_quests

    def has_failed_quest(self, quest_id: str) -> bool:
        validate_quest_id(quest_id)
        return quest_id in self.failed_quests

    def is_chain_locked(self, chain_id: str) -> bool:
        validate_quest_id(chain_id)
        return chain_id in self.locked_chains

    def cooldown_for(self, quest_id: str) -> int:
        validate_quest_id(quest_id)
        return self.cooldowns.get(quest_id, 0)

    def register_available_quest(self, quest_id: str) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        self._add_unique(self.available_quests, quest_id)
        return self

    def register_available_quests(self, quest_ids: Sequence[str]) -> "QuestNPCState":
        for quest_id in quest_ids:
            self.register_available_quest(quest_id)
        return self

    def mark_quest_unavailable(self, quest_id: str) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        self._remove_value(self.available_quests, quest_id)
        return self

    def lock_chain(self, chain_id: str) -> "QuestNPCState":
        chain_id = validate_quest_id(chain_id)
        self._add_unique(self.locked_chains, chain_id)
        return self

    def unlock_chain(self, chain_id: str) -> "QuestNPCState":
        chain_id = validate_quest_id(chain_id)
        self._remove_value(self.locked_chains, chain_id)
        return self

    def set_cooldown(self, quest_id: str, days: int) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        if not isinstance(days, int):
            raise TypeError(f"Cooldown for {quest_id!r} must be an int, got {type(days)!r}")
        if days < 0:
            raise ValueError("Cooldown days cannot be negative")
        if days == 0:
            self.cooldowns.pop(quest_id, None)
        else:
            self.cooldowns[quest_id] = days
        return self

    def tick_cooldowns(self, days: int = 1) -> list[str]:
        if not isinstance(days, int):
            raise TypeError(f"days must be an int, got {type(days)!r}")
        if days < 0:
            raise ValueError("days cannot be negative")
        expired: list[str] = []
        if self.cooldown_days > 0:
            self.cooldown_days = max(self.cooldown_days - days, 0)
        for quest_id, remaining in list(self.cooldowns.items()):
            next_remaining = max(remaining - days, 0)
            if next_remaining <= 0:
                expired.append(quest_id)
                self.cooldowns.pop(quest_id, None)
            else:
                self.cooldowns[quest_id] = next_remaining
        if self.cooldown_days <= 0 and self.state == "cooldown":
            self.state = "available" if self.available_quests else "idle"
        return expired

    def set_relationship_threshold(self, key: str, value: int) -> "QuestNPCState":
        key = validate_quest_id(key)
        if not isinstance(value, int):
            raise TypeError(f"Relationship threshold {key!r} must be an int, got {type(value)!r}")
        self.relationship_thresholds[key] = value
        return self

    def set_player_reputation(self, key: str, value: int) -> "QuestNPCState":
        key = validate_quest_id(key)
        if not isinstance(value, int):
            raise TypeError(f"Player reputation {key!r} must be an int, got {type(value)!r}")
        self.player_reputation[key] = value
        return self

    def adjust_player_reputation(self, key: str, delta: int) -> "QuestNPCState":
        key = validate_quest_id(key)
        if not isinstance(delta, int):
            raise TypeError(f"Reputation delta for {key!r} must be an int, got {type(delta)!r}")
        self.player_reputation[key] = self.player_reputation.get(key, 0) + delta
        return self

    def advance_story_arc(self, arc_id: str, stage: Any = 1) -> "QuestNPCState":
        arc_id = validate_quest_id(arc_id)
        self.story_arc_progression[arc_id] = stage
        return self

    def set_special_flag(self, flag_id: str, value: Any = True) -> "QuestNPCState":
        flag_id = validate_quest_id(flag_id)
        self.special_flags[flag_id] = value
        return self

    def clear_special_flag(self, flag_id: str) -> "QuestNPCState":
        flag_id = validate_quest_id(flag_id)
        self.special_flags.pop(flag_id, None)
        return self

    def has_special_flag(self, flag_id: str) -> bool:
        flag_id = validate_quest_id(flag_id)
        return bool(self.special_flags.get(flag_id))

    def set_dialogue_mode(self, mode: str) -> "QuestNPCState":
        self.dialogue_mode = _validate_text("npc_state.dialogue_mode", mode)
        return self

    def resolved_dialogue_mode(
        self,
        event_type: str,
        quest_id: str = "",
        *,
        context: Mapping[str, Any] | None = None,
        default: str = "",
    ) -> str:
        event_type = _validate_text("npc_state.event_type", event_type)
        resolved_context = dict(context or {})
        for key in (
            f"{event_type}_dialogue_mode",
            f"{event_type}_dialogue_state",
            "dialogue_mode",
            "dialogue_state",
            "default_dialogue_mode",
            "default_dialogue_state",
        ):
            value = resolved_context.get(key, self.metadata.get(key))
            if isinstance(value, str) and value.strip():
                return value.strip()

        personality_modes = self.metadata.get("personality_dialogue_modes")
        if isinstance(personality_modes, Mapping) and self.personality:
            value = personality_modes.get(self.personality)
            if isinstance(value, str) and value.strip():
                return value.strip()

        if self.personality:
            personality_key = f"{self.personality}_{event_type}_dialogue_mode"
            value = resolved_context.get(personality_key, self.metadata.get(personality_key))
            if isinstance(value, str) and value.strip():
                return value.strip()

        if quest_id:
            quest_key = f"{quest_id}_{event_type}_dialogue_mode"
            value = resolved_context.get(quest_key, self.metadata.get(quest_key))
            if isinstance(value, str) and value.strip():
                return value.strip()

        if default:
            return _validate_text("npc_state.dialogue_mode", default)
        if self.dialogue_mode:
            return self.dialogue_mode
        return self.state

    def dialogue_context(
        self,
        quest_id: str = "",
        *,
        event_type: str = "",
        context: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        resolved_context = dict(context or {})
        resolved_context.update(self.metadata)
        resolved_context["npc_id"] = self.npc_id
        resolved_context["npc_state"] = self.state
        resolved_context["npc_state_snapshot"] = self.to_snapshot()
        resolved_context["dialogue_mode"] = self.resolved_dialogue_mode(
            event_type or self.state,
            quest_id,
            context=resolved_context,
        )
        resolved_context["personality"] = self.personality
        resolved_context["faction_alignment"] = self.faction_alignment
        resolved_context["available_quests"] = tuple(self.available_quests)
        resolved_context["completed_quests"] = tuple(self.completed_quests)
        resolved_context["failed_quests"] = tuple(self.failed_quests)
        resolved_context["locked_chains"] = tuple(self.locked_chains)
        resolved_context["cooldowns"] = dict(self.cooldowns)
        resolved_context["relationship_thresholds"] = dict(self.relationship_thresholds)
        resolved_context["player_reputation"] = dict(self.player_reputation)
        resolved_context["special_flags"] = dict(self.special_flags)
        resolved_context["story_arc_progression"] = dict(self.story_arc_progression)
        return resolved_context

    def mark_quest_offered(self, quest_id: str, *, dialogue_state: str | None = None) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        self.state = "offered"
        self.last_quest_id = quest_id
        self.register_available_quest(quest_id)
        if dialogue_state is not None:
            resolved_dialogue_state = _validate_text("npc_state.dialogue_state", dialogue_state)
            self.dialogue_state = resolved_dialogue_state
            self.dialogue_mode = resolved_dialogue_state
        return self

    def mark_quest_accepted(self, quest_id: str, *, dialogue_state: str | None = None) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        self.state = "engaged"
        self.last_quest_id = quest_id
        if dialogue_state is not None:
            resolved_dialogue_state = _validate_text("npc_state.dialogue_state", dialogue_state)
            self.dialogue_state = resolved_dialogue_state
            self.dialogue_mode = resolved_dialogue_state
        return self

    def mark_quest_completed(
        self,
        quest_id: str,
        *,
        cooldown_days: int = 0,
        unlock_quests: Sequence[str] = (),
        unlock_chains: Sequence[str] = (),
        lock_chains: Sequence[str] = (),
        reputation_changes: Mapping[str, int] | None = None,
        story_arc_updates: Mapping[str, Any] | None = None,
        special_flags: Mapping[str, Any] | None = None,
        dialogue_mode: str = "",
    ) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        self.state = "completed"
        self.last_quest_id = quest_id
        self._add_unique(self.completed_quests, quest_id)
        self._remove_value(self.failed_quests, quest_id)
        self._remove_value(self.available_quests, quest_id)
        self.set_cooldown(quest_id, cooldown_days)
        for item in unlock_quests:
            self.register_available_quest(item)
        for chain_id in unlock_chains:
            self.unlock_chain(chain_id)
        for chain_id in lock_chains:
            self.lock_chain(chain_id)
        if reputation_changes is not None:
            for key, delta in reputation_changes.items():
                self.adjust_player_reputation(key, delta)
        if story_arc_updates is not None:
            for arc_id, stage in story_arc_updates.items():
                self.advance_story_arc(arc_id, stage)
        if special_flags is not None:
            for flag_id, value in special_flags.items():
                self.set_special_flag(flag_id, value)
        if dialogue_mode:
            resolved_dialogue_mode = _validate_text("npc_state.dialogue_mode", dialogue_mode)
            self.dialogue_mode = resolved_dialogue_mode
            self.dialogue_state = resolved_dialogue_mode
        return self

    def mark_quest_failed(
        self,
        quest_id: str,
        *,
        cooldown_days: int = 0,
        lock_chains: Sequence[str] = (),
        reputation_changes: Mapping[str, int] | None = None,
        story_arc_updates: Mapping[str, Any] | None = None,
        special_flags: Mapping[str, Any] | None = None,
        dialogue_mode: str = "",
    ) -> "QuestNPCState":
        quest_id = validate_quest_id(quest_id)
        self.state = "failed"
        self.last_quest_id = quest_id
        self._add_unique(self.failed_quests, quest_id)
        self._remove_value(self.available_quests, quest_id)
        self.set_cooldown(quest_id, cooldown_days)
        for chain_id in lock_chains:
            self.lock_chain(chain_id)
        if reputation_changes is not None:
            for key, delta in reputation_changes.items():
                self.adjust_player_reputation(key, delta)
        if story_arc_updates is not None:
            for arc_id, stage in story_arc_updates.items():
                self.advance_story_arc(arc_id, stage)
        if special_flags is not None:
            for flag_id, value in special_flags.items():
                self.set_special_flag(flag_id, value)
        if dialogue_mode:
            resolved_dialogue_mode = _validate_text("npc_state.dialogue_mode", dialogue_mode)
            self.dialogue_mode = resolved_dialogue_mode
            self.dialogue_state = resolved_dialogue_mode
        return self

    def can_offer(
        self,
        quest_id: str,
        *,
        chain_id: str = "",
        context: Mapping[str, Any] | None = None,
    ) -> bool:
        quest_id = validate_quest_id(quest_id)
        context = dict(context or {})

        if self.state in {"locked", "cooldown"} and not context.get("ignore_state"):
            return False
        if self.cooldown_days > 0 and not context.get("ignore_cooldown"):
            return False
        if self.cooldown_for(quest_id) > 0 and not context.get("ignore_quest_cooldown"):
            return False
        if chain_id:
            chain_id = validate_quest_id(chain_id)
            if self.is_chain_locked(chain_id):
                return False

        if self.available_quests and quest_id not in self.available_quests and not context.get("allow_unlisted_offer"):
            return False
        if quest_id in self.completed_quests and not context.get("allow_repeat"):
            return False
        if quest_id in self.failed_quests and not context.get("allow_repeat"):
            return False

        required_dialogue_mode = context.get("required_dialogue_mode")
        if required_dialogue_mode and self.dialogue_mode != str(required_dialogue_mode).strip():
            return False

        required_alignment = context.get("required_faction_alignment")
        if required_alignment and self.faction_alignment != str(required_alignment).strip():
            return False

        required_flags = self._coerce_sequence(
            context.get("required_flags")
            or self.metadata.get("required_flags")
            or ()
        )
        blocked_flags = self._coerce_sequence(
            context.get("blocked_flags")
            or self.metadata.get("blocked_flags")
            or ()
        )
        for flag_id in required_flags:
            if not self.has_special_flag(flag_id):
                return False
        for flag_id in blocked_flags:
            if self.has_special_flag(flag_id):
                return False

        required_relationships = context.get("required_relationships")
        if required_relationships is None:
            required_relationships = self.relationship_thresholds
        if isinstance(required_relationships, Mapping):
            for key, threshold in required_relationships.items():
                if not isinstance(key, str):
                    return False
                validate_quest_id(key)
                if not isinstance(threshold, int):
                    return False
                if self.player_reputation.get(key, 0) < threshold:
                    return False

        required_reputation = context.get("required_reputation")
        if isinstance(required_reputation, Mapping):
            for key, threshold in required_reputation.items():
                if not isinstance(key, str):
                    return False
                validate_quest_id(key)
                if not isinstance(threshold, int):
                    return False
                if self.player_reputation.get(key, 0) < threshold:
                    return False

        required_story_arcs = context.get("required_story_arcs")
        if isinstance(required_story_arcs, Mapping):
            for arc_id, required_stage in required_story_arcs.items():
                if not isinstance(arc_id, str):
                    return False
                validate_quest_id(arc_id)
                current_stage = self.story_arc_progression.get(arc_id)
                if current_stage != required_stage:
                    return False
        elif required_story_arcs:
            for arc_id in self._coerce_sequence(required_story_arcs):
                if arc_id not in self.story_arc_progression:
                    return False

        return True

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "npc_id": self.npc_id,
            "state": self.state,
            "last_quest_id": self.last_quest_id,
            "cooldown_days": self.cooldown_days,
            "dialogue_state": self.dialogue_state,
            "available_quests": list(self.available_quests),
            "completed_quests": list(self.completed_quests),
            "failed_quests": list(self.failed_quests),
            "locked_chains": list(self.locked_chains),
            "cooldowns": dict(self.cooldowns),
            "relationship_thresholds": dict(self.relationship_thresholds),
            "faction_alignment": self.faction_alignment,
            "story_arc_progression": dict(self.story_arc_progression),
            "player_reputation": dict(self.player_reputation),
            "special_flags": dict(self.special_flags),
            "dialogue_mode": self.dialogue_mode,
            "personality": self.personality,
            "metadata": dict(self.metadata),
        }
@dataclass
class QuestWorldContext:
    context_id: str
    location_id: str = ""
    center_id: str = ""
    party_id: str = ""
    faction_id: str = ""
    region: str = ""
    day: int | None = None
    turn: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestWorldContext":
        validate_quest_id(self.context_id)
        if self.location_id:
            _validate_text("world_context.location_id", self.location_id)
        if self.center_id:
            _validate_text("world_context.center_id", self.center_id)
        if self.party_id:
            _validate_text("world_context.party_id", self.party_id)
        if self.faction_id:
            _validate_text("world_context.faction_id", self.faction_id)
        if self.region:
            _validate_text("world_context.region", self.region)
        _validate_optional_int("world_context.day", self.day)
        _validate_optional_int("world_context.turn", self.turn)
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def is_location_bound(self) -> bool:
        return any(
            value != ""
            for value in (self.location_id, self.center_id, self.party_id, self.region)
        )

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "location_id": self.location_id,
            "center_id": self.center_id,
            "party_id": self.party_id,
            "faction_id": self.faction_id,
            "region": self.region,
            "day": self.day,
            "turn": self.turn,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestBattleObjective:
    objective_id: str
    action_kind: str
    target_troop_id: str = ""
    target_party_id: str = ""
    target_center_id: str = ""
    required_count: int = 1
    progress: int = 0
    timer_start: int | None = None
    timer_duration: int = 0
    wave_index: int = 0
    failure_state: str = ""
    required_payload_keys: tuple[str, ...] = ()
    success_message: str = ""
    failure_message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestBattleObjective":
        validate_quest_id(self.objective_id)
        self.action_kind = normalize_battle_objective_action_kind(self.action_kind)
        _validate_optional_text("battle_objective.target_troop_id", self.target_troop_id)
        _validate_optional_text("battle_objective.target_party_id", self.target_party_id)
        _validate_optional_text("battle_objective.target_center_id", self.target_center_id)
        if not isinstance(self.required_count, int):
            raise TypeError(
                f"battle_objective.required_count must be an int, got {type(self.required_count)!r}"
            )
        if self.required_count < 1:
            raise ValueError("battle_objective.required_count must be at least 1")
        if not isinstance(self.progress, int):
            raise TypeError(f"battle_objective.progress must be an int, got {type(self.progress)!r}")
        if self.progress < 0:
            raise ValueError("battle_objective.progress cannot be negative")
        _validate_optional_int("battle_objective.timer_start", self.timer_start)
        if not isinstance(self.timer_duration, int):
            raise TypeError(
                f"battle_objective.timer_duration must be an int, got {type(self.timer_duration)!r}"
            )
        if self.timer_duration < 0:
            raise ValueError("battle_objective.timer_duration cannot be negative")
        if not isinstance(self.wave_index, int):
            raise TypeError(f"battle_objective.wave_index must be an int, got {type(self.wave_index)!r}")
        if self.wave_index < 0:
            raise ValueError("battle_objective.wave_index cannot be negative")
        if self.failure_state:
            _validate_text("battle_objective.failure_state", self.failure_state)
        if not self.required_payload_keys:
            self.required_payload_keys = QUEST_BATTLE_OBJECTIVE_REQUIRED_PAYLOAD_KEYS.get(
                self.action_kind,
                (),
            )
        self.required_payload_keys = tuple(
            _validate_text("battle_objective.required_payload_keys", key).strip()
            for key in self.required_payload_keys
        )
        if not self.success_message:
            self.success_message = QUEST_BATTLE_OBJECTIVE_MESSAGE_TEMPLATES[self.action_kind]["success"]
        if not self.failure_message:
            self.failure_message = QUEST_BATTLE_OBJECTIVE_MESSAGE_TEMPLATES[self.action_kind]["failure"]
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "objective_id": self.objective_id,
            "action_kind": self.action_kind,
            "target_troop_id": self.target_troop_id,
            "target_party_id": self.target_party_id,
            "target_center_id": self.target_center_id,
            "required_count": self.required_count,
            "progress": self.progress,
            "timer_start": self.timer_start,
            "timer_duration": self.timer_duration,
            "wave_index": self.wave_index,
            "failure_state": self.failure_state,
            "required_payload_keys": list(self.required_payload_keys),
            "success_message": self.success_message,
            "failure_message": self.failure_message,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestStage:
    """
    Structured stage information for multi-step quest authoring.

    Stages can hold both raw compatibility fields and structured domain objects.
    The helper constructors normalize strings into structured objects so build-
    time lowering can stay declarative while the legacy compiler output stays
    intact.
    """

    stage_id: str
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
    battle_objective: QuestBattleObjective | None = None

    def normalized_battle_objective(self) -> QuestBattleObjective | None:
        if self.battle_objective is None:
            return None
        return self.battle_objective.validate()

    def normalized_conditions(self) -> tuple[QuestCondition, ...]:
        return tuple(
            _coerce_condition_item(condition, self.stage_id, index)
            for index, condition in enumerate(self.conditions, start=1)
        )

    def normalized_actions(self) -> tuple[QuestAction, ...]:
        return tuple(
            _coerce_action_item(action, self.stage_id, index)
            for index, action in enumerate(self.actions, start=1)
        )

    def normalized_triggers(self) -> tuple[QuestTrigger, ...]:
        structured_triggers = tuple(
            _coerce_trigger_item(trigger, self.stage_id, index)
            for index, trigger in enumerate(self.triggers, start=1)
        )
        compatibility_triggers = tuple(
            quest_trigger(f"{self.stage_id}_battle_hook_{index}", battle_hook)
            for index, battle_hook in enumerate(self.battle_hooks, start=1)
        )
        return structured_triggers + compatibility_triggers

    def normalized_rewards(self) -> tuple[QuestReward, ...]:
        return tuple(
            _coerce_reward_item(reward, self.stage_id, index)
            for index, reward in enumerate(self.rewards, start=1)
        )

    def normalized_failures(self) -> tuple[QuestFailure, ...]:
        return tuple(
            _coerce_failure_item(failure, self.stage_id, index)
            for index, failure in enumerate(self.failures, start=1)
        )

    def normalized_transitions(self) -> dict[str, str]:
        return _validate_transition_map("stage.transitions", self.transitions)

    def matches_hook(self, hook_name: str) -> bool:
        if hook_name in self.battle_hooks:
            return True
        for trigger in self.normalized_triggers():
            if trigger.matches(hook_name):
                return True
        return False

    def matches_action(self, action_name: str) -> bool:
        for action in self.normalized_actions():
            if action.expression == action_name or action.action_id == action_name:
                return True
        battle_objective = self.normalized_battle_objective()
        if battle_objective is not None and battle_objective.action_kind == action_name:
            return True
        return False

    def validate(self) -> "QuestStage":
        validate_quest_id(self.stage_id)
        _validate_text("stage.title", self.title)
        _validate_text("stage.objective", self.objective)
        if self.description:
            _validate_text("stage.description", self.description)
        for hook_name in self.battle_hooks:
            _validate_text("stage.battle_hook", hook_name)
        for condition in self.normalized_conditions():
            condition.validate()
        for action in self.normalized_actions():
            action.validate()
        for trigger in self.normalized_triggers():
            trigger.validate()
        for reward in self.normalized_rewards():
            reward.validate()
        for failure in self.normalized_failures():
            failure.validate()
        self.battle_objective = self.normalized_battle_objective()
        self.transitions = _validate_transition_map("stage.transitions", self.transitions)
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "title": self.title,
            "objective": self.objective,
            "description": self.description,
            "conditions": [condition.to_snapshot() for condition in self.normalized_conditions()],
            "actions": [action.to_snapshot() for action in self.normalized_actions()],
            "battle_hooks": list(self.battle_hooks),
            "triggers": [trigger.to_snapshot() for trigger in self.normalized_triggers()],
            "rewards": [reward.to_snapshot() for reward in self.normalized_rewards()],
            "failures": [failure.to_snapshot() for failure in self.normalized_failures()],
            "transitions": dict(self.normalized_transitions()),
            "battle_objective": self.normalized_battle_objective().to_snapshot() if self.normalized_battle_objective() else None,
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestTemplate:
    """
    Structured quest definition that can be serialized into the legacy tuple
    layout or kept as a richer authoring object for future build steps.
    """

    quest_id: str
    name: str
    flags: Any
    description: str
    stages: tuple[QuestStage | str, ...] = ()
    conditions: tuple[QuestCondition | str, ...] = ()
    actions: tuple[QuestAction | str, ...] = ()
    triggers: tuple[QuestTrigger | str, ...] = ()
    rewards: tuple[QuestReward | str, ...] = ()
    failures: tuple[QuestFailure | str, ...] = ()
    transitions: dict[str, str] = field(default_factory=dict)
    npc_state: QuestNPCState | None = None
    world_context: QuestWorldContext | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_stages(self) -> tuple[QuestStage, ...]:
        return tuple(
            _coerce_stage_item(stage, self.quest_id, index)
            for index, stage in enumerate(self.stages, start=1)
        )

    def normalized_conditions(self) -> tuple[QuestCondition, ...]:
        return tuple(
            _coerce_condition_item(condition, self.quest_id, index)
            for index, condition in enumerate(self.conditions, start=1)
        )

    def normalized_actions(self) -> tuple[QuestAction, ...]:
        return tuple(
            _coerce_action_item(action, self.quest_id, index)
            for index, action in enumerate(self.actions, start=1)
        )

    def normalized_triggers(self) -> tuple[QuestTrigger, ...]:
        return tuple(
            _coerce_trigger_item(trigger, self.quest_id, index)
            for index, trigger in enumerate(self.triggers, start=1)
        )

    def normalized_rewards(self) -> tuple[QuestReward, ...]:
        return tuple(
            _coerce_reward_item(reward, self.quest_id, index)
            for index, reward in enumerate(self.rewards, start=1)
        )

    def normalized_failures(self) -> tuple[QuestFailure, ...]:
        return tuple(
            _coerce_failure_item(failure, self.quest_id, index)
            for index, failure in enumerate(self.failures, start=1)
        )

    def normalized_transitions(self) -> dict[str, str]:
        return _validate_transition_map("quest.transitions", self.transitions)

    def matches_hook(self, hook_name: str) -> bool:
        for trigger in self.normalized_triggers():
            if trigger.matches(hook_name):
                return True
        return False

    def matches_action(self, action_name: str) -> bool:
        for action in self.normalized_actions():
            if action.expression == action_name or action.action_id == action_name:
                return True
        return False

    def validate(self) -> "QuestTemplate":
        validate_quest_id(self.quest_id)
        _validate_text("quest.name", self.name)
        _validate_text("quest.description", self.description)
        for stage in self.normalized_stages():
            stage.validate()
        ensure_unique_stage_ids(self.normalized_stages(), quest_id=self.quest_id)
        for condition in self.normalized_conditions():
            condition.validate()
        for action in self.normalized_actions():
            action.validate()
        for trigger in self.normalized_triggers():
            trigger.validate()
        for reward in self.normalized_rewards():
            reward.validate()
        for failure in self.normalized_failures():
            failure.validate()
        self.transitions = _validate_transition_map("quest.transitions", self.transitions)
        if self.npc_state is not None:
            self.npc_state.validate()
        if self.world_context is not None:
            self.world_context.validate()
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def as_legacy_tuple(self) -> tuple[str, str, Any, str]:
        """
        Return the current four-field quest tuple expected by the compiler.
        """
        self.validate()
        return (self.quest_id, self.name, self.flags, self.description)

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "quest_id": self.quest_id,
            "name": self.name,
            "flags": self.flags,
            "description": self.description,
            "stages": [stage.to_snapshot() for stage in self.normalized_stages()],
            "conditions": [condition.to_snapshot() for condition in self.normalized_conditions()],
            "actions": [action.to_snapshot() for action in self.normalized_actions()],
            "triggers": [trigger.to_snapshot() for trigger in self.normalized_triggers()],
            "rewards": [reward.to_snapshot() for reward in self.normalized_rewards()],
            "failures": [failure.to_snapshot() for failure in self.normalized_failures()],
            "transitions": dict(self.normalized_transitions()),
            "npc_state": self.npc_state.to_snapshot() if self.npc_state else None,
            "world_context": self.world_context.to_snapshot() if self.world_context else None,
            "metadata": dict(self.metadata),
        }


QuestBlueprint = QuestTemplate


@dataclass
class QuestOffer:
    offer_id: str
    template: QuestTemplate | None = None
    quest_id: str = ""
    giver_id: str = ""
    title: str = ""
    summary: str = ""
    conditions: tuple[QuestCondition | str, ...] = ()
    actions: tuple[QuestAction | str, ...] = ()
    triggers: tuple[QuestTrigger | str, ...] = ()
    rewards: tuple[QuestReward | str, ...] = ()
    failures: tuple[QuestFailure | str, ...] = ()
    npc_state: QuestNPCState | None = None
    world_context: QuestWorldContext | None = None
    expires_in_days: int = 0
    transitions: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def effective_quest_id(self) -> str:
        if self.quest_id:
            return self.quest_id
        if self.template is not None:
            return self.template.quest_id
        return ""

    @property
    def effective_title(self) -> str:
        if self.title:
            return self.title
        if self.template is not None:
            return self.template.name
        return ""

    @property
    def effective_summary(self) -> str:
        if self.summary:
            return self.summary
        if self.template is not None:
            return self.template.description
        return ""

    def offer_context(self, extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
        context: dict[str, Any] = {}
        if self.template is not None:
            context.update(dict(self.template.metadata))
            context["template_quest_id"] = self.template.quest_id
            context["template_name"] = self.template.name
            context["template_flags"] = self.template.flags
            context["template_description"] = self.template.description
            context["template_snapshot"] = self.template.to_snapshot()
            if self.template.npc_state is not None:
                context["template_npc_state"] = self.template.npc_state.to_snapshot()
            if self.template.world_context is not None:
                context["template_world_context"] = self.template.world_context.to_snapshot()
        if self.npc_state is not None:
            context["npc_state"] = self.npc_state.to_snapshot()
            context["npc_dialogue_mode"] = self.npc_state.dialogue_mode
            context["npc_dialogue_state"] = self.npc_state.dialogue_state
            context["npc_personality"] = self.npc_state.personality
        if self.world_context is not None:
            context["world_context"] = self.world_context.to_snapshot()
        context.update(dict(self.metadata))
        context["offer_id"] = self.offer_id
        context["quest_id"] = self.effective_quest_id
        context["giver_id"] = self.giver_id
        context["title"] = self.effective_title
        context["summary"] = self.effective_summary
        context["expires_in_days"] = self.expires_in_days
        context["transitions"] = dict(self.normalized_transitions())
        if extra:
            context.update(dict(extra))
        return context

    def conditions_met(
        self,
        context: Mapping[str, Any] | None = None,
        *,
        resolver: Any = None,
    ) -> bool:
        evaluation_context = self.offer_context(context)

        def lookup(source: Mapping[str, Any], key: str) -> Any:
            if key in source:
                return source[key]
            value: Any = source
            for part in key.split("."):
                if isinstance(value, Mapping) and part in value:
                    value = value[part]
                else:
                    return None
            return value

        resolver_fn = resolver if callable(resolver) else None
        for condition in self.normalized_conditions():
            expression = condition.expression.strip()
            if not expression:
                return False

            if resolver_fn is not None:
                try:
                    if resolver_fn(expression, evaluation_context):
                        continue
                except Exception:
                    return False

            lowered = expression.lower()
            if lowered in {"true", "yes", "on"}:
                continue
            if lowered in {"false", "no", "off"}:
                return False

            value = lookup(evaluation_context, expression)
            if value is None:
                metadata = evaluation_context.get("metadata", {})
                if isinstance(metadata, Mapping):
                    value = lookup(metadata, expression)

            if expression.startswith("!"):
                target = expression[1:].strip()
                if lookup(evaluation_context, target):
                    return False
                continue

            if "=" in expression and "==" not in expression:
                lhs, rhs = expression.split("=", 1)
                lhs_value = lookup(evaluation_context, lhs.strip())
                if lhs_value is None and isinstance(evaluation_context.get("metadata"), Mapping):
                    lhs_value = lookup(evaluation_context["metadata"], lhs.strip())
                if lhs_value is None or str(lhs_value) != rhs.strip().strip("'\""):
                    return False
                continue

            if not value:
                return False

        return True

    def can_be_offered_by(
        self,
        npc_state: QuestNPCState | None = None,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> bool:
        active_npc_state = npc_state or self.npc_state
        if active_npc_state is None:
            return False
        try:
            active_npc_state.validate()
        except Exception:
            return False
        if self.npc_state is not None and self.npc_state.npc_id != active_npc_state.npc_id:
            return False

        offer_context = self.offer_context(context)
        if self.giver_id and self.giver_id != active_npc_state.npc_id and not bool(
            offer_context.get("allow_cross_giver", False)
        ):
            return False
        if not self.conditions_met(offer_context, resolver=offer_context.get("condition_resolver")):
            return False

        quest_id = self.effective_quest_id or self.quest_id
        if quest_id and not active_npc_state.can_offer(
            quest_id,
            chain_id=str(offer_context.get("chain_id", offer_context.get("quest_chain_id", "")) or ""),
            context=offer_context,
        ):
            return False
        return True

    def apply_offer_to_npc(
        self,
        npc_state: QuestNPCState | None = None,
        *,
        context: Mapping[str, Any] | None = None,
        dialogue_state: str | None = None,
    ) -> QuestNPCState:
        active_npc_state = npc_state or self.npc_state
        if active_npc_state is None:
            raise ValueError("QuestOffer requires an NPC state to apply an offer.")
        offer_context = self.offer_context(context)
        quest_id = self.effective_quest_id or self.quest_id
        if not quest_id:
            raise ValueError("QuestOffer requires a quest_id or template to apply to NPC state.")
        if not self.can_be_offered_by(active_npc_state, context=offer_context):
            raise RuntimeError(f"QuestOffer {self.offer_id!r} cannot be applied to NPC {active_npc_state.npc_id!r}.")
        resolved_dialogue_state = dialogue_state or active_npc_state.resolved_dialogue_mode(
            "offer",
            quest_id,
            context=offer_context,
        )
        active_npc_state.mark_quest_offered(quest_id, dialogue_state=resolved_dialogue_state)
        active_npc_state.dialogue_state = resolved_dialogue_state
        return active_npc_state

    def apply_acceptance_to_npc(
        self,
        npc_state: QuestNPCState | None = None,
        *,
        context: Mapping[str, Any] | None = None,
        dialogue_state: str | None = None,
    ) -> QuestNPCState:
        active_npc_state = npc_state or self.npc_state
        if active_npc_state is None:
            raise ValueError("QuestOffer requires an NPC state to apply acceptance.")
        offer_context = self.offer_context(context)
        quest_id = self.effective_quest_id or self.quest_id
        if not quest_id:
            raise ValueError("QuestOffer requires a quest_id or template to apply to NPC state.")
        resolved_dialogue_state = dialogue_state or active_npc_state.resolved_dialogue_mode(
            "accept",
            quest_id,
            context=offer_context,
        )
        active_npc_state.mark_quest_accepted(quest_id, dialogue_state=resolved_dialogue_state)
        active_npc_state.dialogue_state = resolved_dialogue_state
        return active_npc_state

    def apply_completion_to_npc(
        self,
        npc_state: QuestNPCState | None = None,
        *,
        context: Mapping[str, Any] | None = None,
        quest_id: str = "",
        cooldown_days: int | None = None,
        dialogue_mode: str = "",
    ) -> QuestNPCState:
        active_npc_state = npc_state or self.npc_state
        if active_npc_state is None:
            raise ValueError("QuestOffer requires an NPC state to apply completion.")
        offer_context = self.offer_context(context)
        active_quest_id = validate_quest_id(quest_id or self.effective_quest_id or self.quest_id)
        if not active_quest_id:
            raise ValueError("QuestOffer requires a quest_id or template to apply to NPC state.")

        cooldown_value = cooldown_days
        if cooldown_value is None:
            cooldown_value = offer_context.get("cooldown_days", offer_context.get("quest_cooldown_days", 0))
        try:
            cooldown_days_value = int(cooldown_value)
        except (TypeError, ValueError):
            cooldown_days_value = 0

        unlock_quests = active_npc_state._coerce_sequence(
            offer_context.get("unlock_quests") or offer_context.get("followup_quests") or ()
        )
        lock_quests = active_npc_state._coerce_sequence(
            offer_context.get("lock_quests") or offer_context.get("blocked_quests") or ()
        )
        unlock_chains = active_npc_state._coerce_sequence(offer_context.get("unlock_chains") or ())
        lock_chains = active_npc_state._coerce_sequence(offer_context.get("lock_chains") or ())
        reputation_changes = offer_context.get("reputation_changes")
        story_arc_updates = offer_context.get("story_arc_updates")
        special_flags = offer_context.get("special_flags")
        resolved_dialogue_state = dialogue_mode or active_npc_state.resolved_dialogue_mode(
            "complete",
            active_quest_id,
            context=offer_context,
        )

        active_npc_state.mark_quest_completed(
            active_quest_id,
            cooldown_days=cooldown_days_value,
            unlock_quests=unlock_quests,
            unlock_chains=unlock_chains,
            lock_chains=lock_chains,
            reputation_changes=reputation_changes if isinstance(reputation_changes, Mapping) else None,
            story_arc_updates=story_arc_updates if isinstance(story_arc_updates, Mapping) else None,
            special_flags=special_flags if isinstance(special_flags, Mapping) else None,
            dialogue_mode=resolved_dialogue_state,
        )
        active_npc_state.dialogue_state = resolved_dialogue_state
        for blocked_quest_id in lock_quests:
            active_npc_state.mark_quest_unavailable(blocked_quest_id)
        return active_npc_state

    def apply_failure_to_npc(
        self,
        npc_state: QuestNPCState | None = None,
        *,
        context: Mapping[str, Any] | None = None,
        quest_id: str = "",
        cooldown_days: int | None = None,
        dialogue_mode: str = "",
    ) -> QuestNPCState:
        active_npc_state = npc_state or self.npc_state
        if active_npc_state is None:
            raise ValueError("QuestOffer requires an NPC state to apply failure.")
        offer_context = self.offer_context(context)
        active_quest_id = validate_quest_id(quest_id or self.effective_quest_id or self.quest_id)
        if not active_quest_id:
            raise ValueError("QuestOffer requires a quest_id or template to apply to NPC state.")

        cooldown_value = cooldown_days
        if cooldown_value is None:
            cooldown_value = offer_context.get("cooldown_days", offer_context.get("quest_cooldown_days", 0))
        try:
            cooldown_days_value = int(cooldown_value)
        except (TypeError, ValueError):
            cooldown_days_value = 0

        lock_quests = active_npc_state._coerce_sequence(
            offer_context.get("lock_quests") or offer_context.get("blocked_quests") or ()
        )
        lock_chains = active_npc_state._coerce_sequence(offer_context.get("lock_chains") or ())
        reputation_changes = offer_context.get("reputation_changes")
        story_arc_updates = offer_context.get("story_arc_updates")
        special_flags = offer_context.get("special_flags")
        resolved_dialogue_state = dialogue_mode or active_npc_state.resolved_dialogue_mode(
            "fail",
            active_quest_id,
            context=offer_context,
        )

        active_npc_state.mark_quest_failed(
            active_quest_id,
            cooldown_days=cooldown_days_value,
            lock_chains=lock_chains,
            reputation_changes=reputation_changes if isinstance(reputation_changes, Mapping) else None,
            story_arc_updates=story_arc_updates if isinstance(story_arc_updates, Mapping) else None,
            special_flags=special_flags if isinstance(special_flags, Mapping) else None,
            dialogue_mode=resolved_dialogue_state,
        )
        active_npc_state.dialogue_state = resolved_dialogue_state
        for blocked_quest_id in lock_quests:
            active_npc_state.mark_quest_unavailable(blocked_quest_id)
        return active_npc_state

    def normalized_conditions(self) -> tuple[QuestCondition, ...]:
        return tuple(
            _coerce_condition_item(condition, self.offer_id, index)
            for index, condition in enumerate(self.conditions, start=1)
        )

    def normalized_actions(self) -> tuple[QuestAction, ...]:
        return tuple(
            _coerce_action_item(action, self.offer_id, index)
            for index, action in enumerate(self.actions, start=1)
        )

    def normalized_triggers(self) -> tuple[QuestTrigger, ...]:
        return tuple(
            _coerce_trigger_item(trigger, self.offer_id, index)
            for index, trigger in enumerate(self.triggers, start=1)
        )

    def normalized_rewards(self) -> tuple[QuestReward, ...]:
        return tuple(
            _coerce_reward_item(reward, self.offer_id, index)
            for index, reward in enumerate(self.rewards, start=1)
        )

    def normalized_failures(self) -> tuple[QuestFailure, ...]:
        return tuple(
            _coerce_failure_item(failure, self.offer_id, index)
            for index, failure in enumerate(self.failures, start=1)
        )

    def normalized_transitions(self) -> dict[str, str]:
        return _validate_transition_map("offer.transitions", self.transitions)

    def validate(self) -> "QuestOffer":
        validate_quest_id(self.offer_id)
        if self.template is None and not self.quest_id:
            raise ValueError("QuestOffer requires either quest_id or template")
        if self.quest_id:
            validate_quest_id(self.quest_id)
        if self.template is not None:
            self.template.validate()
            if self.quest_id and self.quest_id != self.template.quest_id:
                raise ValueError(
                    f"QuestOffer {self.offer_id!r} quest_id {self.quest_id!r} does not match "
                    f"template quest_id {self.template.quest_id!r}"
                )
        if self.giver_id:
            validate_quest_id(self.giver_id)
        if self.title:
            _validate_text("offer.title", self.title)
        if self.summary:
            _validate_text("offer.summary", self.summary)
        for condition in self.normalized_conditions():
            condition.validate()
        for action in self.normalized_actions():
            action.validate()
        for trigger in self.normalized_triggers():
            trigger.validate()
        for reward in self.normalized_rewards():
            reward.validate()
        for failure in self.normalized_failures():
            failure.validate()
        self.transitions = _validate_transition_map("offer.transitions", self.transitions)
        if self.npc_state is not None:
            self.npc_state.validate()
        if self.world_context is not None:
            self.world_context.validate()
        if not isinstance(self.expires_in_days, int):
            raise TypeError(
                f"offer.expires_in_days must be an int, got {type(self.expires_in_days)!r}"
            )
        if self.expires_in_days < 0:
            raise ValueError("offer.expires_in_days cannot be negative")
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def to_snapshot(self) -> dict[str, Any]:
        return {
            "offer_id": self.offer_id,
            "quest_id": self.effective_quest_id,
            "giver_id": self.giver_id,
            "title": self.effective_title,
            "summary": self.effective_summary,
            "conditions": [condition.to_snapshot() for condition in self.normalized_conditions()],
            "actions": [action.to_snapshot() for action in self.normalized_actions()],
            "triggers": [trigger.to_snapshot() for trigger in self.normalized_triggers()],
            "rewards": [reward.to_snapshot() for reward in self.normalized_rewards()],
            "failures": [failure.to_snapshot() for failure in self.normalized_failures()],
            "npc_state": self.npc_state.to_snapshot() if self.npc_state else None,
            "world_context": self.world_context.to_snapshot() if self.world_context else None,
            "expires_in_days": self.expires_in_days,
            "transitions": dict(self.normalized_transitions()),
            "template": (
                {
                    "quest_id": self.template.quest_id,
                    "name": self.template.name,
                }
                if self.template is not None
                else None
            ),
            "metadata": dict(self.metadata),
        }


@dataclass
class QuestChain:
    """
    Higher-level container for linked quest templates.

    This keeps chain metadata, the entry quest, and branch layout separate from
    the authored quest objects themselves so future build steps can lower the
    structure into engine-specific script output without forcing runtime code to
    understand tuples.
    """

    chain_id: str
    title: str
    quests: tuple[QuestTemplate | str, ...] = ()
    entry_quest_id: str = ""
    branches: dict[str, tuple[str, ...]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_quests(self) -> tuple[QuestTemplate, ...]:
        return tuple(
            _coerce_template_item(quest, self.chain_id, index)
            for index, quest in enumerate(self.quests, start=1)
        )

    def validate(self) -> "QuestChain":
        validate_quest_id(self.chain_id)
        _validate_text("chain.title", self.title)
        normalized_quests = self.normalized_quests()
        for quest in normalized_quests:
            quest.validate()
        ensure_unique_quest_ids(normalized_quests)
        if self.entry_quest_id:
            validate_quest_id(self.entry_quest_id)
            if self.entry_quest_id not in {quest.quest_id for quest in normalized_quests}:
                raise ValueError(
                    f"entry_quest_id {self.entry_quest_id!r} is not present in chain {self.chain_id!r}"
                )
        validated_branches: dict[str, tuple[str, ...]] = {}
        quest_ids = {quest.quest_id for quest in normalized_quests}
        for branch_name, branch_quests in self.branches.items():
            _validate_text("chain.branch_name", branch_name)
            if not isinstance(branch_quests, tuple):
                branch_quests = tuple(branch_quests)
            validated_branch: list[str] = []
            for quest_id in branch_quests:
                validate_quest_id(quest_id)
                if quest_id not in quest_ids:
                    raise ValueError(
                        f"Branch {branch_name!r} in chain {self.chain_id!r} references unknown "
                        f"quest id {quest_id!r}"
                    )
                validated_branch.append(quest_id)
            validated_branches[branch_name] = tuple(validated_branch)
        self.branches = validated_branches
        self.metadata = _coerce_metadata(self.metadata)
        return self

    def as_legacy_tuples(self) -> list[tuple[str, str, Any, str]]:
        self.validate()
        return [quest.as_legacy_tuple() for quest in self.normalized_quests()]

    @property
    def templates(self) -> tuple[QuestTemplate | str, ...]:
        return self.quests

    def to_snapshot(self) -> dict[str, Any]:
        normalized_quests = self.normalized_quests()
        return {
            "chain_id": self.chain_id,
            "title": self.title,
            "entry_quest_id": self.entry_quest_id,
            "quests": [quest.to_snapshot() for quest in normalized_quests],
            "branches": {key: list(value) for key, value in self.branches.items()},
            "metadata": dict(self.metadata),
        }


def _coerce_template_item(
    value: "QuestTemplate | str",
    prefix: str,
    index: int,
) -> QuestTemplate:
    if isinstance(value, QuestTemplate):
        return value.validate()
    if isinstance(value, str):
        return quest_template(
            f"{prefix}_quest_{index}",
            value,
            None,
            value,
        )
    raise TypeError(
        f"Expected QuestTemplate or str for {prefix} quest, got {type(value)!r}"
    )


def quest_condition(
    condition_id: str,
    expression: str,
    *,
    description: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestCondition:
    return QuestCondition(
        condition_id=validate_quest_id(condition_id),
        expression=_validate_text("condition.expression", expression),
        description=description,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_action(
    action_id: str,
    expression: str,
    *,
    description: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestAction:
    return QuestAction(
        action_id=validate_quest_id(action_id),
        expression=_validate_text("action.expression", expression),
        description=description,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_reward(
    reward_id: str,
    expression: str,
    *,
    description: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestReward:
    return QuestReward(
        reward_id=validate_quest_id(reward_id),
        expression=_validate_text("reward.expression", expression),
        description=description,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_failure(
    failure_id: str,
    expression: str,
    *,
    description: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestFailure:
    return QuestFailure(
        failure_id=validate_quest_id(failure_id),
        expression=_validate_text("failure.expression", expression),
        description=description,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_trigger(
    trigger_id: str,
    event_name: str,
    *,
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    description: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestTrigger:
    return QuestTrigger(
        trigger_id=validate_quest_id(trigger_id),
        event_name=_validate_text("trigger.event_name", event_name),
        conditions=tuple(conditions),
        actions=tuple(actions),
        description=description,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_npc_state(
    npc_id: str,
    *,
    state: str = "idle",
    last_quest_id: str = "",
    cooldown_days: int = 0,
    dialogue_state: str = "",
    available_quests: Sequence[str] = (),
    completed_quests: Sequence[str] = (),
    failed_quests: Sequence[str] = (),
    locked_chains: Sequence[str] = (),
    cooldowns: Mapping[str, int] | None = None,
    relationship_thresholds: Mapping[str, int] | None = None,
    faction_alignment: str = "",
    story_arc_progression: Mapping[str, Any] | None = None,
    player_reputation: Mapping[str, int] | None = None,
    special_flags: Mapping[str, Any] | None = None,
    dialogue_mode: str = "",
    personality: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestNPCState:
    return QuestNPCState(
        npc_id=validate_quest_id(npc_id),
        state=_validate_text("npc_state.state", state),
        last_quest_id=last_quest_id,
        cooldown_days=cooldown_days,
        dialogue_state=dialogue_state,
        available_quests=list(available_quests),
        completed_quests=list(completed_quests),
        failed_quests=list(failed_quests),
        locked_chains=list(locked_chains),
        cooldowns=dict(cooldowns or {}),
        relationship_thresholds=dict(relationship_thresholds or {}),
        faction_alignment=faction_alignment,
        story_arc_progression=dict(story_arc_progression or {}),
        player_reputation=dict(player_reputation or {}),
        special_flags=dict(special_flags or {}),
        dialogue_mode=dialogue_mode,
        personality=personality,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_world_context(
    context_id: str,
    *,
    location_id: str = "",
    center_id: str = "",
    party_id: str = "",
    faction_id: str = "",
    region: str = "",
    day: int | None = None,
    turn: int | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestWorldContext:
    return QuestWorldContext(
        context_id=validate_quest_id(context_id),
        location_id=location_id,
        center_id=center_id,
        party_id=party_id,
        faction_id=faction_id,
        region=region,
        day=day,
        turn=turn,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_battle_objective(
    objective_id: str,
    action_kind: str,
    *,
    target_troop_id: str = "",
    target_party_id: str = "",
    target_center_id: str = "",
    required_count: int = 1,
    progress: int = 0,
    timer_start: int | None = None,
    timer_duration: int = 0,
    wave_index: int = 0,
    failure_state: str = "",
    required_payload_keys: Sequence[str] = (),
    success_message: str = "",
    failure_message: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> QuestBattleObjective:
    return QuestBattleObjective(
        objective_id=validate_quest_id(objective_id),
        action_kind=action_kind,
        target_troop_id=target_troop_id,
        target_party_id=target_party_id,
        target_center_id=target_center_id,
        required_count=required_count,
        progress=progress,
        timer_start=timer_start,
        timer_duration=timer_duration,
        wave_index=wave_index,
        failure_state=failure_state,
        required_payload_keys=tuple(required_payload_keys),
        success_message=success_message,
        failure_message=failure_message,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_stage(
    stage_id: str,
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
    battle_objective: QuestBattleObjective | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestStage:
    stage_id = validate_quest_id(stage_id)
    return QuestStage(
        stage_id=stage_id,
        title=_validate_text("stage.title", title),
        objective=_validate_text("stage.objective", objective),
        description=description,
        conditions=tuple(conditions),
        actions=tuple(actions),
        battle_hooks=tuple(battle_hooks),
        triggers=tuple(triggers),
        rewards=tuple(rewards),
        failures=tuple(failures),
        transitions=dict(transitions or {}),
        battle_objective=battle_objective,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_template(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    stages: Sequence[QuestStage | str] = (),
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestTemplate:
    quest_id = validate_quest_id(quest_id)
    return QuestTemplate(
        quest_id=quest_id,
        name=_validate_text("quest.name", name),
        flags=flags,
        description=_validate_text("quest.description", description),
        stages=tuple(stages),
        conditions=tuple(conditions),
        actions=tuple(actions),
        triggers=tuple(triggers),
        rewards=tuple(rewards),
        failures=tuple(failures),
        transitions=dict(transitions or {}),
        npc_state=npc_state,
        world_context=world_context,
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_blueprint(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    stages: Sequence[QuestStage | str] = (),
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestTemplate:
    return quest_template(
        quest_id,
        name,
        flags,
        description,
        stages=stages,
        conditions=conditions,
        actions=actions,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transitions,
        npc_state=npc_state,
        world_context=world_context,
        metadata=metadata,
    )


def quest_chain(
    chain_id: str,
    title: str,
    quests: Sequence[QuestTemplate | str] = (),
    *,
    entry_quest_id: str = "",
    branches: Mapping[str, Sequence[str]] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuestChain:
    return QuestChain(
        chain_id=validate_quest_id(chain_id),
        title=_validate_text("chain.title", title),
        quests=tuple(quests),
        entry_quest_id=entry_quest_id,
        branches={key: tuple(value) for key, value in dict(branches or {}).items()},
        metadata=_coerce_metadata(metadata),
    ).validate()


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
    return QuestOffer(
        offer_id=validate_quest_id(offer_id),
        template=template,
        quest_id=quest_id,
        giver_id=giver_id,
        title=title,
        summary=summary,
        conditions=tuple(conditions),
        actions=tuple(actions),
        triggers=tuple(triggers),
        rewards=tuple(rewards),
        failures=tuple(failures),
        npc_state=npc_state,
        world_context=world_context,
        expires_in_days=expires_in_days,
        transitions=dict(transitions or {}),
        metadata=_coerce_metadata(metadata),
    ).validate()


def quest_single_stage_quest(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    stage_title: str,
    stage_objective: str,
    stage_id: str | None = None,
    stage_description: str = "",
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
) -> QuestTemplate:
    """
    Convenience helper for a one-stage quest.

    This keeps the current tuple-based compiler format intact while making
    authoring more declarative.
    """
    quest_id = validate_quest_id(quest_id)
    blueprint_stage = quest_stage(
        stage_id=stage_id or f"{quest_id}_stage_1",
        title=stage_title,
        objective=stage_objective,
        description=stage_description,
        conditions=conditions,
        actions=actions,
        battle_hooks=battle_hooks,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transitions,
        metadata=stage_metadata,
    )
    return quest_template(
        quest_id,
        name,
        flags,
        description,
        stages=(blueprint_stage,),
        transitions=transitions,
        npc_state=npc_state,
        world_context=world_context,
        metadata=quest_metadata,
    )


def quest_delivery_quest(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    item_name: str = "the goods",
    destination: str = "the destination",
    stage_title: str = "Deliver the Goods",
    stage_id: str | None = None,
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
) -> QuestTemplate:
    return quest_single_stage_quest(
        quest_id,
        name,
        flags,
        description,
        stage_title=stage_title,
        stage_objective=f"Deliver {item_name} to {destination}.",
        stage_id=stage_id,
        stage_description=f"Carry out a delivery quest for {item_name}.",
        conditions=conditions,
        actions=actions,
        battle_hooks=battle_hooks,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transitions,
        quest_metadata=quest_metadata,
        stage_metadata=stage_metadata,
        npc_state=npc_state,
        world_context=world_context,
    )


def quest_hunt_quest(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    target_name: str = "the target",
    stage_title: str = "Hunt the Target",
    stage_id: str | None = None,
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
) -> QuestTemplate:
    return quest_single_stage_quest(
        quest_id,
        name,
        flags,
        description,
        stage_title=stage_title,
        stage_objective=f"Hunt down {target_name}.",
        stage_id=stage_id,
        stage_description=f"Track {target_name} and defeat it.",
        conditions=conditions,
        actions=actions,
        battle_hooks=battle_hooks,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transitions,
        quest_metadata=quest_metadata,
        stage_metadata=stage_metadata,
        npc_state=npc_state,
        world_context=world_context,
    )


def quest_escort_quest(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    person_name: str = "the escort target",
    stage_title: str = "Escort the Party",
    stage_id: str | None = None,
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
) -> QuestTemplate:
    return quest_single_stage_quest(
        quest_id,
        name,
        flags,
        description,
        stage_title=stage_title,
        stage_objective=f"Escort {person_name} to safety.",
        stage_id=stage_id,
        stage_description=f"Keep {person_name} protected until the destination is reached.",
        conditions=conditions,
        actions=actions,
        battle_hooks=battle_hooks,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transitions,
        quest_metadata=quest_metadata,
        stage_metadata=stage_metadata,
        npc_state=npc_state,
        world_context=world_context,
    )


def quest_rescue_quest(
    quest_id: str,
    name: str,
    flags: Any,
    description: str,
    *,
    person_name: str = "the prisoner",
    stage_title: str = "Rescue the Prisoner",
    stage_id: str | None = None,
    conditions: Sequence[QuestCondition | str] = (),
    actions: Sequence[QuestAction | str] = (),
    battle_hooks: Sequence[str] = (),
    triggers: Sequence[QuestTrigger | str] = (),
    rewards: Sequence[QuestReward | str] = (),
    failures: Sequence[QuestFailure | str] = (),
    transitions: Mapping[str, str] | None = None,
    quest_metadata: Mapping[str, Any] | None = None,
    stage_metadata: Mapping[str, Any] | None = None,
    npc_state: QuestNPCState | None = None,
    world_context: QuestWorldContext | None = None,
) -> QuestTemplate:
    return quest_single_stage_quest(
        quest_id,
        name,
        flags,
        description,
        stage_title=stage_title,
        stage_objective=f"Rescue {person_name}.",
        stage_id=stage_id,
        stage_description=f"Break {person_name} out and escort them to safety.",
        conditions=conditions,
        actions=actions,
        battle_hooks=battle_hooks,
        triggers=triggers,
        rewards=rewards,
        failures=failures,
        transitions=transitions,
        quest_metadata=quest_metadata,
        stage_metadata=stage_metadata,
        npc_state=npc_state,
        world_context=world_context,
    )


def ensure_unique_quest_ids(blueprints: Iterable[QuestTemplate]) -> None:
    seen: dict[str, QuestTemplate] = {}
    for blueprint in blueprints:
        blueprint.validate()
        if blueprint.quest_id in seen:
            first = seen[blueprint.quest_id]
            raise ValueError(
                f"Duplicate quest id {blueprint.quest_id!r} in chain data: "
                f"{first.name!r} and {blueprint.name!r}"
            )
        seen[blueprint.quest_id] = blueprint


def ensure_unique_stage_ids(stages: Iterable[QuestStage], *, quest_id: str) -> None:
    seen: dict[str, QuestStage] = {}
    for stage in stages:
        stage.validate()
        if stage.stage_id in seen:
            first = seen[stage.stage_id]
            raise ValueError(
                f"Duplicate stage id {stage.stage_id!r} in quest {quest_id!r}: "
                f"{first.title!r} and {stage.title!r}"
            )
        seen[stage.stage_id] = stage


# Backwards-compatible alias exported for older content.
QuestBlueprint = QuestTemplate
