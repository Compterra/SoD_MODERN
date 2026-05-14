DIALOGS = [
[anyone, "lord_suggest_go_to_friendly_town3", [(str_store_party_name, 1, "$town_suggested_to_go_to")],
   "Then {s1} becomes our anchor. A rested host obeys orders better than a hungry one.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_holding_center, "$town_suggested_to_go_to"),
       ]],
]
