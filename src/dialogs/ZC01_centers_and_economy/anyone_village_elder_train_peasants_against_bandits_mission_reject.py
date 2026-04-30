DIALOGS = [
[anyone, "village_elder_train_peasants_against_bandits_mission_reject", [], "Yes, of course {sir/madam}.\
 Thank you for your counsel.", "close_window",
   [
     (troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
     ]],
]
