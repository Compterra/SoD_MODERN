DIALOGS = [
[anyone|plyr, "defeat_hero_answer", [],
   "You are my prisoner now.", "defeat_hero_answer_1",
   [
     (party_add_prisoners, "p_main_party", "$g_talk_troop", 1), #take prisoner
     #(troop_set_slot, "$g_talk_troop", slot_troop_is_prisoner, 1),
     (troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
     (call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
    ]],
]
