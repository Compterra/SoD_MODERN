# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from src.quests.quest_domain import (
    QuestCondition,
    QuestNPCState,
    QuestOffer,
    QuestReward,
    QuestTemplate,
    QuestWorldContext,
    quest_condition,
    quest_offer,
    quest_reward,
    quest_single_stage_quest,
    quest_world_context,
    validate_quest_id,
)

QUEST_GENERATION_TYPES = (
    "rescue",
    "escort",
    "hunt",
    "delivery",
    "sabotage",
    "defense",
    "diplomacy",
    "recruitment",
    "investigation",
    "revenge",
    "retaliation",
    "infiltration",
    "siege_support",
    "recovery",
    "assassination",
    "relief_supply",
    "prisoner_exchange",
)

QUEST_GENERATION_INPUTS = (
    "faction_war_state",
    "settlement_danger",
    "economy_state",
    "player_relation",
    "player_renown",
    "party_size",
    "nearby_threats",
    "recent_battles",
    "center_ownership",
    "prisoner_state",
    "trade_routes",
    "regional_unrest",
)


def _coerce_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(value or {})


def _coerce_sequence(value: Any) -> tuple[Any, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, Sequence) and not isinstance(value, str):
        return tuple(value)
    return (value,)


def _coerce_int(value: Any, default: int = 0) -> int:
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


def _coerce_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return default
    return default


def _context_value(context: Mapping[str, Any], key: str, default: Any = 0) -> Any:
    if key in context:
        return context[key]
    value: Any = context
    for part in key.split("."):
        if isinstance(value, Mapping) and part in value:
            value = value[part]
        else:
            return default
    return value


def _normalize_type(quest_type: str) -> str:
    if not isinstance(quest_type, str):
        raise TypeError(f"quest_type must be a string, got {type(quest_type)!r}")
    normalized = quest_type.strip().lower()
    if normalized not in QUEST_GENERATION_TYPES:
        raise ValueError(f"Unknown dynamic quest generation type {quest_type!r}")
    return normalized


@dataclass
class QuestGenerationContext:
    context_id: str = "dynamic_quest_context"
    faction_war_state: int = 0
    settlement_danger: int = 0
    economy_state: int = 0
    player_relation: int = 0
    player_renown: int = 0
    party_size: int = 0
    nearby_threats: int = 0
    recent_battles: int = 0
    center_ownership: int = 0
    prisoner_state: int = 0
    trade_routes: int = 0
    regional_unrest: int = 0
    region: str = ""
    center_id: str = ""
    faction_id: str = ""
    day: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestGenerationContext":
        validate_quest_id(self.context_id)
        for field_name in QUEST_GENERATION_INPUTS:
            setattr(self, field_name, _coerce_int(getattr(self, field_name), 0))
        if self.day is not None:
            self.day = _coerce_int(self.day, 0)
        self.metadata = _coerce_mapping(self.metadata)
        return self

    def to_mapping(self) -> dict[str, Any]:
        self.validate()
        result = {
            "context_id": self.context_id,
            "region": self.region,
            "center_id": self.center_id,
            "faction_id": self.faction_id,
            "day": self.day,
            "metadata": dict(self.metadata),
        }
        for field_name in QUEST_GENERATION_INPUTS:
            result[field_name] = getattr(self, field_name)
        return result

    def to_world_context(self) -> QuestWorldContext:
        data = self.to_mapping()
        return quest_world_context(
            self.context_id,
            center_id=self.center_id,
            faction_id=self.faction_id,
            region=self.region,
            day=self.day,
            metadata=data,
        )


@dataclass
class QuestGenerationRule:
    rule_id: str
    input_key: str
    min_value: int | None = None
    max_value: int | None = None
    weight_delta: int = 0
    difficulty_delta: int = 0
    required: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "QuestGenerationRule":
        validate_quest_id(self.rule_id)
        if not isinstance(self.input_key, str) or not self.input_key.strip():
            raise ValueError("QuestGenerationRule.input_key cannot be empty")
        if self.min_value is not None:
            self.min_value = _coerce_int(self.min_value, 0)
        if self.max_value is not None:
            self.max_value = _coerce_int(self.max_value, 0)
        self.weight_delta = _coerce_int(self.weight_delta, 0)
        self.difficulty_delta = _coerce_int(self.difficulty_delta, 0)
        self.required = bool(self.required)
        self.metadata = _coerce_mapping(self.metadata)
        return self

    def applies(self, context: Mapping[str, Any]) -> bool:
        self.validate()
        value = _coerce_int(_context_value(context, self.input_key, 0), 0)
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True


