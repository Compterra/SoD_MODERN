# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Any, Mapping, MutableMapping, Sequence

from src.quests.quest_domain import QuestFailure, QuestReward

__all__ = [
    "QUEST_CONSEQUENCE_EFFECT_TYPES",
    "QUEST_REWARD_EFFECT_TYPES",
    "apply_consequence_effect",
    "apply_reward_effect",
    "initial_campaign_state",
    "normalize_consequence_effect",
    "normalize_reward_effect",
]

QUEST_REWARD_EFFECT_TYPES = frozenset(
    {
        "gold",
        "relation",
        "faction_standing",
        "renown",
        "troop_xp",
        "items",
        "prisoners",
        "titles",
        "access_flag",
        "access_flags",
        "discount",
        "discounts",
        "followup_quest",
        "followup_quests",
        "permanent_world_change",
        "permanent_world_changes",
    }
)

QUEST_CONSEQUENCE_EFFECT_TYPES = frozenset(
    {
        "relation_loss",
        "reputation_loss",
        "faction_hostility",
        "quest_lockout",
        "quest_lockouts",
        "time_penalty",
        "time_penalties",
        "regional_instability",
        "npc_distrust",
        "chain_failure",
        "alternate_quest",
        "alternate_quest_availability",
        "alternate_quests",
    }
)


def initial_campaign_state() -> dict[str, Any]:
    return {
        "gold": 0,
        "renown": 0,
        "time_penalties": 0,
        "relation": {},
        "reputation": {},
        "faction_standing": {},
        "troop_xp": {},
        "items": {},
        "prisoners": [],
        "titles": [],
        "access_flags": {},
        "discounts": {},
        "followup_quests": [],
        "alternate_quests": [],
        "quest_lockouts": {},
        "regional_instability": {},
        "npc_distrust": {},
        "faction_hostility": {},
        "permanent_world_changes": {},
        "chain_failures": [],
        "outcome_log": [],
    }


def _coerce_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(value or {})


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


def _coerce_sequence(value: Any) -> tuple[Any, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in value.split("|") if part.strip())
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(item for item in value if item is not None)
    return (value,)


_EFFECT_TYPE_ALIASES = {
    "follow_up_quest": "followup_quest",
    "follow_up_quests": "followup_quests",
}


def _normalize_effect_type_name(effect_type: Any, *, default: str = "") -> str:
    if effect_type is None:
        return default
    text = str(effect_type).strip().lower()
    if not text:
        return default
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return _EFFECT_TYPE_ALIASES.get(text, text) or default


def _append_unique(sequence: list[Any], value: Any) -> None:
    if value not in sequence:
        sequence.append(value)


def _increment_mapping(mapping: MutableMapping[str, Any], key: str, amount: int) -> int:
    current = mapping.get(key, 0)
    if not isinstance(current, int):
        current = _coerce_int(current, default=0)
    current += amount
    mapping[key] = current
    return current


def _set_mapping_value(mapping: MutableMapping[str, Any], key: str, value: Any) -> Any:
    mapping[key] = value
    return value


def _extract_metadata(source: Any) -> dict[str, Any]:
    metadata = getattr(source, "metadata", None)
    if isinstance(metadata, Mapping):
        return dict(metadata)
    if isinstance(source, Mapping):
        nested = source.get("metadata")
        if isinstance(nested, Mapping):
            return dict(nested)
    return {}


def _extract_field(source: Any, name: str, *, default: Any = None) -> Any:
    if isinstance(source, Mapping) and name in source:
        return source[name]
    value = getattr(source, name, default)
    if value is not default:
        return value
    metadata = _extract_metadata(source)
    if name in metadata:
        return metadata[name]
    return default


def _normalize_amount(value: Any, *, default: int = 0) -> int:
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


