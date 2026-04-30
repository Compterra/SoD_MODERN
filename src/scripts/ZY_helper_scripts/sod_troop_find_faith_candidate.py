# COST: O(1)
SCRIPTS = [
("sod_troop_find_faith_candidate",
 [
   (assign, reg0, 0), # found
   (assign, reg1, 0), # noble consumed
   (assign, reg2, 0), # noble candidate shell
   (assign, reg3, 0), # faith result

   (try_begin),
     (eq, "$g_sod_country", cb_antares),
     (assign, ":base_noble", "trp_sod_ant_honor_guard"),
     (assign, ":candidate", "trp_sod_ant_honor_guard1"),
   (else_try),
     (eq, "$g_sod_country", cb_marina),
     (assign, ":base_noble", "trp_sod_mar_condottieri"),
     (assign, ":candidate", "trp_sod_mar_condottieri1"),
   (else_try),
     (eq, "$g_sod_country", cb_aden),
     (assign, ":base_noble", "trp_sod_ade_magnate"),
     (assign, ":candidate", "trp_sod_ade_magnate1"),
   (else_try),
     (eq, "$g_sod_country", cb_villian),
     (assign, ":base_noble", "trp_sod_vil_high_chief"),
     (assign, ":candidate", "trp_sod_vil_high_chief1"),
   (else_try),
     (eq, "$g_sod_country", cb_zerrikan),
     (assign, ":base_noble", "trp_sod_zer_3_noble"),
     (assign, ":candidate", "trp_sod_zer_3_noble1"),
   (else_try),
     (assign, ":base_noble", 0),
     (assign, ":candidate", 0),
   (try_end),

   (try_begin),
     (gt, ":base_noble", 0),
     (party_count_companions_of_type, ":troop_count", "p_main_party", ":base_noble"),
     (gt, ":troop_count", 0),
     (call_script, "script_sod_troop_get_faith_upgrade", ":candidate"),
     (gt, reg0, 0),
     (assign, reg3, reg0),
     (assign, reg2, ":candidate"),
     (assign, reg1, ":base_noble"),
     (assign, reg0, 1),
   (try_end),
 ]),
]
