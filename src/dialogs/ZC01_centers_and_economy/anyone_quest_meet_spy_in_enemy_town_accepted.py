DIALOGS = [
[anyone, "quest_meet_spy_in_enemy_town_accepted", [], "Then go to {s13} quickly, and remember that a spy who waits too long starts looking like a corpse or a trap.", "quest_meet_spy_in_enemy_town_accepted_response",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":secret_sign", "$random_quest_no", slot_quest_target_amount),
     (store_sub, ":countersign", ":secret_sign", secret_signs_begin),
     (val_add, ":countersign", countersigns_begin),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_string, s11, ":secret_sign"),
     (str_store_string, s12, ":countersign"),
     (str_store_party_name_link, s13, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} has asked you to meet with a spy in {s13}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_cf_center_get_free_walker", ":quest_target_center"),
     (call_script, "script_center_set_walker_to_type", ":quest_target_center", reg0, walkert_spy),
     (str_store_item_name, s14, "$spy_item_worn"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1),
    ]],
]
