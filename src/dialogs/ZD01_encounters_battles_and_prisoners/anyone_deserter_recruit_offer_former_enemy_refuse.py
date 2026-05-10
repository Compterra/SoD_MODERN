DIALOGS = [
[anyone, "deserter_recruit_offer", [
    (gt, "$players_kingdom", 0),
    (party_slot_eq, "$g_encountered_party", slot_party_sod_threat_active_quest, "qst_regional_threat_contract"),
    (party_slot_eq, "$g_encountered_party", slot_party_sod_threat_sponsor_faction, "$players_kingdom"),
], "Your colors fly over the roads that hunted us. We will not trade one noose for another.", "deserter_talk", []],
]
