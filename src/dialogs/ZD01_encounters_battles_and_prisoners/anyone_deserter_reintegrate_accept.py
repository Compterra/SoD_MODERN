DIALOGS = [
[anyone, "deserter_reintegrate_offer", [
    (gt, "$players_kingdom", 0),
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (ge, ":persuasion", 2),
], "If your word reaches a lord before the rope does, we will take that road.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 1),
    (call_script, "script_change_player_honor", 1),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The deserters agree to seek reintegration under your realm's protection."),
]],
]
