DIALOGS = [
[anyone, "gm_market_report", [
   (call_script, "script_sod_merc_guild_describe_ledger_to_s20", "$g_talk_troop_faction"),
   (store_relation, ":player_relation", "$g_talk_troop_faction", "fac_player_faction"),
   (faction_get_slot, ":player_debt", "$g_talk_troop_faction", player_debt_to_faction),
   (str_store_string, s30, "@Our ledgers are open to anyone with coin, but preference is earned."),
   (try_begin),
     (gt, ":player_debt", 0),
     (assign, reg33, ":player_debt"),
     (str_store_string, s30, "@Your name carries debt in our books: {reg33} denars. Until that is settled, every offer comes with sharper edges."),
   (else_try),
     (ge, ":player_relation", 40),
     (str_store_string, s30, "@You have made yourself useful. If work is scarce, I will give you preferential hearing before I remember a stranger's purse."),
   (else_try),
     (le, ":player_relation", -10),
     (str_store_string, s30, "@You ask like a buyer, not a friend. That is acceptable; the arrangement will stay transactional, and the price will speak plainly."),
   (try_end),
   ], "{s30}^^{s20}", "gm_pretalk",[]],
]
