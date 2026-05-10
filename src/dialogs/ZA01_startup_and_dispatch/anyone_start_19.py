DIALOGS = [
[anyone, "start", [(store_partner_quest, ":lords_quest"),
						(this_or_next|eq, ":lords_quest", "qst_elephant_guard_troublesome_bandits"),
						(this_or_next|eq, ":lords_quest", "qst_serpent_host_troublesome_bandits"),
						(this_or_next|eq, ":lords_quest", "qst_bc_troublesome_bandits"),
						(this_or_next|eq, ":lords_quest", "qst_jotnar_clan_free_clansmen"),
						(eq, ":lords_quest", "qst_conquistadors_troublesome_bandits"),
                          (check_quest_succeeded, ":lords_quest"),
                          (quest_slot_eq, ":lords_quest", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "I have heard about your deeds. You have given those bandits the punishment they deserved.\
 You are really as good as they say.", "gm_pretalk", [
							(store_partner_quest, ":lords_quest"),
							  (quest_get_slot, ":quest_gold_reward", ":lords_quest", slot_quest_gold_reward),
                              (assign, ":xp_reward", ":quest_gold_reward"),
							  (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                              (val_mul, ":xp_reward", 10),
                              (add_xp_as_reward, ":xp_reward"),
                              (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 5),
                              (call_script, "script_change_troop_renown", "trp_player", 3),
                              (call_script, "script_succeed_quest", ":lords_quest"),
                              (call_script, "script_end_quest", ":lords_quest"),
                              ]],
]
