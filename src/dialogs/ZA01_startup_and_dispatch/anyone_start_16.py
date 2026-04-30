DIALOGS = [
[anyone, "start", [
					(store_relation, ":rel", "fac_player_faction", "$g_talk_troop_faction"),
					(talk_info_set_relation_bar, ":rel"),
		(check_quest_active, "qst_jotnar_clan_escort"),
		(check_quest_failed, "qst_jotnar_clan_escort"),
		(quest_slot_eq, "qst_jotnar_clan_escort", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "You disappoint me, {playername}!", "close_window",
   [
    (call_script, "script_change_troop_renown", "trp_player", -3),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -10),
    (call_script, "script_fail_quest", "qst_jotnar_clan_escort"),
    (call_script, "script_end_quest", "qst_jotnar_clan_escort"),
  (finish_mission),
    ]],
]
