DIALOGS = [
[anyone|plyr, "lord_talk_ask_something_2",
  [
    (call_script, "script_sod_troop_has_claimant_dialog_to_reg", "$g_talk_troop"),
    (eq, reg0, 1),
  ],
  "Where do you stand in the claimant wars?", "lord_talk_claimant_allegiance", []],
]