@dataclass
class DynamicQuestTemplate:
    template_id: str
    quest_type: str
    title: str
    summary: str
    base_weight: int = 10
    min_difficulty: int = 1
    max_difficulty: int = 5
    cooldown_days: int = 7
    parameters: dict[str, Any] = field(default_factory=dict)
    conditions: tuple[QuestCondition | str, ...] = ()
    rewards: tuple[QuestReward | str, ...] = ()
    rules: tuple[QuestGenerationRule | Mapping[str, Any], ...] = ()
    chain_id: str = ""
    faction_personality_weights: dict[str, int] = field(default_factory=dict)
    region_tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> "DynamicQuestTemplate":
        validate_quest_id(self.template_id)
        self.quest_type = _normalize_type(self.quest_type)
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("DynamicQuestTemplate.title cannot be empty")
        if not isinstance(self.summary, str) or not self.summary.strip():
            raise ValueError("DynamicQuestTemplate.summary cannot be empty")
        self.base_weight = max(0, _coerce_int(self.base_weight, 0))
        self.min_difficulty = max(1, _coerce_int(self.min_difficulty, 1))
        self.max_difficulty = max(self.min_difficulty, _coerce_int(self.max_difficulty, self.min_difficulty))
        self.cooldown_days = max(0, _coerce_int(self.cooldown_days, 0))
        self.parameters = _coerce_mapping(self.parameters)
        self.faction_personality_weights = {
            str(key): _coerce_int(value, 0)
            for key, value in self.faction_personality_weights.items()
        }
        self.region_tags = tuple(str(tag).strip().lower() for tag in self.region_tags if str(tag).strip())
        self.metadata = _coerce_mapping(self.metadata)
        normalized_rules = []
        for index, rule in enumerate(self.rules, start=1):
            if isinstance(rule, QuestGenerationRule):
                normalized_rules.append(rule.validate())
            elif isinstance(rule, Mapping):
                normalized_rules.append(
                    QuestGenerationRule(
                        rule_id=str(rule.get("rule_id") or rule.get("id") or f"{self.template_id}_rule_{index}"),
                        input_key=str(rule.get("input_key") or rule.get("key") or ""),
                        min_value=rule.get("min_value"),
                        max_value=rule.get("max_value"),
                        weight_delta=_coerce_int(rule.get("weight_delta"), 0),
                        difficulty_delta=_coerce_int(rule.get("difficulty_delta"), 0),
                        required=bool(rule.get("required", False)),
                        metadata=_coerce_mapping(rule.get("metadata")),
                    ).validate()
                )
            else:
                raise TypeError(f"Unknown generation rule type: {type(rule)!r}")
        self.rules = tuple(normalized_rules)
        return self

    def score(self, context: Mapping[str, Any]) -> tuple[int, int, list[str]]:
        self.validate()
        weight = self.base_weight
        difficulty = self.min_difficulty
        reasons = [f"base:{self.base_weight}"]

        region = str(context.get("region", "") or "").strip().lower()
        if self.region_tags and region and region not in self.region_tags:
            return 0, difficulty, ["region_mismatch"]

        personality = str(
            context.get("faction_personality")
            or context.get("personality")
            or _context_value(context, "metadata.faction_personality", "")
            or ""
        ).strip().lower()
        if personality and personality in self.faction_personality_weights:
            delta = self.faction_personality_weights[personality]
            weight += delta
            reasons.append(f"personality:{personality}:{delta}")

        for rule in self.rules:
            if rule.applies(context):
                weight += rule.weight_delta
                difficulty += rule.difficulty_delta
                reasons.append(f"{rule.rule_id}:{rule.weight_delta}")
            elif rule.required:
                return 0, difficulty, [f"missing_required:{rule.rule_id}"]

        difficulty += _coerce_int(context.get("difficulty_bias"), 0)
        if context.get("player_renown"):
            difficulty += min(2, max(0, _coerce_int(context.get("player_renown"), 0) // 300))
        if context.get("party_size"):
            difficulty += min(1, max(0, _coerce_int(context.get("party_size"), 0) // 80))
        difficulty = max(self.min_difficulty, min(self.max_difficulty, difficulty))
        return max(0, weight), difficulty, reasons

    def to_quest_template(self, *, difficulty: int = 1, context: Mapping[str, Any] | None = None) -> QuestTemplate:
        self.validate()
        context = _coerce_mapping(context)
        metadata = dict(self.metadata)
        metadata.update(
            {
                "authoring": "dynamic_generation",
                "quest_type": self.quest_type,
                "dynamic_template_id": self.template_id,
                "difficulty": difficulty,
                "chain_id": self.chain_id,
                "parameters": dict(self.parameters),
            }
        )
        return quest_single_stage_quest(
            self.template_id,
            self.title,
            0,
            self.summary,
            stage_title=self.title,
            stage_objective=self.summary,
            conditions=self.conditions,
            rewards=self.rewards,
            world_context=context.get("world_context"),
            quest_metadata=metadata,
            stage_metadata={
                "quest_type": self.quest_type,
                "difficulty": difficulty,
                "dynamic_template_id": self.template_id,
            },
        )

    def to_offer(
        self,
        *,
        context: Mapping[str, Any],
        npc_state: QuestNPCState | None = None,
        offer_index: int = 1,
    ) -> QuestOffer:
        weight, difficulty, reasons = self.score(context)
        world_context = context.get("world_context")
        if world_context is None:
            world_context = quest_generation_context_from_mapping(context).to_world_context()
        template = self.to_quest_template(difficulty=difficulty, context={"world_context": world_context})
        metadata = dict(self.metadata)
        metadata.update(
            {
                "dynamic": True,
                "quest_type": self.quest_type,
                "weight": weight,
                "difficulty": difficulty,
                "selection_reasons": tuple(reasons),
                "cooldown_days": self.cooldown_days,
                "chain_id": self.chain_id,
                "parameters": dict(self.parameters),
            }
        )
        return quest_offer(
            f"{self.template_id}_offer_{offer_index}",
            template=template,
            giver_id=npc_state.npc_id if npc_state is not None else str(context.get("giver_id", "") or ""),
            title=self.title,
            summary=self.summary,
            conditions=self.conditions,
            rewards=self.rewards,
            npc_state=npc_state,
            world_context=world_context,
            expires_in_days=max(1, self.cooldown_days),
            metadata=metadata,
        ).validate()


@dataclass
class GeneratedQuestOffer:
    offer: QuestOffer
    weight: int
    difficulty: int
    reasons: tuple[str, ...] = ()

    def to_snapshot(self) -> dict[str, Any]:
        data = self.offer.to_snapshot()
        data["weight"] = self.weight
        data["difficulty"] = self.difficulty
        data["reasons"] = list(self.reasons)
        return data


def quest_generation_context_from_mapping(mapping: Mapping[str, Any] | None) -> QuestGenerationContext:
    data = _coerce_mapping(mapping)
    return QuestGenerationContext(
        context_id=str(data.get("context_id") or "dynamic_quest_context"),
        faction_war_state=_coerce_int(data.get("faction_war_state"), 0),
        settlement_danger=_coerce_int(data.get("settlement_danger"), 0),
        economy_state=_coerce_int(data.get("economy_state"), 0),
        player_relation=_coerce_int(data.get("player_relation"), 0),
        player_renown=_coerce_int(data.get("player_renown"), 0),
        party_size=_coerce_int(data.get("party_size"), 0),
        nearby_threats=_coerce_int(data.get("nearby_threats"), 0),
        recent_battles=_coerce_int(data.get("recent_battles"), 0),
        center_ownership=_coerce_int(data.get("center_ownership"), 0),
        prisoner_state=_coerce_int(data.get("prisoner_state"), 0),
        trade_routes=_coerce_int(data.get("trade_routes"), 0),
        regional_unrest=_coerce_int(data.get("regional_unrest"), 0),
        region=str(data.get("region", "") or ""),
        center_id=str(data.get("center_id", "") or ""),
        faction_id=str(data.get("faction_id", "") or ""),
        day=data.get("day"),
        metadata=_coerce_mapping(data.get("metadata")),
    ).validate()


def dynamic_quest_template(
    template_id: str,
    quest_type: str,
    title: str,
    summary: str,
    **kwargs: Any,
) -> DynamicQuestTemplate:
    return DynamicQuestTemplate(template_id, quest_type, title, summary, **kwargs).validate()


def quest_generation_rule(
    rule_id: str,
    input_key: str,
    **kwargs: Any,
) -> QuestGenerationRule:
    return QuestGenerationRule(rule_id, input_key, **kwargs).validate()


def generate_dynamic_quest_offers(
    templates: Sequence[DynamicQuestTemplate | Mapping[str, Any]],
    context: Mapping[str, Any] | QuestGenerationContext,
    *,
    npc_state: QuestNPCState | None = None,
    limit: int = 3,
    recent_offer_ids: Sequence[str] = (),
) -> list[GeneratedQuestOffer]:
    if isinstance(context, QuestGenerationContext):
        context_data = context.to_mapping()
        world_context = context.to_world_context()
    else:
        generation_context = quest_generation_context_from_mapping(context)
        context_data = generation_context.to_mapping()
        world_context = generation_context.to_world_context()
    context_data["world_context"] = world_context

    recent = set(str(item) for item in recent_offer_ids)
    scored: list[GeneratedQuestOffer] = []
    for index, template in enumerate(templates, start=1):
        if isinstance(template, DynamicQuestTemplate):
            active_template = template.validate()
        elif isinstance(template, Mapping):
            active_template = dynamic_quest_template(
                str(template.get("template_id") or template.get("id") or f"dynamic_quest_{index}"),
                str(template.get("quest_type") or template.get("type") or "delivery"),
                str(template.get("title") or template.get("name") or f"Dynamic Quest {index}"),
                str(template.get("summary") or template.get("description") or "A local problem needs attention."),
                base_weight=_coerce_int(template.get("base_weight"), 10),
                min_difficulty=_coerce_int(template.get("min_difficulty"), 1),
                max_difficulty=_coerce_int(template.get("max_difficulty"), 5),
                cooldown_days=_coerce_int(template.get("cooldown_days"), 7),
                parameters=_coerce_mapping(template.get("parameters")),
                conditions=tuple(template.get("conditions", ()) or ()),
                rewards=tuple(template.get("rewards", ()) or ()),
                rules=tuple(template.get("rules", ()) or ()),
                chain_id=str(template.get("chain_id", "") or ""),
                faction_personality_weights=_coerce_mapping(template.get("faction_personality_weights")),
                region_tags=tuple(template.get("region_tags", ()) or ()),
                metadata=_coerce_mapping(template.get("metadata")),
            )
        else:
            raise TypeError(f"Unknown dynamic quest template type: {type(template)!r}")

        if active_template.template_id in recent:
            continue
        weight, difficulty, reasons = active_template.score(context_data)
        if weight <= 0:
            continue
        offer = active_template.to_offer(
            context=context_data,
            npc_state=npc_state,
            offer_index=len(scored) + 1,
        )
        scored.append(
            GeneratedQuestOffer(
                offer=offer,
                weight=weight,
                difficulty=difficulty,
                reasons=tuple(reasons),
            )
        )

    scored.sort(key=lambda item: (-item.weight, item.offer.offer_id))
    return scored[: max(0, _coerce_int(limit, 3))]


DEFAULT_DYNAMIC_QUEST_TEMPLATES = (
    dynamic_quest_template(
        "dynamic_rescue_prisoner",
        "rescue",
        "Rescue a Captive",
        "A prisoner tied to this region can be recovered before they are moved.",
        base_weight=8,
        rules=(
            quest_generation_rule("prisoner_pressure", "prisoner_state", min_value=1, weight_delta=18, difficulty_delta=1, required=True),
            quest_generation_rule("nearby_threat_pressure", "nearby_threats", min_value=2, weight_delta=6, difficulty_delta=1),
        ),
        cooldown_days=10,
        metadata={"family": "captivity"},
    ),
    dynamic_quest_template(
        "dynamic_escort_caravan",
        "escort",
        "Escort a Caravan",
        "A trade route needs armed company through dangerous country.",
        base_weight=9,
        rules=(
            quest_generation_rule("trade_route_need", "trade_routes", min_value=1, weight_delta=14, difficulty_delta=0, required=True),
            quest_generation_rule("dangerous_roads", "settlement_danger", min_value=3, weight_delta=5, difficulty_delta=1),
        ),
        cooldown_days=6,
        metadata={"family": "trade"},
    ),
    dynamic_quest_template(
        "dynamic_hunt_raiders",
        "hunt",
        "Hunt Local Raiders",
        "Nearby threats are growing bold enough to warrant a direct hunt.",
        base_weight=10,
        rules=(
            quest_generation_rule("threat_density", "nearby_threats", min_value=1, weight_delta=16, difficulty_delta=1, required=True),
            quest_generation_rule("unrest_pressure", "regional_unrest", min_value=3, weight_delta=4, difficulty_delta=1),
        ),
        cooldown_days=5,
        metadata={"family": "security"},
    ),
    dynamic_quest_template(
        "dynamic_relief_supply",
        "relief_supply",
        "Bring Relief Supplies",
        "A distressed settlement needs supplies before hardship turns into unrest.",
        base_weight=8,
        rules=(
            quest_generation_rule("poor_economy", "economy_state", max_value=-1, weight_delta=14, difficulty_delta=0, required=True),
            quest_generation_rule("danger_pressure", "settlement_danger", min_value=2, weight_delta=5, difficulty_delta=1),
        ),
        cooldown_days=7,
        metadata={"family": "relief"},
    ),
    dynamic_quest_template(
        "dynamic_siege_support",
        "siege_support",
        "Support the Siege Line",
        "War pressure has created a need for scouts, supplies, or disruption around a contested center.",
        base_weight=7,
        rules=(
            quest_generation_rule("war_state", "faction_war_state", min_value=1, weight_delta=16, difficulty_delta=1, required=True),
            quest_generation_rule("recent_battle_pressure", "recent_battles", min_value=1, weight_delta=5, difficulty_delta=1),
        ),
        cooldown_days=9,
        faction_personality_weights={"militant": 5, "honorable": 2},
        metadata={"family": "war"},
    ),
    dynamic_quest_template(
        "dynamic_delivery_dispatch",
        "delivery",
        "Carry Urgent Dispatches",
        "A sealed message must reach a nearby authority before the situation changes.",
        base_weight=8,
        rules=(
            quest_generation_rule("active_trade_routes", "trade_routes", min_value=1, weight_delta=7),
            quest_generation_rule("relation_trust", "player_relation", min_value=5, weight_delta=5),
        ),
        cooldown_days=4,
        faction_personality_weights={"calculating": 4, "honorable": 2},
        metadata={"family": "courier"},
    ),
    dynamic_quest_template(
        "dynamic_sabotage_supply_cache",
        "sabotage",
        "Sabotage Enemy Supplies",
        "A hostile force depends on a vulnerable supply cache in this region.",
        base_weight=6,
        rules=(
            quest_generation_rule("war_pressure", "faction_war_state", min_value=1, weight_delta=13, difficulty_delta=1, required=True),
            quest_generation_rule("recent_battle_need", "recent_battles", min_value=1, weight_delta=4, difficulty_delta=1),
        ),
        cooldown_days=9,
        faction_personality_weights={"calculating": 6, "militant": 3},
        metadata={"family": "war"},
    ),
    dynamic_quest_template(
        "dynamic_defend_settlement",
        "defense",
        "Defend a Threatened Settlement",
        "A settlement expects trouble and needs defenders before raiders arrive.",
        base_weight=9,
        rules=(
            quest_generation_rule("settlement_danger", "settlement_danger", min_value=2, weight_delta=15, difficulty_delta=1, required=True),
            quest_generation_rule("local_unrest", "regional_unrest", min_value=2, weight_delta=5),
        ),
        cooldown_days=7,
        faction_personality_weights={"honorable": 4, "militant": 2},
        metadata={"family": "security"},
    ),
    dynamic_quest_template(
        "dynamic_diplomacy_envoy",
        "diplomacy",
        "Serve as Envoy",
        "A tense political matter needs a reliable messenger with enough standing to be heard.",
        base_weight=6,
        rules=(
            quest_generation_rule("renown_threshold", "player_renown", min_value=80, weight_delta=10, required=True),
            quest_generation_rule("strained_relation", "player_relation", max_value=0, weight_delta=5),
        ),
        cooldown_days=10,
        faction_personality_weights={"honorable": 5, "calculating": 3},
        metadata={"family": "politics"},
    ),
    dynamic_quest_template(
        "dynamic_recruitment_drive",
        "recruitment",
        "Raise Local Recruits",
        "A sponsor needs recruits gathered before danger overwhelms the district.",
        base_weight=7,
        rules=(
            quest_generation_rule("danger_need", "settlement_danger", min_value=1, weight_delta=7),
            quest_generation_rule("small_party_fit", "party_size", max_value=70, weight_delta=5),
            quest_generation_rule("war_need", "faction_war_state", min_value=1, weight_delta=4),
        ),
        cooldown_days=6,
        metadata={"family": "manpower"},
    ),
    dynamic_quest_template(
        "dynamic_investigate_unrest",
        "investigation",
        "Investigate Local Unrest",
        "Rumors, disappearances, or missing goods point to a deeper local problem.",
        base_weight=7,
        rules=(
            quest_generation_rule("unrest_signal", "regional_unrest", min_value=2, weight_delta=14, required=True),
            quest_generation_rule("threat_hint", "nearby_threats", min_value=1, weight_delta=3),
        ),
        cooldown_days=8,
        faction_personality_weights={"calculating": 4},
        metadata={"family": "mystery"},
    ),
    dynamic_quest_template(
        "dynamic_revenge_warrant",
        "revenge",
        "Avenge a Local Wrong",
        "A recent attack has left a sponsor demanding justice against a known culprit.",
        base_weight=6,
        rules=(
            quest_generation_rule("recent_battle_grievance", "recent_battles", min_value=1, weight_delta=13, difficulty_delta=1, required=True),
            quest_generation_rule("threat_followup", "nearby_threats", min_value=1, weight_delta=5),
        ),
        cooldown_days=11,
        faction_personality_weights={"vengeful": 7, "militant": 3},
        metadata={"family": "vendetta"},
    ),
    dynamic_quest_template(
        "dynamic_retaliation_raid",
        "retaliation",
        "Strike Back at Raiders",
        "A faction or center wants a measured reprisal before enemies grow bolder.",
        base_weight=6,
        rules=(
            quest_generation_rule("war_or_threat", "nearby_threats", min_value=2, weight_delta=10, required=True),
            quest_generation_rule("regional_instability", "regional_unrest", min_value=2, weight_delta=6),
        ),
        cooldown_days=9,
        faction_personality_weights={"militant": 5, "vengeful": 5},
        metadata={"family": "reprisal"},
    ),
    dynamic_quest_template(
        "dynamic_infiltrate_camp",
        "infiltration",
        "Infiltrate a Hostile Camp",
        "A discreet entry could expose enemy plans without committing an army.",
        base_weight=5,
        rules=(
            quest_generation_rule("war_state_required", "faction_war_state", min_value=1, weight_delta=12, difficulty_delta=1, required=True),
            quest_generation_rule("high_renown_trust", "player_renown", min_value=120, weight_delta=4),
        ),
        cooldown_days=12,
        faction_personality_weights={"calculating": 7},
        metadata={"family": "intrigue"},
    ),
    dynamic_quest_template(
        "dynamic_recover_heirloom",
        "recovery",
        "Recover a Lost Heirloom",
        "A valuable object has passed into dangerous hands and must be recovered intact.",
        base_weight=7,
        rules=(
            quest_generation_rule("thief_pressure", "nearby_threats", min_value=1, weight_delta=8),
            quest_generation_rule("unrest_clue", "regional_unrest", min_value=1, weight_delta=5),
        ),
        cooldown_days=8,
        metadata={"family": "artifact"},
    ),
    dynamic_quest_template(
        "dynamic_assassination_plot",
        "assassination",
        "Disrupt an Assassin's Plot",
        "A vulnerable figure is being stalked by hired killers or political enemies.",
        base_weight=4,
        rules=(
            quest_generation_rule("high_stakes_relation", "player_relation", min_value=10, weight_delta=6),
            quest_generation_rule("war_conspiracy", "faction_war_state", min_value=1, weight_delta=8),
            quest_generation_rule("unrest_cover", "regional_unrest", min_value=2, weight_delta=5),
        ),
        cooldown_days=14,
        faction_personality_weights={"calculating": 4, "honorable": 2},
        metadata={"family": "intrigue"},
    ),
    dynamic_quest_template(
        "dynamic_prisoner_exchange",
        "prisoner_exchange",
        "Arrange a Prisoner Exchange",
        "Captives on both sides have created an opening for negotiation or leverage.",
        base_weight=6,
        rules=(
            quest_generation_rule("prisoner_state_required", "prisoner_state", min_value=1, weight_delta=13, required=True),
            quest_generation_rule("war_context", "faction_war_state", min_value=1, weight_delta=4),
            quest_generation_rule("renown_trust", "player_renown", min_value=80, weight_delta=3),
        ),
        cooldown_days=10,
        faction_personality_weights={"honorable": 4, "calculating": 3},
        metadata={"family": "captivity"},
    ),
)


__all__ = [
    "DEFAULT_DYNAMIC_QUEST_TEMPLATES",
    "DynamicQuestTemplate",
    "GeneratedQuestOffer",
    "QUEST_GENERATION_INPUTS",
    "QUEST_GENERATION_TYPES",
    "QuestGenerationContext",
    "QuestGenerationRule",
    "dynamic_quest_template",
    "generate_dynamic_quest_offers",
    "quest_generation_context_from_mapping",
    "quest_generation_rule",
]
