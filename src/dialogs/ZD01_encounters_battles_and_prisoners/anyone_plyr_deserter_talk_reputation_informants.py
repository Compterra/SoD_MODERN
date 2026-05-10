DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (ge, "$g_sod_hostile_informant_count", 2),
    (party_slot_eq, "$g_encountered_party", slot_party_sod_threat_active_quest, "qst_regional_threat_contract"),
], "Others bought their lives with useful words. You may do the same.", "deserter_informant_demand", []],
]
