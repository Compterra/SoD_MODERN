# -*- coding: utf-8 -*-
# Sample campaign fragment showing a quest chain authored with the schema helpers.
# Keep quest definitions in numbered fragments and rebuild with build/build_quests.py.
#
# SAMPLE CAMPAIGN AUTHORING NOTES
# -------------------------------
# This file is intentionally more verbose than normal production content. It is
# both a compile-safe quest fragment and a living feature tour for the Advanced
# Quest framework. When adding a new framework helper, add at least one compact
# usage here and leave a short note explaining why the helper exists.
#
# The sample has two jobs:
# 1. Keep a realistic, multi-quest campaign arc in QUESTS so legacy tuple output
#    remains stable.
# 2. Keep small preview objects near the top so authors can copy a minimal
#    pattern without reading the entire stress-test chain.
#
# FEATURE COVERAGE CHECKLIST
# --------------------------
# - quest_chain_from_specs for a grouped campaign arc
# - quest_template_spec for single-stage and multi-stage quest templates
# - quest_stage_spec and mapping-based stage authoring
# - stage metadata, quest metadata, transitions, and dialogue/choice-oriented text
# - quest_condition, quest_action, quest_reward, quest_failure, and quest_trigger helpers
# - quest_offer, quest_template, quest_blueprint, and the delivery/hunt/escort/rescue
#   convenience helpers
# - quest_npc_state, quest_world_context, and quest_battle_objective helpers
# - QuestComponentRegistry plus both manual and mapping-based registry population
# - quest_motif_from_mapping and named motif helpers through a compact motif demo
# - quest_reward_bundle, quest_failure_bundle, quest_branch, optional/timed/repeatable
#   DSL stages, and graph snapshot/report/diagram helpers
# - quest_lane_contract, quest_dialogue_lanes, and quest_outcome_triggers for
#   connecting graph lanes to dialogue, journal, and outcome trigger names
#
# Everything lives inside QUESTS so build/build_quests.py copies a self-contained
# payload into compile/module_quests.py.
#
# The terminal quests_end sentinel stays in src/quests/9999_quests_end.py so
# all authored quest content loads before the terminal transition target.

# NOTE: Registry setup.
# The registry gives authors named, reusable building blocks. This sample keeps
# one manually constructed registry and one mapping-constructed registry so both
# authoring styles are covered. Production quest files should prefer the mapping
# form when a family has many reusable components.
SAMPLE_AUTHORING_REGISTRY = quest_component_registry(
 "sample_authoring_registry",
 metadata={"category": "sample", "framework": "component_registry"},
)
SAMPLE_AUTHORING_REGISTRY.update_from_mapping(
 {
  "conditions": {
   "contract_ready": "contract ready",
  },
  "actions": {
   "brief_patrol": "brief patrol",
  },
  "rewards": {
   "route_secured": "route secured",
  },
  "failures": {
   "route_lost": "route lost",
  },
 }
)

SAMPLE_BULK_AUTHORING_REGISTRY = quest_components_from_mapping(
 "sample_bulk_authoring_registry",
 {
  "conditions": {
   "captain_available": "captain available",
  },
  "actions": {
   "mark_route": "mark route",
  },
  "rewards": {
   "captain_trust": "captain trust improved",
  },
  "failures": {
   "captain_doubt": "captain confidence lost",
  },
 },
 metadata={"category": "sample", "framework": "component_registry_bulk"},
)

# NOTE: DSL preview objects.
# These are stored as metadata previews rather than emitted as standalone legacy
# quests. They keep the sample's main campaign readable while still proving the
# DSL helpers can create structured rewards, failures, branches, and stage
# variants. Copy these patterns into real quest stages when authoring content.
SAMPLE_DSL_REWARDS = quest_reward_bundle(
 "sample_campaign_dsl_rewards",
 "captain praise",
 gold=150,
 xp=75,
 renown=1,
 metadata={"category": "sample", "framework": "dsl_reward_bundle"},
)
SAMPLE_DSL_FAILURES = quest_failure_bundle(
 "sample_campaign_dsl_failures",
 "captain disappointed",
 relation=-1,
 cooldown_days=2,
 metadata={"category": "sample", "framework": "dsl_failure_bundle"},
)
SAMPLE_DSL_BRANCH = quest_branch(
 "sample_campaign_dsl_success",
 "sample_campaign_dsl_optional",
 from_stage="sample_campaign_dsl_start",
 condition="success",
 description="A preview branch used by the optional/timed/repeatable stage examples.",
 metadata={"category": "sample", "framework": "dsl_branch"},
)
SAMPLE_DSL_OPTIONAL_STAGE = quest_optional_stage(
 "sample_campaign_dsl_optional",
 "Optional Road Clue",
 "Find the optional road clue before committing the patrol.",
 rewards=SAMPLE_DSL_REWARDS,
 metadata={"category": "sample", "framework": "dsl_optional_stage"},
)
SAMPLE_DSL_TIMED_STAGE = quest_timed_stage(
 "sample_campaign_dsl_timed",
 "Timed Patrol Muster",
 "Muster the patrol before the gate closes.",
 duration_hours=8,
 transitions=(SAMPLE_DSL_BRANCH,),
 failures=SAMPLE_DSL_FAILURES,
 metadata={"category": "sample", "framework": "dsl_timed_stage"},
)
SAMPLE_DSL_REPEATABLE_STAGE = quest_repeatable_stage(
 "sample_campaign_dsl_repeatable",
 "Repeat Watch Sweep",
 "Repeat the watch sweep until the route is quiet.",
 max_repeats=3,
 repeat_cooldown_days=1,
 rewards=SAMPLE_DSL_REWARDS,
 metadata={"category": "sample", "framework": "dsl_repeatable_stage"},
)

