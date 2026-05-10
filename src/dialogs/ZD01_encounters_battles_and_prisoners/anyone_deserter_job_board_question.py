DIALOGS = [
[anyone, "sod_deserter_job_board_question", [
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_threat_sponsor_center),
    (str_store_party_name, s6, ":origin_center"),
], "No lord sent us. {s6} stopped feeding men like us, so men like us started feeding on {s6}.", "deserter_talk", []],
]
