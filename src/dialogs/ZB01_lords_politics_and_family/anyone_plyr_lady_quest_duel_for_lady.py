DIALOGS = [
[anyone|plyr, "lady_quest_duel_for_lady", [], "Tell me what the problem is, and I can make my own decision.", "lady_quest_duel_for_lady_2",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (call_script, "script_store_troop_name", s11, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
     (str_store_string, s2, "@You agreed to challenge {s13} to defend {s11}'s honour."),
     (setup_quest_text, "$random_quest_no"),
    ]],
]