# NOTE: Quest lane contract preview.
# Lanes are the bridge between a graph edge and actual gameplay surfaces. A
# transition such as "accepted" is only useful when dialogue, journal text, and
# script/outcome triggers agree on what that lane means.
SAMPLE_LANE_CONTRACT = quest_lane_contract(
 "sample_campaign_lane_contract",
 dialogue_lanes=quest_dialogue_lanes(
  offer="sample_campaign_offer_lane",
  accepted="sample_campaign_accepted_lane",
  declined="sample_campaign_declined_lane",
  success="sample_campaign_success_lane",
  failure="sample_campaign_failure_lane",
  complete="sample_campaign_complete_lane",
 ),
 outcome_triggers=quest_outcome_triggers(
  success="sample_campaign_success_trigger",
  failure="sample_campaign_failure_trigger",
  complete="sample_campaign_complete_trigger",
 ),
 journal_lanes={
  "offer": "sample_campaign_offer_journal",
  "accepted": "sample_campaign_accepted_journal",
  "declined": "sample_campaign_declined_journal",
  "success": "sample_campaign_success_journal",
  "failure": "sample_campaign_failure_journal",
  "complete": "sample_campaign_complete_journal",
 },
 required_lanes=("offer", "accepted", "declined"),
 required_outcomes=("success", "failure"),
 metadata={"category": "sample", "framework": "lane_contract"},
)

# NOTE: Motif and graph preview.
# Motifs are intentionally compact. The detailed campaign below remains the
# stress test; this motif is the copy-friendly version that shows how a new
# author can get a chain, registry defaults, graph snapshots, and diagram text
# with very little boilerplate.
SAMPLE_MOTIF_CHAIN = quest_motif_from_mapping(
 {
  "chain_id": "sample_campaign_motif",
  "title": "Sample Campaign Motif",
  "motif": "escort_ambush_debrief",
  "flags": qf_random_quest,
  "registry": SAMPLE_AUTHORING_REGISTRY,
  "metadata": {
   "category": "sample",
   "framework": "motif_demo",
   "registry": SAMPLE_AUTHORING_REGISTRY.snapshot(),
   "lane_contract": SAMPLE_LANE_CONTRACT.to_snapshot(),
  },
 }
)
SAMPLE_MOTIF_SNAPSHOTS = quest_graph_snapshots((SAMPLE_MOTIF_CHAIN,))
SAMPLE_MOTIF_GRAPH_REPORT = quest_graph_report_json((SAMPLE_MOTIF_CHAIN,), diagnostics=())
SAMPLE_MOTIF_MERMAID = quest_graph_mermaid(SAMPLE_MOTIF_CHAIN)
SAMPLE_MOTIF_DOT = quest_graph_dot(SAMPLE_MOTIF_CHAIN)

