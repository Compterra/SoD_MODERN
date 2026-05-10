DIALOGS = [
[anyone|plyr, "bandit_recruit_2",
   [
      (store_troop_gold, ":gold", "trp_player"),
      (store_encountered_party, ":party"),
      (store_party_size, ":size", ":party"),
      (store_mul, ":size", ":size", 50),
      (assign, reg0, ":size"),
      (ge, ":gold", reg0),
      (party_can_join),
   ], "Okay", "close_window",
   [
      (store_encountered_party, ":party"),
      (store_party_size, ":size", ":party"),
      (store_mul, ":size", ":size", 50),
      (assign, reg0, ":size"),
      (call_script, "script_sod_player_charge_gold", reg0),
      (play_sound, "snd_money_paid"),
      (val_add, "$g_sod_weekly_troops_hired", reg0), # track player expenses
      (party_join),
      (assign, "$g_leave_encounter", 1)
   ]],
]
