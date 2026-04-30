DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_skirmish7gg",
    [(store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", "trp_sod_faith1_mount", "trp_sod_peasant11"),
      (call_script, "script_store_troop_name", s1, ":troop_no"),],"{s1}", "marshal_skirmish7",[(store_repeat_object, "$sod_skirmish_troop"),]],
]
