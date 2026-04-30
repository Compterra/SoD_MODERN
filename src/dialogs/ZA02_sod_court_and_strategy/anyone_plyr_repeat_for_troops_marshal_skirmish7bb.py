DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_skirmish7bb",
    [(store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", "trp_sod_mar_conscript", "trp_sod_peasant3"),
      (call_script, "script_store_troop_name", s1, ":troop_no"),],"{s1}", "marshal_skirmish7",[(store_repeat_object, "$sod_skirmish_troop"),]],
]
