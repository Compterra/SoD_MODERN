DIALOGS = [
[anyone,"start", [(eq,"$g_talk_troop", elephant_guard_guild_master),(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
	(check_quest_succeeded, "qst_elephant_guard_train_peasants_against_bandits"),
  ],"Thank you, {playername}. Now we have greater chances to survive here.", "gm_pretalk",[
  (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 7),
  (complete_quest, "qst_elephant_guard_train_peasants_against_bandits"),
  (add_xp_as_reward, 800),
  (call_script, "script_succeed_quest", "qst_elephant_guard_train_peasants_against_bandits"),
  (call_script, "script_end_quest", "qst_elephant_guard_train_peasants_against_bandits"),
  ]],
]
