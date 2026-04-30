SCRIPTS = [
("calculate_amount_of_cattle_can_be_stolen",
        [
          (store_script_param, ":village_no", 1),
          (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
          (assign, ":max_skill", reg0),
          (store_mul, ":can_steal", ":max_skill", 2),
          (call_script, "script_party_count_fit_for_battle", "p_main_party"),
          (store_add, ":num_men_effect", reg0, 10),
          (val_div, ":num_men_effect", 10),
          (val_add, ":can_steal", ":num_men_effect"),
          (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
          (val_min, ":can_steal", ":num_cattle"),
          (assign, reg0, ":can_steal"),
      ]),
]
