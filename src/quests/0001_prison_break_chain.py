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
  "prison_break_chain",
  "Prison Break Chain",
  quests=(
   quest_template_spec(
    "slave_q1",
    "Deliver message to {s13}",
    0,
    "Diego, a village elder imprisoned by the Slavers, asked you to take a message to his old friend {s13}.",
    stage_title="Deliver Diego's Message",
    stage_objective="Take Diego's message to {s13}.",
    stage_description="Travel to the target and deliver the message from Diego.",
    metadata={
     "category": "story",
     "authoring": "schema",
     "chain": "prison_break_chain",
     "sequence": 1,
    },
    stage_metadata={
     "phase": "intro",
     "tracking": "delivery",
    },
   ),
   quest_template_spec(
    "slave_q2",
    "Return to Diego with the bad news",
    0,
    "The lord you spoke with refused to help Diego directly. Return to Diego and tell him the bad news.",
    stage_title="Report Back to Diego",
    stage_objective="Return to Diego with the bad news.",
    stage_description="Tell Diego that his request was denied and close out the failed diplomacy step.",
    metadata={
     "category": "story",
     "authoring": "schema",
     "chain": "prison_break_chain",
     "sequence": 2,
    },
    stage_metadata={
     "phase": "followup",
     "tracking": "reporting",
    },
   ),
   quest_template_spec(
    "slave_q3",
    "Prison Break",
    0,
    "Free Diego and fight your way out of the dungeon.",
    stage_title="Break Out of the Dungeon",
    stage_objective="Free Diego and escape the dungeon.",
    stage_description="Force a breakout, secure Diego, and fight through the escape route.",
    metadata={
     "category": "story",
     "authoring": "schema",
     "chain": "prison_break_chain",
     "sequence": 3,
    },
    stage_metadata={
     "phase": "escape",
     "tracking": "rescue",
    },
   ),
  ),
  metadata={
   "category": "story",
   "authoring": "schema",
   "legacy_fragment": "0001_prison_break_chain",
   "converted_from": "legacy_tuple_fragment",
  },
 ).as_legacy_tuples(),
]
