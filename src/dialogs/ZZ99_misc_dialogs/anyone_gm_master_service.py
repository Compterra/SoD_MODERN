DIALOGS = [
[anyone, "gm_master_service", [
   (call_script, "script_merc_describe_master_service", "$g_talk_troop_faction"),
   (store_num_regular_prisoners, ":num_prisoners"),
   (try_begin),
     (eq, "$g_talk_troop_faction", "fac_sod_merc_guild6"),
     (ge, ":num_prisoners", 1),
     (str_store_string, s57, "@For trusted partners, I can {s55}. If you have captives, I can move them through my hidden market and cut you in on the take. It will cost coin and a little goodwill."),
   (else_try),
     (eq, "$g_talk_troop_faction", "fac_sod_merc_guild6"),
     (str_store_string, s57, "@For trusted partners, I can {s55}. Even without fresh stock, my people know where chains and secrets change hands. It will cost coin and a little goodwill."),
   (else_try),
     (str_store_string, s57, "@For trusted partners, I can {s55}. It will cost coin and a little goodwill."),
   (try_end),
   ], "{s57}", "gm_master_service_confirm",[]],
]
