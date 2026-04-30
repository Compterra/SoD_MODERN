DIALOGS = [
[anyone|plyr|repeat_for_troops, "center_captured_lord_advice",
   [
     (store_repeat_object, ":troop_no"),
     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (neq, "$g_talk_troop", ":troop_no"),
     (neq, "trp_player", ":troop_no"),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (eq, ":faction_no", "fac_player_supporters_faction"),
     (call_script, "script_store_troop_name", s11, ":troop_no"),
     (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", ":troop_no"),
     (try_begin),
       (eq, reg0, 0),
       (str_store_string, s1, "@(no fiefs)"),
     (else_try),
       (str_store_string, s1, "@(fiefs: {s0})"),
     (try_end),
     ],
   "{s11}. {s1}", "center_captured_lord_advice_2",
   [
     (store_repeat_object, "$temp"),
     ]],
]
