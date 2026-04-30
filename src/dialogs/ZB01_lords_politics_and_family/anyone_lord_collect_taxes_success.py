DIALOGS = [
[anyone, "lord_collect_taxes_success", [(quest_get_slot, ":total_revenue", "qst_collect_taxes", slot_quest_gold_reward),
                                         (store_mul, ":owner_share", ":total_revenue", 8),
                                         (val_div, ":owner_share", 10),
                                         (assign, reg20, ":owner_share"),
                                         (store_sub, reg21, ":total_revenue", ":owner_share")],
   "Well done, {playername}, very well done indeed! You were truly the right {man/person} for the job.\
 I promised you a fifth of the taxes, so that amounts to {reg21} denars.\
 If you give me {reg20} denars, you may keep the difference.\
 A good result for everyone, eh?", "lord_pretalk",
   [
    (troop_remove_gold, "trp_player", reg20),
    (play_sound, "snd_money_paid"),
    (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, 0),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 4),
    (call_script, "script_end_quest", "qst_collect_taxes"),
    ]],
]
