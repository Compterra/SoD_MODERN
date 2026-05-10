DIALOGS = [
[trp_sod_strategy_advisor, "sod_sa_war_room", [
    (try_begin),
      (eq, "$g_sod_sa_in_court", 1),
      (str_store_string, s1, "@The long table is ready. Speak, and I will mark the danger in ink before it becomes blood."),
    (else_try),
      (str_store_string, s1, "@No table, then. The saddle will do. Speak, and I will draw the war in dust if I must."),
    (try_end),
], "{s1}", "sod_sa_war_room_answer", []],
]
