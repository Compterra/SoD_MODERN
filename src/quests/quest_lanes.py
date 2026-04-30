# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from src.quests.quest_domain import validate_quest_id

__all__ = [
    "QuestLaneContract",
    "quest_dialogue_lanes",
    "quest_lane_contract",
    "quest_outcome_triggers",
]


def _coerce_lane_map(value: Mapping[str, Any] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, lane_id in dict(value or {}).items():
        key_text = str(key).strip()
        lane_text = str(lane_id).strip()
        if key_text and lane_text:
            result[key_text] = lane_text
    return result


@dataclass
class QuestLaneContract:
    contract_id: str
    dialogue_lanes: dict[str, str] = field(default_factory=dict)
    outcome_triggers: dict[str, str] = field(default_factory=dict)
    journal_lanes: dict[str, str] = field(default_factory=dict)
    required_lanes: tuple[str, ...] = ()
    required_outcomes: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestLaneContract":
        self.contract_id = validate_quest_id(self.contract_id)
        self.dialogue_lanes = _coerce_lane_map(self.dialogue_lanes)
        self.outcome_triggers = _coerce_lane_map(self.outcome_triggers)
        self.journal_lanes = _coerce_lane_map(self.journal_lanes)
        self.required_lanes = tuple(str(item).strip() for item in self.required_lanes if str(item).strip())
        self.required_outcomes = tuple(str(item).strip() for item in self.required_outcomes if str(item).strip())
        self.metadata = dict(self.metadata or {})
        return self

    def to_snapshot(self) -> dict[str, Any]:
        self.validate()
        return {
            "contract_id": self.contract_id,
            "dialogue_lanes": dict(sorted(self.dialogue_lanes.items())),
            "outcome_triggers": dict(sorted(self.outcome_triggers.items())),
            "journal_lanes": dict(sorted(self.journal_lanes.items())),
            "required_lanes": list(self.required_lanes),
            "required_outcomes": list(self.required_outcomes),
            "metadata": dict(self.metadata),
        }


def quest_lane_contract(
    contract_id: str,
    *,
    dialogue_lanes: Mapping[str, Any] | None = None,
    outcome_triggers: Mapping[str, Any] | None = None,
    journal_lanes: Mapping[str, Any] | None = None,
    required_lanes: Sequence[str] = (),
    required_outcomes: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> QuestLaneContract:
    return QuestLaneContract(
        contract_id=contract_id,
        dialogue_lanes=_coerce_lane_map(dialogue_lanes),
        outcome_triggers=_coerce_lane_map(outcome_triggers),
        journal_lanes=_coerce_lane_map(journal_lanes),
        required_lanes=tuple(required_lanes),
        required_outcomes=tuple(required_outcomes),
        metadata=dict(metadata or {}),
    ).validate()


def quest_dialogue_lanes(**lanes: Any) -> dict[str, str]:
    return _coerce_lane_map(lanes)


def quest_outcome_triggers(**triggers: Any) -> dict[str, str]:
    return _coerce_lane_map(triggers)
