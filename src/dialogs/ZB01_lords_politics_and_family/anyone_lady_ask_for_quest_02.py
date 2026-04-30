DIALOGS = [
[anyone, "lady_ask_for_quest", [(eq, "$random_quest_no", "qst_rescue_lord_by_replace")],
   "Oh, I fear I may never see my {s17}, {s13}, again... He is a prisoner in the dungeon of {s14}.\
 We have tried to negotiate his ransom, but it has been set too high.\
 We can never hope to raise that much money without selling everything we own,\
 and God knows {s13} would rather spend his life in prison than make us destitute.\
 Instead I came up with a plan to get him out of there, but it requires someone to make a great sacrifice,\
 and so far my pleas have fallen on deaf ears...", "lady_mission_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (try_begin),
       (troop_get_slot, ":cur_lord", "$g_talk_troop", slot_troop_spouse),
       (gt, ":cur_lord", 0),
       (str_store_string, s17, "str_husband"),
     (else_try),
       (str_store_string, s17, "str_father"),
     (try_end),

     (call_script, "script_store_troop_name", s11, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to rescue her {s17}, {s13}, from {s14} by switching clothes and taking his place in prison."),
    ]],
]
