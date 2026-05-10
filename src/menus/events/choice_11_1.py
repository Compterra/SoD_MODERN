MENUS = [
(
    "event_11", mnf_disable_all_keys,
    "Good news M'lord, your realm is benefitting from an especially bountiful harvest. The villagers claim to have not done anything different this year, yet many of their fields grow tall with lush yields of grain and by this so have the cattle grown fat and comfortable. Still, with good fortune comes a few prickly questions that require royal guidance. The most important question being just who exactly will benefit the most from this fortunate reaping. The workers? They were in fact the ones to do all of the work and will certainly be eating the most of it. Your Nobles claim that it can be the result of nothing less than superior management and wise choice of seed, but even now prominent religious figures within your realm have spoken up and claimed the divine miracle as a gift from God! But who is to say that it was not the result of even you, my King?",
    "none",
    [

    ],
    [
      ("choice_11_1", [], "Reward hard work.",
       [
        (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (try_begin),
                (party_slot_eq, ":center_no", slot_party_type, spt_village),
                (store_random_in_range, ":rand", 1, 30),
                (party_get_slot, ":center_population", ":center_no", slot_center_sod_local_population),
                (val_add, ":center_population", ":rand"),
                (party_set_slot, ":center_no", slot_center_sod_local_population, ":center_population"),
            (else_try),
                (store_random_in_range, ":rand", 10, 80),
                (party_get_slot, ":center_population", ":center_no", slot_center_sod_local_population),
                (val_add, ":center_population", ":rand"),
                (party_set_slot, ":center_no", slot_center_sod_local_population, ":center_population"),
            (try_end),
        (try_end),
        (display_message, "@Your kingdom is experiencing population boom!", quest_success_color),
        (change_screen_return),
      ]
      ),
      ("choice_11_2", [], "Disperse profits amongst the Lords.",
      [
        (call_script, "script_change_player_honor", 10),
        (call_script, "script_change_troop_renown", "trp_player", 30),
        (change_screen_return),
      ]
      ),
      ("choice_11_3", [], "Surely this is God's will. Donate to the Church.",
      [
        (val_add, "$g_sod_global_faith", 200),
        (val_clamp, "$g_sod_global_faith", -2000, 2001),
        (display_message, "@Faith in your realm grows stronger.", faith_color),
        (change_screen_return),
      ]
      ),
      ("choice_11_4", [], "Sell off what we do not need and institute a special grain tax.",
      [
        (troop_add_gold, "trp_player", 2000),
        (call_script, "script_change_player_honor", -5),
        (change_screen_return),
      ]
    ),
  ]
  ),
]
