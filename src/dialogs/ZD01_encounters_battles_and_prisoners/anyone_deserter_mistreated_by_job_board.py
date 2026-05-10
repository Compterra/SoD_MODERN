DIALOGS = [
[anyone, "deserter_mistreated_by", [
    (party_slot_eq, "$g_encountered_party", slot_party_sod_threat_active_quest, "qst_regional_threat_contract"),
    (party_get_slot, ":sponsor_faction", "$g_encountered_party", slot_party_sod_threat_sponsor_faction),
    (gt, ":sponsor_faction", 0),
    (str_store_faction_name, s6, ":sponsor_faction"),
], "{s6} called us expendable, then traitors, then prey. We learned the difference was only who held the quill.", "deserter_talk", []],
]
