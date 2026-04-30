DIALOGS = [
[anyone, "member_separate_yes", [
      ], "Well. I'll be off, then. Look me up if you need me.", "close_window",
   [
            (troop_set_slot, "$g_talk_troop", slot_troop_occupation, 0),
            (troop_set_slot, "$g_talk_troop", slot_troop_playerparty_history, pp_history_dismissed),
            (remove_member_from_party, "$g_talk_troop"),
       ]],
]
