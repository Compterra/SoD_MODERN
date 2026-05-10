DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (gt, "$encountered_party_hostile", 0),
                    (encountered_party_is_attacker),
                    (call_script, "script_sod_store_hostile_greeting"),
                    ],
   "{s5}", "party_encounter_hostile_attacker",
   [(try_begin),
      (eq, "$g_encountered_party_template", "pt_steppe_bandits"),
      (play_sound, "snd_encounter_steppe_bandits"),
    (try_end)]],
]
