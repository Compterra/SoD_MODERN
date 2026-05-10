DIALOGS = [
[anyone, "runaway_slave_let_go", [], "Then we will look for smoke from a kinder hearth. We will not forget your help, {sir/madam}.", "close_window",
   [
   (call_script, "script_get_closest_village", "p_main_party"),
   (assign, ":rand_village", reg0),
   (try_begin),
      (neg|is_between, ":rand_village", villages_begin, villages_end),
      (store_random_in_range, ":rand_village", villages_begin, villages_end),
   (try_end),
   (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_party),
   (party_set_ai_object, "$g_encountered_party", ":rand_village"),
   (call_script, "script_sod_slavers_apply_player_action", sod_slaver_action_free_runaways, 2),
   (assign, "$g_leave_encounter", 1),
   ]],
]
