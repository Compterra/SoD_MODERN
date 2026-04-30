DIALOGS = [
[anyone|plyr, "lost_sh_spy_4", [(store_troop_gold, ":gold"),
                                          (quest_get_slot, ":quest_target_amount", "qst_serpent_host_free_spy", slot_quest_target_amount),
                                          (ge, ":gold", ":quest_target_amount"),
                                          ],
   "Of course. Here you are...", "sh_quest_about_job_5a", [(quest_get_slot, ":quest_target_amount", "qst_serpent_host_free_spy", slot_quest_target_amount),
                                                                (troop_remove_gold, "trp_player", ":quest_target_amount"), (play_sound, "snd_money_paid"),
                                                                ]],
]
