DIALOGS = [
[anyone, "lord_mission_told_deliver_cattle_to_army_rejected", [], "That . . . is unfortunate, {playername}. I shall have to find someone else who's up to the task. Please go now, I've work to do.", "close_window",
   [(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
    (assign, "$g_leave_encounter", 1), ]],
]
