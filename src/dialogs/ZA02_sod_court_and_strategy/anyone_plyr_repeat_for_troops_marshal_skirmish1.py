DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_skirmish1",
    [
      (store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", heroes_begin, heroes_end),
      (call_script, "script_store_troop_name", s1, ":troop_no"),
	  (assign, "$sod_skirmish_fcount", 0),
	  (assign, "$sod_skirmish_ecount", 0),
    ],
    "{s1}", "marshal_skirmish2",
    [
      (store_repeat_object, "$sod_skirmish_leader"),]],
]
