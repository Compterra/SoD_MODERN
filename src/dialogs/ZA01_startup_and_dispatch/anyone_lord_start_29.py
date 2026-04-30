DIALOGS = [
[anyone, "lord_start", [(party_slot_eq, "$g_encountered_party", slot_town_lord, "$g_talk_troop"), #we are talking to Town's Lord.
                         (ge, "$g_talk_troop_faction_relation", 0),
                         (neq, "$g_ransom_offer_rejected", 1),
                         (lt, "$g_encountered_party_2", 0), #town is not under siege
                         (hero_can_join_as_prisoner, "$g_encountered_party"),
                         (store_random_in_range, ":random_no", 0, 100),
                         (lt, ":random_no", 10), #start this conversation with a 10% chance
                         (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_main_party"),
                         (assign, "$prisoner_lord_to_buy", -1),
                         (try_for_range, ":i_pris_stack", 0, ":num_prisoner_stacks"),
                           (party_prisoner_stack_get_troop_id, ":t_id", "p_main_party", ":i_pris_stack"),
                           (troop_slot_eq, ":t_id", slot_troop_occupation, slto_kingdom_hero),
                           (store_troop_faction, ":fac", ":t_id"),
                           (store_relation, ":rel", ":fac", "$g_talk_troop_faction"),
                           (lt,  ":rel", 0),
                           (assign, "$prisoner_lord_to_buy", ":t_id"),
                         (try_end),
                         (gt, "$prisoner_lord_to_buy", 0), #we have a prisoner lord.
                         (assign, ":continue", 1),
                         (try_begin),
                           (check_quest_active, "qst_capture_enemy_hero"),
                           (store_troop_faction, ":prisoner_faction", "$prisoner_lord_to_buy"),
                           (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":prisoner_faction"),
                           (assign, ":continue", 0),
                         (try_end),
                         (eq, ":continue", 1),
                         (call_script, "script_store_troop_name", s3, "$prisoner_lord_to_buy"),
                         (assign, reg5, "$prisoner_lord_to_buy"),
                         (call_script, "script_calculate_ransom_amount_for_troop", "$prisoner_lord_to_buy"),
                         (assign, reg6, reg0),
                         (val_div, reg6, 2),
                         (assign, "$temp", reg6),
                         ],
   "I heard that you have captured our enemy {s3} and he is with you at the moment.\
 I can pay you {reg6} denars for him if you want to get rid of him.\
 You can wait for his family to pay his ransom of course, but there is no telling how long that will take, eh?\
", "lord_buy_prisoner", []],
]
