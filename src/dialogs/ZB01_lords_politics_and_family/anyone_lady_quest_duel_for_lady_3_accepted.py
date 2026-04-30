DIALOGS = [
[anyone, "lady_quest_duel_for_lady_3_accepted", [], "Oh! I can't ask that of you, {playername}, but...\
 I would be forever indebted to you, and you are so sure. It would mean so much if you would defend my honour.\
 Thank you a thousand times, all my prayers and my favour go with you.", "close_window",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_report_quest_troop_positions", "$random_quest_no", ":quest_target_troop", 3),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     ]],
]
