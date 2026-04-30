DIALOGS = [
[anyone, "lord_ask_pardon_after_renounce_peace",
   [],
   "Excellent. Though you strayed from us, {playername}, it gladdens all our hearts that you have found your way back to the right path. I hereby restore your homage to me. Rise once more as an honoured {man/warrior} in my service.", "lord_pretalk",
   [
     (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
       (store_faction_of_party, ":cur_center_faction", ":cur_center"),
       (eq, ":cur_center_faction", "fac_player_supporters_faction"),
       (party_slot_eq, ":cur_center", slot_center_faction_when_oath_renounced, "$g_talk_troop_faction"),
       (neq, ":cur_center", "$players_oath_renounced_given_center"),
       (call_script, "script_give_center_to_faction", ":cur_center", "$g_talk_troop_faction"),
     (try_end),

     (call_script, "script_player_join_faction", "$g_talk_troop_faction"),
     (assign, "$player_has_homage", 1),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
     ]],
]