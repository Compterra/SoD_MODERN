DIALOGS = [
[anyone|plyr, "lord_talk", [(eq, "$talk_context", tc_party_encounter),
                             (lt, "$g_encountered_party_relation", 0),
                             (call_script, "script_store_troop_name", s4, "$g_talk_troop")],
   "I say this only once, {s4}! Surrender or die!", "party_encounter_lord_hostile_ultimatum_surrender", []],
]
