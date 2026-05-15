DIALOGS = [
[anyone, "party_encounter_offer_dont_fight", [(gt, "$g_talk_troop_relation", 30),
#TODO: Add additional conditions, lord personalities, battle advantage, etc...
                    ],
   "I owe you a favor, don't I. Well... all right then. I will let you go just this once.", "close_window", [
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -7),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (assign, "$g_leave_encounter", 1)
       ]],
]
