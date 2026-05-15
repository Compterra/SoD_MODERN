DIALOGS = [
[trp_sod_jester|plyr|repeat_for_troops, "jester_cheatt1",
   [
     (this_or_next|eq, "$cheat_mode", 1),
     (eq, "$g_sod_cheat_mode", 1),
     (store_repeat_object, ":troop_no"),
   (is_between, ":troop_no", "trp_sod_ant_regular", "trp_sod_peasant11"),
     (call_script, "script_store_troop_name", s1, ":troop_no")
     ],
   "{s1}", "jester_cheatt1",
   [(store_repeat_object, "$temp"),
   (party_force_add_members, "p_main_party", "$temp", 5),
   (val_add, "$g_sod_cheat_mode_used", 1)
   ]
   ],
]
