DIALOGS = [
[trp_sod_strategy_advisor, "sod_sa_war_room_houses", [
    (try_begin),
      (neq, "$g_sod_house_politics_active", 1),
      (call_script, "script_sod_initialize_house_identity"),
      (assign, "$g_sod_house_politics_active", 1),
    (try_end),
    (call_script, "script_sod_strategy_advisor_describe_house_politics_to_s1"),
], "{s1}", "sod_sa_war_room", []],
]
