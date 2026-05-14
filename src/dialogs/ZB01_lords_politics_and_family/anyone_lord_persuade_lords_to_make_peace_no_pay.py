DIALOGS = [
[anyone , "lord_persuade_lords_to_make_peace_no_pay", [],
   "You have done what councils, priests, and exhausted captains could not.\
 This war has eaten enough sons; refusing payment for ending it will be remembered longer than any purse I could press into your hand.\
 I will not insult the deed by arguing. Take our respect, and the quieter streets you helped return.", "close_window",
   [
    (call_script, "script_change_player_honor", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 8),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    ]],
]
