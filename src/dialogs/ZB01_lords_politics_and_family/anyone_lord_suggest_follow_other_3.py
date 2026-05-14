DIALOGS = [
[anyone, "lord_suggest_follow_other_3", [(str_store_party_name, 1, "$town_suggested_to_go_to")],
   "I will put my banner beside {s1}. If the army frays, at least one more lord will be close enough to stitch it back together.", "lord_pretalk",
   [
       (party_set_slot, "$g_talk_troop_party", slot_party_commander_party, "$town_suggested_to_go_to"),
       (call_script, "script_party_decide_next_ai_state_under_command", "$g_talk_troop_party"),
       ]],
]
