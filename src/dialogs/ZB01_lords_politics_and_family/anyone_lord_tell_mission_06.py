DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_collect_taxes"),
                                (assign, reg9, 0),
                                (try_begin),
                                  (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
                                  (party_slot_eq, ":quest_target_center", slot_party_type, spt_town),
                                  (assign, reg9, 1),
                                (try_end),
                                ], "You probably know that I am the lord of the {reg9?town:village} of {s3}.\
 However, it has been months since {s3} has delivered the taxes and rents due me as its rightful lord.\
 Apparently the populace there has grown unruly lately and I need someone to go there and remind them of\
 their obligations. And to . . . persuade them if they won't listen.\
 If you go there and raise the taxes they owe me, I will grant you one-fifth of everything you collect.", "lord_mission_collect_taxes_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_party_name_link, s3, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to collect the taxes owed by {s3}. He offered to leave you one-fifth of all the money you collect."),
   ]],
]
