DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_incriminate_loyal_commander"),
                         (check_quest_failed, "qst_incriminate_loyal_commander")],
   "You werent't able to complete a simple task. I had set up everything.\
 The only thing you needed to do was sacrifice a messenger, and we would be celebrating now.\
 But no, you were too damned honorable, weren't you?", "close_window", [
     (call_script, "script_end_quest", "qst_incriminate_loyal_commander"),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5),
     (call_script, "script_change_player_honor", 3),
 ]],
]
