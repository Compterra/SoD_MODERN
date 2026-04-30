DIALOGS = [
[trp_sod_treasurer, "treasurer_invest",
    [
      (eq, "$g_sod_invested", 0),

      (assign, ":risk", 100),

      #MORDACHAI - 5% per trade skill risk reduction
      (call_script, "script_get_max_skill_of_player_party", skl_trade),
      (val_mul, reg0, 5),
      (val_sub, ":risk", reg0),

      # count the number of guilds in the player's kingdom
      (assign, ":guilds", 0),
      (try_for_range, ":center_no", towns_begin, towns_end),
        # only count towns in player's kingdom
        (store_faction_of_party, ":center_faction", ":center_no"),
        (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
        (eq, ":center_faction", "fac_player_faction"),
        # which have a guild
        (party_slot_eq, ":center_no", slot_center_has_guild, 1),
        (val_add, ":guilds", 1),
      (try_end),

      #MORDACHAI - your risk is reduced by 5% per guild, but never below 33% risk
      (store_mul, reg0, ":guilds", 5),
      (val_sub, ":risk", reg0),
      (val_max, ":risk", investment_min_risk),

      # determine the degree of success (or failure)
      (store_random_in_range, ":success", 1, 101),
      (val_sub, ":success", ":risk"),
      (assign, "$g_sod_invested_succes", ":success"),

      # setup our dialog values
      (assign, reg1, ":risk"),
    ],
    "Considering our current knowledge of the market and our relations with the merchant's guilds, I estimate investment risk at {reg1} percent.", "treasurer_invest2",
    []
  ],
]
