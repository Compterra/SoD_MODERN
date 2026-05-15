SCRIPTS = [
("sod_prisoner_process_hero_escape_checks",
   [
       (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", "p_main_party", 50),
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         # SOD - reduce chance of lord escape to 15% (was 30%).
         (assign, ":chance", 15),
         (try_begin),
           # SOD - increase effectiveness of a tower to 1 in 50 (was 1 in 20).
           (party_slot_eq, ":center_no", slot_center_has_prisoner_tower, 1),
           (assign, ":chance", 2),
         (try_end),
         (try_begin),
           (troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_crusader),
           (val_mul, ":chance", 3),
         (else_try),
           (troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_imperialist),
           (val_mul, ":chance", 2),
         (try_end),
         (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", ":center_no", ":chance"),
       (try_end),
    ]),

("sod_prisoner_process_daily_ransom_offer",
   [
       (try_begin),
         (neq, "$g_ransom_offer_rejected", 1),
         (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", "p_main_party"),
         (eq, reg0, 0), # no prisoners offered
         (assign, ":end_cond", walled_centers_end),
         (try_for_range, ":center_no", walled_centers_begin, ":end_cond"),
           (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
           (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", ":center_no"),
           (eq, reg0, 1), # a prisoner is offered
           (assign, ":end_cond", 0), # break
         (try_end),
       (try_end),
    ]),
]
