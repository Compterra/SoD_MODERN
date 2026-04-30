DIALOGS = [
[anyone, "lady_quest_duel_for_lady_3_rejected", [], "Oh... Perhaps you're right, {playername}.\
 I should let go of these silly childhood ideas of chivalry and courage. {Men/People} are not like that,\
 not anymore. Good day to you.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    ]],
]
