DIALOGS = [
[anyone|plyr, "town_dweller_quest_meet_spy_in_enemy_town_know", [
     (quest_get_slot, ":quest_giver", "qst_meet_spy_in_enemy_town", slot_quest_giver_troop),
     (call_script, "script_store_troop_name", s4, ":quest_giver"),
  ],
   "{s4} sent me to collect your reports. Do you have them with you?", "town_dweller_quest_meet_spy_in_enemy_town_chat", []],
]
