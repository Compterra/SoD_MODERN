DIALOGS = [
[anyone, "lord_suggest_go_to_friendly_town3", [(str_store_party_name, 1, "$town_suggested_to_go_to")],
   "Very well, we go to {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_holding_center, "$town_suggested_to_go_to"),
       ]],
]
