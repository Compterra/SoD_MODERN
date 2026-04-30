DIALOGS = [
[anyone, "runaway_slave_let_go", [], "God bless you, {sir/madam}. We will not forget your help.", "close_window",
   [
   (store_random_in_range, ":rand_village", villages_begin, villages_end),
   (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_party),
   (party_set_ai_object, "$g_encountered_party", ":rand_village"),
   (assign, "$g_leave_encounter", 1),
   ]],
]
