# COST: low
SCRIPTS = [
("cf_sod_player_has_active_merc_company_from_guild",
 [
   (store_script_param_1, ":guild_faction"),

   (assign, ":found", 0),
   (try_for_parties, ":cur_party"),
     (eq, ":found", 0),
     (party_slot_eq, ":cur_party", slot_party_type, spt_player_mercenaries),
     (party_slot_eq, ":cur_party", slot_party_boss, "trp_player"),
     (try_begin),
       (party_slot_eq, ":cur_party", slot_party_sod_merc_contract_guild, ":guild_faction"),
       (assign, ":found", 1),
     (else_try),
       (party_slot_eq, ":cur_party", slot_party_orginal_faction, ":guild_faction"),
       (assign, ":found", 1),
     (try_end),
   (try_end),
   (eq, ":found", 1),
 ]),
]
