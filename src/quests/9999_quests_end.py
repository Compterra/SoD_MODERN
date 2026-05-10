# Keep the terminal quest sentinel in its own final fragment.
# Several quest-chain helpers use "quests_end" as the terminal transition target.

QUESTS = [
 *quest_chain_from_specs(
  "quest_terminal_sentinel",
  "Quest Terminal Sentinel",
  quests=(
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
