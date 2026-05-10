MENUS = [
(
    "investment_report", mnf_disable_all_keys|mnf_scale_picture,
    "Your Treasurer sends you a report on your last trade enterprise. You {s1}.",
    "none",
    [
      (set_background_mesh, "mesh_pic_payment"),

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

      (try_begin),
        # some degree of success
        (gt, "$g_sod_invested_succes", 0),

        # exaggerate success based on number of guilds (20% bonus income per guild)
        (store_mul, ":guild_factor", ":guilds", 20),
        (val_add, "$g_sod_invested_succes", ":guild_factor"),

        # determine profit
        (assign, ":gold", "$g_sod_invested_gold"),
        (val_mul, ":gold", "$g_sod_invested_succes"),
        (val_div, ":gold", 100),

        # apply change
        (val_add, "$g_sod_invested_gold", ":gold"),
        (troop_add_gold, "trp_player", "$g_sod_invested_gold"),

        # menu strings
        (assign, reg1, ":gold"),
        (try_begin),
          (gt, ":guilds", 0),
          (str_store_string, s1, "@have gained {reg1} denars. Your guild contacts helped turn the market in your favor."),
        (else_try),
          (str_store_string, s1, "@have gained {reg1} denars. The venture found a profitable opening."),
        (try_end),
      (else_try),
        # draw
        (eq, "$g_sod_invested_succes", 0),
        # apply change
        (troop_add_gold, "trp_player", "$g_sod_invested_gold"),
        # menu strings
        (str_store_string, s1, "@broke even."),
      (else_try),
        # lost money
        (store_mul, ":loss", "$g_sod_invested_succes", -1),

        # determine how much denars were lost
        (assign, ":gold", "$g_sod_invested_gold"),

        # reduce your loss by 10% per guild
        (store_mul, reg0, ":guilds", 10),
        (store_sub, ":guild_factor", 100, reg0),
        (val_clamp, ":guild_factor", 10, 101), # no more than a 90% mitigation factor
        (val_mul, ":loss", ":guild_factor"),
        (val_div, ":loss", 100),
		
        (val_mul, ":gold", ":loss"),
        (val_div, ":gold", 100),

        # apply change
        (val_sub, "$g_sod_invested_gold", ":gold"),
        (troop_add_gold, "trp_player", "$g_sod_invested_gold"),

        # menu strings
        (assign, reg1, ":gold"),
        (try_begin),
          (gt, ":guilds", 0),
          (str_store_string, s1, "@have lost {reg1} denars. Guild contacts softened the blow, but not enough to save the venture."),
        (else_try),
          (str_store_string, s1, "@have lost {reg1} denars. The venture turned against you."),
        (try_end),
      (try_end),
    ],
    [
      ("choice_investment_report", [] , "Leave.", [(assign, "$g_sod_invested", 0), (assign, "$g_sod_invested_day", 0), (assign, "$g_sod_invested_gold", 0), (assign, "$g_sod_invested_succes", 0), (change_screen_return), ]),
    ]
  ),
]
