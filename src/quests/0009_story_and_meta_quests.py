# -*- coding: utf-8 -*-
# Auto-generated from src/quests/0001_all_quests.py.
# Keep quest definitions in the numbered fragments and rebuild with build/build_quests.py.
#
# Schema-backed authoring example:
# - quest_chain_from_specs groups related quests
# - quest_template_spec captures the legacy quest tuple shape plus richer metadata
# - quest_stage_spec keeps stage authoring compact for future runtime integration

QUESTS = [
 *quest_chain_from_specs(
  "story_and_meta_quests",
  "Story and Meta Quests",
  quests=(
   quest_template_spec(
    "regional_threat_contract",
    "Regional Threat Contract",
    qf_random_quest,
    "You accepted a regional threat-board contract. Track down the marked warband, defeat it, and return to any threat board to claim the posted reward.",
    stages=(
     quest_stage_spec(
      "stage_1",
      "Hunt the Threat",
      "Find and defeat the marked warband.",
      description="Pursue the target and clear the contract objective.",
      conditions=(
       "contract accepted",
       "warband tracked",
      ),
      actions=(
       "travel to marked target",
       "defeat warband",
       "return to threat board",
      ),
      rewards=(
       "posted reward",
      ),
      metadata={
       "phase": "hunt",
       "tracking": "contract",
      },
     ),
    ),
    metadata={
     "category": "story",
     "authoring": "schema",
    },
   ),
   quest_template_spec(
    "join_faction",
    "Give Oath of Homage to {s1}",
    qf_random_quest,
    "Find {s1} and give him your oath of homage.",
    metadata={
     "category": "story",
     "authoring": "schema",
    },
   ),
   quest_template_spec(
    "rebel_against_kingdom",
    "Help {s13} Claim the Throne of {s14}",
    qf_random_quest,
    "None",
    metadata={
     "category": "story",
     "authoring": "schema",
    },
   ),
   quest_template_spec(
    "quests_end",
    "Quests End",
    0,
    ".",
    metadata={
     "category": "meta",
     "authoring": "schema",
     "sentinel": True,
    },
   ),
  ),
 ).as_legacy_tuples(),
]
