DIALOGS = [
[anyone , "start", [(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                     (check_quest_active, "qst_join_faction"),
                     (eq, "$g_invite_faction_lord", "$g_talk_troop"),
                     (try_begin),
                       (gt, "$g_invite_offered_center", 0),
                       (store_faction_of_party, ":offered_center_faction", "$g_invite_offered_center"),
                       (neq, ":offered_center_faction", "$g_talk_troop_faction"),
                       (call_script, "script_get_poorest_village_of_faction", "$g_talk_troop_faction"),
                       (assign, "$g_invite_offered_center", reg0),
                     (try_end),
                     ],
   #TODO: change conversations according to relation.
   "{playername}, I've been expecting you. Word has reached my ears of your exploits.\
 Why, I keep hearing such tales of prowess and bravery that my mind was quickly made up.\
 I knew that I had found someone worthy of becoming my vassal.", "lord_invite_1",
   []],
]
