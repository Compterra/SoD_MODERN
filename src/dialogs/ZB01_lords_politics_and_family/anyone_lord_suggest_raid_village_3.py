DIALOGS = [
[anyone, "lord_suggest_raid_village_3", [(str_store_party_name, s1, "$suggested_to_attack_center")],
   "That should be possible. Very well, we'll attack {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_raiding_around_center, "$suggested_to_attack_center"),
       ]],
]
