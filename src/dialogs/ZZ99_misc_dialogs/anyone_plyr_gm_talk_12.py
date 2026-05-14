DIALOGS = [
[anyone|plyr, "gm_talk", [
   (check_quest_active, "qst_jotnar_clan_competition"),
   (eq,"$g_talk_troop", jotnar_clan_guild_master),
   ], "I am ready join this competition.", "close_window", [
   (jump_to_menu, "mnu_jotnar_clan_competition"),
   (finish_mission),
   ],],
]
