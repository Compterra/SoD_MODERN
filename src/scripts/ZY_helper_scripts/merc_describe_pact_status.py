# COST: trivial
SCRIPTS = [
("merc_describe_pact_status",
 [
   (store_script_param_1, ":guild_faction"),
   (str_store_string, s59, "@No active pact."),
   (try_begin),
     (gt, ":guild_faction", 0),
     (store_relation, ":rel", ":guild_faction", "fac_player_faction"),
     (assign, reg5, "$g_mercenary_guild_weekly_payment"),
     (faction_get_slot, reg6, ":guild_faction", player_debt_to_faction),
     (try_begin),
       (ge, ":rel", 35),
       (str_store_string, s59, "@Trusted pact: your standing softens the burden and helps contain debt."),
     (else_try),
       (ge, ":rel", 20),
       (str_store_string, s59, "@Stable pact: the guild still expects punctual payment, but relations are sound."),
     (else_try),
       (str_store_string, s59, "@Fragile pact: missed payments will quickly poison this arrangement."),
     (try_end),
   (try_end),
 ]),
]
