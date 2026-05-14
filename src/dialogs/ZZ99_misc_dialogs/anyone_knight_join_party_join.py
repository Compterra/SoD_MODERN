DIALOGS = [
[anyone , "knight_join_party_join", [], "Excellent.\
 My lads and I will ride with you.", "close_window", [
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),
      (party_remove_members, "p_main_party", "$g_talk_troop", 1),

      (troop_get_slot, ":companions_party", "$g_talk_troop", slot_troop_leaded_party),
      (assign, "$g_move_heroes", 1),
      (try_begin),
        (gt, ":companions_party", 0),
        (neq, ":companions_party", "p_main_party"),
        (party_is_active, ":companions_party"),
        (call_script, "script_party_add_party", "p_main_party", ":companions_party"),
        (party_detach, ":companions_party"),
        (remove_party, ":companions_party"),
      (try_end),
      (assign, "$g_leave_encounter", 1)
      ]],
]
