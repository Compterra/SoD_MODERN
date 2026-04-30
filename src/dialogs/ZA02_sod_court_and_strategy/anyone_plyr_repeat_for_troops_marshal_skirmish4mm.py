DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_skirmish4mm",
    [(store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", "trp_farmer", "trp_swadian_recruit"),
      (call_script, "script_store_troop_name", s1, ":troop_no"),],"{s1}", "marshal_skirmish4",[(store_repeat_object, "$sod_skirmish_troop"),]],
]
