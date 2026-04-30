# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any as _Any, TypedDict as _TypedDict

from src.quests.quest_domain import *  # noqa: F401,F403
from src.quests.quest_domain import __all__ as _domain_all  # re-export the domain surface
from src.quests.quest_specs import (
    QuestChainSpec,
    QuestStageSpec,
    QuestTemplateSpec,
    quest_chain_from_specs,
    quest_chain_spec,
    quest_chain_spec_from_mapping,
    quest_stage_spec,
    quest_stage_spec_from_mapping,
    quest_template_spec,
    quest_template_spec_from_mapping,
)
from src.quests.quest_generation import (
    DEFAULT_DYNAMIC_QUEST_TEMPLATES,
    DynamicQuestTemplate,
    GeneratedQuestOffer,
    QUEST_GENERATION_INPUTS,
    QUEST_GENERATION_TYPES,
    QuestGenerationContext,
    QuestGenerationRule,
    dynamic_quest_template,
    generate_dynamic_quest_offers,
    quest_generation_context_from_mapping,
    quest_generation_rule,
)
from src.quests.quest_dsl import (
    QuestBranch,
    ambush_quest,
    delivery_quest,
    diplomacy_quest,
    escort_quest,
    hunt_quest,
    investigation_quest,
    quest_branch,
    quest_failure_bundle,
    quest_optional_stage,
    quest_repeatable_stage,
    quest_reward_bundle,
    quest_timed_stage,
    rescue_quest,
    siege_quest,
)
from src.quests.quest_diagnostics import (
    QuestDiagnostic,
    QuestDiagnosticsReport,
    quest_graph_dot,
    quest_graph_mermaid,
    quest_graph_report_json,
    quest_graph_snapshot,
    quest_graph_snapshots,
    validate_dynamic_generation_templates,
    validate_quest_chain_graph,
    validate_quest_template_graph,
)
from src.quests.quest_authoring import (
    QuestComponentRegistry,
    quest_components_from_mapping,
    quest_component_registry,
    quest_motif_from_mapping,
    quest_motif_delivery_complication_reward,
    quest_motif_escort_ambush_debrief,
    quest_motif_linear_chain,
    quest_motif_rescue_pursuit_return,
)
from src.quests.quest_lanes import (
    QuestLaneContract,
    quest_dialogue_lanes,
    quest_lane_contract,
    quest_outcome_triggers,
)
from src.quests.quest_migration import (
    QuestMigrationCandidate,
    QuestMigrationPlan,
    build_quest_migration_plan,
)
from src.quests.quest_outcomes import (
    QUEST_CONSEQUENCE_EFFECT_TYPES,
    QUEST_REWARD_EFFECT_TYPES,
    apply_consequence_effect,
    apply_reward_effect,
    initial_campaign_state,
    normalize_consequence_effect,
    normalize_reward_effect,
)

__all__ = [
    *_domain_all,
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
    "QuestDiagnostic",
    "QuestDiagnosticsReport",
    "quest_graph_dot",
    "quest_graph_mermaid",
    "quest_graph_report_json",
    "quest_graph_snapshot",
    "quest_graph_snapshots",
    "QuestComponentRegistry",
    "quest_components_from_mapping",
    "quest_component_registry",
    "quest_motif_from_mapping",
    "quest_motif_delivery_complication_reward",
    "quest_motif_escort_ambush_debrief",
    "quest_motif_linear_chain",
    "quest_motif_rescue_pursuit_return",
    "QuestLaneContract",
    "quest_dialogue_lanes",
    "quest_lane_contract",
    "quest_outcome_triggers",
    "QuestMigrationCandidate",
    "QuestMigrationPlan",
    "build_quest_migration_plan",
    "validate_dynamic_generation_templates",
    "validate_quest_chain_graph",
    "validate_quest_template_graph",
    "QUEST_CONSEQUENCE_EFFECT_TYPES",
    "QUEST_REWARD_EFFECT_TYPES",
    "apply_consequence_effect",
    "apply_reward_effect",
    "initial_campaign_state",
    "normalize_consequence_effect",
    "normalize_reward_effect",
    "QuestEventSubscriptionSpec",
]


class QuestEventSubscriptionSpec(_TypedDict, total=False):
    event_types: tuple[str, ...]
    quest_ids: tuple[_Any, ...]
    stage_ids: tuple[_Any, ...]
    faction_ids: tuple[_Any, ...]
    troop_ids: tuple[_Any, ...]
    center_ids: tuple[_Any, ...]
    party_ids: tuple[_Any, ...]
    region_ids: tuple[_Any, ...]
    location_ids: tuple[_Any, ...]
    sources: tuple[str, ...]
    categories: tuple[str, ...]
    tags: tuple[str, ...]
    payload_keys: tuple[str, ...]
    priority: int
    enabled: bool
    once: bool
    terminal_only: bool
    non_terminal_only: bool
    metadata: dict[str, _Any]
    callback: _Any
