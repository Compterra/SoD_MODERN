DIALOGS = [
[anyone|plyr|repeat_for_troops, "marshal_skirmish4ll",
    [(store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", "trp_rhodok_tribesman", "trp_rhodok_messenger"),
      (call_script, "script_store_troop_name", s1, ":troop_no"),],"{s1}", "marshal_skirmish4",[(store_repeat_object, "$sod_skirmish_troop"),]],
]