# NOTE: Legacy payload.
# Only objects expanded inside QUESTS become legacy quest tuples. Preview
# objects above are intentionally included through metadata snapshots so the
# compiler receives the same tuple shape while the framework still exercises
# richer authoring/reporting features.
QUESTS = [
 *quest_chain_from_specs(
  "sample_campaign_quests",
  "Sample Campaign Quests",
  quests=(
   quest_template_spec(
    "sample_campaign_briefing",
    "Brief the Gate Captain",
    qf_random_quest,
    "The gate captain needs a reliable runner. Hear the problem, accept or decline the job, and prepare the patrol if you take it.",
    stage_title="Choose Your Contract",
    stage_objective="Meet the captain and decide whether to accept the campaign.",
    stage_id="sample_campaign_briefing_stage",
    stage_description="This opening stage exercises the dialogue-driven quest path and the accept / decline choice flow.",
    conditions=(
     quest_condition(
      "sample_campaign_contract_condition",
      "contract accepted",
      description="The player has accepted the sample contract.",
      metadata={
       "category": "sample",
       "kind": "condition",
      },
     ),
     "player near gate",
    ),
    actions=(
     quest_action(
      "sample_campaign_assembly_action",
      "assemble patrol",
      description="Bring the patrol together and prepare the route.",
      metadata={
       "category": "sample",
       "kind": "action",
      },
     ),
     "record the player choice",
     "open the patrol quest",
    ),
    triggers=(
     quest_trigger(
      "sample_campaign_contract_trigger",
      "conversation started",
      conditions=(
       quest_condition(
        "sample_campaign_contract_condition",
        "contract accepted",
        description="The player has accepted the sample contract.",
        metadata={
         "category": "sample",
         "kind": "condition",
        },
       ),
      ),
      actions=(
       quest_action(
        "sample_campaign_assembly_action",
        "assemble patrol",
        description="Bring the patrol together and prepare the route.",
        metadata={
         "category": "sample",
         "kind": "action",
        },
       ),
      ),
      description="Marks the quest-giver conversation path for the sample contract.",
      metadata={
       "category": "sample",
       "kind": "trigger",
      },
     ),
     quest_trigger(
      "sample_campaign_contract_end_trigger",
      "conversation ended",
      conditions=(
       quest_condition(
        "sample_campaign_contract_condition",
        "contract accepted",
        description="The player has accepted the sample contract.",
        metadata={
         "category": "sample",
         "kind": "condition",
        },
       ),
      ),
      actions=(
       quest_action(
        "sample_campaign_return_action",
        "deliver report",
        description="Return the report to the captain and close out the campaign.",
        metadata={
         "category": "sample",
         "kind": "action",
        },
       ),
      ),
      description="Marks the end of the sample contract conversation path.",
      metadata={
       "category": "sample",
       "kind": "trigger",
      },
     ),
    ),
    rewards=(
     quest_reward(
      "sample_campaign_route_reward",
      "patrol formed",
      description="The patrol has been assembled and is ready to move.",
      metadata={
       "category": "sample",
       "kind": "reward",
      },
     ),
    ),
    failures=(
     quest_failure(
      "sample_campaign_route_failure",
      "patrol delayed",
      description="The patrol could not be assembled in time.",
      metadata={
       "category": "sample",
       "kind": "failure",
      },
     ),
     "job declined",
    ),
    transitions={
     "accepted": "sample_campaign_patrol",
     "declined": "sample_campaign_debrief",
    },
    metadata={
     "category": "sample",
     "framework": "dialogue",
     "choice_flow": "accept_decline",
     "offer_preview": quest_offer(
      "sample_campaign_briefing_offer",
      quest_id="sample_campaign_briefing",
      giver_id="trp_swadian_castle_guard",
      title="Brief the Gate Captain",
      summary="A sample offer that opens the contract and demonstrates the offer helper.",
      conditions=(
       quest_condition(
        "sample_campaign_contract_condition",
        "contract accepted",
        description="The player has accepted the sample contract.",
        metadata={
         "category": "sample",
         "kind": "condition",
        },
       ),
      ),
      actions=(
       quest_action(
        "sample_campaign_assembly_action",
        "assemble patrol",
        description="Bring the patrol together and prepare the route.",
        metadata={
         "category": "sample",
         "kind": "action",
        },
       ),
      ),
      triggers=(
       quest_trigger(
        "sample_campaign_contract_trigger",
        "conversation started",
        conditions=(),
        actions=(),
        description="Marks the quest-giver conversation path for the sample contract.",
        metadata={
         "category": "sample",
         "kind": "trigger",
        },
       ),
      ),
      rewards=(),
      failures=(),
      npc_state=quest_npc_state(
       "trp_swadian_castle_guard",
       state="available",
       dialogue_state="briefing",
       available_quests=("sample_campaign_briefing",),
       completed_quests=(),
       failed_quests=(),
       locked_chains=("sample_campaign_quests",),
       cooldown_days=0,
       faction_alignment="neutral",
       personality="pragmatic",
       special_flags={
        "sample": True,
        "framework": "npc_state",
       },
       metadata={
        "category": "sample",
        "kind": "npc_state",
       },
      ),
      world_context=quest_world_context(
       "sample_campaign_gate_context",
       location_id="town_gate",
       center_id="sample_town",
       party_id="sample_patrol_party",
       faction_id="sample_faction",
       region="roadside",
       day=12,
       turn=3,
       metadata={
        "category": "sample",
        "kind": "world_context",
       },
      ),
      expires_in_days=3,
      transitions={
       "accepted": "sample_campaign_briefing",
       "declined": "sample_campaign_debrief",
      },
      metadata={
       "category": "sample",
       "kind": "offer",
      },
     ).to_snapshot(),
     "helper_library": {
      "direct_template": quest_template(
       "sample_campaign_direct_template",
       "Ledger the Watch",
       qf_random_quest,
       "A direct template that exercises the raw quest_template helper.",
       stages=(
        quest_stage(
         "sample_campaign_direct_stage",
         "Keep the Watch",
         "Hold the line until the road is secure.",
         description="This stage uses the raw quest_template and quest_stage helpers.",
         conditions=(
          quest_condition(
           "sample_campaign_contract_condition",
           "contract accepted",
           description="The player has accepted the sample contract.",
           metadata={
            "category": "sample",
            "kind": "condition",
           },
          ),
          quest_condition(
           "sample_campaign_route_condition",
           "route known",
           description="The patrol route has been identified.",
           metadata={
            "category": "sample",
            "kind": "condition",
           },
          ),
         ),
         actions=(
          quest_action(
           "sample_campaign_assembly_action",
           "assemble patrol",
           description="Bring the patrol together and prepare the route.",
           metadata={
            "category": "sample",
            "kind": "action",
           },
          ),
         ),
         battle_hooks=("sample_direct_battle_hook",),
         triggers=(
          quest_trigger(
           "sample_campaign_contract_trigger",
           "conversation started",
           conditions=(),
           actions=(),
           description="Marks the quest-giver conversation path for the sample contract.",
           metadata={
            "category": "sample",
            "kind": "trigger",
           },
          ),
          quest_trigger(
           "sample_campaign_contract_end_trigger",
           "conversation ended",
           conditions=(),
           actions=(),
           description="Marks the end of the sample contract conversation path.",
           metadata={
            "category": "sample",
            "kind": "trigger",
           },
          ),
         ),
         rewards=(
          quest_reward(
           "sample_campaign_route_reward",
           "patrol formed",
           description="The patrol has been assembled and is ready to move.",
           metadata={
            "category": "sample",
            "kind": "reward",
           },
          ),
         ),
         failures=(
          quest_failure(
           "sample_campaign_route_failure",
           "patrol delayed",
           description="The patrol could not be assembled in time.",
           metadata={
            "category": "sample",
            "kind": "failure",
           },
          ),
         ),
         battle_objective=quest_battle_objective(
          "sample_campaign_tower_objective",
          "hold_position",
          target_party_id="sample_raider_party",
          required_count=1,
          progress=0,
          wave_index=1,
          failure_state="tower_lost",
          required_payload_keys=("road", "route"),
          success_message="The watchtower is secure.",
          failure_message="The tower fell before the patrol could regroup.",
          metadata={
           "category": "sample",
           "kind": "battle_objective",
          },
         ),
         metadata={
          "category": "sample",
          "kind": "direct_template",
         },
        ),
       ),
       conditions=(
        quest_condition(
         "sample_campaign_contract_condition",
         "contract accepted",
         description="The player has accepted the sample contract.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_assembly_action",
         "assemble patrol",
         description="Bring the patrol together and prepare the route.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_contract_trigger",
         "conversation started",
         conditions=(),
         actions=(),
         description="Marks the quest-giver conversation path for the sample contract.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_route_reward",
         "patrol formed",
         description="The patrol has been assembled and is ready to move.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_route_failure",
         "patrol delayed",
         description="The patrol could not be assembled in time.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
       metadata={
        "category": "sample",
        "framework": "direct_template",
       },
      ).to_snapshot(),
      "blueprint": quest_blueprint(
       "sample_campaign_blueprint",
       "Blueprint the Tower",
       qf_random_quest,
       "A direct blueprint that exercises the quest_blueprint alias.",
       stages=(
        quest_stage(
         "sample_campaign_blueprint_stage",
         "Secure the Tower",
         "Use the tower vantage point to hold off attackers until the road is clear.",
         description="This stage exercises quest_blueprint, quest_stage, and the battle objective helper.",
         conditions=(
          quest_condition(
           "sample_campaign_combat_condition",
           "ambush spotted",
           description="The patrol has spotted the ambush site.",
           metadata={
            "category": "sample",
            "kind": "condition",
           },
          ),
         ),
         actions=(
          quest_action(
           "sample_campaign_combat_action",
           "engage raiders",
           description="Fight through the ambush and secure the road.",
           metadata={
            "category": "sample",
            "kind": "action",
           },
          ),
         ),
         battle_hooks=("sample_blueprint_battle_hook",),
         triggers=(
          quest_trigger(
           "sample_campaign_combat_trigger",
           "battle started",
           conditions=(),
           actions=(),
           description="Tracks the combat-facing patrol ambush phase.",
           metadata={
            "category": "sample",
            "kind": "trigger",
           },
          ),
          quest_trigger(
           "sample_campaign_end_trigger",
           "battle ended",
           conditions=(),
           actions=(),
           description="Tracks the campaign wrap-up path.",
           metadata={
            "category": "sample",
            "kind": "trigger",
           },
          ),
         ),
         rewards=(
          quest_reward(
           "sample_campaign_combat_reward",
           "road secured",
           description="The road is safe again after the ambush is cleared.",
           metadata={
            "category": "sample",
            "kind": "reward",
           },
          ),
         ),
         failures=(
          quest_failure(
           "sample_campaign_combat_failure",
           "patrol scattered",
           description="The ambush broke the patrol and forced a fallback.",
           metadata={
            "category": "sample",
            "kind": "failure",
           },
          ),
         ),
         battle_objective=quest_battle_objective(
          "sample_campaign_tower_objective",
          "hold_position",
          target_party_id="sample_raider_party",
          required_count=1,
          progress=0,
          wave_index=1,
          failure_state="tower_lost",
          required_payload_keys=("road", "route"),
          success_message="The watchtower is secure.",
          failure_message="The tower fell before the patrol could regroup.",
          metadata={
           "category": "sample",
           "kind": "battle_objective",
          },
         ),
         metadata={
          "category": "sample",
          "kind": "blueprint",
         },
        ),
       ),
       conditions=(
        quest_condition(
         "sample_campaign_combat_condition",
         "ambush spotted",
         description="The patrol has spotted the ambush site.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_combat_action",
         "engage raiders",
         description="Fight through the ambush and secure the road.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_combat_trigger",
         "battle started",
         conditions=(),
         actions=(),
         description="Tracks the combat-facing patrol ambush phase.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_combat_reward",
         "road secured",
         description="The road is safe again after the ambush is cleared.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_combat_failure",
         "patrol scattered",
         description="The ambush broke the patrol and forced a fallback.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
       metadata={
        "category": "sample",
        "kind": "blueprint",
       },
      ).to_snapshot(),
      "delivery": quest_delivery_quest(
       "sample_campaign_delivery",
       "Carry the Supply Crates",
       qf_random_quest,
       "Carry crates to the patrol camp and demonstrate the delivery helper.",
       item_name="supply crates",
       destination="the patrol camp",
       stage_title="Deliver the Crates",
       stage_id="sample_campaign_delivery_stage",
       conditions=(
        quest_condition(
         "sample_campaign_contract_condition",
         "contract accepted",
         description="The player has accepted the sample contract.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_assembly_action",
         "assemble patrol",
         description="Bring the patrol together and prepare the route.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_contract_trigger",
         "conversation started",
         conditions=(),
         actions=(),
         description="Marks the quest-giver conversation path for the sample contract.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_route_reward",
         "patrol formed",
         description="The patrol has been assembled and is ready to move.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_route_failure",
         "patrol delayed",
         description="The patrol could not be assembled in time.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       quest_metadata={
        "category": "sample",
        "kind": "delivery",
       },
       stage_metadata={
        "category": "sample",
        "kind": "delivery_stage",
       },
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
      ).to_snapshot(),
      "hunt": quest_hunt_quest(
       "sample_campaign_hunt",
       "Hunt the Raiders",
       qf_random_quest,
       "Track the raiders down and defeat them to demonstrate the hunt helper.",
       target_name="the raiders",
       stage_title="Hunt the Raiders",
       stage_id="sample_campaign_hunt_stage",
       conditions=(
        quest_condition(
         "sample_campaign_contract_condition",
         "contract accepted",
         description="The player has accepted the sample contract.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_combat_action",
         "engage raiders",
         description="Fight through the ambush and secure the road.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_combat_trigger",
         "battle started",
         conditions=(),
         actions=(),
         description="Tracks the combat-facing patrol ambush phase.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_combat_reward",
         "road secured",
         description="The road is safe again after the ambush is cleared.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_combat_failure",
         "patrol scattered",
         description="The ambush broke the patrol and forced a fallback.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       quest_metadata={
        "category": "sample",
        "kind": "hunt",
       },
       stage_metadata={
        "category": "sample",
        "kind": "hunt_stage",
       },
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
      ).to_snapshot(),
      "escort": quest_escort_quest(
       "sample_campaign_escort",
       "Escort the Captain",
       qf_random_quest,
       "Escort the captain to the next watch post to demonstrate the escort helper.",
       person_name="the captain",
       stage_title="Escort the Captain",
       stage_id="sample_campaign_escort_stage",
       conditions=(
        quest_condition(
         "sample_campaign_contract_condition",
         "contract accepted",
         description="The player has accepted the sample contract.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_assembly_action",
         "assemble patrol",
         description="Bring the patrol together and prepare the route.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_contract_end_trigger",
         "conversation ended",
         conditions=(),
         actions=(),
         description="Marks the end of the sample contract conversation path.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_route_reward",
         "patrol formed",
         description="The patrol has been assembled and is ready to move.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_route_failure",
         "patrol delayed",
         description="The patrol could not be assembled in time.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       quest_metadata={
        "category": "sample",
        "kind": "escort",
       },
       stage_metadata={
        "category": "sample",
        "kind": "escort_stage",
       },
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
      ).to_snapshot(),
      "rescue": quest_rescue_quest(
       "sample_campaign_rescue",
       "Rescue the Scout",
       qf_random_quest,
       "Free the captured scout and demonstrate the rescue helper.",
       person_name="the scout",
       stage_title="Rescue the Scout",
       stage_id="sample_campaign_rescue_stage",
       conditions=(
        quest_condition(
         "sample_campaign_combat_condition",
         "ambush spotted",
         description="The patrol has spotted the ambush site.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_combat_action",
         "engage raiders",
         description="Fight through the ambush and secure the road.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_end_trigger",
         "battle ended",
         conditions=(),
         actions=(),
         description="Tracks the campaign wrap-up path.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_combat_reward",
         "road secured",
         description="The road is safe again after the ambush is cleared.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_combat_failure",
         "patrol scattered",
         description="The ambush broke the patrol and forced a fallback.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       quest_metadata={
        "category": "sample",
        "kind": "rescue",
       },
       stage_metadata={
        "category": "sample",
        "kind": "rescue_stage",
       },
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
      ).to_snapshot(),
      "single_stage": quest_template(
       "sample_campaign_single_stage",
       "Single Stage Showcase",
       qf_random_quest,
       "A direct template variant that shows the single-stage quest path.",
       stages=(
        quest_stage(
         "sample_campaign_single_stage_entry",
         "Showcase the Contract",
         "Demonstrate the framework in a compact single-stage setup.",
         description="This keeps the single-stage path visible for the generated module.",
         conditions=(
          quest_condition(
           "sample_campaign_contract_condition",
           "contract accepted",
           description="The player has accepted the sample contract.",
           metadata={
            "category": "sample",
            "kind": "condition",
           },
          ),
        ),
         actions=(
          quest_action(
           "sample_campaign_return_action",
           "deliver report",
           description="Return the report to the captain and close out the campaign.",
           metadata={
            "category": "sample",
            "kind": "action",
           },
          ),
        ),
         battle_hooks=("sample_single_stage_hook",),
         triggers=(
          quest_trigger(
           "sample_campaign_contract_end_trigger",
           "conversation ended",
           conditions=(),
           actions=(),
           description="Marks the end of the sample contract conversation path.",
           metadata={
            "category": "sample",
            "kind": "trigger",
           },
          ),
         ),
         rewards=(
          quest_reward(
           "sample_campaign_wrap_reward",
           "campaign complete",
           description="The sample campaign has reached a successful conclusion.",
           metadata={
            "category": "sample",
            "kind": "reward",
           },
          ),
         ),
         failures=(
          quest_failure(
           "sample_campaign_wrap_failure",
           "report lost",
           description="The final report was lost before the captain could review it.",
           metadata={
            "category": "sample",
            "kind": "failure",
           },
          ),
         ),
         battle_objective=quest_battle_objective(
          "sample_campaign_tower_objective",
          "hold_position",
          target_party_id="sample_raider_party",
          required_count=1,
          progress=0,
          wave_index=1,
          failure_state="tower_lost",
          required_payload_keys=("road", "route"),
          success_message="The watchtower is secure.",
          failure_message="The tower fell before the patrol could regroup.",
          metadata={
           "category": "sample",
           "kind": "battle_objective",
          },
         ),
         metadata={
          "category": "sample",
          "kind": "single_stage",
         },
        ),
       ),
       conditions=(
        quest_condition(
         "sample_campaign_contract_condition",
         "contract accepted",
         description="The player has accepted the sample contract.",
         metadata={
          "category": "sample",
          "kind": "condition",
         },
        ),
       ),
       actions=(
        quest_action(
         "sample_campaign_return_action",
         "deliver report",
         description="Return the report to the captain and close out the campaign.",
         metadata={
          "category": "sample",
          "kind": "action",
         },
        ),
       ),
       triggers=(
        quest_trigger(
         "sample_campaign_contract_end_trigger",
         "conversation ended",
         conditions=(),
         actions=(),
         description="Marks the end of the sample contract conversation path.",
         metadata={
          "category": "sample",
          "kind": "trigger",
         },
        ),
       ),
       rewards=(
        quest_reward(
         "sample_campaign_wrap_reward",
         "campaign complete",
         description="The sample campaign has reached a successful conclusion.",
         metadata={
          "category": "sample",
          "kind": "reward",
         },
        ),
       ),
       failures=(
        quest_failure(
         "sample_campaign_wrap_failure",
         "report lost",
         description="The final report was lost before the captain could review it.",
         metadata={
          "category": "sample",
          "kind": "failure",
         },
        ),
       ),
       npc_state=quest_npc_state(
        "trp_swadian_castle_guard",
        state="available",
        dialogue_state="briefing",
        available_quests=("sample_campaign_briefing",),
        completed_quests=(),
        failed_quests=(),
        locked_chains=("sample_campaign_quests",),
        cooldown_days=0,
        faction_alignment="neutral",
        personality="pragmatic",
        special_flags={
         "sample": True,
         "framework": "npc_state",
        },
        metadata={
         "category": "sample",
         "kind": "npc_state",
        },
       ),
       world_context=quest_world_context(
        "sample_campaign_gate_context",
        location_id="town_gate",
        center_id="sample_town",
        party_id="sample_patrol_party",
        faction_id="sample_faction",
        region="roadside",
        day=12,
        turn=3,
        metadata={
         "category": "sample",
         "kind": "world_context",
        },
       ),
       metadata={
        "category": "sample",
        "framework": "single_stage",
       },
      ).to_snapshot(),
     },
     "battle_objective_preview": quest_battle_objective(
      "sample_campaign_tower_objective",
      "hold_position",
      target_party_id="sample_raider_party",
      required_count=1,
      progress=0,
      wave_index=1,
      failure_state="tower_lost",
      required_payload_keys=("road", "route"),
      success_message="The watchtower is secure.",
      failure_message="The tower fell before the patrol could regroup.",
      metadata={
       "category": "sample",
       "kind": "battle_objective",
      },
     ).to_snapshot(),
     "npc_state_preview": quest_npc_state(
      "trp_swadian_castle_guard",
      state="available",
      dialogue_state="briefing",
      available_quests=("sample_campaign_briefing",),
      completed_quests=(),
      failed_quests=(),
      locked_chains=("sample_campaign_quests",),
      cooldown_days=0,
      faction_alignment="neutral",
      personality="pragmatic",
      special_flags={
       "sample": True,
       "framework": "npc_state",
      },
      metadata={
       "category": "sample",
       "kind": "npc_state",
      },
     ).to_snapshot(),
     "world_context_preview": quest_world_context(
      "sample_campaign_gate_context",
      location_id="town_gate",
      center_id="sample_town",
      party_id="sample_patrol_party",
      faction_id="sample_faction",
      region="roadside",
      day=12,
      turn=3,
      metadata={
       "category": "sample",
       "kind": "world_context",
      },
     ).to_snapshot(),
    },
    stage_metadata={
     "tone": "introductory",
     "sample": True,
    },
   ),
   quest_template_spec(
    "sample_campaign_patrol",
    "Road Patrol",
    qf_random_quest,
    "Escort the patrol, secure the road, and handle the ambush that tests the combat layer.",
    stages=(
     {
      "key": "patrol_assembly",
      "title": "Assemble the Patrol",
      "objective": "Ready the patrol at the gate and brief the squad.",
      "description": "The first patrol stage uses mapping-based authoring to exercise the stage mapping helpers.",
      "conditions": (
       quest_condition(
        "sample_campaign_route_condition",
        "route known",
        description="The patrol route has been identified.",
        metadata={
         "category": "sample",
         "kind": "condition",
        },
       ),
       "squad ready",
      ),
      "actions": (
       quest_action(
        "sample_campaign_assembly_action",
        "assemble patrol",
        description="Bring the patrol together and prepare the route.",
        metadata={
         "category": "sample",
         "kind": "action",
        },
       ),
       "inspect the route",
      ),
      "triggers": (
       quest_trigger(
        "sample_campaign_patrol_trigger",
        "party assembled",
        conditions=(),
        actions=(),
        description="Tracks the patrol assembly phase.",
        metadata={
         "category": "sample",
         "kind": "trigger",
        },
       ),
      ),
      "rewards": (
       quest_reward(
        "sample_campaign_route_reward",
        "patrol formed",
        description="The patrol has been assembled and is ready to move.",
        metadata={
         "category": "sample",
         "kind": "reward",
        },
       ),
      ),
      "failures": (
       quest_failure(
        "sample_campaign_route_failure",
        "patrol delayed",
        description="The patrol could not be assembled in time.",
        metadata={
         "category": "sample",
         "kind": "failure",
        },
       ),
       "patrol delayed",
      ),
      "transitions": {
       "advance": "patrol_ambush",
      },
      "metadata": {
       "phase": "assembly",
       "source": "mapping",
      },
     },
     quest_stage_spec(
      "patrol_ambush",
      "Break the Ambush",
      "Defeat the raiders on the road and keep the patrol intact.",
      description="The second stage exercises the direct stage helper and the combat-facing narrative layer.",
      conditions=(
       quest_condition(
        "sample_campaign_combat_condition",
        "ambush spotted",
        description="The patrol has spotted the ambush site.",
        metadata={
         "category": "sample",
         "kind": "condition",
        },
       ),
      ),
      actions=(
       quest_action(
        "sample_campaign_combat_action",
        "engage raiders",
        description="Fight through the ambush and secure the road.",
        metadata={
         "category": "sample",
         "kind": "action",
        },
       ),
       "secure the road",
       "return to the captain",
      ),
      battle_hooks=("sample_patrol_battle_hook",),
      triggers=(
       quest_trigger(
        "sample_campaign_combat_trigger",
        "battle started",
        conditions=(),
        actions=(),
        description="Tracks the combat-facing patrol ambush phase.",
        metadata={
         "category": "sample",
         "kind": "trigger",
        },
       ),
       quest_trigger(
        "sample_campaign_end_trigger",
        "battle ended",
        conditions=(),
        actions=(),
        description="Tracks the campaign wrap-up path.",
        metadata={
         "category": "sample",
         "kind": "trigger",
        },
       ),
      ),
      rewards=(
       quest_reward(
        "sample_campaign_combat_reward",
        "road secured",
        description="The road is safe again after the ambush is cleared.",
        metadata={
         "category": "sample",
         "kind": "reward",
        },
       ),
       quest_reward(
        "sample_campaign_wrap_reward",
        "campaign complete",
        description="The sample campaign has reached a successful conclusion.",
        metadata={
         "category": "sample",
         "kind": "reward",
        },
       ),
      ),
      failures=(
       quest_failure(
        "sample_campaign_combat_failure",
        "patrol scattered",
        description="The ambush broke the patrol and forced a fallback.",
        metadata={
         "category": "sample",
         "kind": "failure",
        },
       ),
      ),
      transitions={
       "success": "sample_campaign_debrief",
      },
      metadata={
       "phase": "combat",
       "source": "direct",
      },
     ),
    ),
    metadata={
     "category": "sample",
     "framework": "combat",
     "choice_flow": "battle_resolution",
    },
   ),
   quest_template_spec(
    "sample_campaign_debrief",
    "Return the Report",
    qf_random_quest,
    "Bring the report back, resolve the outcome, and collect the final reward or consequence.",
    stage_title="Campaign Debrief",
    stage_objective="Return to the captain and close out the sample campaign.",
    stage_id="sample_campaign_debrief_stage",
    stage_description="This closing stage wraps the sample campaign and demonstrates the single-stage helper fields again.",
    conditions=(
     quest_condition(
      "sample_campaign_contract_condition",
      "contract accepted",
      description="The player has accepted the sample contract.",
      metadata={
       "category": "sample",
       "kind": "condition",
      },
     ),
     "captain present",
    ),
    actions=(
     quest_action(
      "sample_campaign_return_action",
      "deliver report",
      description="Return the report to the captain and close out the campaign.",
      metadata={
       "category": "sample",
       "kind": "action",
      },
     ),
     "claim the reward",
     "record the outcome",
    ),
    triggers=(
     quest_trigger(
      "sample_campaign_contract_end_trigger",
      "conversation ended",
      conditions=(),
      actions=(),
      description="Marks the end of the sample contract conversation path.",
      metadata={
       "category": "sample",
       "kind": "trigger",
      },
     ),
     quest_trigger(
      "sample_campaign_end_trigger",
      "battle ended",
      conditions=(),
      actions=(),
      description="Tracks the campaign wrap-up path.",
      metadata={
       "category": "sample",
       "kind": "trigger",
      },
     ),
    ),
    rewards=(
     quest_reward(
      "sample_campaign_wrap_reward",
      "campaign complete",
      description="The sample campaign has reached a successful conclusion.",
      metadata={
       "category": "sample",
       "kind": "reward",
      },
     ),
    ),
    failures=(
     quest_failure(
      "sample_campaign_wrap_failure",
      "report lost",
      description="The final report was lost before the captain could review it.",
      metadata={
       "category": "sample",
       "kind": "failure",
      },
     ),
     "report lost",
    ),
    transitions={
     "done": "quests_end",
    },
    metadata={
     "category": "sample",
     "framework": "wrap_up",
     "choice_flow": "consequence_resolution",
    },
    stage_metadata={
     "tone": "closing",
     "sample": True,
    },
   ),
  ),
  entry_quest_id="sample_campaign_briefing",
  metadata={
   "category": "sample",
   "framework": "framework_demo",
   "campaign": "sample_campaign",
  },
  quest_metadata={
   "campaign": "sample_campaign",
   "demo": True,
 },
 stage_metadata={
   "campaign": "sample_campaign",
   "demo": True,
  },
 ).as_legacy_tuples(),
 *quest_chain(
  "sample_campaign_authoring_demo",
  "Sample Campaign Authoring Demo",
  quests=SAMPLE_MOTIF_CHAIN.normalized_quests(),
  entry_quest_id=SAMPLE_MOTIF_CHAIN.entry_quest_id,
  branches=SAMPLE_MOTIF_CHAIN.branches,
  metadata={
   "category": "sample",
   "framework": "authoring_demo",
   "registry": SAMPLE_AUTHORING_REGISTRY.snapshot(),
   "bulk_registry": SAMPLE_BULK_AUTHORING_REGISTRY.snapshot(),
   "lane_contract": SAMPLE_LANE_CONTRACT.to_snapshot(),
   "graph": quest_graph_snapshot(SAMPLE_MOTIF_CHAIN),
   "graph_snapshots": SAMPLE_MOTIF_SNAPSHOTS,
   "graph_report": SAMPLE_MOTIF_GRAPH_REPORT,
   "graph_mermaid": SAMPLE_MOTIF_MERMAID,
   "graph_dot": SAMPLE_MOTIF_DOT,
   "dsl_previews": {
    "reward_bundle": [reward.to_snapshot() for reward in SAMPLE_DSL_REWARDS],
    "failure_bundle": [failure.to_snapshot() for failure in SAMPLE_DSL_FAILURES],
    "branch": {
     "branch_id": SAMPLE_DSL_BRANCH.branch_id,
     "from_stage": SAMPLE_DSL_BRANCH.from_stage,
     "to_stage": SAMPLE_DSL_BRANCH.to_stage,
     "condition": SAMPLE_DSL_BRANCH.condition,
     "description": SAMPLE_DSL_BRANCH.description,
     "metadata": dict(SAMPLE_DSL_BRANCH.metadata),
    },
    "optional_stage": SAMPLE_DSL_OPTIONAL_STAGE.to_snapshot(),
    "timed_stage": SAMPLE_DSL_TIMED_STAGE.to_snapshot(),
    "repeatable_stage": SAMPLE_DSL_REPEATABLE_STAGE.to_snapshot(),
   },
  },
 ).as_legacy_tuples(),
]
