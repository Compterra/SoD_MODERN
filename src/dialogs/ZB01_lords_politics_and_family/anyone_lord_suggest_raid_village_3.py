DIALOGS = [
[anyone, "lord_suggest_raid_village_3", [(str_store_party_name, s1, "$suggested_to_attack_center")],
   "A hard order, but war is fed by hard orders. We ride for {s1}, and their lord can count the smoke.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_raiding_around_center, "$suggested_to_attack_center"),
       ]],
]
