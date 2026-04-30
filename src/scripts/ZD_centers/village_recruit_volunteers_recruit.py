SCRIPTS = [
("village_recruit_volunteers_recruit", [
		  (store_script_param, ":native", 1),
          # determine what troop type and amount to recruit
          (call_script, "script_village_recruit_volunteers_get_params", ":native"),
          (assign, ":volunteer_troop", reg0),
          (assign, ":volunteer_amount", reg1),

          # generate the actual troops
          (party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount"),

          # charge the player for the costs
          (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
          (store_mul, ":cost", ":volunteer_amount", 10), #10 denars per man
          (troop_remove_gold, "trp_player", ":cost"),

          # track player expenditures
          (val_max, ":cost", 0),
          (val_add, "$g_sod_weekly_troops_upgraded", ":cost"),
          (val_clamp, "$g_sod_weekly_troops_upgraded", 0, 2000001),

          # update remaining population (troops come from pops)
          (call_script, "script_spend_center_population_for_recruitment", "$current_town", ":volunteer_amount"),
      ]),
]
