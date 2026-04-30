DIALOGS = [
[anyone, "quest_meet_spy_in_enemy_town_completed_2", [],
   "Ahh, well done. It's good to have competent {men/people} on my side. Here is the payment I promised you.", "lord_pretalk",
   [
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     (add_xp_as_reward, 500),
     (quest_get_slot, ":gold", "qst_meet_spy_in_enemy_town", slot_quest_gold_reward),
     (call_script, "script_troop_add_gold", "trp_player", ":gold"),
     (call_script, "script_end_quest", "qst_meet_spy_in_enemy_town"),
     ]],
]
