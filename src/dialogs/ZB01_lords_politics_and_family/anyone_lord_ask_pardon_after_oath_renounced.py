DIALOGS = [
[anyone, "lord_ask_pardon_after_oath_renounced",
   [
     (faction_get_slot, ":faction_leader", "$g_talk_troop_faction", slot_faction_leader),
     (neq, ":faction_leader", "$g_talk_troop"),
     (call_script, "script_store_troop_name", s4, ":faction_leader"),
     ], "That is too great a matter for me to decide, {playername}. You should seek out {s4}. Such clemency is his alone to grant or deny.", "lord_pretalk", []],
]
