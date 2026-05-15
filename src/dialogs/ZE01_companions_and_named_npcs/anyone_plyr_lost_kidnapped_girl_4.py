DIALOGS = [
[anyone|plyr, "lost_kidnapped_girl_4", [(store_troop_gold, ":gold", "trp_player"),
                                          (gt, "$g_sod_lost_rescue_repayment_amount", 0),
                                          (ge, ":gold", "$g_sod_lost_rescue_repayment_amount"),
                                          ],
   "Of course. Here you are.", "merchant_quest_about_job_5a", [(call_script, "script_sod_player_charge_gold", "$g_sod_lost_rescue_repayment_amount"),
                                                                (play_sound, "snd_money_paid"),
                                                                (assign, "$g_sod_lost_rescue_repayment_amount", 0),
                                                                ]],
]
