DIALOGS = [
[anyone, "lord_mission_collect_taxes_accepted", [], "Welcome news, {playername}.\
 I will entrust this matter to you.\
 Remember, those {reg9?townsmen:peasants} are foxy beasts, they will make every excuse not to pay me my rightful incomes.\
 Do not let them fool you.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
    (assign, "$g_leave_encounter", 1),
    (assign, reg9, 0),
    (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
    (try_begin),
      (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
      (assign, reg9, 1),
    (try_end),
   ]],
]
