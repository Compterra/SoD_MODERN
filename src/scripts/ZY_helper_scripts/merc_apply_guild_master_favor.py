# COST: low
SCRIPTS = [
("merc_apply_guild_master_favor",
 [
   (store_script_param_1, ":guild_faction"),

   (assign, ":applied", 0),
   (call_script, "script_merc_describe_guild_favor", ":guild_faction"),

   (try_for_parties, ":cur_party"),
     (eq, ":applied", 0),
     (party_slot_eq, ":cur_party", slot_party_type, spt_player_mercenaries),
     (party_slot_eq, ":cur_party", slot_party_boss, "trp_player"),
     (party_slot_eq, ":cur_party", slot_party_orginal_faction, ":guild_faction"),
     (call_script, "script_merc_apply_contract_favor", ":cur_party"),
     (assign, ":applied", 1),
   (try_end),

   (try_begin),
     (eq, ":applied", 0),
     (faction_slot_eq, "fac_player_faction", slot_faction_merc_pact, ":guild_faction"),
     (assign, ":rel_cost", -3),
     (call_script, "script_change_player_relation_with_faction", ":guild_faction", ":rel_cost"),
     (assign, ":debt_relief", "$g_mercenary_guild_weekly_payment"),
     (val_div, ":debt_relief", 2),
     (val_max, ":debt_relief", 100),
     (faction_get_slot, ":current_debt", ":guild_faction", player_debt_to_faction),
     (val_sub, ":current_debt", ":debt_relief"),
     (val_max, ":current_debt", 0),
     (faction_set_slot, ":guild_faction", player_debt_to_faction, ":current_debt"),
     (display_message, "@Your trusted standing secures temporary leniency from the guild. Part of your debt is waived, but the favor costs you a little reputation.", 0x66CC66),
     (assign, ":applied", 1),
   (try_end),
 ]),
]
