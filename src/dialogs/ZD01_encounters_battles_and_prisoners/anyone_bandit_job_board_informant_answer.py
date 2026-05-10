DIALOGS = [
[anyone, "bandit_job_board_informant_demand", [
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_threat_sponsor_center),
    (str_store_party_name, s6, ":origin_center"),
], "Around {s6}, watch the crossings and the low farms. Men hide where patrols hate riding.", "bandit_talk", [
    (call_script, "script_sod_note_hostile_reputation", 4),
    (display_message, "@The bandits reveal likely hiding ground near the threat contract origin."),
]],
]
