DIALOGS = [
[anyone, "lord_suggets_attack_enemy_castle3", [(str_store_party_name, 1, "$suggested_to_attack_center")],
   "That should be possible. Very well, we'll attack {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_besieging_center, "$suggested_to_attack_center"),

       ]],
]
