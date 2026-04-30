DIALOGS = [
[anyone, "lady_mission_accepted", [], "You are a true {gentleman/lady}, {playername}.\
 Thank you so much for helping me", "close_window",
   [
     (try_begin),
       (eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord"),
       (call_script, "script_troop_add_gold", "trp_player", 10),
     (try_end),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    ]],
]
