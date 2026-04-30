DIALOGS = [
[anyone , "knight_join_party_disband", [], "Ah . . . Very well, {playername}. Much as I dislike losing good men,\
 the decision is yours. I'll disband my troops and join you.", "close_window", [
      (call_script, "script_recruit_troop_as_companion", "$g_talk_troop"),

      (troop_get_slot, ":companions_party", "$g_talk_troop", slot_troop_leaded_party),
      (party_detach, ":companions_party"),
      (remove_party, ":companions_party"),
      (assign, "$g_leave_encounter", 1)
      ]],
]
