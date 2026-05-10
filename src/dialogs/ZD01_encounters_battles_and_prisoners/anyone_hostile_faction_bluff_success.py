DIALOGS = [
[anyone, "hostile_faction_bluff", [
    (gt, "$players_kingdom", 0),
    (store_relation, ":relation", "$players_kingdom", "$g_encountered_party_faction"),
    (ge, ":relation", 0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (ge, ":renown", 150),
], "Fine. We do not need a feud with your colors today. Pass, and remember who chose restraint.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 5),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
