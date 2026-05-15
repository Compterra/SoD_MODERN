DIALOGS = [
[anyone|plyr, "jotnar_clansmen", [
   (check_quest_active, "qst_jotnar_clan_free_clansmen"),
   (neg|check_quest_concluded, "qst_jotnar_clan_free_clansmen"),
   (quest_slot_eq, "qst_jotnar_clan_free_clansmen", slot_quest_target_party, "$g_encountered_party"),
   (party_is_active, "$g_encountered_party"),
   ],
   "Yes. Stay close and I will get you home.", "close_window", [(assign, "$g_leave_encounter", 1),
   (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
   (party_set_ai_object, "$g_encountered_party", "p_main_party"),
   (party_set_flags, "$g_encountered_party", pf_default_behavior, 0),
   (call_script, "script_sod_companion_dispatch_player_action", sod_companion_action_free_captives, 1),
   ]],
]
