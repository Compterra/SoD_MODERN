SCRIPTS = [
("merc_party_change_state",
 [
   (store_script_param_1, ":cur_party"),

   (assign, ":assigned", 0),
   (try_begin),
     (party_is_active, ":cur_party"),
     (party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
     (call_script, "script_sod_merc_party_try_renew_contract", ":cur_party"),
     (assign, ":assigned", reg0),
     (try_begin),
       (eq, ":assigned", 0),
       (call_script, "script_sod_merc_party_try_reassign_contract", ":cur_party"),
       (assign, ":assigned", reg0),
     (try_end),
   (try_end),

   (try_begin),
     (eq, ":assigned", 0),
     (call_script, "script_sod_merc_party_return_to_guild_or_disband", ":cur_party"),
   (try_end),
 ]),
]
