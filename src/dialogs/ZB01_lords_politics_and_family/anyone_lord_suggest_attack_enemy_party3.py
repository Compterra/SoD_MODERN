DIALOGS = [
[anyone, "lord_suggest_attack_enemy_party3", [
       (str_store_party_name, 1, "$suggested_to_attack_party"),
       (call_script, "script_sod_lord_get_battle_willingness", "$g_talk_troop", "$suggested_to_attack_party"),
       (assign, ":sod_battle_willingness", reg0),
       (ge, ":sod_battle_willingness", 25),
       ],
   "Then we put steel where the war can feel it. I will move on {s1}, and let their scouts carry the fear ahead of us.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_engaging_army, "$suggested_to_attack_party"),
       ]],
[anyone, "lord_suggest_attack_enemy_party3", [
       (str_store_party_name, 1, "$suggested_to_attack_party"),
       (call_script, "script_sod_lord_get_battle_willingness", "$g_talk_troop", "$suggested_to_attack_party"),
       (assign, ":sod_battle_willingness", reg0),
       (lt, ":sod_battle_willingness", 25),
       ],
   "Not with my men in this state. They will not stand for a hopeless field.", "lord_pretalk",
   [
       (store_current_day, ":cur_day"),
       (troop_set_slot, "$g_talk_troop", slot_troop_sod_lord_last_battle_refusal_day, ":cur_day"),
       ]],
]
