DIALOGS = [
[anyone, "sod_raider_job_board_question", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_threat_sponsor_center),
    (try_begin),
      (gt, ":origin_center", 0),
      (str_store_party_name, s6, ":origin_center"),
    (else_try),
      (str_store_string, s6, "@the local roads"),
    (try_end),
], "Sent? No. The weak roads around {s6} invited us, and the board merely taught you our name.", "battle_reason_stated", []],
]
