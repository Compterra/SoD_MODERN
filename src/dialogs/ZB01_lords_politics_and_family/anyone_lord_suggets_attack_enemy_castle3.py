DIALOGS = [
[anyone, "lord_suggets_attack_enemy_castle3", [
       (str_store_party_name, 1, "$suggested_to_attack_center"),
       (call_script, "script_sod_lord_get_battle_willingness", "$g_talk_troop", "$suggested_to_attack_center"),
       (assign, ":sod_battle_willingness", reg0),
       (ge, ":sod_battle_willingness", 25),
       ],
   "That should be possible. Very well, we'll attack {s1}.", "lord_pretalk",
   [
       (call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_besieging_center, "$suggested_to_attack_center"),

       ]],
[anyone, "lord_suggets_attack_enemy_castle3", [
       (str_store_party_name, 1, "$suggested_to_attack_center"),
       (call_script, "script_sod_lord_get_battle_willingness", "$g_talk_troop", "$suggested_to_attack_center"),
       (assign, ":sod_battle_willingness", reg0),
       (lt, ":sod_battle_willingness", 25),
       ],
   "Not now. My household is too strained for an assault like that.", "lord_pretalk",
   [
       (store_current_day, ":cur_day"),
       (troop_set_slot, "$g_talk_troop", slot_troop_sod_lord_last_battle_refusal_day, ":cur_day"),
       ]],
]
