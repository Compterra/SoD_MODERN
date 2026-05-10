DIALOGS = [
[anyone, "lord_join_rebellion_suggest", [
              ], "{s43}", "lord_join_rebellion_suggest_1b",
   [

       (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),

       (faction_get_slot, ":pretender", "$players_kingdom", slot_faction_leader),
       (troop_get_type, reg3, ":pretender"),
       (faction_get_slot, ":current_ruler", "$g_talk_troop_faction", slot_faction_leader),

       (call_script, "script_store_troop_name", 45, ":pretender"),
       (call_script, "script_store_troop_name", 46, ":current_ruler"),

       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_rebellion_dilemma_default"),
       (call_script, "script_find_rival_from_faction", "$g_talk_troop", "$players_kingdom"),
       (assign, "$rival_lord", reg0),
       (assign, "$rebellion_chance", 40),
       (call_script, "script_sod_pretender_get_claim_pressure_to_reg", ":pretender", "$g_talk_troop"),
       (store_sub, "$sod_rebel_pressure_mod", reg0, 50),
       (val_div, "$sod_rebel_pressure_mod", 5),
       (val_clamp, "$sod_rebel_pressure_mod", -8, 13),
       (val_add, "$rebellion_chance", "$sod_rebel_pressure_mod"),

       (assign, "$prior_argument_value", 0),

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_claim),
       (store_mul, ":prior_claim", reg0, "$player_made_legitimacy_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_ruler),
       (store_mul, ":prior_claim", reg0, "$player_made_ruler_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_victory),
       (store_mul, ":prior_claim", reg0, "$player_made_strength_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),

       (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_benefit),
       (store_mul, ":prior_claim", reg0, "$player_made_benefit_claim"),
       (val_add, "$prior_argument_value", ":prior_claim"),

       (val_div, "$prior_argument_value", 5),



    ]],
]
