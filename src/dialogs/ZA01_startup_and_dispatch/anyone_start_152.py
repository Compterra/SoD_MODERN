DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (gt, "$encountered_party_hostile", 0),
                    (encountered_party_is_attacker),
                    ],
   "You have no chance against us. Surrender now or we will kill you all...", "party_encounter_hostile_attacker",
   [(try_begin),
      (eq, "$g_encountered_party_template", "pt_steppe_bandits"),
      (play_sound, "snd_encounter_steppe_bandits"),
    (try_end)]],
]
