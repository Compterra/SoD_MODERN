DIALOGS = [
[anyone, "lord_suggest_attack_enemy_party3", [(str_store_party_name, 1, "$suggested_to_attack_party")],
   "As you wish, we will attack {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_engaging_army, "$suggested_to_attack_party"),
       ]],
]
