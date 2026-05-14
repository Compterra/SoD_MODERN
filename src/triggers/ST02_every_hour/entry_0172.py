SIMPLE_TRIGGERS = [
(1,
  [
    (call_script, "script_sod_camp_passive_jobs_update"),
  ]),

(1,
  [
    (eq, "$g_sod_camp_job_active", 1),
    (eq, "$g_camp_mode", 1),
    (eq, "$g_player_icon_state", pis_camping),
    (store_current_hours, ":cur_hours"),
    (ge, ":cur_hours", "$g_sod_camp_job_finish_hour"),
    (call_script, "script_sod_camp_job_resolve"),
  ]),
]
