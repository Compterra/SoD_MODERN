DIALOGS = [
[anyone|plyr, "gm_talk", [(store_partner_quest, "$g_gm_quest"),
                                                 (this_or_next|eq, "$g_gm_quest", "qst_serpent_host_raise_troops"),
                                                 (this_or_next|eq, "$g_gm_quest", "qst_bc_raise_troops"),
												(this_or_next|eq, "$g_gm_quest", "qst_black_army_raise_troops"),
												 (eq, "$g_gm_quest", "qst_conquistadors_raise_troops"),
                                                 (quest_get_slot, ":quest_target_amount", "$g_gm_quest", slot_quest_target_amount),
												 (quest_get_slot, ":quest_target_troop", "$g_gm_quest", slot_quest_target_troop),
                                                 (party_count_companions_of_type, ":num_companions", "p_main_party", ":quest_target_troop"),
												(ge, ":num_companions", ":quest_target_amount"),
												(assign, reg1, ":quest_target_amount"),
												(str_store_troop_name_plural, s13, ":quest_target_troop")
                                                 ],
   "I brought you {reg1} {s13}.", "gm_raise_troops_thank",
   []],
]
