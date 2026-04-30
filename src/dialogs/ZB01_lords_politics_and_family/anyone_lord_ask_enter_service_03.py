DIALOGS = [
[anyone, "lord_ask_enter_service",
   [
     (assign, "$g_invite_offered_center", -1),
     (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
     (store_mul, ":vassal_potential", "$g_talk_troop_relation", 5),
     (val_add, ":vassal_potential", ":renown"),
     (call_script, "script_get_number_of_hero_centers", "trp_player"),
     (assign, ":num_centers_owned", reg0),
     (store_mul, ":center_affect", ":num_centers_owned", 50),
     (val_add, ":vassal_potential", ":center_affect"),
     (ge, ":vassal_potential", 150),
     (try_begin),
       (eq, ":num_centers_owned", 0),
       (call_script, "script_get_poorest_village_of_faction", "$g_talk_troop_faction"),
       (gt, reg0, 0),
       (assign, "$g_invite_offered_center", reg0),
     (try_end),
     ],
   "You are known as a brave {man-at-arms/warrior} and a fine leader of men, {playername}.\
 I shall be pleased to accept your sword into my service and bestow vassalage upon you,\
 if you are ready to swear homage to me.", "lord_give_oath_1", []],
]
