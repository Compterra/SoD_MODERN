DIALOGS = [
[anyone, "town_dweller_quest_meet_spy_in_enemy_town_chat", [
     (quest_get_slot, ":quest_giver", "qst_meet_spy_in_enemy_town", slot_quest_giver_troop),
     (call_script, "script_store_troop_name", s4, ":quest_giver"),
  ],
   "I've been expecting you. Here they are, make sure they reach {s4} intact and without delay.", "town_dweller_quest_meet_spy_in_enemy_town_chat_2", [
     (call_script, "script_succeed_quest", "qst_meet_spy_in_enemy_town"),
     (call_script, "script_center_remove_walker_type_from_walkers", "$current_town", walkert_spy),
   ]],
]
