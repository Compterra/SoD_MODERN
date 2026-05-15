DIALOGS = [
[anyone|plyr, "companion_home_description", [
      ],  "Homesickness does not change my orders.", "close_window", [
                    (call_script, "script_sod_companion_shift_approval", "$g_talk_troop", -2),
                    (assign, "$disable_local_histories", 1),
          ]],
]
