DIALOGS = [
[anyone|plyr, "lost_kidnapped_girl_4", [(store_troop_gold, ":gold"),
                                          (quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                          (ge, ":gold", ":quest_target_amount"),
                                          ],
   "Of course. Here you are...", "merchant_quest_about_job_5a", [(quest_get_slot, ":quest_target_amount", "qst_kidnapped_girl", slot_quest_target_amount),
                                                                (call_script, "script_sod_player_charge_gold", ":quest_target_amount"), (play_sound, "snd_money_paid"),
                                                                ]],
]
