DIALOGS = [
[anyone, "mayor_begin", [(check_quest_active, "qst_troublesome_bandits"),
                          (check_quest_succeeded, "qst_troublesome_bandits"),
                          (quest_slot_eq, "qst_troublesome_bandits", slot_quest_giver_troop, "$g_talk_troop"),
                          ],
   "I have heard about your deeds. You have given those bandits the punishment they deserved.\
 You are really as good as they say.\
 Here is your reward: {reg5} denars.\
 I would like to give more but those bandits almost brought me to bankruptcy.",
   "mayor_friendly_pretalk", [(quest_get_slot, ":quest_gold_reward", "qst_troublesome_bandits", slot_quest_gold_reward),
                              (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                              (assign, ":xp_reward", ":quest_gold_reward"),
                              (val_mul, ":xp_reward", 7),
                              (add_xp_as_reward, ":xp_reward"),
                              (call_script, "script_change_player_relation_with_center", "$current_town", 2),
                              (call_script, "script_change_troop_renown", "trp_player", 3),
                              (call_script, "script_end_quest", "qst_troublesome_bandits"),
                              (assign, reg5, ":quest_gold_reward"),
                              ]],
]
