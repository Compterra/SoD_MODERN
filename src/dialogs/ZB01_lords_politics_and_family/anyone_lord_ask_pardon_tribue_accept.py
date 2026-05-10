DIALOGS = [
[anyone, "lord_ask_pardon_tribue_accept", [], "Excellent, {playername}. I'll use the coin to smooth the feathers of those that can oppose your pardon, and I'm sure that word will soon spread that you are no longer an enemy of {s4}.", "close_window",
   [
     (call_script, "script_sod_player_charge_gold", reg16),
     (play_sound, "snd_money_paid"),
     (try_begin),
       (eq, "$players_kingdom", 0),
       (call_script, "script_set_player_relation_with_faction", "$g_talk_troop_faction", 0),
     (else_try),
    #MORDACHAI - bug fix: not enough arguments for script (final argument required!)
       (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_talk_troop_faction", "$players_kingdom", 1),
     (try_end),
     (assign, "$g_leave_town_outside", 1),
     (assign, "$g_leave_encounter", 1),
     ]],
]
