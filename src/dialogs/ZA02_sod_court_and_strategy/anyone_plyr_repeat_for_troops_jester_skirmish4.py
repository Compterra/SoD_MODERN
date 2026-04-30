DIALOGS = [
[anyone|plyr|repeat_for_troops, "jester_skirmish4",
    [
      (store_repeat_object, ":troop_no"),
      (is_between, ":troop_no", heroes_begin, heroes_end),
      (call_script, "script_store_troop_name", s1, ":troop_no"),
    ],
    "{s1}", "marshal_skirmish",
    [
      (store_repeat_object, "$sod_skirmish_playertroop"),]],
]
