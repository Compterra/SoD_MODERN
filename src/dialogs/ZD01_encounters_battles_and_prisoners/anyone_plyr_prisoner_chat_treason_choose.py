DIALOGS = [
[anyone|plyr, "prisoner_chat_treason_choose", [], "I am a {man/woman} of honor.  I shall spare your life this day!", "prisoner_chat_treason_not_guilty",
    [
      (call_script, "script_sod_treason_apply_spared_outcome", "$g_talk_troop"),

      # make sure we don't try to recruit this prisoner later!
      (troop_set_slot, "$g_talk_troop", slot_prisoner_agreed, 0),
    ]
  ],
]