def _normalize_effect_spec(
    source: QuestReward | QuestFailure | Mapping[str, Any] | str,
    *,
    effect_key: str,
    fallback_effect_type: str,
) -> dict[str, Any]:
    if isinstance(source, Mapping):
        metadata = _coerce_mapping(source.get("metadata")) if isinstance(source.get("metadata"), Mapping) else {}
        effect_type = _normalize_effect_type_name(
            source.get(effect_key)
            or source.get("effect_type")
            or source.get("kind")
            or metadata.get(effect_key)
            or metadata.get("effect_type")
            or metadata.get("kind")
            or fallback_effect_type,
            default=fallback_effect_type,
        )
        return {
            "id": str(source.get("id") or source.get("reward_id") or source.get("failure_id") or "").strip(),
            "expression": str(source.get("expression") or source.get("value") or effect_type).strip(),
            "description": str(source.get("description") or "").strip(),
            "effect_type": effect_type,
            "target": str(source.get("target") or source.get("scope") or metadata.get("target") or "").strip(),
            "amount": _normalize_amount(source.get("amount") or source.get("value") or metadata.get("amount"), default=0),
            "value": source.get("value", metadata.get("value")),
            "metadata": _coerce_mapping(metadata),
        }

    if isinstance(source, str):
        effect_type = fallback_effect_type
        expression = source.strip()
        if ":" in expression:
            maybe_type, maybe_value = expression.split(":", 1)
            if maybe_type.strip():
                effect_type = maybe_type.strip()
                expression = maybe_value.strip()
        return {
            "id": "",
            "expression": expression,
            "description": "",
            "effect_type": effect_type,
            "target": "",
            "amount": _normalize_amount(expression, default=0),
            "value": expression,
            "metadata": {},
        }

    metadata = _extract_metadata(source)
    effect_type = str(
        _extract_field(source, effect_key, default="")
        or _extract_field(source, "effect_type", default="")
        or _extract_field(source, "kind", default="")
        or fallback_effect_type
    ).strip()
    target = str(_extract_field(source, "target", default="") or metadata.get("target") or "").strip()
    amount = _normalize_amount(_extract_field(source, "amount", default=None) or metadata.get("amount"), default=0)
    value = _extract_field(source, "value", default=metadata.get("value"))
    identifier = ""
    if isinstance(source, QuestReward):
        identifier = source.reward_id
    elif isinstance(source, QuestFailure):
        identifier = source.failure_id
    expression = str(_extract_field(source, "expression", default=effect_type) or effect_type).strip()
    description = str(_extract_field(source, "description", default="") or "").strip()
    return {
        "id": identifier,
        "expression": expression,
        "description": description,
        "effect_type": effect_type,
        "target": target,
        "amount": amount,
        "value": value,
        "metadata": metadata,
    }


def normalize_reward_effect(source: QuestReward | Mapping[str, Any] | str) -> dict[str, Any]:
    return _normalize_effect_spec(source, effect_key="reward_type", fallback_effect_type="gold")


def normalize_consequence_effect(source: QuestFailure | Mapping[str, Any] | str) -> dict[str, Any]:
    return _normalize_effect_spec(source, effect_key="consequence_type", fallback_effect_type="relation_loss")


def _reward_bucket(state: MutableMapping[str, Any], key: str, default: Any) -> Any:
    bucket = state.get(key)
    if bucket is None:
        bucket = default
        state[key] = bucket
    return bucket


def _apply_collection_reward(state: MutableMapping[str, Any], key: str, value: Any) -> None:
    bucket = _reward_bucket(state, key, {})
    if not isinstance(bucket, MutableMapping):
        bucket = {}
        state[key] = bucket
    if isinstance(value, Mapping):
        for sub_key, sub_value in value.items():
            if isinstance(sub_value, int):
                _increment_mapping(bucket, str(sub_key), sub_value)
            else:
                bucket[str(sub_key)] = sub_value
    else:
        bucket[str(value)] = True


def _apply_list_reward(state: MutableMapping[str, Any], key: str, values: Any) -> None:
    bucket = _reward_bucket(state, key, [])
    if not isinstance(bucket, list):
        bucket = []
        state[key] = bucket
    for item in _coerce_sequence(values):
        _append_unique(bucket, str(item))


