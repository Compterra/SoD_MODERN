DIALOGS = [
[anyone, "lord_enter_service_reject", [], "What pigswill!\
 And to think I would offer you a place among my nobles. Begone, beggar, before I lose my temper!", "close_window",
   [
     (try_begin),
       (store_partner_quest, ":lords_quest"),
       (eq, ":lords_quest", "qst_join_faction"),
       (call_script, "script_abort_quest", "qst_join_faction", 1),
     (try_end),
     (assign, "$g_invite_faction", 0),
     (assign, "$g_invite_faction_lord", 0),
     (assign, "$g_invite_offered_center", 0),
     (assign, "$g_leave_encounter", 1),
    ]],
]
