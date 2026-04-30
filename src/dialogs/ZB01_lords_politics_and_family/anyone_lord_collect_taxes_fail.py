DIALOGS = [
[anyone, "lord_collect_taxes_fail", [],
   "God, what a bloody mess you've gotten us into, {playername}.\
This could turn very ugly if I do not take immediate action.\
I certainly hope you're not here expecting to be paid for failure.\
Hand over my {reg19} denars, if you please, and end our business together.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (quest_get_slot, ":gold_reward", "qst_collect_taxes", slot_quest_gold_reward),
    (troop_remove_gold, "trp_player", ":gold_reward"),
    (play_sound, "snd_money_paid"),
    (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, 0),
    (call_script, "script_end_quest", "qst_collect_taxes"),
    ]],
]
