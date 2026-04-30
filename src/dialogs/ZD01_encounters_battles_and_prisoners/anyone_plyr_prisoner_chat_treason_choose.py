DIALOGS = [
[anyone|plyr, "prisoner_chat_treason_choose", [], "I am a {man/woman} of honor.  I shall spare your life this day!", "prisoner_chat_treason_not_guilty",
    [
      #TODO: have the relation with the prison have a mixed (random) result - relief, anger, etc, which dictates their final monologue to the player before exiting the dialog

      # make sure we don't try to recruit this prisoner later!
      (troop_set_slot, "$g_talk_troop", slot_prisoner_agreed, 0),
    ]
  ],
]
