SCRIPTS = [
("sod_upgrade_troop_count_to_at",
                      [
                        (store_script_param, ":troop", 1),
                        (store_script_param, ":count", 2),
                        (store_script_param, ":upgrade", 3),
                        (store_script_param, ":center", 4),
                        (store_script_param, ":garrison", 5),
						
						(try_begin),
							(eq, ":garrison", 1),
							(assign, ":source", ":center"),
						(else_try),
							(assign, ":source", "p_main_party"),
						(try_end),
						
                        # remove the old ones
                        (party_remove_members, ":source", ":troop", ":count"),

                        # add the new ones
                        (party_add_members, ":source", ":upgrade", ":count"),

                        # get the cost to do this
                        (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade", ":center"),
                        (store_mul, ":cost", reg0, ":count"),

                        # charge the player the cost of this upgrade (can be future debt)
                        (store_troop_gold, ":gold", "trp_player"),
                        (try_begin),
                          (ge, ":gold", ":cost"),
                          (call_script, "script_sod_player_charge_gold", ":cost"),
                        (else_try),
                          (call_script, "script_sod_player_charge_gold", ":gold"),
                          (val_sub, ":cost", ":gold"),
                          (val_max, ":cost", 0),
                          (val_add, "$g_player_debt_to_party_members", ":cost"),
                          (val_clamp, "$g_player_debt_to_party_members", 0, 2000001),
                        (try_end),
                        (play_sound, "snd_money_paid"),

                        # keep track of money spent on troops
                        (val_max, ":cost", 0),
                        (val_add, "$g_sod_weekly_troops_upgraded", ":cost"),
                        (val_clamp, "$g_sod_weekly_troops_upgraded", 0, 2000001),
                        (try_begin),
                          (gt, "$g_sod_doctrine_inspiration", 0),
                          (val_sub, "$g_sod_doctrine_inspiration", ":count"),
                          (val_max, "$g_sod_doctrine_inspiration", 0),
                        (try_end),
                      ]
                    ),
]
