DIALOGS = [
[anyone , "town_dweller_quest_meet_spy_in_enemy_town",
   [
     (call_script, "script_agent_get_town_walker_details", "$g_talk_agent"),
     (assign, ":walker_type", reg0),
     (eq, ":walker_type", walkert_spy),
     (quest_get_slot, ":secret_sign", "qst_meet_spy_in_enemy_town", slot_quest_target_amount),
     (val_sub, ":secret_sign", secret_signs_begin),
     (eq, ":secret_sign", "$temp"),
     (store_add, ":countersign", ":secret_sign", countersigns_begin),
     (str_store_string, s4, ":countersign"),
     ],
   "{s4}", "town_dweller_quest_meet_spy_in_enemy_town_know", []],
]
