DIALOGS = [
[anyone, "gm_tell_mission", [
  (this_or_next|eq, "$random_quest_no", "qst_black_army_fight_guild_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_conquistadors_fight_guild_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_elephant_guard_fight_guild_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_jotnar_clan_fight_guild_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_serpent_host_fight_guild_troops"),
  (this_or_next|eq, "$random_quest_no", "qst_serpent_host_fight_guild_troops_2"),
  (this_or_next|eq, "$random_quest_no", "qst_slavers_fight_guild_troops"),
  (eq, "$random_quest_no", "qst_bc_fight_guild_troops"),
  (quest_get_slot, ":message_text", "$random_quest_no", slot_quest_apply),
  (str_store_string, s15, ":message_text"),
  ],
   "{s15}", "gm_tell_mission_fight_troops", [
     ]],
]
