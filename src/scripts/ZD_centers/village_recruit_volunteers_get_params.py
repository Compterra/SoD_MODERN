SCRIPTS = [
("village_recruit_volunteers_get_params",
        [
		  (store_script_param, ":which", 1),
          (party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
          (party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
          (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
          (val_min, ":volunteer_amount", ":free_capacity"),
          (store_troop_gold, ":gold", "trp_player"),
          (store_div, ":gold_capacity", ":gold", 10), #10 denars per man
          (val_min, ":volunteer_amount", ":gold_capacity"),
          (call_script, "script_get_center_recruitable_population", "$current_town", ":volunteer_amount"),
          (assign, ":volunteer_amount", reg0),
          #SoD ARMY MANAGEMENT BEGIN
          (try_begin),
            (eq, ":which", 1),
            (assign, ":volunteer_troop", "trp_farmer"), # use mercenaries if you're still a mercenary yourself
          (else_try),
            (eq, ":which", 2),
            (try_begin),
              (eq, "$g_sod_country", cb_antares),
              (assign, ":volunteer_troop", "trp_sod_peasant1"),
            (else_try),
              (eq, "$g_sod_country", cb_marina),
              (assign, ":volunteer_troop", "trp_sod_peasant2"),
            (else_try),
              (eq, "$g_sod_country", cb_aden),
              (assign, ":volunteer_troop", "trp_sod_peasant3"),
            (else_try),
              (eq, "$g_sod_country", cb_villian),
              (assign, ":volunteer_troop", "trp_sod_peasant4"),
            (else_try),
              (eq, "$g_sod_country", cb_zerrikan),
              (assign, ":volunteer_troop", "trp_sod_peasant5"),
            (try_end),
          (try_end),
          #SoD ARMY MANAGEMENT END

          # return the data to the caller
          (assign, reg0, ":volunteer_troop"),
          (assign, reg1, ":volunteer_amount"),
        ]
      ),
]
