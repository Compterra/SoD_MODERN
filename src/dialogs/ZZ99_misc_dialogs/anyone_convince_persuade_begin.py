DIALOGS = [
[anyone, "convince_persuade_begin",
  [(troop_get_slot, ":last_persuasion_time", "$g_talk_troop", slot_troop_last_persuasion_time),
   (store_current_hours, ":cur_hours"),
   (store_add, ":valid_time", ":last_persuasion_time", 24),
   (gt, ":cur_hours", ":valid_time"),
   ],
   "Very well. Make your case.", "convince_persuade_begin_2", []],
]