def _apply_reward_type(state: MutableMapping[str, Any], effect: dict[str, Any]) -> None:
    effect_type = _normalize_effect_type_name(effect["effect_type"], default="gold")
    target = effect["target"] or "default"
    amount = effect["amount"]

    if effect_type == "gold":
        state["gold"] = _coerce_int(state.get("gold"), default=0) + amount
        return
    if effect_type == "renown":
        state["renown"] = _coerce_int(state.get("renown"), default=0) + amount
        return
    if effect_type in {"relation", "faction_standing", "troop_xp"}:
        bucket = _reward_bucket(state, effect_type, {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state[effect_type] = bucket
        _increment_mapping(bucket, target, amount)
        return
    if effect_type == "items":
        bucket = _reward_bucket(state, "items", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["items"] = bucket
        _increment_mapping(bucket, target, max(amount, 1))
        return
    if effect_type == "prisoners":
        _apply_list_reward(state, "prisoners", effect.get("value") or target)
        return
    if effect_type == "titles":
        _apply_list_reward(state, "titles", effect.get("value") or target)
        return
    if effect_type in {"access_flag", "access_flags"}:
        bucket = _reward_bucket(state, "access_flags", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["access_flags"] = bucket
        _set_mapping_value(bucket, target, effect.get("value", True))
        return
    if effect_type in {"discount", "discounts"}:
        bucket = _reward_bucket(state, "discounts", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["discounts"] = bucket
        _set_mapping_value(bucket, target, effect.get("value", amount))
        return
    if effect_type in {"followup_quest", "followup_quests"}:
        _apply_list_reward(state, "followup_quests", effect.get("value") or target)
        return
    if effect_type in {"permanent_world_change", "permanent_world_changes"}:
        bucket = _reward_bucket(state, "permanent_world_changes", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["permanent_world_changes"] = bucket
        _set_mapping_value(bucket, target, effect.get("value"))
        return

    bucket = _reward_bucket(state, "permanent_world_changes", {})
    if not isinstance(bucket, MutableMapping):
        bucket = {}
        state["permanent_world_changes"] = bucket
    _set_mapping_value(bucket, target, effect.get("value", amount))


def _apply_consequence_type(state: MutableMapping[str, Any], effect: dict[str, Any]) -> None:
    effect_type = _normalize_effect_type_name(effect["effect_type"], default="relation_loss")
    target = effect["target"] or "default"
    amount = abs(effect["amount"])

    if effect_type == "relation_loss":
        bucket = _reward_bucket(state, "relation", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["relation"] = bucket
        _increment_mapping(bucket, target, -amount)
        return
    if effect_type == "reputation_loss":
        bucket = _reward_bucket(state, "reputation", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["reputation"] = bucket
        _increment_mapping(bucket, target, -amount)
        return
    if effect_type == "faction_hostility":
        bucket = _reward_bucket(state, "faction_hostility", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["faction_hostility"] = bucket
        _set_mapping_value(bucket, target, effect.get("value", True))
        return
    if effect_type in {"quest_lockout", "quest_lockouts"}:
        bucket = _reward_bucket(state, "quest_lockouts", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["quest_lockouts"] = bucket
        _set_mapping_value(bucket, target, amount or 1)
        return
    if effect_type in {"time_penalty", "time_penalties"}:
        state["time_penalties"] = _coerce_int(state.get("time_penalties"), default=0) + max(amount, 1)
        return
    if effect_type == "regional_instability":
        bucket = _reward_bucket(state, "regional_instability", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["regional_instability"] = bucket
        _increment_mapping(bucket, target, max(amount, 1))
        return
    if effect_type == "npc_distrust":
        bucket = _reward_bucket(state, "npc_distrust", {})
        if not isinstance(bucket, MutableMapping):
            bucket = {}
            state["npc_distrust"] = bucket
        _increment_mapping(bucket, target, max(amount, 1))
        return
    if effect_type == "chain_failure":
        _apply_list_reward(state, "chain_failures", effect.get("value") or target)
        return
    if effect_type in {"alternate_quest", "alternate_quest_availability", "alternate_quests"}:
        _apply_list_reward(state, "alternate_quests", effect.get("value") or target)
        return

    bucket = _reward_bucket(state, "chain_failures", [])
    if not isinstance(bucket, list):
        bucket = []
        state["chain_failures"] = bucket
    _append_unique(bucket, target)


def _record_outcome(
    state: MutableMapping[str, Any],
    *,
    outcome_kind: str,
    effect: dict[str, Any],
    source: str,
    quest_id: str = "",
    stage_id: str = "",
) -> dict[str, Any]:
    log = state.get("outcome_log")
    if not isinstance(log, list):
        log = []
        state["outcome_log"] = log
    entry = {
        "outcome_kind": outcome_kind,
        "effect_type": effect["effect_type"],
        "target": effect["target"],
        "amount": effect["amount"],
        "value": effect["value"],
        "source": source,
        "quest_id": quest_id,
        "stage_id": stage_id,
        "id": effect["id"],
        "description": effect["description"],
    }
    log.append(entry)
    return entry


def apply_reward_effect(
    state: MutableMapping[str, Any],
    reward: QuestReward | Mapping[str, Any] | str,
    *,
    source: str = "quest",
    quest_id: str = "",
    stage_id: str = "",
) -> dict[str, Any]:
    if not isinstance(state, MutableMapping):
        raise TypeError(f"state must be a mutable mapping, got {type(state)!r}")
    effect = normalize_reward_effect(reward)
    _apply_reward_type(state, effect)
    return _record_outcome(
        state,
        outcome_kind="reward",
        effect=effect,
        source=source,
        quest_id=quest_id,
        stage_id=stage_id,
    )


def apply_consequence_effect(
    state: MutableMapping[str, Any],
    failure: QuestFailure | Mapping[str, Any] | str,
    *,
    source: str = "quest",
    quest_id: str = "",
    stage_id: str = "",
) -> dict[str, Any]:
    if not isinstance(state, MutableMapping):
        raise TypeError(f"state must be a mutable mapping, got {type(state)!r}")
    effect = normalize_consequence_effect(failure)
    _apply_consequence_type(state, effect)
    return _record_outcome(
        state,
        outcome_kind="consequence",
        effect=effect,
        source=source,
        quest_id=quest_id,
        stage_id=stage_id,
    )
