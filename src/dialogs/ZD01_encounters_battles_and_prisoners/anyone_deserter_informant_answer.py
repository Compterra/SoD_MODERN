DIALOGS = [
[anyone, "deserter_informant_demand", [
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_threat_sponsor_center),
    (str_store_party_name, s6, ":origin_center"),
], "Then listen: the weak roads are around {s6}. Patrols pass slow, wagons pass fat, and frightened men talk too much.", "deserter_talk", [
    (call_script, "script_sod_note_hostile_reputation", 4),
    (display_message, "@The deserters reveal local road pressure around the threat contract origin."),
]],
]
