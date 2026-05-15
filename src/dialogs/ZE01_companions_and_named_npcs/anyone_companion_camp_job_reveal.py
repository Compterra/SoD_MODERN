DIALOGS = [
[anyone, "companion_camp_job_reveal",
  [
    (is_between, "$g_talk_troop", companions_begin, companions_end),
    (main_party_has_troop, "$g_talk_troop"),
    (call_script, "script_sod_camp_passive_job_dialogue_to_s68", "$g_talk_troop"),
  ],
  "{s68}", "member_talk",
  []],
]
