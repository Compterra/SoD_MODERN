DIALOGS = [
[anyone|plyr, "gm_tell_mission_fight_troops", [
  (quest_get_slot, ":message_text", "$random_quest_no", slot_quest_no),
  (str_store_string, s15, ":message_text"),
  ], "{s15}", "gm_tell_mission_fight_troops_rejected", []],
]
