DIALOGS = [
[anyone, "gm_tell_mission", [(this_or_next|eq, "$random_quest_no", "qst_serpent_host_raise_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_black_army_raise_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_bc_raise_troops"),
  (eq, "$random_quest_no", "qst_conquistadors_raise_troops"),
  (faction_get_slot, ":message_text", "$g_talk_troop_faction", slot_guild_raise_troops_text),
  (str_store_string, s15, ":message_text"),
  ],
   "{s15}", "gm_tell_mission_raise_troops", [
     ]],
]
