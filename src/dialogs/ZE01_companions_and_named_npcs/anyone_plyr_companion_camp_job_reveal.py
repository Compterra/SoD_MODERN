DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
  ],
  "What work do you take up when we make camp?", "companion_camp_job_reveal",
  []],
]
