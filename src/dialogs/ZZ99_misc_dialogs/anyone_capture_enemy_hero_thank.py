DIALOGS = [
[anyone, "capture_enemy_hero_thank", [],
   "Many thanks, my friend. He will serve very well for a bargain. You've done a fine work here. Please accept these {reg5} denars for your help.", "capture_enemy_hero_thank_2",
   [(quest_get_slot, ":quest_target_troop", "qst_capture_enemy_hero", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_faction", "qst_capture_enemy_hero", slot_quest_target_faction),
     (party_remove_prisoners, "p_main_party", ":quest_target_troop", 1),
     (store_relation, ":reln", "$g_encountered_party_faction", ":quest_target_faction"),
     (try_begin),
       (lt, ":reln", 0),
       (party_add_prisoners, "$g_encountered_party", ":quest_target_troop", 1), #Adding him to the dungeon
     (else_try),
       #Do not add a non-enemy lord to the dungeon (due to recent diplomatic changes or due to a neutral town/castle)
       (troop_set_slot, ":quest_target_troop", slot_troop_prisoner_of_party, -1),
     (try_end),
     (quest_get_slot, ":reward", "qst_capture_enemy_hero", slot_quest_gold_reward),
     (call_script, "script_troop_add_gold", "trp_player", ":reward"),
     (add_xp_as_reward, 2500),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
     (call_script, "script_end_quest", "qst_capture_enemy_hero"),
   ]],
]
