DIALOGS = [
[anyone , "lord_persuade_lords_to_make_peace_no_pay", [],
   "You are indeed an extraordinary person, {sir/madame}, and it is an honour for me to have known you.\
 You not only did what was impossible and put an end to this terrible war, but you won't even accept a reward for it.\
 Very well, I will not insist on the matter, but please know that you will have our eternal respect and gratitude.", "close_window",
   [
    (call_script, "script_change_player_honor", 3),
    (call_script, "script_change_player_relation_with_center", "$current_town", 8),
    (call_script, "script_end_quest", "qst_persuade_lords_to_make_peace"),
    ]],
]